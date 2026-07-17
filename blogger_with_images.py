
import os
import json
import pickle
import time
import random
import requests
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 画像アップロードは共通モジュールに委譲（Catbox リトライ + ImgBB フォールバック）
from image_host import upload_image

# --- Configuration ---
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
ARTICLES_FILE = 'trivia_articles.json'
TOKEN_FILE = 'token.pickle'

# Already uploaded indices (to be skipped in automatic posting)
ALREADY_UPLOADED = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14]

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.exceptions import RefreshError
            try:
                creds.refresh(Request())
            except RefreshError:
                print("トークンの有効期限が切れています。再認証します...")
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('blogger', 'v3', credentials=creds)

def post_to_blogger(service, blog_id, title, content, labels, publish_time=None):
    body = {
        'kind': 'blogger#post',
        'title': title,
        'content': content,
        'labels': labels
    }
    if publish_time:
        body['published'] = publish_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    try:
        request = service.posts().insert(blogId=blog_id, body=body)
        response = request.execute()
        print(f"Successfully posted: {title}")
        return response
    except Exception as e:
        print(f"Failed to post {title}: {e}")
        return None

def main():
    # Try to read blog_id from file automatically
    blog_id_file = 'Blogger_brog_id.txt'
    blog_id = ""
    if os.path.exists(blog_id_file):
        with open(blog_id_file, 'r') as f:
            blog_id = f.read().strip()
    
    if not blog_id:
        blog_id = input("Enter your Blogger Blog ID: ").strip()
    else:
        print(f"Using Blog ID from {blog_id_file}: {blog_id}")
    
    service = get_authenticated_service()
    
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Calculate the next base_date from previously scheduled posts
    latest_publish = None
    for article in articles:
        pub_str = article.get("publish_date")
        if pub_str:
            dt = datetime.strptime(pub_str, '%Y-%m-%dT%H:%M:%SZ')
            if latest_publish is None or dt > latest_publish:
                latest_publish = dt

    if latest_publish:
        base_date = latest_publish + timedelta(days=1)
        base_date = base_date.replace(hour=12, minute=0, second=0, microsecond=0)
    else:
        # Tomorrow 21:00 JST (which is 12:00 UTC)
        base_date = datetime.now() + timedelta(days=1)
        base_date = base_date.replace(hour=12, minute=0, second=0, microsecond=0)

    # Save progress back to JSON
    changed = False
    posts_this_run = 0
    MAX_POSTS_PER_RUN = 5

    for i, article in enumerate(articles):
        if i in ALREADY_UPLOADED:
            print(f"Skipping index {i} (Already uploaded manually).")
            continue
        if article.get("posted_status") == "scheduled":
            print(f"Skipping index {i} (Already scheduled).")
            continue
            
        if posts_this_run >= MAX_POSTS_PER_RUN:
            print(f"\nReached the limit of {MAX_POSTS_PER_RUN} posts for this run to avoid spam detection.")
            break
            
        # 1. Handle Image
        img_url = article.get('image_url')
        img_path = article.get('image_path')
        
        # Auto-detect image by article index if path is not set (e.g., images/15.jpg)
        if not img_path or not os.path.exists(img_path):
            for ext in ['.jpg', '.png', '.jpeg', '.webp']:
                test_path = os.path.join('images', f"{i}{ext}")
                if os.path.exists(test_path):
                    img_path = test_path
                    article['image_path'] = img_path
                    break
        
        # Condition: Only post if an illustration image exists
        if not img_url and not (img_path and os.path.exists(img_path)):
            # Keep it silent for articles without images
            continue
            
        # If we reach here, we found a target article to upload!
        print(f"\n[Target Found!] Processing Article {i}: {article['title']}")

        if not img_url:
            img_url = upload_image(img_path)
            if img_url:
                article['image_url'] = img_url
                changed = True
            else:
                print(f"Warning: Failed to upload image at {img_path}. Skipping post.")
                continue

        # 2. Handle Amazon Link (Temporarily disabled for AdSense review)
        # import urllib.parse
        # keyword = article['labels'][0] if article.get('labels') else "本"
        # associate_id = "hyakushiki005-22"
        # encoded_keyword = urllib.parse.quote(keyword)
        # amazon_url = f"https://www.amazon.co.jp/s?k={encoded_keyword}&tag={associate_id}"
        
        # ad_html = f'''
        # <div class="amazon-ad-box">
        #     <p>＼ この記事に関連する商品をチェック ／</p>
        #     <a href="{amazon_url}" target="_blank" rel="noopener" class="amazon-btn">
        #         📦 Amazonで「{keyword}」を検索する
        #     </a>
        # </div>
        # '''
        ad_html = "" # AdSense審査通過までは広告を挿入しない

        # 3. Construct HTML
        img_tag = f'<div style="text-align: center;"><img src="{img_url}" style="max-width: 100%; height: auto; border-radius: 10px; margin-bottom: 20px;"></div>' if img_url else ""
        
        # 4. Fetch recent posts for internal linking
        internal_links_html = ""
        try:
            recent_posts_req = service.posts().list(blogId=blog_id, maxResults=3, fetchImages=False)
            recent_posts_res = recent_posts_req.execute()
            if 'items' in recent_posts_res:
                internal_links_html += "<div class='internal-links' style='margin-top: 30px; padding: 15px; background: #2a2a2a; border-radius: 8px;'>"
                internal_links_html += "<h3 style='color: #bb86fc; font-size: 1.2rem; margin-top: 0;'>あわせて読みたい関連記事</h3><ul style='line-height: 1.8;'>"
                for pItem in recent_posts_res['items']:
                    internal_links_html += f"<li><a href='{pItem['url']}'>{pItem['title']}</a></li>"
                internal_links_html += "</ul></div>"
        except Exception as e:
            print(f"Warning: Failed to fetch recent posts for internal linking: {e}")

        html_content = f"{img_tag}\n<p>{article['hook']}</p>\n{article['content']}\n{internal_links_html}\n{ad_html}"
        
        # 3. Post
        # Schedule: 1 post per day at 21:00
        publish_time = base_date + timedelta(days=posts_this_run)
        
        success = post_to_blogger(
            service, 
            blog_id, 
            article['title'], 
            html_content, 
            article['labels'],
            publish_time=publish_time
        )
        
        if success:
            article["posted_status"] = "scheduled"
            article["publish_date"] = publish_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            changed = True
            posts_this_run += 1
            
            # Save progress back to JSON immediately after each success
            with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            wait_time = random.randint(60, 180)
            print(f"Waiting {wait_time} seconds before next API call to avoid spam detection...")
            time.sleep(wait_time)
        else:
            print(f"Stopping due to error at index {i}. Google might have rate-limited you.")
            break

    if changed:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

    print("\n--- Completed ---")

if __name__ == '__main__':
    main()
