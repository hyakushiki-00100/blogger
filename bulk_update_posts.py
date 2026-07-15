
import os
import json
import pickle
import time
import re
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
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('blogger', 'v3', credentials=creds)

def remove_amazon_links(content):
    """Remove amazon-ad-box div from post content."""
    # Remove <div class="amazon-ad-box">...</div> (including whitespace/newlines)
    cleaned = re.sub(
        r'\s*<div\s+class=["\']amazon-ad-box["\']>.*?</div>\s*',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )
    return cleaned.strip()

def build_internal_links_html(recent_posts):
    """Build 'also read' internal links HTML block."""
    if not recent_posts:
        return ""
    html = "<div class='internal-links' style='margin-top: 30px; padding: 15px; background: #2a2a2a; border-radius: 8px;'>"
    html += "<h3 style='color: #bb86fc; font-size: 1.2rem; margin-top: 0;'>あわせて読みたい関連記事</h3>"
    html += "<ul style='line-height: 1.8;'>"
    for p in recent_posts:
        html += f"<li><a href='{p['url']}'>{p['title']}</a></li>"
    html += "</ul></div>"
    return html

def get_all_posts(service, blog_id):
    """Fetch all posts from Blogger with pagination."""
    all_posts = []
    page_token = None
    print("Fetching all posts from Blogger...")
    while True:
        req = service.posts().list(
            blogId=blog_id,
            maxResults=500,
            status=['LIVE', 'SCHEDULED'],
            pageToken=page_token
        )
        res = req.execute()
        items = res.get('items', [])
        all_posts.extend(items)
        print(f"  Fetched {len(all_posts)} posts so far...")
        page_token = res.get('nextPageToken')
        if not page_token:
            break
    print(f"Total posts fetched: {len(all_posts)}")
    return all_posts

def main():
    blog_id_file = 'Blogger_brog_id.txt'
    blog_id = ""
    if os.path.exists(blog_id_file):
        with open(blog_id_file, 'r') as f:
            blog_id = f.read().strip()
    if not blog_id:
        blog_id = input("Enter your Blogger Blog ID: ").strip()

    service = get_authenticated_service()
    all_posts = get_all_posts(service, blog_id)

    if not all_posts:
        print("No posts found.")
        return

    # Use all posts as internal link pool, take first 3 as "recent"
    # (sorted by published date descending — Blogger returns newest first by default)
    recent_posts_for_links = all_posts[:3]
    internal_links_html = build_internal_links_html(recent_posts_for_links)

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for i, post in enumerate(all_posts):
        post_id = post['id']
        post_title = post['title']
        original_content = post.get('content', '')

        # Step 1: Remove Amazon ad box
        new_content = remove_amazon_links(original_content)

        # Step 2: Check if internal links already added (avoid duplicates)
        already_has_internal = "internal-links" in original_content

        # Step 3: Append internal links if not already present
        if not already_has_internal:
            new_content = new_content + "\n" + internal_links_html

        # If nothing changed, skip API call
        if new_content.strip() == original_content.strip():
            print(f"[{i+1}/{len(all_posts)}] SKIP (no change): {post_title[:40]}...")
            skipped_count += 1
            continue

        # Step 4: Update post via API
        body = {
            'kind': 'blogger#post',
            'id': post_id,
            'title': post_title,
            'content': new_content,
            'labels': post.get('labels', [])
        }
        try:
            service.posts().update(blogId=blog_id, postId=post_id, body=body).execute()
            print(f"[{i+1}/{len(all_posts)}] UPDATED: {post_title[:50]}...")
            updated_count += 1
        except Exception as e:
            print(f"[{i+1}/{len(all_posts)}] ERROR: {post_title[:40]}... -> {e}")
            error_count += 1

        # Pause to avoid rate limiting
        time.sleep(2)

    print(f"\n--- Complete ---")
    print(f"Updated: {updated_count}, Skipped: {skipped_count}, Errors: {error_count}")

if __name__ == '__main__':
    main()
