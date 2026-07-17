import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
with open('scratch/titles_91_100.txt', 'w', encoding='utf-8') as out:
    for i in range(91, 101):
        out.write(f'ID {i}: {articles[i]["title"]}\n')
