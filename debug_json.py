
import json

with open('trivia_articles.json', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
    # If the corruption makes it invalid JSON, we might need to fix it manually
    try:
        data = json.loads(content)
        print(f"Successfully loaded {len(data)} articles (with replacement characters)")
        for i, a in enumerate(data):
            title = a.get('title', 'NO TITLE')
            # Check if it's a placeholder
            is_placeholder = "未解決ミステリー" in title or "驚異：知られざる事実" in title or "placeholder" in a.get('content', '').lower()
            if i < 10 or i > 90 or not is_placeholder:
                 print(f"{i}: {title} {'(PLACEHOLDER)' if is_placeholder else ''}")
    except Exception as e:
        print(f"JSON Load Error: {e}")
        # Try to find where it breaks
        print("Content around break (approx):")
        print(content[39800:40000])
