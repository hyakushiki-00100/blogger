"""バイラル記事(インデックス311〜320)専用のBloggerアップロードスクリプト。

既存記事の予約枠(毎日21:00 JST = 12:00 UTC)と衝突しないよう、
バイラル記事は毎日12:00 JST(= 03:00 UTC)に予約投稿する。

予約日はバイラル記事同士のみで連結するため、既存記事の
予約キュー(数ヶ月先まで埋まっている)を待たずに明日から投稿が始まる。
"""

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

# --- Configuration ---
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
ARTICLES_FILE = 'trivia_articles.json'
TOKEN_FILE = 'token.pickle'
UPLOAD_API_URL = 'https://catbox.moe/user/api.php'

# バイラル記事のインデックス範囲
VIRAL_INDICES = list(range(311, 321))

# 12:00 JST = 03:00 UTC
VIRAL_PUBLISH_HOUR_UTC = 3

MAX_POSTS_PER_RUN = 5


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


def upload_image(file_path):
    """Uploads an image to Catbox and returns the URL."""
    if not os.path.exists(file_path):
        print(f"Image not found: {file_path}")
        return None

    print(f"Uploading {file_path}...")
    try:
        with open(file_path, 'rb') as f:
            files = {
                'fileToUpload': (
                    os.path.basename(file_path),
                    f,
                    'application/octet-stream'
                )
            }
            data = {'reqtype': 'fileupload'}
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/150.0.0.0 Safari/537.36'
                )
            }
            response = requests.post(
                UPLOAD_API_URL, data=data, files=files,
                headers=headers, timeout=60
            )

        if response.status_code != 200:
            print(f"Upload failed: {response.status_code}")
            return None

        url = response.text.strip()
        if not url.startswith('https://'):
            print(f"Unexpected response: {url}")
            return None

        print(f"Success: {url}")
        return url

    except requests.Timeout:
        print("Upload timed out.")
        return None
    except requests.RequestException as e:
        print(f"Upload request error: {type(e).__name__}: {e}")
        return None
    except OSError as e:
        print(f"Image file error: {type(e).__name__}: {e}")
        return None


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
    # Blog IDをファイルから自動読み込み
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

    # --- バイラル記事同士のみで予約日を連結する ---
    # (既存記事の予約キューとは独立。時刻も12:00 JSTで既存の21:00と衝突しない)
    latest_viral_publish = None
    for i in VIRAL_INDICES:
        if i >= len(articles):
            continue
        pub_str = articles[i].get("publish_date")
        if pub_str:
            dt = datetime.strptime(pub_str, '%Y-%m-%dT%H:%M:%SZ')
            if latest_viral_publish is None or dt > latest_viral_publish:
                latest_viral_publish = dt

    if latest_viral_publish:
        base_date = latest_viral_publish + timedelta(days=1)
    else:
        # 明日の12:00 JST(03:00 UTC)から開始
        base_date = datetime.now() + timedelta(days=1)
    base_date = base_date.replace(
        hour=VIRAL_PUBLISH_HOUR_UTC, minute=0, second=0, microsecond=0
    )

    changed = False
    posts_this_run = 0

    for i in VIRAL_INDICES:
        if i >= len(articles):
            print(f"Index {i} does not exist in {ARTICLES_FILE}. Skipping.")
            continue

        article = articles[i]

        if article.get("posted_status") == "scheduled":
            print(f"Skipping index {i} (Already scheduled).")
            continue

        if posts_this_run >= MAX_POSTS_PER_RUN:
            print(f"\nReached the limit of {MAX_POSTS_PER_RUN} posts for this run.")
            break

        # 1. Handle Image
        img_url = article.get('image_url')
        img_path = article.get('image_path')

        if not img_path or not os.path.exists(img_path):
            for ext in ['.jpg', '.png', '.jpeg', '.webp']:
                test_path = os.path.join('images', f"{i}{ext}")
                if os.path.exists(test_path):
                    img_path = test_path
                    article['image_path'] = img_path
                    break

        # イラストが存在する記事のみ投稿する
        if not img_url and not (img_path and os.path.exists(img_path)):
            print(f"Skipping index {i} (No illustration yet: images/{i}.png).")
            continue

        print(f"\n[Target Found!] Processing Viral Article {i}: {article['title']}")

        if not img_url:
            img_url = upload_image(img_path)
            if img_url:
                article['image_url'] = img_url
                changed = True
            else:
                print(f"Warning: Failed to upload image at {img_path}. Skipping post.")
                continue

        # 2. Amazonリンク (AdSense審査通過までは広告を挿入しない)
        ad_html = ""

        # 3. Construct HTML
        img_tag = (
            f'<div style="text-align: center;">'
            f'<img src="{img_url}" style="max-width: 100%; height: auto; '
            f'border-radius: 10px; margin-bottom: 20px;"></div>'
        ) if img_url else ""

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

        # 5. Post — 1日1本、12:00 JST(03:00 UTC)で予約
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

    print("\n--- Completed (Viral batch) ---")
    print("バイラル記事は毎日12:00(正午)に予約投稿されます。既存記事の21:00枠とは重複しません。")


if __name__ == '__main__':
    main()
