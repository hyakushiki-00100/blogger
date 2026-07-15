
import json
import os

def update_json_structure():
    with open('trivia_articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    for i, article in enumerate(articles):
        # Add image_path field if it doesn't exist
        # We will use local paths like 'images/article_0.png'
        article['image_path'] = f"images/article_{i}.png"
        # Add image_url field to store the uploaded URL later
        if 'image_url' not in article:
            article['image_url'] = ""
            
    with open('trivia_articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {len(articles)} articles with image fields.")

if __name__ == '__main__':
    update_json_structure()
