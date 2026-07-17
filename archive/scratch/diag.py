import json
import os

json_path = 'trivia_articles.json'
abs_path = os.path.abspath(json_path)
print(f'CWD: {os.getcwd()}')
print(f'Absolute path: {abs_path}')
print(f'File exists: {os.path.exists(abs_path)}')
print(f'File size: {os.path.getsize(abs_path)}')
print(f'Last modified: {os.path.getmtime(abs_path)}')

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

content_111 = articles[111].get('content', '')
print(f'len(articles[111].content) = {len(content_111)}')
print(f'First 100 chars: {content_111[:100]}')
