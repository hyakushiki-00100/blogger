import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/hyaku/Dropbox/ブログ/trivia_articles.json', encoding='utf-8') as f:
    data = json.load(f)

# Show exact content lengths of 100 to 115
for idx in range(100, 116):
    if idx < len(data):
        title = data[idx].get('title', 'N/A')
        clen = len(data[idx].get('content', ''))
        print(f"[{idx}] ({clen} chars) {title[:40]}")
