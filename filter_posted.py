
import json

already_posted = [
    "「ジャガイモが“火あぶり”にされた日 ― 近世ヨーロッパと異端の植物」",
    "4998mの謎、5000mの壁、 トンネルが5000mを超えない理由と、非常時に覆るルール",
    "4998メートルの壁：日本の長いトンネルに隠された秘密"
]

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# タイトルの一部が一致する場合も含めて除外
filtered = []
for a in articles:
    is_posted = False
    for p in already_posted:
        if p in a['title'] or a['title'] in p:
            is_posted = True
            break
    if not is_posted:
        filtered.append(a)

with open('trivia_articles.json', 'w', encoding='utf-8') as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"Removed posted articles. Remaining: {len(filtered)}")
