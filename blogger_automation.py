import os
import json
import pickle
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# --- Configuration ---
# You need to download 'credentials.json' from Google Cloud Console
# and put it in the same directory as this script.
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
ARTICLES_FILE = 'trivia_articles.json'
TOKEN_FILE = 'token.pickle'

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"Error: {CLIENT_SECRETS_FILE} not found.")
                print("Please download it from Google Cloud Console (OAuth 2.0 Client ID).")
                return None
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
        # Format: 2026-04-30T08:00:00Z
        body['published'] = publish_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        is_draft = False
    else:
        is_draft = False

    try:
        request = service.posts().insert(blogId=blog_id, body=body, isDraft=is_draft)
        response = request.execute()
        print(f"Successfully posted: {title}")
        return response
    except Exception as e:
        print(f"Failed to post {title}: {e}")
        return None

def main():
    # --- USER INPUT ---
    blog_id = input("Enter your Blogger Blog ID: ").strip()
    if not blog_id:
        print("Blog ID is required.")
        return

    service = get_authenticated_service()
    if not service:
        return

    if not os.path.exists(ARTICLES_FILE):
        print(f"Error: {ARTICLES_FILE} not found.")
        return

    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles. Starting upload...")

    # Start scheduling from tomorrow at 21:00 (9 PM) - a good time for "Sleepless Trivia"
    start_date = datetime.now() + timedelta(days=1)
    start_date = start_date.replace(hour=21, minute=0, second=0, microsecond=0)

    for i, article in enumerate(articles):
        publish_time = start_date + timedelta(days=i) # One post per day
        
        # Construct HTML content
        import urllib.parse
        keyword = article['labels'][0] if article.get('labels') else "本"
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
        
        # Construct HTML content (Amazonリンクを末尾に追加)
        html_content = f"<p>{article['hook']}</p>\n{article['content']}\n{ad_html}"
        
        post_to_blogger(
            service, 
            blog_id, 
            article['title'], 
            html_content, 
            article['labels'],
            publish_time=publish_time
        )
        
        # Brief pause to avoid rate limits
        time.sleep(1)

    print("\n--- All articles processed! ---")
    print("Check your Blogger 'Scheduled' tab to see the pending posts.")

if __name__ == '__main__':
    main()
