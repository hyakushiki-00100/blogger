import json
import os

print(f"CWD: {os.getcwd()}")
json_path = 'trivia_articles.json'
abs_path = os.path.abspath(json_path)
print(f"Resolved JSON path: {abs_path}")
print(f"File exists: {os.path.exists(abs_path)}")
