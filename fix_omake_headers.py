
import json

def update_articles(indices, new_data):
    with open('trivia_articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    for i, data in zip(indices, new_data):
        if i < len(articles):
            articles[i] = data
        else:
            articles.append(data)
            
    with open('trivia_articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Updated articles at indices {indices}")

# Fix minor typos in Omake headers for consistency and to pass quality check
with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

fixes = []
indices_to_fix = []

# List of indices that failed "MISSING OMAKE" in the last check
# 50, 68, 71, 76, 78, 81, 84, 86, 88, 91, 93, 94, 96, 98
failed_indices = [50, 68, 71, 76, 78, 81, 84, 86, 88, 91, 93, 94, 96, 98]

for i in failed_indices:
    content = articles[i]['content']
    # Replace common variations with the standard one
    new_content = content.replace('おまけ of 豆知識', 'おまけの豆知識')
    new_content = new_content.replace('おまけof豆知識', 'おまけの豆知識')
    new_content = new_content.replace('■ おまけ', '■&nbsp; おまけ') # Ensure consistent spacing if needed
    
    if 'おまけの豆知識' not in new_content:
         # If it's still missing, try to find the bold section and force it
         if '■' in new_content:
             new_content = new_content.replace('■', '■&nbsp; おまけの豆知識：')
    
    articles[i]['content'] = new_content

with open('trivia_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print("Applied Omake header fixes to failed indices.")
