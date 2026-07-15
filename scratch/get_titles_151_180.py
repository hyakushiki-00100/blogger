import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('scratch/titles_151_180.txt', 'w', encoding='utf-8') as out:
    for i in range(151, 181):
        if i < len(articles):
            out.write(f'ID {i}: {articles[i]["title"]}\n')
