import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('scratch/titles_271_310.txt', 'w', encoding='utf-8') as out:
    for i in range(271, 311):
        if i < len(articles):
            out.write(f'ID {i}: {articles[i]["title"]}\n')
