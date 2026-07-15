import feedparser
import os

# --- Configuration ---
RSS_URL = "https://sleepless-trivia.blogspot.com/feeds/posts/default?alt=rss"
LAST_POST_FILE = "last_x_manual_post_url.txt"

def print_tweet_helper():
    # 1. Fetch RSS feed
    print(f"--- Blog to X Helper ---")
    print(f"Fetching RSS feed...")
    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No posts found in the RSS feed.")
        return

    # 2. Get the latest post
    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link
    
    print(f"\n[Latest Article Found]\nTitle: {title}")

    # 3. Check if it's already been handled
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as f:
            last_url = f.read().strip()
        if last_url == link:
            print("\n(Note: This article was likely already handled. See below for content anyway)\n")

    # 4. Compose the tweet text for easy copy-pasting
    tweet_text = f"【新しい記事を公開しました】\n\n{title}\n\n#雑学 #ブログ #豆知識\n{link}"

    print("-" * 30)
    print("COPY AND PASTE TO X:")
    print("-" * 30)
    print(tweet_text)
    print("-" * 30)

    # 5. Ask if the user wants to mark this as done
    print("\nDid you post this? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        with open(LAST_POST_FILE, "w") as f:
            f.write(link)
        print("Marked as posted.")

if __name__ == "__main__":
    print_tweet_helper()
