
import urllib.request
import re

url = 'https://sleepless-trivia.blogspot.com/'
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        match = re.search(r'blogId["\']?:\s*["\']?(\d+)["\']?', html)
        if match:
            print(f"BLOG_ID={match.group(1)}")
        else:
            # Try another way
            match = re.search(r'data-blog-id=["\']?(\d+)["\']?', html)
            if match:
                print(f"BLOG_ID={match.group(1)}")
            else:
                print("Blog ID not found")
except Exception as e:
    print(f"Error: {e}")
