
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for i in range(0, 15):
    if i < len(articles):
        print(f"{i}: {articles[i]['title']}")
