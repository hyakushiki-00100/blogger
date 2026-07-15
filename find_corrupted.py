
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for i, a in enumerate(articles):
    if 'hook' not in a or 'title' not in a or 'content' not in a:
        print(f"Corrupted index {i}: Keys {list(a.keys())}")
    elif "ヴォイニッチ" in a['title']:
        print(f"Index {i}: {a['title']}")
