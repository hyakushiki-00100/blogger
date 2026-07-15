
import os
import json
import pickle
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# --- Configuration ---
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
    blog_id = input("Enter your Blogger Blog ID: ").strip()
    start_index = int(input("Enter start index to resume from (e.g., 10 if you finished 10): ").strip())
    
    service = get_authenticated_service()
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Resuming from index {start_index}. Remaining: {len(articles) - start_index}")

    # Schedule from tomorrow at 21:00
    base_date = datetime.now() + timedelta(days=1)
    base_date = base_date.replace(hour=21, minute=0, second=0, microsecond=0)

    for i in range(start_index, len(articles)):
        article = articles[i]
        
        # --- Fixed scheduling logic: Relative to start_index ---
        days_from_start = i - start_index
        publish_time = base_date + timedelta(days=days_from_start)
        
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
        
        html_content = f"<p>{article['hook']}</p>\n{article['content']}\n{ad_html}"
        
        success = post_to_blogger(
            service, 
            blog_id, 
            article['title'], 
            html_content, 
            article['labels'],
            publish_time=publish_time
        )
        
        if success:
            # Update the article status in memory
            articles[i]['posted_status'] = 'scheduled'
            articles[i]['publish_date'] = publish_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            # Save progress back to JSON file immediately after each success
            with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
        else:
            print(f"Stopping at index {i} due to error. Please try again later.")
            break
        # Increased pause to be gentler on API (5 seconds)
        time.sleep(5)

    print("\n--- All articles processed! ---")
    print("Check your Blogger 'Scheduled' tab to see the pending posts.")

if __name__ == '__main__':
    main()
