
import os
import json
import pickle
import time
import requests
import urllib.parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# --- Configuration ---
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
ARTICLES_FILE = 'trivia_articles.json'
TOKEN_FILE = 'token.pickle'
UPLOAD_API_URL = 'https://catbox.moe/user/api.php'

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('blogger', 'v3', credentials=creds)

def upload_image(file_path):
    """Uploads an image to Catbox and returns the URL."""
    if not os.path.exists(file_path):
        return None
    
    print(f"Uploading {file_path}...")
    try:
        with open(file_path, 'rb') as f:
            files = {'fileToUpload': f}
            data = {'reqtype': 'fileupload'}
            response = requests.post(UPLOAD_API_URL, data=data, files=files)
            if response.status_code == 200:
                url = response.text.strip()
                print(f"Success: {url}")
                return url
            else:
                print(f"Upload failed: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error during upload: {e}")
        return None

def update_post(service, blog_id, post_id, title, content, labels):
    body = {
        'kind': 'blogger#post',
        'id': post_id,
        'title': title,
        'content': content,
        'labels': labels
    }
    try:
        request = service.posts().update(blogId=blog_id, postId=post_id, body=body)
        response = request.execute()
        print(f"Successfully updated: {title}")
        return response
    except Exception as e:
        print(f"Failed to update {title}: {e}")
        return None

def main():
    blog_id = input("Enter your Blogger Blog ID: ").strip()
    if not blog_id:
        print("Blog ID is required.")
        return

    service = get_authenticated_service()
    
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Fetch existing posts from Blogger
    print("Fetching existing posts from Blogger...")
    try:
        posts_request = service.posts().list(blogId=blog_id, maxResults=500)
        posts_response = posts_request.execute()
        existing_posts = posts_response.get('items', [])
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return

    if not existing_posts:
        print("No posts found to update.")
        return

    print(f"Found {len(existing_posts)} posts on Blogger. Starting matching process...")

    changed_json = False

    for post in existing_posts:
        post_title = post['title'].strip()
        post_id = post['id']
        
        # Normalize titles for better matching
        def normalize(t):
            return t.replace(' ', '').replace('　', '').replace('\n', '').replace('\r', '')

        # Find matching article in JSON
        matching_article = None
        article_index = -1
        
        # 1. Try exact match (normalized)
        norm_post_title = normalize(post_title)
        for i, art in enumerate(articles):
            if normalize(art['title']) == norm_post_title:
                matching_article = art
                article_index = i
                break
        
        # 2. Try partial match if no exact match
        if not matching_article:
            for i, art in enumerate(articles):
                # If either title is contained in the other
                if normalize(art['title']) in norm_post_title or norm_post_title in normalize(art['title']):
                    matching_article = art
                    article_index = i
                    break
        
        if not matching_article:
            print(f"Generic Update: '{post_title}' (No matching article in JSON, appending Amazon link only)")
            # Guess a keyword from the title for Amazon search
            # Simple heuristic: take the first part before a colon, space, or special char
            keyword = post_title.split('：')[0].split(':')[0].split(' ')[0].strip(' 「」“”')
            if 'ジャガイモ' in post_title: keyword = 'ジャガイモ'
            if 'トンネル' in post_title: keyword = 'トンネル'
            
            associate_id = "hyakushiki005-22"
            encoded_keyword = urllib.parse.quote(keyword)
            amazon_url = f"https://www.amazon.co.jp/s?k={encoded_keyword}&tag={associate_id}"
            
            ad_html = f'''
            <div class="amazon-ad-box">
                <p>＼ この記事に関連する商品をチェック ／</p>
                <a href="{amazon_url}" target="_blank" rel="noopener" class="amazon-btn">
                    📦 Amazonで「{keyword}」を検索する
                </a>
            </div>
            '''
            # Check if link already exists to avoid double appending
            if 'amazon-ad-box' in post.get('content', ''):
                print(f"Skipping: '{post_title}' (Already has Amazon link)")
                continue
                
            # Wrap existing content with better styling if possible, or just append
            new_content = post.get('content', '') + ad_html
            update_post(service, blog_id, post_id, post_title, new_content, post.get('labels', []))
            continue

        print(f"\nUpdating Post ID {post_id}: {post_title}")

        # 1. Image Handling
        img_url = matching_article.get('image_url')
        img_path = matching_article.get('image_path')

        # Auto-detect image if path is not set
        if not img_path:
            for ext in ['.png', '.jpg', '.jpeg', '.webp']:
                test_path = os.path.join('images', f"{article_index}{ext}")
                if os.path.exists(test_path):
                    img_path = test_path
                    matching_article['image_path'] = img_path
                    changed_json = True
                    break

        if not img_url and img_path and os.path.exists(img_path):
            img_url = upload_image(img_path)
            if img_url:
                matching_article['image_url'] = img_url
                changed_json = True

        # 2. Amazon Link Styling
        keyword = matching_article['labels'][0] if matching_article.get('labels') else "本"
        associate_id = "hyakushiki005-22"
        encoded_keyword = urllib.parse.quote(keyword)
        amazon_url = f"https://www.amazon.co.jp/s?k={encoded_keyword}&tag={associate_id}"
        
        ad_html = f'''
        <div class="amazon-ad-box">
            <p>＼ この記事に関連する商品をチェック ／</p>
            <a href="{amazon_url}" target="_blank" rel="noopener" class="amazon-btn">
                📦 Amazonで「{keyword}」を検索する
            </a>
        </div>
        '''

        # 3. Construct Content
        img_tag = f'<div style="text-align: center;"><img src="{img_url}" style="max-width: 100%; height: auto; border-radius: 10px; margin-bottom: 20px;"></div>' if img_url else ""
        new_content = f"{img_tag}\n<p>{matching_article['hook']}</p>\n{matching_article['content']}\n{ad_html}"

        # 4. Update on Blogger
        update_post(service, blog_id, post_id, post_title, new_content, matching_article['labels'])
        
        # Pause to avoid rate limits
        time.sleep(2)

    if changed_json:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print("\nUpdated trivia_articles.json with new image URLs.")

    print("\n--- All matching posts have been updated! ---")

if __name__ == '__main__':
    main()
