import chardet

files = ['scratch/expand_111_120.py', 'scratch/expand_221_230.py', 'scratch/expand_121_130.py']
for f in files:
    try:
        with open(f, 'rb') as fp:
            raw = fp.read(1000)
        detected = chardet.detect(raw)
        print(f"{f}: {detected}")
    except:
        print(f"{f}: ERROR")
