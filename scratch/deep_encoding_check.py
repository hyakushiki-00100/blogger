import os

# Read expand_111_120.py as UTF-8 and count characters  
try:
    with open('scratch/expand_111_120.py', 'r', encoding='utf-8') as f:
        src = f.read()
    print(f"UTF-8 read: {len(src)} chars")
except Exception as e:
    print(f"UTF-8 read failed: {e}")

try:
    with open('scratch/expand_111_120.py', 'r', encoding='cp932') as f:
        src = f.read()
    print(f"CP932 read: {len(src)} chars")
except Exception as e:
    print(f"CP932 read failed: {e}")

# Also check expand_221_230.py
try:
    with open('scratch/expand_221_230.py', 'r', encoding='utf-8') as f:
        src = f.read()
    print(f"expand_221_230.py UTF-8 read: {len(src)} chars")
except Exception as e:
    print(f"expand_221_230.py UTF-8 read failed: {e}")

# Read as binary and decode
with open('scratch/expand_111_120.py', 'rb') as f:
    raw = f.read()

# Try decoding as UTF-8
try:
    decoded = raw.decode('utf-8')
    print(f"Binary->UTF8: {len(decoded)} chars")
    # Find the content area
    idx = decoded.find('content')
    if idx >= 0:
        print(f"First 'content' at {idx}: ...{decoded[idx:idx+200]}...")
except Exception as e:
    print(f"Binary->UTF8 failed: {e}")
