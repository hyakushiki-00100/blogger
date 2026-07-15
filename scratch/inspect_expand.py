import json
import sys

# Read the expand_111_120.py script as a module to inspect its content
import importlib.util
spec = importlib.util.spec_from_file_location("expand_111_120", "scratch/expand_111_120.py")
# Can't inspect easily, so let's just check what the actual content string looks like in that file

with open('scratch/expand_111_120.py', 'r', encoding='utf-8') as f:
    src = f.read()

print(f"Script size: {len(src)} chars")
# Find where articles[111] content is defined
idx = src.find('articles[111]')
print(f"Found articles[111] at position {idx}")
# Print 200 chars around it
print(src[idx:idx+500])
