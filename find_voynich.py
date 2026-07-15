
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for i, a in enumerate(articles):
    if "ヴォイニッチ" in a['title']:
        print(f"Index {i}: {a['title']}")
        if 'hook' not in a:
            print("MISSING HOOK")
