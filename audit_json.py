
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f"Total articles: {len(articles)}")

for i, a in enumerate(articles):
    issues = []
    if 'title' not in a: issues.append("MISSING TITLE")
    if 'hook' not in a: issues.append("MISSING HOOK")
    if 'content' not in a: issues.append("MISSING CONTENT")
    if 'labels' not in a: issues.append("MISSING LABELS")
    
    if issues:
        print(f"Index {i}: {issues}")
        if 'title' in a: print(f"  Title: {a['title']}")
