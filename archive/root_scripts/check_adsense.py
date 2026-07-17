import json
import re
import os

def analyze():
    print("--- AdSense Analysis ---")
    try:
        with open('trivia_articles.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Total articles: {len(data)}")
        
        has_privacy = any("プライバシー" in d['title'] or "プライバシー" in d['content'] for d in data)
        has_contact = any("問い合" in d['title'] or "問い合" in d['content'] for d in data)
        has_about = any("運営者" in d['title'] or "プロフィール" in d['title'] for d in data)
        
        print(f"Privacy Policy found: {has_privacy}")
        print(f"Contact page found: {has_contact}")
        print(f"About page found: {has_about}")
        
        links = []
        for d in data:
            found_links = re.findall(r'href=[\"\'](.*?)[\"\']', d['content'])
            links.extend(found_links)
            
        print(f"Total links in content: {len(links)}")
        if links:
            print(f"Sample links: {links[:10]}")
            
    except Exception as e:
        print(f"Error reading JSON: {e}")

if __name__ == "__main__":
    analyze()
