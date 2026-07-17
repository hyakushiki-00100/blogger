import json

json_path = 'trivia_articles.json'

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f"Loaded {len(articles)} articles")
print(f"Article 111 content length BEFORE: {len(articles[111].get('content', ''))}")

# Simulate what expand_111_120.py does
articles[111] = {
    "title": "111: キツツキの脳振盪：なぜ1秒間に20回も頭をぶつけて無事なのか？ 驚異の衝撃吸収システム",
    "hook": "テスト用フック",
    "content": "<p>テスト内容" + "あ" * 2000 + "</p>",
    "labels": ["生物", "科学", "自然"]
}

print(f"Article 111 content length AFTER assignment: {len(articles[111].get('content', ''))}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("Written")

with open(json_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
print(f"Verified: {len(verify[111].get('content', ''))}")
