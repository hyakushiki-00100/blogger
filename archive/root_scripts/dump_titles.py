
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('titles.txt', 'w', encoding='utf-8') as f:
    for i, a in enumerate(articles):
        f.write(f"{i}: {a['title']}\n")
print("Titles dumped to titles.txt")
