import pickle
import os
from googleapiclient.discovery import build

token_path = r'c:\Users\hyaku\Dropbox\ブログ\token.pickle'
if not os.path.exists(token_path):
    print("Token not found.")
    exit()

with open(token_path, 'rb') as token:
    creds = pickle.load(token)

service = build('blogger', 'v3', credentials=creds)
blog_id = '8261510983860135912'
try:
    blog = service.blogs().get(blogId=blog_id).execute()
    url = blog['url']
    print(f"URL: {url}")
    print(f"RSS: {url}feeds/posts/default?alt=rss")
except Exception as e:
    print(f"Error: {e}")
