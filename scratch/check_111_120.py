import json

data = json.load(open('trivia_articles.json', encoding='utf-8'))
print(f'Total: {len(data)}')
for i in range(111, 121):
    c = data[i].get('content', '')
    title = data[i].get('title', 'N/A')[:50]
    print(f'[{i}] len={len(c)} title={title}')
