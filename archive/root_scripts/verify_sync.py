
import json

with open('trivia_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('titles.txt', 'r', encoding='utf-8') as f:
    titles_txt = f.readlines()

mismatches = []
for i in range(len(data)):
    json_title = data[i]['title']
    # titles.txt starts with index 0 at line 1 (i=0 -> titles_txt[0])
    # Wait, titles.txt content:
    # 0: エミュー戦争...
    # So it should match.
    if i < len(titles_txt):
        line = titles_txt[i].strip()
        if json_title not in line:
            mismatches.append(f"Index {i}: JSON='{json_title}' vs TXT='{line}'")

if not mismatches:
    print("ALL SYNCED PERFECTLY.")
else:
    for m in mismatches:
        print(m)
