
import json

def try_read(path):
    encodings = ['utf-8', 'shift-jis', 'cp932', 'utf-8-sig']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                data = json.load(f)
                print(f"Successfully read with {enc}")
                return data
        except Exception as e:
            print(f"Failed with {enc}: {e}")
    return None

data = try_read('trivia_articles.json')
if data:
    with open('trivia_articles_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved as trivia_articles_fixed.json in utf-8")
