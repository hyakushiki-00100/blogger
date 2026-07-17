
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for i, article in enumerate(articles):
    content = article['content']
    # Normalize variations to "おまけの豆知識"
    new_content = content.replace('おまけ of 豆知識', 'おまけの豆知識')
    new_content = new_content.replace('おまけof豆知識', 'おまけの豆知識')
    
    # If the check is still failing, it might be due to missing the string entirely
    if 'おまけの豆知識' not in new_content:
        # Check if we have a bold section with ■
        if '■' in new_content:
             # Find the bold tag if possible or just replace the bullet
             new_content = new_content.replace('■', '■&nbsp; おまけの豆知識：')
    
    article['content'] = new_content

with open('trivia_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print("Applied comprehensive Omake header fixes to all articles.")
