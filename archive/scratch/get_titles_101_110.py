import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
with open('scratch/titles_101_110.txt', 'w', encoding='utf-8') as out:
    for i in range(101, 111):
        out.write(f'ID {i}: {articles[i]["title"]}\n')
