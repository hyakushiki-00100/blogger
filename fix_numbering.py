import json
import re

def fix_all():
    json_path = r'c:\Users\hyaku\Dropbox\ブログ\trivia_articles.json'
    titles_path = r'c:\Users\hyaku\Dropbox\ブログ\titles.txt'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
        
    titles_list = []
    
    for i, article in enumerate(articles):
        title = article['title']
        # Remove any existing number prefix like "12: " or "200: "
        clean_title = re.sub(r'^\d+:\s*', '', title)
        
        # Add the correct prefix
        new_title = f"{i}: {clean_title}"
        article['title'] = new_title
        titles_list.append(new_title)
        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
        
    with open(titles_path, 'w', encoding='utf-8') as f:
        for t in titles_list:
            f.write(t + '\n')
            
    print(f"Fixed numbering for {len(articles)} articles.")

if __name__ == "__main__":
    fix_all()
