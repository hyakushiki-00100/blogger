import json

path = r'c:\Users\hyaku\Dropbox\ブログ\trivia_articles.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

last_scheduled = -1
for i, article in enumerate(data):
    if article.get('posted_status') == 'scheduled':
        last_scheduled = i

print(f"Last scheduled index: {last_scheduled}")
if last_scheduled != -1:
    print(f"Title: {data[last_scheduled]['title']}")
    print(f"Publish Date: {data[last_scheduled].get('publish_date')}")
