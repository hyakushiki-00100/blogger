import json
import os

json_path = 'trivia_articles.json'

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f'Before: articles[111] content len = {len(articles[111].get("content", ""))}')

articles[111] = {
    "title": "111: キツツキの脳振盪：なぜ1秒間に20回も頭をぶつけて無事なのか？ 驚異の衝撃吸収システム",
    "hook": "森に響き渡るキツツキのドラミング音。彼らは1秒間に最大20回、重力の1000倍以上の衝撃で木をつつきますが、決して脳振盪を起こしません。",
    "content": "<p>静かな森の中を歩いていると、突然「ドドドドド！」という機関銃のような音が聞こえてくることがあります。キツツキが木の幹をくちばしで激しく叩く「ドラミング」です。彼らは虫を探したり、巣穴を掘ったり、あるいは求愛の合図として木を叩き続けます。そのスピードは1秒間に最大20回、頭にかかる衝撃は重力加速度の1000倍（1000G）を超えます。人間ならたった1回で重度の脳振盪を起こす衝撃ですが、なぜ彼らの脳は無事なのでしょうか。</p><h3>1. 頭蓋骨を包み込む「シートベルト」</h3><p>キツツキの衝撃吸収システムの最大の秘密は、「舌」にあります。キツツキの舌は驚くほど長く、くちばしの付け根から後頭部をぐるりと迂回し、なんと右の鼻の穴にまで達しています。この長く強靭な舌の骨（舌骨）と筋肉が、ヘルメットのあご紐やシートベルトのように頭蓋骨をしっかりとホールドし、衝撃から脳を守っているのです。</p><h3>2. スポンジ状の骨と極小の脳</h3><p>さらに、キツツキの頭蓋骨の一部（特に前頭部）は、細かい空洞がたくさんある「スポンジ状（海綿状）」になっており、これがクッションの役割を果たして衝撃を分散させます。また、彼らの脳自体が約2グラムと非常に小さく、頭蓋骨の中に隙間なくピタッと収まっているため、衝撃を受けても脳が頭蓋骨の中で揺れ動くことがありません。</p><h3>3. 人類の安全技術への応用</h3><p>キツツキのこの完璧な衝撃吸収システムは、バイオミメティクス（生物模倣技術）の分野で大きな注目を集めています。現在、自動車のショックアブソーバーや、アメリカンフットボールの選手のヘルメット、さらには宇宙船の微小隕石保護シールドなど、様々な安全技術にキツツキの頭部構造を応用する研究が進められています。</p>",
    "labels": ["生物", "科学", "自然"]
}

new_len = len(articles[111]['content'])
print(f'After assignment: articles[111] content len = {new_len}')

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f'Written. File size: {os.path.getsize(json_path)}')

# Re-read
with open(json_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
print(f'Verified: articles[111] content len = {len(verify[111].get("content", ""))}')
