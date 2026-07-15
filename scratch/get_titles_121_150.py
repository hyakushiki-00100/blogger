import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('scratch/titles_121_150.txt', 'w', encoding='utf-8') as out:
    for i in range(121, 151):
        if i < len(articles):
            out.write(f'ID {i}: {articles[i]["title"]}\n')
