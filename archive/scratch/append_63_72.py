import re

md_path = 'c:/Users/hyaku/Dropbox/ブログ/Illustration_Outsourcing_Instructions.md'
txt_path = 'c:/Users/hyaku/Dropbox/ブログ/Illustration_Outsourcing_Instructions.txt'

with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update total counts
content = re.sub(r'## 制作リスト（計\d+枚）', '## 制作リスト（計43枚）', content)
content = re.sub(r'以下の\d+記事分のイラスト制作をお願いいたします。', '以下の43記事分のイラスト制作をお願いいたします。', content)

new_entries = '''

### 34. 【ID: 63】デジタルタトゥー
- **テーマ**: 一生消えないネットの記憶。あなたの不用意な一言が、未来のあなたを殺す日。
- **ファイル名**: `63.png`
- **イラストのイメージ**: 
  暗い部屋でスマートフォンを持つ人物。しかしその人物の肌（顔や腕）には、悪意のあるメッセージや過去の失敗を表すデジタルの文字が、まるで発光する刺青（タトゥー）のように深く刻み込まれている。サイバーパンク調のサスペンスフルで後戻りできない絶望感。
- **参考プロンプト**: A person in a dark room holding a glowing smartphone. Their skin is covered in glowing, glitchy digital text resembling tattoos, representing malicious messages and past mistakes permanently etched into them. Digital tattoo, cyberbullying, cyberpunk, psychological thriller, cinematic lighting, highly detailed.

### 35. 【ID: 64】沈黙の旋律
- **テーマ**: 一音も鳴らさない「世界一静かな曲」が、私たちに聴かせる本当の音とは？
- **ファイル名**: `64.png`
- **イラストのイメージ**: 
  荘厳なコンサートホール。スポットライトを浴びてグランドピアノの前に座るピアニスト。しかしピアニストは全く鍵盤に触れず、ただじっと静寂を守っている。客席には息を呑んで「無音」に耳を傾ける観客たち。静けさの中にある圧倒的な緊張感と芸術的な美しさ。
- **参考プロンプト**: A grand, majestic concert hall illuminated by a dramatic spotlight. A pianist sitting at a grand piano but not touching the keys, perfectly still in total silence. The audience is listening intently to the silence. John Cage's 4'33", profound silence, artistic tension, cinematic lighting, highly detailed.

### 36. 【ID: 65】プラズマ
- **テーマ**: 固体・液体・気体に続く「第4の物質状態」。宇宙の99%以上を占める「真の主役」の正体。
- **ファイル名**: `65.png`
- **イラストのイメージ**: 
  暗闇の中で、美しく輝くプラズマボールを中心に、紫やピンク、青の稲妻のようなプラズマのエネルギーが空間全体に幾何学的に広がっている。宇宙の神秘と、エネルギーの根源を感じさせるSF的で抽象的なアート。
- **参考プロンプト**: A glowing plasma ball in the dark, with beautiful purple, pink, and blue lightning-like plasma energy spreading geometrically across the space. The fourth state of matter, cosmic energy, sci-fi abstract art, mystical, cinematic lighting, highly detailed.

### 37. 【ID: 66】100年前の未来予測
- **テーマ**: 1900年に描かれた「西暦2000年」の姿。実現した夢と、想像もできなかった現実。
- **ファイル名**: `66.png`
- **イラストのイメージ**: 
  スチームパンクやレトロフューチャーの世界観。シルクハットやクラシックなドレスを着た人々が、真鍮で作られた奇妙な空飛ぶ機械や、奇妙なロボットが行き交うレトロで幻想的な未来都市を歩いている。温かみのあるセピア調と黄金色の光。
- **参考プロンプト**: A retro-futuristic or steampunk city set in the year 2000 as imagined by people in 1900. People in Victorian clothing and silk hats walking among brass flying machines and primitive robots. Retro-futurism, warm sepia and golden lighting, nostalgic, highly detailed, cinematic.

### 38. 【ID: 67】青い血液
- **テーマ**: カブトガニが持つ「魔法の血」が、私たちの命を救い続けているという衝撃の事実。
- **ファイル名**: `67.png`
- **イラストのイメージ**: 
  近未来的な医療ラボ、または薄暗い海岸。古代生物であるカブトガニの体が神秘的に発光しており、そこから採取された「鮮やかな青い血」が試験管やガラスの容器の中で魔法の薬のように美しく光を放っている。生命の神秘と医療技術の融合。
- **参考プロンプト**: A prehistoric horseshoe crab glowing mystically in a futuristic medical lab or a dark beach. Bright, glowing neon blue blood is being collected into glass vials, looking like a magical elixir. Horseshoe crab blue blood, medical miracle, ancient life, sci-fi, cinematic lighting, highly detailed.

### 39. 【ID: 68】アニミズム
- **テーマ**: 道具にも魂が宿るという人類最古の「孤独の癒し方」。
- **ファイル名**: `68.png`
- **イラストのイメージ**: 
  薄暗い古道具屋、または古い日本の家屋。長く使い込まれた時計やハサミ、急須などの古い道具たちが、まるで命を持っているかのように、かすかな霊的な光や精霊のシルエットをまとっている。暖かくも少し切ない、ジブリ映画のような神秘的な和の雰囲気。
- **参考プロンプト**: A dimly lit antique shop or old traditional house. Well-used tools like an old clock, scissors, and a teapot are enveloped in a faint, magical aura or spiritual silhouettes, as if they possess souls. Animism, spirits in objects, mystical, warm and slightly nostalgic, cinematic, highly detailed.

### 40. 【ID: 69】最後の言葉
- **テーマ**: 死の間際に放たれた「人生の凝縮」は、私たちに何を語るのか？
- **ファイル名**: `69.png`
- **イラストのイメージ**: 
  歴史的な偉人が最期を迎えるベッド。部屋全体は薄暗いが、人物の口元から発せられる「最後の言葉」が、金色の光を帯びた羽や文字となって空中に舞い上がっている。厳かでドラマチックな、人生の幕引きを象徴する美しいシーン。
- **参考プロンプト**: A historical figure on their deathbed in a dimly lit, solemn room. Their 'famous last words' materialize as glowing golden text or ethereal feathers floating up into the air from their lips. The final moment of life, dramatic, majestic, cinematic lighting, highly detailed.

### 41. 【ID: 70】夢の上書き
- **テーマ**: 目覚める直前の「二度寝」が、記憶と創造性を書き換える？
- **ファイル名**: `70.png`
- **イラストのイメージ**: 
  まどろみの中にある寝室。ベッドで眠る人物の頭の上で、現実の風景（時計や窓からの光）と、幻想的な夢の世界（空飛ぶ魚や歪んだ時計など）がパッチワークのように複雑に混ざり合い、キャンバスに上書きされるように溶け合っている。シュールレアリスムの絵画のような世界。
- **参考プロンプト**: A bedroom in the state of half-sleep. Above the sleeping person, the reality (a clock, morning light) and a surreal dream world (flying fish, melting clocks) are intricately mixing and overwriting each other like a surrealist painting canvas. Lucid dreaming, surrealism, mystical, highly detailed.

### 42. 【ID: 71】信号機のボタン
- **テーマ**: 押しても意味がない「プラセボ・ボタン」が、現代社会を救っている？
- **ファイル名**: `71.png`
- **イラストのイメージ**: 
  雨の降る都会の交差点。焦燥感に駆られた人物が、信号機の「歩行者用押しボタン」を何度も押している。しかし、そのボタンの内部の配線はどこにも繋がっておらず、ただ光るだけの偽物のボタンであることが透けて見えている。現代社会の虚無感と皮肉を描いたダークな風景。
- **参考プロンプト**: A rainy city intersection. An impatient person repeatedly pressing the pedestrian crosswalk button. However, an X-ray view reveals the wires inside the button are disconnected, showing it is just a glowing fake button. Placebo button, illusion of control, urban isolation, cinematic, highly detailed.

### 43. 【ID: 72】人体自然発火現象
- **テーマ**: 何の前触れもなく、人間が「足だけを残して」燃え尽きる戦慄のミステリー。
- **ファイル名**: `72.png`
- **イラストのイメージ**: 
  19世紀のクラシックな部屋。安楽椅子の上に、煙を上げる黒焦げの灰の山と、靴を履いたままの「無傷の片足」だけが残されている。周囲の家具は全く燃えておらず、部屋の中央だけが異常な超高温で燃え尽きたことを示す。不気味で背筋が凍るようなミステリーシーン。
- **参考プロンプト**: A classic 19th-century room. On an armchair rests a pile of smoking black ashes and a single perfectly intact human leg still wearing a shoe. The surrounding wooden furniture is completely unburned. Spontaneous human combustion, eerie, true mystery, creepy, cinematic lighting, highly detailed.
'''

md_content = content + new_entries

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

# Now convert md_content to txt format
txt_content = re.sub(r'^###\s+', '', md_content, flags=re.MULTILINE)
txt_content = re.sub(r'^##\s+', '', txt_content, flags=re.MULTILINE)
txt_content = re.sub(r'^#\s+', '', txt_content, flags=re.MULTILINE)

# Bold list items
txt_content = re.sub(r'^-\s\*\*(.*?)\*\*:\s?', r'\1: ', txt_content, flags=re.MULTILINE)

# Remove 2-space indentation
txt_content = re.sub(r'^  ', '', txt_content, flags=re.MULTILINE)

with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(txt_content)
