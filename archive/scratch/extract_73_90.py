import json

def main():
    with open('trivia_articles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open('scratch/temp_73_90.txt', 'w', encoding='utf-8') as out:
        for i, a in enumerate(data):
            if 73 <= i <= 90:
                out.write(f"ID: {i}\n")
                out.write(f"Title: {a.get('title', '')}\n")
                out.write(f"Hook: {a.get('hook', '')}\n")
                out.write("-" * 40 + "\n")

if __name__ == '__main__':
    main()
