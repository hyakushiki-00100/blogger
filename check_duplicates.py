
import json
from collections import Counter

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f"Total articles: {len(articles)}")

titles = [a['title'] for a in articles]
counts = Counter(titles)

print("\n--- Duplicates found ---")
has_duplicates = False
for title, count in counts.items():
    if count > 1:
        indices = [i for i, t in enumerate(titles) if t == title]
        print(f"'{title}' appears {count} times at indices: {indices}")
        has_duplicates = True

if not has_duplicates:
    print("No duplicate titles found.")

print("\n--- All Titles (0-99) ---")
for i, a in enumerate(articles):
    print(f"{i}: {a['title']}")
