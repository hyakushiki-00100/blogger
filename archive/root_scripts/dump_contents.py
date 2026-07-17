
import json
import re

def strip_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('all_contents.txt', 'w', encoding='utf-8') as f:
    for i, a in enumerate(articles):
        f.write(f"【No.{i}】 {a['title']}\n")
        f.write(f"HOOK: {a['hook']}\n")
        f.write("-" * 50 + "\n")
        # Strip HTML for readability in text file, but keep some spacing
        content = a['content'].replace('</h3>', '</h3>\n').replace('</p>', '</p>\n\n')
        f.write(strip_html(content))
        f.write("\n" + "=" * 80 + "\n\n")

print(f"Contents dumped to all_contents.txt. Total: {len(articles)} articles.")
