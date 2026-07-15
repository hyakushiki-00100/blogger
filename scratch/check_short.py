import json

with open('c:/Users/hyaku/Dropbox/ブログ/trivia_articles.json', encoding='utf-8') as f:
    data = json.load(f)

# Find ALL short articles and group by range
short = [i for i, a in enumerate(data) if len(a.get('content', '')) < 2000]

print(f"Total articles: {len(data)}")
print(f"Short articles (< 2000 chars): {len(short)}")
print()

# Check which expand scripts exist and if they were run
ranges_to_check = [
    (100, 110), (111, 120), (121, 130), (131, 140), (141, 150), (151, 160),
    (161, 170), (171, 180), (181, 190), (191, 200), (201, 210), (211, 220),
    (221, 230), (231, 240), (241, 250), (251, 260), (261, 270), (271, 280),
    (281, 290), (291, 300), (301, 310)
]

for start, end in ranges_to_check:
    short_in_range = [i for i in short if start <= i <= end]
    total_in_range = len([i for i in range(start, min(end+1, len(data)))])
    if short_in_range:
        print(f"  [{start}-{end}]: {len(short_in_range)}/{total_in_range} still short")
    else:
        print(f"  [{start}-{end}]: ALL DONE OK")

print()
print("=== Next batch to expand ===")
# Find the first contiguous block of short articles
next_short = [i for i in short if i >= 100]
if next_short:
    first = next_short[0]
    print(f"Next short article starts at index {first}")
    # Show titles of next 10 to expand
    print(f"\nNext 10 short articles to expand:")
    for idx in next_short[:10]:
        title = data[idx].get('title', 'N/A')
        clen = len(data[idx].get('content', ''))
        print(f"  [{idx}] ({clen} chars) {title[:60]}")
