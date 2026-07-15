files = ['scratch/expand_111_120.py', 'scratch/expand_221_230.py', 'scratch/expand_121_130.py']
for fname in files:
    try:
        with open(fname, 'rb') as fp:
            raw = fp.read(200)
        # Check for BOM
        has_utf8_bom = raw[:3] == b'\xef\xbb\xbf'
        # Check first few bytes
        print(f"{fname}:")
        print(f"  BOM: {has_utf8_bom}")
        print(f"  First bytes: {raw[:20]!r}")
        print(f"  File size (binary read): {len(raw)} (first 200 bytes)")
        # Count actual file size
        import os
        print(f"  Full file size: {os.path.getsize(fname)}")
    except Exception as e:
        print(f"{fname}: ERROR - {e}")
    print()
