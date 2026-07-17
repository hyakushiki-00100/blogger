
import json
from collections import Counter

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f"Total articles: {len(articles)}")

# Check for duplicate titles
titles = [a['title'] for a in articles]
title_counts = Counter(titles)
duplicates = [t for t, c in title_counts.items() if c > 1]
if duplicates:
    print("\nDuplicate Titles Found:")
    for d in duplicates:
        print(f"- {d}")
else:
    print("\nNo exact duplicate titles.")

# Check for duplicate hooks
hooks = [a['hook'] for a in articles]
hook_counts = Counter(hooks)
dup_hooks = [h for h, c in hook_counts.items() if c > 1]
if dup_hooks:
    print("\nDuplicate Hooks Found:")
    for d in dup_hooks:
        print(f"- {d}")
else:
    print("\nNo exact duplicate hooks.")

# Check for duplicate content snippets (first 50 chars)
contents = [a['content'][:50] for a in articles]
content_counts = Counter(contents)
dup_contents = [c for c, count in content_counts.items() if count > 1]
if dup_contents:
    print("\nDuplicate Content (Start) Found:")
    for d in dup_contents:
        print(f"- {d}")
else:
    print("\nNo duplicate content starts.")
