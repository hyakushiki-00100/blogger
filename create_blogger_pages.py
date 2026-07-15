import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
TOKEN_FILE = 'token.pickle'
BLOG_ID_FILE = 'Blogger_brog_id.txt'

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

def main():
    blog_id = ""
    if os.path.exists(BLOG_ID_FILE):
        with open(BLOG_ID_FILE, 'r') as f:
            blog_id = f.read().strip()
    
    if not blog_id:
        print("Error: Blogger_brog_id.txt not found.")
        return

    service = get_authenticated_service()

    # 1. About Page
    about_html = """
    <h2>運営者プロフィール</h2>
    <p>当ブログ「深夜に読むと眠れなくなる雑学」の管理人です。</p>
    <p>歴史のミステリー、科学の不思議、世界中の都市伝説など、知的好奇心をくすぐる雑学を毎日お届けしています。</p>
    <p>※AdSense審査用の仮プロフィールです。後でBloggerの管理画面から自由に変更してください。</p>
    """
    about_body = {
        'kind': 'blogger#page',
        'title': '運営者情報',
        'content': about_html
    }
    
    try:
        req = service.pages().insert(blogId=blog_id, body=about_body)
        res = req.execute()
        print(f"Created Page: {res['title']} ({res['url']})")
    except Exception as e:
        print(f"Failed to create About page: {e}")

    # 2. Contact Page
    contact_html = """
    <h2>お問い合わせ</h2>
    <p>当サイトに関するお問い合わせ、ご意見ご感想は以下のフォームよりお願いいたします。</p>
    <p><a href="https://docs.google.com/forms/" target="_blank" rel="noopener">【ここにご自身のGoogleフォームのリンクを貼り付けてください】</a></p>
    """
    contact_body = {
        'kind': 'blogger#page',
        'title': 'お問い合わせ',
        'content': contact_html
    }
    
    try:
        req = service.pages().insert(blogId=blog_id, body=contact_body)
        res = req.execute()
        print(f"Created Page: {res['title']} ({res['url']})")
    except Exception as e:
        print(f"Failed to create Contact page: {e}")

if __name__ == '__main__':
    main()
