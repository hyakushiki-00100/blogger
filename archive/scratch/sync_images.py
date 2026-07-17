import json
import os

path = r'c:\Users\hyaku\Dropbox\ブログ\trivia_articles.json'
img_dir = r'c:\Users\hyaku\Dropbox\ブログ\images'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, article in enumerate(data):
    # Check for image file matching the index
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        if os.path.exists(os.path.join(img_dir, f"{i}{ext}")):
            article['image_path'] = f"images/{i}{ext}"
            break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Synchronized JSON image paths with existing files in images/ directory.")
