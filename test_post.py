
import os
import json
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# --- Configuration ---
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
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
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
            
    return build('blogger', 'v3', credentials=creds)

def main():
    blog_id = input("Enter your Blogger Blog ID: ").strip()
    if not blog_id:
        print("Blog ID is required.")
        return

    service = get_authenticated_service()
    if not service:
        return

    # Test Article (Draft)
    title = "【テスト投稿】眠れない夜の雑学"
    hook = "これはテスト投稿です。自動投稿システムが正常に動作しているか確認しています。"
    content = "<p>テスト投稿の本文です。この投稿は『下書き』として保存されます。</p>"
    labels = ["テスト", "雑学"]

    body = {
        'kind': 'blogger#post',
        'title': title,
        'content': f"<p>{hook}</p>\n{content}",
        'labels': labels
    }

    try:
        # isDraft=True to avoid accidental public posting
        request = service.posts().insert(blogId=blog_id, body=body, isDraft=True)
        response = request.execute()
        print(f"\nSuccessfully created a DRAFT post!")
        print(f"Title: {response['title']}")
        print(f"URL: {response['url']}")
        print("\nPlease check your Blogger dashboard (Drafts tab).")
    except Exception as e:
        print(f"Failed to create test post: {e}")

if __name__ == '__main__':
    main()
