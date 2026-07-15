import json

path = r'c:\Users\hyaku\Dropbox\ブログ\trivia_articles.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Checking articles 100 to 206:")
empty_indices = []
for i in range(100, len(data)):
    content = data[i].get('content', '').strip()
    if not content:
        empty_indices.append(i)

if empty_indices:
    print(f"Found {len(empty_indices)} articles with empty content.")
    print(f"Range: {min(empty_indices)} to {max(empty_indices)}")
    print("\nFirst few empty titles:")
    for idx in empty_indices[:5]:
        print(f"Index {idx}: {data[idx]['title']}")
else:
    print("All articles from 100 onwards have content.")

# Also check the very last ones I added
print("\nChecking the last few articles:")
for i in range(max(0, len(data)-5), len(data)):
    has_content = "Yes" if data[i].get('content', '').strip() else "No"
    print(f"Index {i}: {data[i]['title']} (Content: {has_content})")
