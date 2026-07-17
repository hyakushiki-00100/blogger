import json
import os

path = r'c:\Users\hyaku\Dropbox\ブログ\trivia_articles.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

total = len(data)
posted = [x for x in data if "posted_status" in x]
unposted = [x for x in data if "posted_status" not in x]

print(f"Total articles: {total}")
print(f"Posted/Scheduled: {len(posted)}")
print(f"Un-uploaded: {len(unposted)}")

if unposted:
    print("\nNext few un-uploaded titles:")
    for x in unposted[:5]:
        print(f"- {x['title']}")
