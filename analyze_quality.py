
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for i, a in enumerate(articles):
    title = a.get('title', 'No Title')
    hook = a.get('hook', '')
    content = a.get('content', '')
    
    issues = []
    if not hook:
        issues.append("MISSING HOOK")
    if len(content) < 1000: # Aiming for higher volume as requested
        issues.append(f"SHORT CONTENT ({len(content)} chars)")
    if "おまけの豆知識" not in content:
        issues.append("MISSING OMAKE")
        
    if issues:
        print(f"{i}: {title} -> {', '.join(issues)}")
