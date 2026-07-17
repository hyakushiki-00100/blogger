import json
with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
with open('titles_221_310.txt', 'w', encoding='utf-8') as out:
    for i in range(221, 311):
        t = articles[i]['title']
        h = articles[i].get('hook', '')
        out.write(f'{i}: {t}\n')
        out.write(f'   hook: {h}\n\n')
print('Done')
