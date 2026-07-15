
import json
import os

file_path = r'c:\Users\hyaku\Dropbox\ブログ\trivia_articles.json'

if not os.path.exists(file_path):
    print("File not found")
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"Total articles: {len(articles)}")
    
    placeholders = 0
    valid = 0
    for i, a in enumerate(articles):
        if "未解決ミステリー" in a['title'] or "placeholder" in a['content'].lower() or len(a['content']) < 200:
            placeholders += 1
            if placeholders == 1:
                print(f"First placeholder at index {i}: {a['title']}")
        else:
            valid += 1
            
    print(f"Valid articles: {valid}")
    print(f"Placeholder articles: {placeholders}")
