import json
import os
import time

json_path = 'trivia_articles.json'

# Time before write
mtime_before = os.path.getmtime(json_path)
size_before = os.path.getsize(json_path)
print(f'BEFORE: mtime={mtime_before}, size={size_before}')

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

content_before = len(articles[111].get('content', ''))
print(f'BEFORE: content[111] len = {content_before}')

# Make a small change
articles[111]['content'] = '<p>Updated test content: ' + 'テスト' * 700 + '</p>'
print(f'Setting content[111] to len = {len(articles[111]["content"])}')

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

mtime_after = os.path.getmtime(json_path)
size_after = os.path.getsize(json_path)
print(f'AFTER WRITE: mtime={mtime_after}, size={size_after}')

# Wait a moment
time.sleep(2)

mtime_after2 = os.path.getmtime(json_path)
size_after2 = os.path.getsize(json_path)
print(f'AFTER 2s: mtime={mtime_after2}, size={size_after2}')

with open(json_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)

content_after = len(verify[111].get('content', ''))
print(f'VERIFIED: content[111] len = {content_after}')
