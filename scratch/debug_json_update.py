import json
import os

json_path = 'c:/Users/hyaku/Dropbox/ブログ/trivia_articles.json'

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f"Loaded {len(articles)} articles")
print(f"Article 111 content length before: {len(articles[111].get('content', ''))}")

articles[111] = {
    "title": "TEST 111",
    "hook": "test hook",
    "content": "<p>Test content that is much longer than 2000 characters: " + "x" * 2100 + "</p>",
    "labels": ["test"]
}

print(f"Article 111 content length after assignment: {len(articles[111].get('content', ''))}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("Written successfully")

# Verify
with open(json_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
print(f"Verified article 111 content length: {len(verify[111].get('content', ''))}")
