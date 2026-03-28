"""Species husbandry / care environment data for all 21 species.

Each species entry contains bilingual (ja/en) information about:
- temperature: Optimal temperature range
- humidity: Optimal humidity range
- subtypes (optional): Breed/type-specific care data for species with
  significant variation (e.g. lizard → bearded dragon, leopard gecko, chameleon)
- housing: Housing requirements
- diet: Dietary needs
- enrichment: Environmental enrichment
- socialization: Social needs
- notes: Additional care notes
"""

HUSBANDRY_DATA: dict = {
    # =========================================================================
    # 犬 (Dog)
    # =========================================================================
    "dog": {
        "name": "Dog",
        "name_ja": "犬",
        "temperature": {
            "en": "18–26°C (64–79°F); breed-dependent (brachycephalic breeds are heat-sensitive)",
            "ja": "18〜26℃（短頭種は暑さに弱いため夏季は特に注意）",
        },
        "humidity": {
            "en": "40–60% relative humidity",
            "ja": "40〜60%（高湿度環境では皮膚疾患のリスク上昇）",
        },
        "housing": {
            "en": "Indoor living with outdoor access recommended. Crate training useful for puppies. Adequate space for size/breed. Secure fencing for yard.",
            "ja": "室内飼育＋屋外運動推奨。子犬期はクレートトレーニングが有効。体格・犬種に合った十分なスペースを確保。庭は脱走防止柵を設置。",
        },
        "diet": {
            "en": "Balanced commercial dog food appropriate for life stage (puppy/adult/senior). Fresh water always available. Avoid toxic foods: chocolate, grapes, onions, xylitol, macadamia nuts.",
            "ja": "ライフステージ（子犬・成犬・シニア）に応じた総合栄養食。常に新鮮な水を用意。中毒食品に注意：チョコレート、ブドウ、タマネギ、キシリトール、マカダミアナッツ。",
        },
        "enrichment": {
            "en": "Daily exercise (30–120 min depending on breed). Mental stimulation with puzzle toys, training sessions. Socialization with people and other dogs.",
            "ja": "毎日の運動（犬種により30〜120分）。知育玩具やトレーニングで精神的刺激。人や他の犬との社会化。",
        },
        "socialization": {
            "en": "Highly social species. Critical socialization period: 3–14 weeks of age. Regular interaction with family members essential. Separation anxiety common if left alone too long.",
            "ja": "非常に社会性の高い動物。社会化の臨界期は生後3〜14週齢。家族との日常的な交流が不可欠。長時間の留守番は分離不安の原因に。",
        },
        "notes": {
            "en": "Annual veterinary checkups recommended. Regular dental care, nail trimming, and grooming. Parasite prevention (heartworm, fleas, ticks) year-round in endemic areas.",
            "ja": "年1回以上の定期健診推奨。歯のケア・爪切り・被毛の手入れを定期的に。フィラリア・ノミ・マダニの通年予防（流行地域）。",
        },
    },
    # =========================================================================
    # 猫 (Cat)
    # =========================================================================
    "cat": {
        "name": "Cat",
        "name_ja": "猫",
        "temperature": {
            "en": "18–27°C (64–80°F); cats prefer warm environments",
            "ja": "18〜27℃（猫は暖かい環境を好む）",
        },
        "humidity": {
            "en": "40–60% relative humidity",
            "ja": "40〜60%",
        },
        "housing": {
            "en": "Indoor-only recommended for safety and longevity. Vertical space (cat trees, shelves) important. Multiple litter boxes (n+1 rule: one per cat plus one extra). Scratching posts essential.",
            "ja": "安全と長寿のため完全室内飼育推奨。キャットタワーや棚で垂直空間を確保。トイレは頭数＋1個。爪とぎを必ず設置。",
        },
        "diet": {
            "en": "Obligate carnivore — high-protein diet essential. Wet food helps with hydration. Fresh water (many cats prefer running water/fountains). Avoid: onions, garlic, lilies, chocolate.",
            "ja": "完全肉食動物 — 高タンパク質の食事が不可欠。ウェットフードで水分補給。新鮮な水（流水式給水器を好む猫が多い）。中毒食品：タマネギ、ニンニク、ユリ科植物、チョコレート。",
        },
        "enrichment": {
            "en": "Interactive play sessions (15–30 min/day). Window perches for bird watching. Puzzle feeders. Rotating toys to maintain interest. Catnip or silver vine for stimulation.",
            "ja": "1日15〜30分のインタラクティブな遊び。窓辺にバードウォッチング用の台。フードパズル。おもちゃはローテーション。マタタビやキャットニップ。",
        },
        "socialization": {
            "en": "Independent but social. Critical socialization: 2–7 weeks. Multi-cat households need adequate resources to prevent stress. Some cats prefer being the only pet.",
            "ja": "独立心が強いが社会性もある。社会化の臨界期は生後2〜7週齢。多頭飼育ではストレス予防のため十分な資源を確保。単独飼育を好む個体も。",
        },
        "notes": {
            "en": "Annual veterinary checkups. Indoor cats still need parasite prevention. Dental disease very common — regular dental checks. Senior cats (7+) benefit from biannual checkups.",
            "ja": "年1回の定期健診。室内猫もノミ・寄生虫予防を。歯周病が非常に多い — 定期的な歯科検診を。7歳以上は年2回の健診推奨。",
        },
    },
    # =========================================================================
    # ウサギ (Rabbit)
    # =========================================================================
    "rabbit": {
        "name": "Rabbit",
        "name_ja": "ウサギ",
        "temperature": {
            "en": "15–24°C (59–75°F); heat stroke risk above 28°C. Cold tolerant but drafts should be avoided.",
            "ja": "15〜24℃。28℃以上で熱中症のリスク。寒さには比較的強いが隙間風は避ける。",
        },
        "humidity": {
            "en": "40–60% relative humidity",
            "ja": "40〜60%",
        },
        "housing": {
            "en": "Spacious enclosure (minimum 4x body length). Daily free-roaming time (3+ hours) in rabbit-proofed area. Hide boxes for security. Non-slip flooring (not wire mesh).",
            "ja": "広いケージ（体長の4倍以上）。毎日3時間以上のウサギ対策済みエリアでの放し飼い時間。隠れ家を設置。床は滑りにくい素材（金網不可）。",
        },
        "diet": {
            "en": "80% unlimited timothy hay (critical for dental/GI health). Fresh leafy greens daily (romaine, cilantro, parsley). Limited pellets (1/8–1/4 cup/day for adults). Avoid: iceberg lettuce, beans, potatoes.",
            "ja": "80%はチモシー牧草（食べ放題 — 歯と消化管の健康に不可欠）。毎日新鮮な葉物野菜（ロメインレタス、パクチー、パセリ等）。ペレットは少量（成兎で1日大さじ2〜4杯）。禁忌：玉レタス、豆類、ジャガイモ。",
        },
        "enrichment": {
            "en": "Digging boxes, tunnels, platforms. Chew toys (willow sticks, apple branches). Foraging opportunities (hay in toilet paper rolls). Daily interaction and gentle handling.",
            "ja": "掘り箱、トンネル、段差。かじり木（柳の枝、リンゴの枝）。牧草をトイレットペーパーの芯に詰めて採食エンリッチメント。毎日のふれあい。",
        },
        "socialization": {
            "en": "Social species — bonded pairs thrive. Bonding process requires patience (neutral territory introduction). Can coexist with calm cats/dogs under supervision.",
            "ja": "社会性のある動物 — ペアでの飼育が理想。ペアリングには中立的な場所での慎重な導入が必要。穏やかな犬猫との同居も監視下で可能。",
        },
        "notes": {
            "en": "Spay/neuter recommended (uterine cancer risk 60–80% in unspayed does). Nails need regular trimming. Cecotropes (night feces) are normal and must be eaten. Annual vet checkups with exotic-experienced vet.",
            "ja": "避妊・去勢推奨（未避妊メスの子宮癌リスクは60〜80%）。爪は定期的にカット。盲腸便（夜間糞）は正常で食べる必要あり。エキゾチック診療経験のある獣医で年1回健診。",
        },
    },
    # =========================================================================
    # ハムスター (Hamster)
    # =========================================================================
    "hamster": {
        "name": "Hamster",
        "name_ja": "ハムスター",
        "temperature": {
            "en": "20–24°C (68–75°F); below 10°C can trigger torpor (pseudo-hibernation). Above 30°C causes heat stress.",
            "ja": "20〜24℃。10℃以下で擬似冬眠（トーパー）の危険。30℃以上で熱中症。",
        },
        "humidity": {
            "en": "40–60%; high humidity increases risk of respiratory and skin disease",
            "ja": "40〜60%（高湿度は呼吸器・皮膚疾患のリスク上昇）",
        },
        "housing": {
            "en": "Minimum floor space: 4,000 cm² (Syrian), 2,500 cm² (dwarf). Deep bedding (15+ cm) for burrowing. No cedar/pine shavings (toxic). Exercise wheel (solid surface, no rungs).",
            "ja": "最低床面積：4,000cm²（ゴールデン）、2,500cm²（ドワーフ）。巣穴掘り用に15cm以上の深い床材。杉・松の木くずは有毒のため不可。回し車（足が挟まらないソリッドタイプ）。",
        },
        "diet": {
            "en": "Commercial hamster pellets as base. Fresh vegetables (broccoli, carrot, cucumber) in small amounts. Occasional protein (boiled egg, mealworm). Avoid: citrus, onion, garlic, almonds.",
            "ja": "ハムスター用ペレットを主食に。新鮮な野菜（ブロッコリー、ニンジン、キュウリ）を少量。タンパク質補給（ゆで卵、ミルワーム）を時々。禁忌：柑橘類、タマネギ、ニンニク、アーモンド。",
        },
        "enrichment": {
            "en": "Exercise wheel (essential). Tunnels and hideouts. Sand bath (chinchilla sand). Foraging toys. Chew sticks for dental health. Quiet during day (nocturnal animal).",
            "ja": "回し車（必須）。トンネルと隠れ家。砂浴び用の砂場（チンチラサンド）。採食おもちゃ。かじり木で歯の健康維持。昼間は静かに（夜行性）。",
        },
        "socialization": {
            "en": "Syrian hamsters: strictly solitary (will fight if housed together). Dwarf hamsters: may live in same-sex pairs if introduced young, but monitor closely.",
            "ja": "ゴールデンハムスター：完全単独飼育（同居させると喧嘩）。ドワーフ：幼少期から同性ペアなら可能な場合もあるが要注意。",
        },
        "notes": {
            "en": "Lifespan 2–3 years. Cheek pouches can become impacted. Teeth grow continuously — provide chew materials. Handle gently; startled hamsters may bite. Nocturnal — respect sleep cycle.",
            "ja": "寿命2〜3年。頬袋の詰まりに注意。歯は生涯伸び続ける — かじり木を常備。驚くと噛むことがあるため優しく扱う。夜行性のため昼間の睡眠を尊重。",
        },
    },
    # =========================================================================
    # モルモット (Guinea Pig)
    # =========================================================================
    "guinea_pig": {
        "name": "Guinea Pig",
        "name_ja": "モルモット",
        "temperature": {
            "en": "18–24°C (64–75°F); very sensitive to heat above 27°C. Poor thermoregulation.",
            "ja": "18〜24℃。27℃以上で熱中症の危険。体温調節が苦手。",
        },
        "humidity": {
            "en": "40–60% relative humidity",
            "ja": "40〜60%",
        },
        "housing": {
            "en": "Minimum 0.7 m² per guinea pig (larger is better). C&C cages popular. Solid flooring (no wire). Fleece liners or paper-based bedding. Multiple hide houses.",
            "ja": "1匹あたり最低0.7m²（広いほど良い）。C&Cケージが人気。床は金網不可（ソリッド）。フリースライナーまたは紙系床材。隠れ家を複数設置。",
        },
        "diet": {
            "en": "Unlimited timothy hay (80% of diet). Daily vitamin C supplementation (30–50 mg/day) — guinea pigs cannot synthesize vitamin C. Fresh vegetables: bell pepper, romaine, cilantro. Limited pellets (vitamin C fortified).",
            "ja": "チモシー牧草食べ放題（食事の80%）。毎日のビタミンC補給（30〜50mg/日）— モルモットはビタミンCを体内合成できない。新鮮な野菜：パプリカ、ロメインレタス、パクチー。ペレットは少量（ビタミンC強化タイプ）。",
        },
        "enrichment": {
            "en": "Floor time outside cage daily. Tunnels, paper bags, hay stuffed toys. Vocal animals — enjoy music/conversation. Foraging opportunities in hay piles.",
            "ja": "毎日ケージ外での運動時間。トンネル、紙袋、牧草を詰めたおもちゃ。声でコミュニケーションする動物。牧草に野菜を隠して採食エンリッチメント。",
        },
        "socialization": {
            "en": "Highly social — must be kept in pairs or groups (same-sex or neutered mixed). Single guinea pigs can develop depression. Gentle handling builds trust.",
            "ja": "非常に社会性が高い — ペアまたはグループ飼育が必須（同性または去勢済み混合）。単独飼育はうつ状態の原因に。優しく接して信頼関係を構築。",
        },
        "notes": {
            "en": "Lifespan 5–7 years. Vitamin C deficiency (scurvy) is common and serious. Open-rooted teeth require hay for proper wear. Bumblefoot common on hard/wire surfaces. Exotic vet recommended.",
            "ja": "寿命5〜7年。ビタミンC欠乏症（壊血病）は深刻で多い。常生歯のため牧草で歯の摩耗が必要。硬い床や金網では飛節びらんになりやすい。エキゾチック診療経験のある獣医推奨。",
        },
    },
    # =========================================================================
    # チンチラ (Chinchilla)
    # =========================================================================
    "chinchilla": {
        "name": "Chinchilla",
        "name_ja": "チンチラ",
        "temperature": {
            "en": "15–21°C (59–70°F); heat stroke risk above 24°C. Must be kept cool — extremely heat-sensitive.",
            "ja": "15〜21℃。24℃以上で熱中症の危険 — 極めて暑さに弱い。夏季はエアコン必須。",
        },
        "humidity": {
            "en": "Below 50% — high humidity causes fungal infections in dense fur",
            "ja": "50%以下 — 密な被毛のため高湿度ではカビ感染のリスク",
        },
        "housing": {
            "en": "Tall multi-level cage (minimum 90×60×120 cm). Solid shelves (no wire). Dust bath house (chinchilla dust, 2–3 times/week). No plastic items (will chew and ingest).",
            "ja": "高さのある多段ケージ（最低90×60×120cm）。棚はソリッド（金網不可）。砂浴び容器（チンチラダスト、週2〜3回）。プラスチック製品は不可（齧って誤飲）。",
        },
        "diet": {
            "en": "Unlimited timothy hay. Chinchilla-specific pellets (limited, 1–2 tbsp/day). Occasional dried rosehip or hibiscus as treat. Avoid: nuts, seeds, fruits (high sugar/fat).",
            "ja": "チモシー牧草食べ放題。チンチラ専用ペレット（少量、1日大さじ1〜2杯）。おやつにドライローズヒップやハイビスカスを少量。禁忌：ナッツ類、種子、果物（高糖質・高脂肪）。",
        },
        "enrichment": {
            "en": "Dust baths (essential for coat health). Exercise wheel (15+ inch, solid). Wooden ledges for jumping. Apple wood sticks for chewing. Supervised out-of-cage play time.",
            "ja": "砂浴び（被毛の健康に不可欠）。回し車（直径38cm以上、ソリッド面）。ジャンプ用の木製棚。リンゴの木のかじり棒。監視下でのケージ外運動時間。",
        },
        "socialization": {
            "en": "Social animals — same-sex pairs or small groups ideal. Introduction must be gradual. Crepuscular/nocturnal — most active at dawn/dusk.",
            "ja": "社会性のある動物 — 同性ペアまたは小グループが理想。お見合いは段階的に。薄明薄暮性 — 明け方と夕方が最も活動的。",
        },
        "notes": {
            "en": "Lifespan 15–20 years (long commitment). Fur slip defense mechanism (patches of fur release when stressed). Never get fur wet (doesn't dry properly). Open-rooted teeth — hay is critical.",
            "ja": "寿命15〜20年（長期飼育の覚悟が必要）。ストレス時に被毛が抜けるファースリップ防御反応あり。被毛を絶対に濡らさない（乾きにくい）。常生歯のため牧草が不可欠。",
        },
    },
    # =========================================================================
    # フェレット (Ferret)
    # =========================================================================
    "ferret": {
        "name": "Ferret",
        "name_ja": "フェレット",
        "temperature": {
            "en": "15–24°C (59–75°F); very heat-sensitive, heat stroke risk above 27°C.",
            "ja": "15〜24℃。暑さに非常に弱く、27℃以上で熱中症の危険。",
        },
        "humidity": {
            "en": "40–60% relative humidity",
            "ja": "40〜60%",
        },
        "housing": {
            "en": "Large multi-level ferret cage with hammocks and tunnels. Ferret-proofed room for daily free-roaming (4+ hours). Block small gaps — they can fit through 2.5 cm openings.",
            "ja": "ハンモックとトンネル付き大型多段ケージ。毎日4時間以上のフェレット対策済みの部屋での放し飼い。2.5cmの隙間も通れるため隙間を塞ぐ。",
        },
        "diet": {
            "en": "Obligate carnivore — high-protein, high-fat, low-fiber diet. Quality ferret or kitten food. Raw diet possible with veterinary guidance. Avoid: fruits, vegetables, grains, sugar.",
            "ja": "完全肉食動物 — 高タンパク・高脂肪・低繊維の食事。良質なフェレットフードまたは子猫用フード。生食は獣医指導下で可能。禁忌：果物、野菜、穀物、砂糖。",
        },
        "enrichment": {
            "en": "Tunnels and tubes (favorite activity). Dig boxes with rice/beans. Interactive play sessions. Hide-and-seek games. Rotate toys frequently — they bore easily.",
            "ja": "トンネルとチューブ（大好きな遊び）。米や豆を入れた掘り箱。インタラクティブな遊びの時間。かくれんぼ遊び。飽きやすいためおもちゃはローテーション。",
        },
        "socialization": {
            "en": "Very social — pairs or small groups recommended. Can bond with cats and dogs (supervised). Sleep 14–18 hours/day ('dead sleep' is normal).",
            "ja": "非常に社会的 — ペアまたは小グループ推奨。犬猫との同居も監視下で可能。1日14〜18時間寝る（熟睡で動かないのは正常）。",
        },
        "notes": {
            "en": "Lifespan 6–10 years. Adrenal disease, insulinoma, and lymphoma very common. Annual checkups essential from age 3+. Descenting is cosmetic and not recommended. Must be spayed/neutered.",
            "ja": "寿命6〜10年。副腎疾患・インスリノーマ・リンパ腫が非常に多い。3歳以降は年1回の健診必須。臭腺除去は美容目的で非推奨。避妊去勢は必須。",
        },
    },
    # =========================================================================
    # ハリネズミ (Hedgehog)
    # =========================================================================
    "hedgehog": {
        "name": "Hedgehog",
        "name_ja": "ハリネズミ",
        "temperature": {
            "en": "24–29°C (75–84°F); below 20°C can trigger attempted hibernation (fatal in pet hedgehogs). Above 32°C causes heat stress.",
            "ja": "24〜29℃。20℃以下では致命的な冬眠を試みる可能性あり。32℃以上で熱中症。温度管理が生命に直結。",
        },
        "humidity": {
            "en": "40–60%; avoid overly dry environments (skin issues)",
            "ja": "40〜60%（乾燥しすぎると皮膚トラブル）",
        },
        "housing": {
            "en": "Minimum 60×90 cm floor space. Smooth-sided enclosure (they climb but fall). Exercise wheel (30+ cm, solid surface, no rungs). Fleece liners or paper bedding. No cedar/pine.",
            "ja": "最低60×90cmの床面積。滑りやすい壁のケージ（登るが落ちる）。回し車（直径30cm以上、ソリッド面）。フリースライナーまたは紙系床材。杉・松の木くず不可。",
        },
        "diet": {
            "en": "High-quality cat food (low fat, high protein) as base. Insects (mealworms, crickets) as treats. Occasional cooked egg, vegetables. Avoid: milk, bread, raw meat.",
            "ja": "良質な猫用フード（低脂肪・高タンパク）を主食に。昆虫（ミルワーム、コオロギ）をおやつに。茹で卵や野菜を時々。禁忌：牛乳、パン、生肉。",
        },
        "enrichment": {
            "en": "Exercise wheel (essential — they run 5+ km/night). Tunnels and hiding spots. Supervised floor time. Foraging with hidden insects in substrate.",
            "ja": "回し車（必須 — 一晩に5km以上走る）。トンネルと隠れ家。監視下での部屋んぽ。床材に虫を隠して採食エンリッチメント。",
        },
        "socialization": {
            "en": "Solitary species — house individually. Daily gentle handling for bonding (10–30 min). May ball up and hiss initially — patience required. Nocturnal.",
            "ja": "単独飼育の動物。毎日10〜30分の穏やかなハンドリングで信頼関係構築。最初は丸まったり威嚇するが根気強く。夜行性。",
        },
        "notes": {
            "en": "Lifespan 4–6 years. Wobbly Hedgehog Syndrome (WHS) is common and incurable. Self-anointing (spreading saliva on spines) is normal behavior. Obesity very common — monitor weight.",
            "ja": "寿命4〜6年。ふらつき症候群（WHS）が多く治療法なし。唾液を針に塗る自己塗抹行動は正常。肥満が非常に多い — 体重管理を。",
        },
    },
    # =========================================================================
    # フクロモモンガ (Sugar Glider)
    # =========================================================================
    "sugar_glider": {
        "name": "Sugar Glider",
        "name_ja": "フクロモモンガ",
        "temperature": {
            "en": "24–28°C (75–82°F); sensitive to cold — can enter torpor below 18°C.",
            "ja": "24〜28℃。寒さに弱く、18℃以下ではトーパー（低体温状態）の危険。",
        },
        "humidity": {
            "en": "50–70% relative humidity (tropical species)",
            "ja": "50〜70%（熱帯性の動物）",
        },
        "housing": {
            "en": "Tall cage (minimum 60×60×90 cm) for gliding/climbing. Branches, ropes, pouches. Nesting pouch or box essential. Bar spacing under 1.3 cm. No mesh wheels (tails get caught).",
            "ja": "滑空・登攀用の縦長ケージ（最低60×60×90cm）。枝、ロープ、ポーチ。寝袋型ポーチまたは巣箱は必須。金網の間隔は1.3cm以下。メッシュ回し車は不可（尻尾が挟まる）。",
        },
        "diet": {
            "en": "BML (Bourbon's Modified Leadbeater's) or TPG (The Pet Glider) diet recommended. Calcium:phosphorus ratio (2:1) critical — metabolic bone disease common. Fresh fruits, vegetables, protein (insects, eggs).",
            "ja": "BML食またはTPG食推奨。カルシウム:リン比（2:1）が極めて重要 — 代謝性骨疾患が多い。新鮮な果物、野菜、タンパク質（昆虫、卵）。",
        },
        "enrichment": {
            "en": "Bonding pouch (carry during day for bonding). Foraging toys. Branches for climbing and gliding. Supervised out-of-cage gliding time in secure room.",
            "ja": "ボンディングポーチ（日中に持ち歩いて信頼関係構築）。採食おもちゃ。登攀・滑空用の枝。安全な部屋での監視付き放し飼い時間。",
        },
        "socialization": {
            "en": "Extremely social — MUST be kept in pairs or groups. Single sugar gliders can develop severe depression, self-mutilation. Colony animals in the wild.",
            "ja": "非常に社会性が高い — ペアまたはグループ飼育が必須。単独飼育は重度のうつ・自傷行為の原因。野生では群れで生活。",
        },
        "notes": {
            "en": "Lifespan 12–15 years. Nocturnal. Calcium deficiency is #1 health issue. Males have scent glands (bald spot on head is normal). Illegal in some jurisdictions — check local laws.",
            "ja": "寿命12〜15年。夜行性。カルシウム不足が最大の健康問題。オスの頭頂部の禿げは臭腺で正常。地域によっては飼育規制あり — 法律確認を。",
        },
    },
    # =========================================================================
    # デグー (Degu)
    # =========================================================================
    "degu": {
        "name": "Degu",
        "name_ja": "デグー",
        "temperature": {
            "en": "18–24°C (64–75°F); heat-sensitive above 28°C. Susceptible to heat stroke.",
            "ja": "18〜24℃。28℃以上で熱中症の危険。暑さに弱い。",
        },
        "humidity": {
            "en": "40–60% relative humidity",
            "ja": "40〜60%",
        },
        "housing": {
            "en": "Large multi-level cage (minimum 80×50×80 cm). Solid surfaces (not wire mesh). Sand bath dish available daily. Avoid plastic (will destroy). Metal or glass enclosure preferred.",
            "ja": "大型多段ケージ（最低80×50×80cm）。床はソリッド面（金網不可）。砂浴び容器を毎日設置。プラスチック不可（破壊する）。金属またはガラス製ケージ推奨。",
        },
        "diet": {
            "en": "Timothy hay (unlimited). Degu-specific or chinchilla pellets (sugar-free). Fresh vegetables (dark leafy greens). NO fruit or sugary foods — degus are prone to diabetes.",
            "ja": "チモシー牧草（食べ放題）。デグー専用またはチンチラ用ペレット（無糖）。新鮮な野菜（濃い色の葉物）。果物や糖分を含む食品は厳禁 — デグーは糖尿病になりやすい。",
        },
        "enrichment": {
            "en": "Exercise wheel (25+ cm, solid). Sand baths. Branches for chewing (apple, pear). Tunnels and platforms. Highly intelligent — benefit from puzzle toys and training.",
            "ja": "回し車（直径25cm以上、ソリッド面）。砂浴び。かじり木（リンゴ、梨の枝）。トンネルと棚。知能が高い — パズルおもちゃやトレーニングが効果的。",
        },
        "socialization": {
            "en": "Highly social — must be kept in same-sex pairs or groups. Vocal communicators (15+ distinct calls). Diurnal — active during the day (unlike most rodents).",
            "ja": "非常に社会的 — 同性ペアまたはグループ飼育が必須。15種類以上の鳴き声で会話。昼行性 — 他のげっ歯類と違い日中に活動。",
        },
        "notes": {
            "en": "Lifespan 6–9 years. Diabetes extremely common (no sugar/fruit). Tail degloving if grabbed by tail (skin comes off, never regrows). Teeth are naturally orange. Open-rooted teeth need hay.",
            "ja": "寿命6〜9年。糖尿病が極めて多い（糖分・果物厳禁）。尻尾を掴むと皮膚が剥がれる（再生しない）。歯がオレンジ色なのは正常。常生歯のため牧草が必要。",
        },
    },
    # =========================================================================
    # 鳥 (Bird — general)
    # =========================================================================
    "bird": {
        "name": "Bird",
        "name_ja": "鳥",
        "temperature": {
            "en": "20–27°C (68–80°F); avoid drafts and sudden temperature changes. Keep away from kitchen fumes (PTFE/Teflon is lethal).",
            "ja": "20〜27℃。隙間風や急激な温度変化を避ける。台所の煙から隔離（テフロン加熱で発生するガスは致命的）。",
        },
        "humidity": {
            "en": "50–70%; regular misting or bathing opportunities",
            "ja": "50〜70%。定期的な霧吹きや水浴びの機会を提供。",
        },
        "housing": {
            "en": "Largest cage possible (minimum: wingspan × 2 in each dimension). Natural wood perches of varying diameters. Bar spacing appropriate for species. Cover at night for 10–12 hours of sleep.",
            "ja": "可能な限り大きなケージ（最低：翼開長の2倍）。太さの異なる天然木の止まり木。種に適した金網間隔。夜間は10〜12時間カバーをかけて睡眠。",
        },
        "diet": {
            "en": "Species-specific formulated pellets (60–70%). Fresh vegetables and fruits (20–30%). Seeds as treats only (high fat). Avoid: avocado, chocolate, caffeine, alcohol, onion.",
            "ja": "種に適したペレット（60〜70%）。新鮮な野菜・果物（20〜30%）。シードはおやつ程度（高脂肪）。禁忌：アボカド、チョコレート、カフェイン、アルコール、タマネギ。",
        },
        "enrichment": {
            "en": "Foraging toys (essential for psychological health). Out-of-cage time daily. Variety of textures and materials to shred. Music and conversation. Training with positive reinforcement.",
            "ja": "採食おもちゃ（精神的健康に不可欠）。毎日のケージ外での放鳥時間。様々な素材を噛む・裂く機会。音楽や会話。正の強化によるトレーニング。",
        },
        "socialization": {
            "en": "Highly social species. Flock animals that need daily interaction. Loneliness leads to feather plucking and behavioral issues. Consider pairs if human interaction time is limited.",
            "ja": "非常に社会性が高い。群れの動物で毎日のふれあいが必要。孤独は毛引きや問題行動の原因。人との時間が限られる場合はペア飼育を検討。",
        },
        "notes": {
            "en": "Lifespan varies widely (finch 5–8 yr, cockatiel 15–25 yr, parrot 40–80 yr). Respiratory system extremely sensitive — no aerosols, candles, non-stick cookware fumes. Annual avian vet checkups.",
            "ja": "寿命は種により大きく異なる（フィンチ5〜8年、オカメインコ15〜25年、大型インコ40〜80年）。呼吸器系が非常に敏感 — スプレー、キャンドル、テフロンのガスは厳禁。年1回の鳥類専門獣医での健診。",
        },
    },
    # =========================================================================
    # インコ (Parakeet)
    # =========================================================================
    "parakeet": {
        "name": "Parakeet",
        "name_ja": "インコ",
        "temperature": {
            "en": "20–27°C (68–80°F); avoid drafts. PTFE/Teflon fumes are instantly lethal.",
            "ja": "20〜27℃。隙間風を避ける。テフロン加熱のガスは即死レベルの毒性。",
        },
        "humidity": {
            "en": "50–65%; regular misting helps feather condition",
            "ja": "50〜65%。定期的な霧吹きで羽毛のコンディション維持。",
        },
        "housing": {
            "en": "Cage minimum 45×45×60 cm for budgies (larger for cockatiels). Horizontal bar orientation for climbing. Multiple perches at different heights. Cuttlebone for calcium.",
            "ja": "セキセイインコで最低45×45×60cm（オカメインコはより大きく）。登攀用に横向きの金網。高さの異なる複数の止まり木。カルシウム補給にカトルボーン。",
        },
        "diet": {
            "en": "Pellets as base (Harrison's, Roudybush). Fresh vegetables daily (leafy greens, carrots, bell pepper). Limited seeds. Sprouted seeds excellent. Avoid: avocado, chocolate, fruit pits.",
            "ja": "ペレットを主食に。毎日新鮮な野菜（葉物、ニンジン、パプリカ）。シードは少量。スプラウトシードは優良。禁忌：アボカド、チョコレート、果物の種。",
        },
        "enrichment": {
            "en": "Mirrors and bells (budgies). Shredding toys. Out-of-cage flight time in bird-safe room. Whistling and talking practice. Swings and ladders.",
            "ja": "鏡やベル（セキセイインコ）。裂けるおもちゃ。安全な部屋での放鳥時間。口笛やおしゃべりの練習。ブランコとはしご。",
        },
        "socialization": {
            "en": "Very social — pairs or small flocks ideal. Single birds need significant daily human interaction (2+ hours). Same-species companions preferred.",
            "ja": "非常に社会的 — ペアまたは小さな群れが理想。単独飼育の場合は1日2時間以上の人との交流が必要。同種のコンパニオンが好ましい。",
        },
        "notes": {
            "en": "Budgies: 8–15 years; Cockatiels: 15–25 years. Crop infections common in young birds. Night frights in cockatiels — dim nightlight helps. Egg binding risk in females.",
            "ja": "セキセイインコ：8〜15年、オカメインコ：15〜25年。幼鳥ではそのう炎が多い。オカメインコのナイトフライト — 常夜灯が有効。メスでは卵詰まりに注意。",
        },
    },
    # =========================================================================
    # オウム (Parrot)
    # =========================================================================
    "parrot": {
        "name": "Parrot",
        "name_ja": "オウム",
        "temperature": {
            "en": "20–28°C (68–82°F); tropical species — avoid cold drafts. PTFE fumes are lethal.",
            "ja": "20〜28℃。熱帯性のため冷たい隙間風に注意。テフロンのガスは致命的。",
        },
        "humidity": {
            "en": "50–70%; daily misting or shower perch recommended",
            "ja": "50〜70%。毎日の霧吹きまたはシャワー用止まり木を推奨。",
        },
        "housing": {
            "en": "Large cage (minimum 90×60×120 cm for medium parrots; larger for macaws/cockatoos). Heavy-duty bars (they are strong chewers). Multiple perches of natural wood. Lock-type door latches.",
            "ja": "大型ケージ（中型で最低90×60×120cm、大型種はさらに大きく）。頑丈な金網（噛む力が強い）。天然木の止まり木を複数。鍵付きドアロック。",
        },
        "diet": {
            "en": "Formulated pellets (60–70%). Daily fresh vegetables, leafy greens, cooked legumes. Limited fruits and nuts. Avoid: avocado (lethal), chocolate, caffeine, alcohol, apple seeds.",
            "ja": "ペレット（60〜70%）。毎日新鮮な野菜、葉物、加熱した豆類。果物とナッツは少量。禁忌：アボカド（致死的）、チョコレート、カフェイン、アルコール、リンゴの種。",
        },
        "enrichment": {
            "en": "Foraging toys (critical — prevents feather destructive behavior). Puzzle feeders. Foot toys. Wood blocks for chewing. Training sessions (highly intelligent). Daily out-of-cage time.",
            "ja": "採食おもちゃ（必須 — 毛引き予防）。パズルフィーダー。足で掴むおもちゃ。噛み用の木製ブロック。トレーニング（非常に高い知能）。毎日のケージ外時間。",
        },
        "socialization": {
            "en": "Extremely social and emotionally complex. Bond deeply with owners — rehoming is traumatic. Need 4+ hours daily interaction. Can develop neurotic behaviors if neglected.",
            "ja": "極めて社会的で感情が複雑。飼い主と深く絆を結ぶ — 里親に出すのはトラウマに。1日4時間以上の交流が必要。放置すると神経症的行動が発現。",
        },
        "notes": {
            "en": "Lifespan 30–80+ years (cockatoos, macaws). Feather plucking is #1 behavioral problem. Psittacosis (Chlamydia psittaci) is zoonotic. Extremely loud — consider neighbors. Annual avian vet checkups.",
            "ja": "寿命30〜80年以上（オウム、コンゴウインコ）。毛引きが最大の行動問題。オウム病（クラミジア）は人畜共通感染症。非常にうるさい — 近隣への配慮を。年1回の鳥類専門医での健診。",
        },
    },
    # =========================================================================
    # 馬 (Horse)
    # =========================================================================
    "horse": {
        "name": "Horse",
        "name_ja": "馬",
        "temperature": {
            "en": "Tolerates wide range with shelter. Comfortable 5–25°C. Heat stress above 32°C + high humidity. Blanketing for clipped horses in cold.",
            "ja": "シェルターがあれば広範囲に適応。快適域は5〜25℃。32℃以上＋高湿度で熱中症。クリッピング済みの馬は寒冷時に馬着を。",
        },
        "humidity": {
            "en": "Adequate barn ventilation critical. Ammonia buildup from bedding causes respiratory issues.",
            "ja": "馬房の換気が極めて重要。床材からのアンモニア蓄積は呼吸器疾患の原因。",
        },
        "housing": {
            "en": "Stall: minimum 3.6×3.6 m (12×12 ft). Daily turnout in paddock/pasture essential. Dry, well-drained footing. Shelter from wind, rain, and sun.",
            "ja": "馬房：最低3.6×3.6m。毎日のパドック・放牧が不可欠。乾燥した排水性の良い地面。風雨・日差しを避けるシェルター。",
        },
        "diet": {
            "en": "1.5–2% body weight in forage daily (hay/pasture). Concentrates based on workload. Salt block available. Gradual diet changes to prevent colic/laminitis. Fresh water (30–50 L/day).",
            "ja": "体重の1.5〜2%の粗飼料（乾草/牧草）を毎日。濃厚飼料は運動量に応じて。塩ブロックを常設。急な飼料変更は疝痛・蹄葉炎の原因。新鮮な水（1日30〜50L）。",
        },
        "enrichment": {
            "en": "Pasture turnout with companions. Slow feeders to mimic natural grazing. Regular exercise/riding. Grooming as bonding. Toys (horse balls, treat dispensers).",
            "ja": "仲間と一緒の放牧。スローフィーダーで自然な採食を再現。定期的な運動・騎乗。グルーミングで信頼関係。馬用ボールやトリートディスペンサー。",
        },
        "socialization": {
            "en": "Herd animal — needs equine companions. Isolation causes severe stress. Hierarchy is natural. Bonds with humans through consistent, calm handling.",
            "ja": "群れの動物 — 馬の仲間が必要。隔離は深刻なストレスに。序列は自然な行動。穏やかで一貫したハンドリングで人と信頼関係。",
        },
        "notes": {
            "en": "Lifespan 25–30 years. Farrier every 6–8 weeks. Dental floating every 6–12 months. Colic is #1 cause of death. Vaccinations (tetanus, influenza, EHV) and deworming schedules. Annual vet checkup.",
            "ja": "寿命25〜30年。蹄のケア6〜8週ごと。歯の研磨6〜12ヶ月ごと。疝痛が死因第1位。予防接種（破傷風、インフルエンザ、EHV）と駆虫計画。年1回の定期健診。",
        },
    },
    # =========================================================================
    # 爬虫類 (Reptile — general)
    # =========================================================================
    "reptile": {
        "name": "Reptile",
        "name_ja": "爬虫類",
        "temperature": {
            "en": "Species-dependent. Thermal gradient essential: warm basking zone (30–40°C) and cool zone (22–28°C). UVB lighting required for most species.",
            "ja": "種により異なる。温度勾配が必須：ホットスポット（30〜40℃）とクールゾーン（22〜28℃）。ほとんどの種でUVBライトが必要。",
        },
        "humidity": {"en": "Species-dependent: desert (20–40%), tropical (60–80%)", "ja": "種により異なる：砂漠系（20〜40%）、熱帯系（60〜80%）"},
        "housing": {"en": "Enclosure size varies by species. Secure lid essential (escape artists). Appropriate substrate. Hides on warm and cool sides. UVB bulb replaced every 6 months.", "ja": "ケージサイズは種による。脱走防止の蓋が必須。適切な床材。温暖側・冷涼側それぞれにシェルター。UVBランプは6ヶ月ごとに交換。"},
        "diet": {"en": "Varies: herbivorous (greens, vegetables), insectivorous (gut-loaded crickets, dubia roaches), or carnivorous (whole prey). Calcium + D3 dusting for most species.", "ja": "種により異なる：草食（葉物、野菜）、昆虫食（ガットローディング済みコオロギ、デュビア）、肉食（ホールプレイ）。多くの種でカルシウム＋D3ダスティング。"},
        "enrichment": {"en": "Climbing branches, basking platforms, water features. Environmental complexity reduces stress. Supervised exploration outside enclosure.", "ja": "登攀用枝、バスキング台、水場。環境の複雑さがストレスを軽減。監視下でのケージ外探索。"},
        "socialization": {"en": "Most reptiles are solitary. Co-habitation often causes stress and aggression. Handle regularly but gently for taming. Respect species-specific temperament.", "ja": "多くの爬虫類は単独飼育。同居はストレスと攻撃の原因。定期的に優しくハンドリングして馴らす。種ごとの気性を尊重。"},
        "notes": {"en": "UVB + calcium crucial to prevent MBD. Ecdysis (shedding) problems indicate husbandry issues. Reptile-experienced vet essential. Salmonella risk — wash hands after handling.", "ja": "UVB＋カルシウムはMBD予防に不可欠。脱皮不全は飼育環境の問題を示唆。爬虫類診療経験のある獣医が必須。サルモネラのリスク — 触った後は手洗い。"},
    },
    # =========================================================================
    # リクガメ (Tortoise)
    # =========================================================================
    "tortoise": {
        "name": "Tortoise",
        "name_ja": "リクガメ",
        "temperature": {"en": "Basking spot 32–38°C, cool side 22–28°C. Night drop to 18–22°C acceptable. UVB essential (10.0–12.0 for desert species).", "ja": "ホットスポット32〜38℃、クールゾーン22〜28℃。夜間18〜22℃まで低下可。UVB必須（砂漠種は10.0〜12.0）。"},
        "humidity": {"en": "Species-dependent: Russian/Greek (40–60%), Red-foot/Tropical (70–80%). Humid hide box recommended for all.", "ja": "種による：ロシアリクガメ/ギリシャ（40〜60%）、アカアシ/熱帯種（70〜80%）。湿度の高いシェルターを全種に推奨。"},
        "housing": {"en": "Open-top tortoise table preferred over glass tanks (better ventilation). Outdoor enclosure in warm months ideal. Substrate: coco coir, topsoil mix. Shallow water dish for soaking.", "ja": "ガラス水槽よりオープントップのトータステーブル推奨（換気が良い）。暖かい季節は屋外飼育が理想。床材：ココヤシ繊維、培養土ミックス。浅い水皿で水浴び。"},
        "diet": {"en": "Herbivorous: dark leafy greens (dandelion, endive, watercress), weeds, hay. Calcium supplement 2–3x/week. Avoid: fruit (except tropical species), iceberg lettuce, spinach (oxalates).", "ja": "草食：濃い色の葉物（タンポポ、エンダイブ、クレソン）、野草、牧草。カルシウムを週2〜3回。禁忌：果物（熱帯種以外）、玉レタス、ほうれん草（シュウ酸）。"},
        "enrichment": {"en": "Outdoor grazing time. Varied terrain with slopes and obstacles. Hiding spots. Edible plants in enclosure for foraging. Shallow warm soaks 1–2x/week.", "ja": "屋外での放牧。傾斜や障害物のある変化に富んだ地形。隠れ家。ケージ内に食用植物で採食エンリッチメント。温浴を週1〜2回。"},
        "socialization": {"en": "Generally solitary. Males may fight. Gentle handling acceptable but they are not cuddly pets. Recognize owners over time.", "ja": "基本的に単独飼育。オス同士は喧嘩することも。穏やかなハンドリングは可能だが抱っこ向きではない。時間をかけて飼い主を認識。"},
        "notes": {"en": "Lifespan 50–100+ years. Shell pyramiding indicates poor husbandry (low humidity, excess protein). MBD very common without proper UVB/calcium. Brumation (winter dormancy) natural for temperate species.", "ja": "寿命50〜100年以上。甲羅のピラミッド化は飼育環境の問題（低湿度、過剰タンパク質）を示す。UVB/カルシウム不足でMBDが非常に多い。温帯種のブルメーション（冬眠）は自然。"},
        "subtypes": [
            {
                "name": "Russian Tortoise", "name_ja": "ロシアリクガメ（ホルスフィールド）",
                "temperature": {"en": "Basking 32–35°C, cool side 22–26°C, night 15–18°C. UVB 10.0. Tolerates wider temperature range than tropical species.", "ja": "ホットスポット32〜35℃、クールゾーン22〜26℃、夜間15〜18℃。UVB 10.0。熱帯種より広い温度範囲に耐える。"},
                "humidity": {"en": "40–60%. Dry species from Central Asian steppes. Humid hide still recommended. Avoid constant high humidity.", "ja": "40〜60%。中央アジアのステップ原産の乾燥種。ウェットシェルターは設置推奨。常時高湿度は避ける。"},
                "housing": {"en": "Tortoise table 120×60 cm minimum. Prolific diggers — deep substrate (15+ cm). Outdoor enclosure excellent in warm months. Excellent climbers — secure walls.", "ja": "トータステーブル最低120×60cm。掘るのが好き — 深い床材（15cm以上）。暖かい季節の屋外飼育は最適。登るのが上手 — 壁を確実に。"},
                "diet": {"en": "Weeds and greens: dandelion, plantain, clover, hibiscus leaves. Very high fiber. NO fruit. Timothy hay available. Calcium 3x/week.", "ja": "野草と葉物：タンポポ、オオバコ、クローバー、ハイビスカスの葉。非常に高繊維。果物は不可。チモシー牧草を常備。カルシウム週3回。"},
                "notes": {"en": "Lifespan 40–60+ years. Small species (15–20 cm). Brumation natural and recommended for health. Very active and personable. Most popular pet tortoise species.", "ja": "寿命40〜60年以上。小型種（15〜20cm）。ブルメーションは自然で健康に推奨。非常に活発で人に馴れやすい。最も人気のあるペットリクガメ。"},
            },
            {
                "name": "Hermann's / Greek Tortoise", "name_ja": "ヘルマンリクガメ / ギリシャリクガメ",
                "temperature": {"en": "Basking 30–34°C, cool side 22–26°C, night 16–20°C. UVB 10.0. Mediterranean climate species.", "ja": "ホットスポット30〜34℃、クールゾーン22〜26℃、夜間16〜20℃。UVB 10.0。地中海性気候の種。"},
                "humidity": {"en": "50–60%. Moderate humidity; humid hide essential for proper shell growth and hydration.", "ja": "50〜60%。中程度の湿度。甲羅の正常な成長と水分補給のためウェットシェルター必須。"},
                "housing": {"en": "Tortoise table 120×60 cm minimum. Outdoor gardens ideal in Mediterranean-like climates. Mix of sunny and shaded areas. Varied substrate.", "ja": "トータステーブル最低120×60cm。温暖な気候では屋外庭園が理想。日向と日陰を組み合わせる。様々な床材。"},
                "diet": {"en": "Mediterranean weeds and greens: dandelion, plantain, hawkbit, sow thistle. High fiber, low protein. NO fruit for Hermann's (small amounts OK for Greek). Calcium regularly.", "ja": "地中海の野草と葉物：タンポポ、オオバコ、ブタナ、ノゲシ。高繊維・低タンパク質。ヘルマンは果物不可（ギリシャは少量可）。カルシウムを定期的に。"},
                "notes": {"en": "Lifespan 50–80+ years. Brumation recommended for breeding and long-term health. Pyramiding prevention: adequate humidity + proper diet (no excess protein).", "ja": "寿命50〜80年以上。繁殖と長期的健康のためブルメーション推奨。ピラミッド化予防：適切な湿度＋正しい食事（過剰タンパク質を避ける）。"},
            },
            {
                "name": "Red-footed Tortoise", "name_ja": "アカアシガメ",
                "temperature": {"en": "Basking 32–35°C, ambient 26–30°C, night 22–25°C. UVB 5.0–10.0. Tropical species — no brumation.", "ja": "ホットスポット32〜35℃、環境温度26〜30℃、夜間22〜25℃。UVB 5.0〜10.0。熱帯種 — ブルメーションなし。"},
                "humidity": {"en": "70–80%. High humidity species from South American forests. Frequent misting. Large shallow water dish.", "ja": "70〜80%。南米の森林原産の高湿度種。頻繁な霧吹き。大きな浅い水皿。"},
                "housing": {"en": "Larger enclosure needed (150×60 cm minimum — they grow to 30–35 cm). Closed-top vivarium helps retain humidity. Deep, moisture-retaining substrate (cypress mulch, coco coir).", "ja": "より大きなケージが必要（最低150×60cm — 30〜35cmに成長）。密閉型ビバリウムで湿度維持。保湿性のある深い床材（サイプレスマルチ、ココヤシ繊維）。"},
                "diet": {"en": "Mixed diet: greens (70%), fruits (20% — unlike temperate species, fruit is OK), protein (10% — mushrooms, occasional snail/worm). Calcium 2–3x/week.", "ja": "混合食：葉物（70%）、果物（20% — 温帯種と違い果物OK）、タンパク質（10% — キノコ、時々カタツムリ/ミミズ）。カルシウム週2〜3回。"},
                "notes": {"en": "Lifespan 50+ years. More omnivorous than most tortoises. Personable and interactive. Prone to respiratory infections if kept too cool/dry.", "ja": "寿命50年以上。多くのリクガメより雑食性。人に馴れやすく対話的。低温・乾燥環境では呼吸器感染症になりやすい。"},
            },
        ],
    },
    # =========================================================================
    # ヘビ (Snake)
    # =========================================================================
    "snake": {
        "name": "Snake",
        "name_ja": "ヘビ",
        "temperature": {"en": "Thermal gradient: warm side 28–32°C, cool side 23–27°C. Belly heat (under-tank heater with thermostat) preferred by many species.", "ja": "温度勾配：温暖側28〜32℃、冷涼側23〜27℃。腹部からの加温（サーモスタット付きパネルヒーター）を好む種が多い。"},
        "humidity": {"en": "Species-dependent: corn snake (40–50%), ball python (50–60%), tropical boas (60–80%). Increase during shedding.", "ja": "種による：コーンスネーク（40〜50%）、ボールパイソン（50〜60%）、熱帯ボア（60〜80%）。脱皮時は湿度を上げる。"},
        "housing": {"en": "Minimum length = snake's body length. Secure locking lid mandatory. At least 2 hides (warm and cool side). Water bowl large enough to soak in. Climbing branches for arboreal species.", "ja": "最低ケージ長＝ヘビの体長。施錠できる蓋が必須。最低2つのシェルター（温暖側と冷涼側）。浸かれる大きさの水入れ。樹上性種には登攀用の枝。"},
        "diet": {"en": "Whole prey (frozen-thawed recommended over live). Feeding frequency varies by age/species (weekly for juveniles, biweekly for adults). Size: prey width ≈ snake's widest point.", "ja": "ホールプレイ（冷凍解凍が生き餌より推奨）。給餌頻度は年齢・種による（幼体は週1回、成体は2週に1回）。餌のサイズ：ヘビの最も太い部分と同程度。"},
        "enrichment": {"en": "Multiple hides and cover. Branches and ledges. Novel scents (shed from other species). Environmental changes (rearrange decor). Some species benefit from handling.", "ja": "複数のシェルターとカバー。枝や棚。新しい匂い（他種の脱皮殻など）。環境の模様替え。ハンドリングが有益な種もある。"},
        "socialization": {"en": "Strictly solitary (with very few exceptions). Co-habitation is stressful and dangerous (cannibalism risk in some species). Regular gentle handling tames most species.", "ja": "厳格な単独飼育（ごく一部の例外を除く）。同居はストレスと危険（共食いのリスクも）。定期的な穏やかなハンドリングで多くの種は馴れる。"},
        "notes": {"en": "Lifespan 15–30+ years (ball pythons). Do not handle 48 hours after feeding. Blue/milky eyes indicate upcoming shed. Respiratory infections common with improper humidity. Escape prevention is critical.", "ja": "寿命15〜30年以上（ボールパイソン）。給餌後48時間はハンドリング不可。目が白く濁ると脱皮間近。湿度管理不良で呼吸器感染症が多い。脱走防止が最重要。"},
        "subtypes": [
            {
                "name": "Ball Python", "name_ja": "ボールパイソン",
                "temperature": {"en": "Warm side 30–32°C, cool side 24–26°C, night 24°C. Belly heat (under-tank heater + thermostat) preferred. Ceramic heat emitter for ambient.", "ja": "温暖側30〜32℃、冷涼側24〜26℃、夜間24℃。パネルヒーター＋サーモスタットで腹部加温。暖突で環境温度調整。"},
                "humidity": {"en": "50–60% ambient; 70–80% during shed (humid hide or misting). Dehydration and stuck shed are common issues.", "ja": "通常50〜60%。脱皮時は70〜80%（ウェットシェルターまたは霧吹き）。脱水と脱皮不全がよくある問題。"},
                "housing": {"en": "Minimum 120×60×45 cm for adults. PVC or tub setups retain humidity better than screen cages. Tight-fitting hides (they like snug spaces). Climbing opportunities appreciated.", "ja": "成体で最低120×60×45cm。PVCケージやタブ飼育はメッシュケージより湿度維持が容易。体にフィットする隠れ家（狭い空間を好む）。登る機会も喜ぶ。"},
                "diet": {"en": "Frozen-thawed rats/mice. Juveniles: every 5–7 days. Adults: every 10–14 days. Prey width ≈ widest part of snake. Known for hunger strikes (months-long fasting can be normal).", "ja": "冷凍解凍マウス/ラット。幼体：5〜7日ごと。成体：10〜14日ごと。餌の幅≒ヘビの最太部。拒食しやすい（数ヶ月の絶食が正常なことも）。"},
                "notes": {"en": "Lifespan 20–30+ years. Ball-up defense posture (curls into ball). Notorious picky eaters. Respiratory infections if too cold/humid. Many morphs available but some linked to neurological issues (spider morph wobble).", "ja": "寿命20〜30年以上。ボール防御姿勢（丸まる）。偏食で有名。低温/高湿度で呼吸器感染症。多数のモルフがあるが一部は神経障害と関連（スパイダーモルフのウォブル）。"},
            },
            {
                "name": "Corn Snake", "name_ja": "コーンスネーク",
                "temperature": {"en": "Warm side 28–30°C, cool side 22–25°C, night 20–22°C. Heat mat with thermostat. Room temperature is often too cool.", "ja": "温暖側28〜30℃、冷涼側22〜25℃、夜間20〜22℃。サーモスタット付きヒートマット。室温だけでは低すぎることが多い。"},
                "humidity": {"en": "40–50% ambient; increase to 60–70% during shed. Good ventilation important.", "ja": "通常40〜50%。脱皮時は60〜70%に上げる。換気の確保が重要。"},
                "housing": {"en": "Minimum 90×45×45 cm for adults. Escape-proof lid essential (notorious escape artists). Multiple hides. Semi-arboreal — provide climbing branches.", "ja": "成体で最低90×45×45cm。脱走防止の蓋が必須（脱走の名人）。複数のシェルター。半樹上性 — 登攀用の枝を設置。"},
                "diet": {"en": "Frozen-thawed mice. Hatchlings: pinky mice every 5–7 days. Adults: adult mice every 10–14 days. Usually excellent feeders.", "ja": "冷凍解凍マウス。ハッチリング：ピンクマウスを5〜7日ごと。成体：アダルトマウスを10〜14日ごと。通常は食欲旺盛。"},
                "notes": {"en": "Lifespan 15–20 years. Excellent beginner snake — docile, hardy, great feeders. Many color morphs. Brumation possible (2–3 months at 10–15°C) for breeding.", "ja": "寿命15〜20年。初心者に最適 — 温厚、丈夫、食欲旺盛。多数のカラーモルフ。繁殖にはブルメーション（2〜3ヶ月、10〜15℃）が可能。"},
            },
            {
                "name": "Boa Constrictor", "name_ja": "ボアコンストリクター",
                "temperature": {"en": "Basking 32–35°C, cool side 26–28°C, night 24–26°C. Radiant heat panel or ceramic heat emitter for large enclosures.", "ja": "ホットスポット32〜35℃、冷涼側26〜28℃、夜間24〜26℃。大型ケージにはラジアントヒートパネルまたは暖突。"},
                "humidity": {"en": "60–70%. Higher for tropical subspecies (BCI: 60–70%, BCC: 70–80%). Misting or large water bowl for humidity.", "ja": "60〜70%。熱帯亜種はより高湿度（BCI：60〜70%、BCC：70〜80%）。霧吹きまたは大型水入れで湿度確保。"},
                "housing": {"en": "Adults need 180×60×60 cm minimum (can reach 2–3 m). Heavy-duty enclosure with secure locking. Large water bowl for soaking. PVC enclosures preferred.", "ja": "成体は最低180×60×60cm（体長2〜3mに達する）。頑丈なケージと確実なロック。浸かれる大型水入れ。PVCケージ推奨。"},
                "diet": {"en": "Frozen-thawed rats/rabbits (size-appropriate). Juveniles: every 7–10 days. Adults: every 2–4 weeks. Obesity is common in captivity — monitor body condition.", "ja": "冷凍解凍ラット/ウサギ（サイズに合わせて）。幼体：7〜10日ごと。成体：2〜4週ごと。飼育下では肥満が多い — 体型管理を。"},
                "notes": {"en": "Lifespan 20–30+ years. Can become large and strong — experienced keeper recommended. Inclusion body disease (IBD) is a serious viral threat. Regular health checks important.", "ja": "寿命20〜30年以上。大きく力も強くなるため経験者向け。封入体病（IBD）は深刻なウイルス疾患。定期的な健康チェックが重要。"},
            },
        ],
    },
    # =========================================================================
    # トカゲ (Lizard)
    # =========================================================================
    "lizard": {
        "name": "Lizard",
        "name_ja": "トカゲ",
        "temperature": {"en": "Basking spot 35–42°C (species-dependent), cool side 24–28°C. UVB essential for diurnal species. Thermostat-controlled heating.", "ja": "ホットスポット35〜42℃（種による）、クールゾーン24〜28℃。昼行性種にはUVBが必須。サーモスタット制御の加温。"},
        "humidity": {"en": "Bearded dragon (30–40%), leopard gecko (30–40%), chameleon (50–70%), crested gecko (60–80%). Misting system for tropical species.", "ja": "フトアゴヒゲトカゲ（30〜40%）、ヒョウモントカゲモドキ（30〜40%）、カメレオン（50〜70%）、クレステッドゲッコー（60〜80%）。熱帯種にはミスティングシステム。"},
        "housing": {"en": "Size varies greatly by species. Arboreal species need tall enclosures; terrestrial need floor space. UVB + basking light. Appropriate substrate (no loose sand for bearded dragons).", "ja": "サイズは種により大きく異なる。樹上性種は縦長、地表性種は床面積が重要。UVB＋バスキングライト。適切な床材（フトアゴに砂は不可）。"},
        "diet": {"en": "Varies: omnivore (bearded dragon — insects + greens), insectivore (leopard gecko), herbivore (iguana — greens only). Gut-load insects. Calcium + D3 dusting.", "ja": "種による：雑食（フトアゴ — 昆虫＋野菜）、昆虫食（ヒョウモン）、草食（イグアナ — 野菜のみ）。昆虫はガットローディング。カルシウム＋D3ダスティング。"},
        "enrichment": {"en": "Climbing structures, basking platforms. Varied substrate textures. Live plants (non-toxic). Foraging opportunities. Supervised outdoor time in warm weather.", "ja": "登攀構造物、バスキング台。様々な質感の床材。無毒の生きた植物。採食機会。暖かい日には監視下で屋外日光浴。"},
        "socialization": {"en": "Most lizards are solitary. Bearded dragons can be handleable and interactive. Chameleons are strictly solitary and stress-sensitive. Leopard geckos tolerate gentle handling.", "ja": "多くのトカゲは単独飼育。フトアゴはハンドリングしやすく人馴れする。カメレオンは完全単独でストレスに弱い。ヒョウモンは穏やかなハンドリングを許容。"},
        "notes": {"en": "MBD (metabolic bone disease) is #1 health issue — proper UVB and calcium critical. Tail autotomy in geckos is a defense mechanism (may or may not regrow). Impaction from substrate ingestion is common.", "ja": "MBD（代謝性骨疾患）が最大の健康問題 — UVBとカルシウムが不可欠。ヤモリの尾の自切は防御反応（再生する場合としない場合あり）。床材の誤飲による腸閉塞が多い。"},
        "subtypes": [
            {
                "name": "Bearded Dragon", "name_ja": "フトアゴヒゲトカゲ",
                "temperature": {"en": "Basking 38–42°C, cool side 24–28°C, night 20–22°C. UVB 10.0 essential (10–12 hr/day).", "ja": "ホットスポット38〜42℃、クールゾーン24〜28℃、夜間20〜22℃。UVB 10.0必須（10〜12時間/日）。"},
                "humidity": {"en": "30–40%. Low humidity species; excessive humidity causes respiratory infections.", "ja": "30〜40%。乾燥環境の種。高湿度は呼吸器感染の原因。"},
                "housing": {"en": "120×60×60 cm minimum for adults. Front-opening terrarium preferred. No loose sand substrate (impaction risk) — tile, reptile carpet, or excavator clay.", "ja": "成体で最低120×60×60cm。前面開閉式テラリウム推奨。砂の床材不可（腸閉塞リスク）— タイル、レプタイルカーペット、クレイ系床材。"},
                "diet": {"en": "Juveniles: 70% insects, 30% greens. Adults: 70% greens, 30% insects. Staple insects: dubia roaches, black soldier fly larvae. Greens: collard, mustard, dandelion. Calcium dust daily for juveniles.", "ja": "幼体：昆虫70%、野菜30%。成体：野菜70%、昆虫30%。主食昆虫：デュビアローチ、アメリカミズアブ幼虫。野菜：コラード、マスタードグリーン、タンポポ。幼体はCaダスティング毎日。"},
                "notes": {"en": "Lifespan 10–15 years. Brumation (winter dormancy) normal in adults. Arm waving = submission, head bobbing = dominance/territorial. Black beard = stress or aggression.", "ja": "寿命10〜15年。成体のブルメーション（冬季休眠）は正常。腕振り＝服従、ヘッドボビング＝優位/縄張り。顎が黒くなる＝ストレスまたは攻撃性。"},
            },
            {
                "name": "Leopard Gecko", "name_ja": "ヒョウモントカゲモドキ",
                "temperature": {"en": "Warm side 28–32°C (belly heat via under-tank heater), cool side 24–26°C, night 20–22°C. No UVB strictly required but beneficial.", "ja": "温暖側28〜32℃（パネルヒーターで腹部加温）、冷涼側24〜26℃、夜間20〜22℃。UVBは必須ではないが有益。"},
                "humidity": {"en": "30–40% ambient; humid hide (70–80%) for shedding support.", "ja": "環境湿度30〜40%。脱皮補助用のウェットシェルター（70〜80%）を設置。"},
                "housing": {"en": "60×45×30 cm minimum. Terrestrial — floor space more important than height. 3 hides minimum (warm, cool, humid). Paper towel or tile substrate safest.", "ja": "最低60×45×30cm。地表性 — 高さより床面積重要。最低3つのシェルター（温暖側、冷涼側、ウェット）。キッチンペーパーまたはタイルが最も安全。"},
                "diet": {"en": "Strictly insectivorous: crickets, dubia roaches, mealworms (treat only — high fat). Calcium + D3 dusting every feeding. No vegetables/fruit.", "ja": "完全昆虫食：コオロギ、デュビアローチ、ミルワーム（おやつ程度 — 高脂肪）。毎回Ca＋D3ダスティング。野菜・果物は不可。"},
                "notes": {"en": "Lifespan 15–20+ years. Crepuscular (dawn/dusk active). Fat stored in tail — thin tail indicates illness. Tail autotomy if grabbed — handle body, never tail.", "ja": "寿命15〜20年以上。薄明薄暮性。尻尾に脂肪を蓄積 — 尻尾が細いと体調不良。尻尾を掴むと自切 — 体を持ち、尻尾は決して掴まない。"},
            },
            {
                "name": "Chameleon", "name_ja": "カメレオン",
                "temperature": {"en": "Basking 30–35°C, ambient 24–28°C, night drop to 16–22°C important. UVB 5.0 essential.", "ja": "ホットスポット30〜35℃、環境温度24〜28℃、夜間16〜22℃への温度低下が重要。UVB 5.0必須。"},
                "humidity": {"en": "50–70%. Misting 2–4x daily (they drink water droplets off leaves — do NOT use standing water bowls). Drip system or misting system essential.", "ja": "50〜70%。1日2〜4回の霧吹き（葉の水滴を舐めて飲水 — 水入れは使わない）。ドリップシステムまたはミスティングシステム必須。"},
                "housing": {"en": "Screen/mesh cage (NOT glass — need ventilation). Minimum 60×60×120 cm for veiled/panther chameleons. Live plants (pothos, ficus) essential. Horizontal branches at multiple levels.", "ja": "メッシュケージ（ガラス不可 — 通気性が必要）。エボシ/パンサーで最低60×60×120cm。生きた植物（ポトス、フィカス）必須。複数の高さに水平の枝。"},
                "diet": {"en": "Insectivorous: crickets, silkworms, hornworms. Gut-load insects with greens. Calcium every feeding, D3 2x/month, multivitamin 2x/month.", "ja": "昆虫食：コオロギ、シルクワーム、ホーンワーム。昆虫には野菜でガットローディング。Ca毎回、D3月2回、マルチビタミン月2回。"},
                "notes": {"en": "Lifespan 5–8 years. Strictly solitary — visual contact with other chameleons causes chronic stress. Color changes indicate mood/health. Very stress-sensitive — not a handling pet.", "ja": "寿命5〜8年。厳格な単独飼育 — 他のカメレオンが見えるだけでストレス。体色変化は気分/健康のバロメーター。ストレスに非常に弱い — ハンドリング向きではない。"},
            },
            {
                "name": "Crested Gecko", "name_ja": "クレステッドゲッコー",
                "temperature": {"en": "22–27°C (room temperature often sufficient). Do NOT exceed 30°C — heat-sensitive. No basking light needed. Low UVB beneficial but not essential.", "ja": "22〜27℃（室温で十分なことが多い）。30℃を超えてはならない — 暑さに弱い。バスキングライト不要。低出力UVBは有益だが必須ではない。"},
                "humidity": {"en": "60–80%. Mist heavily in evening, let dry during day. Good ventilation to prevent stagnant air.", "ja": "60〜80%。夕方にたっぷり霧吹き、日中は乾燥させる。空気が淀まないよう換気を確保。"},
                "housing": {"en": "Tall enclosure (45×45×60 cm minimum). Arboreal — vertical space critical. Cork bark, branches, live/artificial plants. Front-opening preferred.", "ja": "縦長ケージ（最低45×45×60cm）。樹上性 — 垂直空間が重要。コルクバーク、枝、生体/人工植物。前面開閉式推奨。"},
                "diet": {"en": "Commercial crested gecko diet (CGD: Repashy, Pangea) as staple — complete nutrition. Insects 1–2x/week as supplement. Fresh CGD every other day.", "ja": "クレステッドゲッコー用人工飼料（CGD：レパシー、パンゲア）が主食 — 完全栄養食。昆虫は週1〜2回の補助。新鮮なCGDを1日おきに。"},
                "notes": {"en": "Lifespan 15–20 years. Dropped tail does NOT regrow (unlike many geckos). 'Floppy tail syndrome' from always hanging upside down. Easy beginner reptile.", "ja": "寿命15〜20年。自切した尻尾は再生しない（他のヤモリと異なる）。常に逆さにいると尻尾が曲がる（フロッピーテール症候群）。初心者向けの飼いやすい種。"},
            },
        ],
    },
    # =========================================================================
    # 両生類 (Amphibian)
    # =========================================================================
    "amphibian": {
        "name": "Amphibian",
        "name_ja": "両生類",
        "temperature": {"en": "18–26°C for most species. Avoid overheating — amphibians are ectothermic and sensitive. No direct sunlight on enclosure.", "ja": "多くの種で18〜26℃。過加温に注意 — 変温動物で敏感。ケージに直射日光を当てない。"},
        "humidity": {"en": "60–80%+ for most species. Misting 1–2x daily. Standing water for aquatic/semi-aquatic species. Dechlorinated water only.", "ja": "多くの種で60〜80%以上。1日1〜2回の霧吹き。水生・半水生種には常水。必ずカルキ抜きした水を使用。"},
        "housing": {"en": "Terrestrial, semi-aquatic, or fully aquatic setup depending on species. Tight-fitting lid (they climb). Live plants help humidity. No sharp objects (delicate skin).", "ja": "種により陸上、半水生、完全水生のセットアップ。しっかり閉まる蓋（登る）。生きた植物で湿度維持。鋭い物は不可（皮膚が繊細）。"},
        "diet": {"en": "Most are insectivorous: gut-loaded crickets, fruit flies (for small species), earthworms. Aquatic species may eat bloodworms, brine shrimp. Calcium dusting essential.", "ja": "多くは昆虫食：ガットローディング済みコオロギ、ショウジョウバエ（小型種）、ミミズ。水生種はアカムシ、ブラインシュリンプ。カルシウムダスティング必須。"},
        "enrichment": {"en": "Live plants, leaf litter, cork bark hides. Water features (small waterfall/drip wall). Varied terrain. Dim lighting (many are nocturnal/crepuscular).", "ja": "生きた植物、落ち葉、コルクバークのシェルター。水場（小さな滝・点滴壁）。変化のある地形。薄暗い照明（夜行性・薄明性が多い）。"},
        "socialization": {"en": "Observation pets — minimal handling recommended. Skin absorbs toxins from human hands (wash hands, wet them before handling). Some species (dart frogs) can be kept in groups.", "ja": "観察型ペット — ハンドリングは最小限推奨。皮膚が人間の手の毒素を吸収（触る前に手を洗い湿らせる）。ヤドクガエルなどはグループ飼育可。"},
        "notes": {"en": "Skin is semi-permeable — water quality and air quality are critical. Chytrid fungus is a global amphibian threat. Never release pet amphibians into the wild. Use dechlorinated or RO water only.", "ja": "皮膚は半透過性 — 水質と空気の質が生命に直結。ツボカビ症は世界的な両生類の脅威。ペットの両生類を野外に放さない。カルキ抜きまたはRO水のみ使用。"},
        "subtypes": [
            {
                "name": "Axolotl", "name_ja": "ウーパールーパー（メキシコサラマンダー）",
                "temperature": {"en": "16–20°C (CRITICAL — cold water species). Above 24°C causes severe stress and death. Aquarium chiller or cool room essential in summer.", "ja": "16〜20℃（厳守 — 冷水種）。24℃以上で重度ストレスと死亡。夏季は水槽用クーラーまたは冷房必須。"},
                "humidity": {"en": "N/A (fully aquatic). Water changes 20% weekly. Dechlorinated water. Ammonia/nitrite must be 0.", "ja": "該当なし（完全水生）。週20%の水替え。カルキ抜き水使用。アンモニア/亜硝酸は0であること。"},
                "housing": {"en": "Minimum 75 L for one axolotl. Fine sand or bare bottom (gravel causes impaction). Gentle filtration (they dislike strong current). Hides and live plants.", "ja": "1匹あたり最低75L。細かい砂またはベアタンク（砂利は誤飲で腸閉塞）。穏やかなろ過（強い水流を嫌う）。隠れ家と水草。"},
                "diet": {"en": "Carnivorous: earthworms (staple), sinking pellets (Hikari), frozen bloodworms. Feed every 1–2 days for juveniles, 2–3x/week for adults.", "ja": "肉食：ミミズ（主食）、沈降性ペレット（ひかり）、冷凍アカムシ。幼体は1〜2日ごと、成体は週2〜3回。"},
                "notes": {"en": "Lifespan 10–15 years. Remarkable regeneration ability (limbs, gills, organs). External gills are normal (neotenic). NEVER house with fish (they eat or get bitten). Critically endangered in the wild.", "ja": "寿命10〜15年。驚異的な再生能力（四肢、鰓、臓器）。外鰓は正常（ネオテニー）。魚との同居は厳禁（食べる/噛まれる）。野生では絶滅危惧種。"},
            },
            {
                "name": "Tree Frog", "name_ja": "ツリーフロッグ（アマガエル類）",
                "temperature": {"en": "22–27°C daytime, 18–22°C night. Avoid overheating. Temperate species (Japanese tree frog) tolerate cooler temperatures.", "ja": "日中22〜27℃、夜間18〜22℃。過加温に注意。温帯種（ニホンアマガエル）はより低温に耐える。"},
                "humidity": {"en": "60–80%. Mist 2–3x daily. Good ventilation to prevent stagnant air. Drip system or large water dish.", "ja": "60〜80%。1日2〜3回霧吹き。換気を確保して空気の淀みを防ぐ。ドリップシステムまたは大きめの水皿。"},
                "housing": {"en": "Tall terrarium (30×30×45 cm minimum). Arboreal — vertical space with branches, vines, broad-leaf plants. Screen or ventilated lid. Shallow water section at bottom.", "ja": "縦長テラリウム（最低30×30×45cm）。樹上性 — 枝、蔓、広葉植物で垂直空間を。メッシュまたは通気性のある蓋。底部に浅い水場。"},
                "diet": {"en": "Small insects: fruit flies, small crickets, springtails. Calcium dusting every feeding. Size-appropriate prey (smaller than frog's head).", "ja": "小型昆虫：ショウジョウバエ、小さなコオロギ、トビムシ。毎回カルシウムダスティング。カエルの頭より小さい餌。"},
                "notes": {"en": "Lifespan varies (5–15+ years by species). Nocturnal/crepuscular — most active at night. Observation pet — handle minimally. Some species produce mild skin toxins.", "ja": "寿命は種により異なる（5〜15年以上）。夜行性/薄明性。観察型ペット — ハンドリングは最小限。軽度の皮膚毒を出す種もある。"},
            },
            {
                "name": "Poison Dart Frog", "name_ja": "ヤドクガエル",
                "temperature": {"en": "22–27°C. Stable temperature crucial. Avoid direct sunlight. Air conditioning may be needed in summer.", "ja": "22〜27℃。安定した温度が重要。直射日光を避ける。夏季はエアコンが必要になることも。"},
                "humidity": {"en": "80–100%. Misting system essential (automatic preferred). Live moss and tropical plants maintain humidity. Fogger can supplement.", "ja": "80〜100%。ミスティングシステム必須（自動が望ましい）。生きた苔と熱帯植物で湿度維持。フォガーで補助。"},
                "housing": {"en": "Bioactive vivarium ideal. Minimum 45×45×45 cm. Drainage layer + substrate + live plants + leaf litter. Tight-fitting lid. Can keep small groups of same species.", "ja": "バイオアクティブビバリウムが理想。最低45×45×45cm。排水層＋床材＋生きた植物＋落ち葉。密閉蓋。同種なら小グループ飼育可。"},
                "diet": {"en": "Tiny insects: fruit flies (Drosophila melanogaster/hydei), springtails, isopods. Calcium + vitamin dusting every feeding. Feed daily.", "ja": "極小昆虫：ショウジョウバエ（メラノガスター/ハイデイ）、トビムシ、ワラジムシ。毎回Ca＋ビタミンダスティング。毎日給餌。"},
                "notes": {"en": "Lifespan 10–20 years. Captive-bred are NOT toxic (toxins come from wild diet). Bold, diurnal, colorful — great display animals. Sensitive to water quality — use RO or spring water.", "ja": "寿命10〜20年。飼育下繁殖個体は無毒（毒は野生の餌由来）。大胆で昼行性、色鮮やか — 素晴らしい観賞動物。水質に敏感 — RO水または湧水を使用。"},
            },
        ],
    },
    # =========================================================================
    # 魚 (Fish)
    # =========================================================================
    "fish": {
        "name": "Fish",
        "name_ja": "魚",
        "temperature": {"en": "Tropical: 24–28°C; Goldfish/Koi: 15–22°C; Marine: 24–27°C. Heater with thermostat essential for tropical. Stable temperature critical.", "ja": "熱帯魚：24〜28℃、金魚/錦鯉：15〜22℃、海水魚：24〜27℃。熱帯魚にはサーモスタット付きヒーター必須。水温の安定が重要。"},
        "humidity": {"en": "N/A (aquatic environment). Tank lid prevents excessive evaporation and fish jumping.", "ja": "該当なし（水中環境）。蓋で蒸発防止と飛び出し事故を予防。"},
        "housing": {"en": "Rule of thumb: 1 inch of fish per gallon (freshwater). Larger is always better. Filtration (mechanical, biological, chemical) essential. Regular water changes (20–30% weekly).", "ja": "目安：魚体長2.5cmあたり約4Lの水量（淡水）。大きいほど良い。ろ過（物理・生物・化学）が必須。定期的な水替え（週20〜30%）。"},
        "diet": {"en": "Species-specific: flake/pellet for community fish, frozen/live foods for predators, algae wafers for bottom feeders. Feed small amounts 1–2x daily. Avoid overfeeding.", "ja": "種に応じて：コミュニティフィッシュにフレーク/ペレット、肉食魚に冷凍/生き餌、底生魚にアルジーウエハー。少量を1日1〜2回。餌の与えすぎに注意。"},
        "enrichment": {"en": "Plants (live preferred), driftwood, rocks, caves. Varied terrain mimicking natural habitat. Appropriate tankmates for social species. LED lighting on timer (8–10 hr photoperiod).", "ja": "水草（生体が望ましい）、流木、石、洞窟。自然の生息地を模した多様な地形。社会性のある種には適切な混泳相手。LEDライトをタイマーで管理（明期8〜10時間）。"},
        "socialization": {"en": "Varies greatly: schooling fish need 6+ of same species, territorial species need space, aggressive species may need solitary tanks. Research compatibility.", "ja": "種により大きく異なる：群泳魚は同種6匹以上、縄張り魚にはスペース、攻撃的な種は単独水槽。混泳の相性を事前に調査。"},
        "notes": {"en": "Nitrogen cycle must be established before adding fish (fishless cycling). Test water parameters regularly (ammonia, nitrite, nitrate, pH). Quarantine new fish 2–4 weeks. Never flush sick fish.", "ja": "魚を入れる前に窒素循環を確立（フィッシュレスサイクリング）。水質パラメータを定期検査（アンモニア、亜硝酸、硝酸、pH）。新しい魚は2〜4週間隔離。病気の魚を流しに捨てない。"},
        "subtypes": [
            {
                "name": "Goldfish / Koi", "name_ja": "金魚・錦鯉",
                "temperature": {"en": "15–22°C (cold water — NO heater needed). Tolerate 4–30°C but optimal range is narrow. Outdoor ponds: seasonal temperature changes are natural.", "ja": "15〜22℃（冷水魚 — ヒーター不要）。4〜30℃に耐えるが最適範囲は狭い。屋外池：季節的な水温変化は自然。"},
                "housing": {"en": "Goldfish: minimum 75 L for first fish, +40 L each additional. Koi: 1,000+ L pond. Powerful filtration essential (heavy bioload). No bowls — goldfish need space and filtration.", "ja": "金魚：最初の1匹に最低75L、追加1匹につき＋40L。錦鯉：1,000L以上の池。強力なろ過が必須（生物負荷が高い）。金魚鉢は不可 — スペースとろ過が必要。"},
                "diet": {"en": "Sinking pellets preferred (floating food causes air gulping → swim bladder issues). Peas (deshelled), blanched vegetables as treats. Feed 2x daily, amount consumed in 2 minutes.", "ja": "沈降性ペレット推奨（浮上性餌は空気を飲む→転覆病の原因）。剥いたエンドウ豆、茹で野菜をおやつに。1日2回、2分で食べ切る量。"},
                "notes": {"en": "Goldfish lifespan 10–15+ years (NOT disposable pets). Koi 25–35+ years. Swim bladder disease very common in fancy varieties. Ammonia burns are #1 killer — cycle the tank first.", "ja": "金魚の寿命10〜15年以上（使い捨てではない）。錦鯉25〜35年以上。琉金等のファンシー種は転覆病が非常に多い。アンモニア中毒が最大の死因 — 先にフィッシュレスサイクリングを。"},
            },
            {
                "name": "Tropical Freshwater", "name_ja": "熱帯淡水魚",
                "temperature": {"en": "24–28°C (heater with thermostat essential). Stable temperature critical — fluctuations cause stress and ich outbreaks.", "ja": "24〜28℃（サーモスタット付きヒーター必須）。安定した水温が重要 — 変動はストレスと白点病の原因。"},
                "housing": {"en": "Community tanks: 60+ L minimum. Planted tanks ideal. Species-appropriate flow rate. Driftwood, rocks for territory. Dimmer lighting for shy species (tetras, corydoras).", "ja": "コミュニティタンク：最低60L以上。水草水槽が理想。種に合った水流。流木、石で縄張り。シャイな種（テトラ、コリドラス）には暗めの照明。"},
                "diet": {"en": "High-quality flake/micro pellets as staple. Frozen/live foods (brine shrimp, daphnia, bloodworms) 2–3x/week. Bottom feeders: algae wafers, sinking pellets. Feed small amounts 1–2x daily.", "ja": "良質なフレーク/マイクロペレットを主食に。冷凍/生き餌（ブラインシュリンプ、ミジンコ、アカムシ）を週2〜3回。底生魚：アルジーウエハー、沈降性ペレット。少量を1日1〜2回。"},
                "notes": {"en": "Water parameters vary by species: tetras/discus prefer soft acidic (pH 6.0–7.0), livebearers prefer hard alkaline (pH 7.0–8.0). Research species requirements before mixing.", "ja": "水質は種により異なる：テトラ/ディスカスは軟水・酸性（pH 6.0〜7.0）、グッピー等は硬水・アルカリ性（pH 7.0〜8.0）。混泳前に種の要件を調査。"},
            },
            {
                "name": "Betta (Siamese Fighting Fish)", "name_ja": "ベタ（闘魚）",
                "temperature": {"en": "25–28°C. Tropical species — heater essential (NOT a cold-water fish despite common misconception). Stable temperature critical.", "ja": "25〜28℃。熱帯魚 — ヒーター必須（一般的な誤解に反して冷水魚ではない）。水温の安定が重要。"},
                "housing": {"en": "Minimum 20 L (NOT tiny bowls/cups). Gentle filtration (they dislike strong current due to long fins). Lid essential (they jump). Live or silk plants (no sharp plastic — fin damage).", "ja": "最低20L（小さなボウル/カップは不可）。穏やかなろ過（長いヒレのため強い水流を嫌う）。蓋必須（飛び出す）。生体またはシルク製の植物（鋭いプラスチックはヒレを傷つける）。"},
                "diet": {"en": "High-protein betta pellets as staple. Frozen/live bloodworms, brine shrimp, daphnia as treats 2–3x/week. Feed 2–3 pellets 2x daily. Prone to bloating from overfeeding.", "ja": "高タンパクのベタ用ペレットを主食に。冷凍/生きアカムシ、ブラインシュリンプ、ミジンコを週2〜3回のおやつに。1回2〜3粒を1日2回。過食で膨満しやすい。"},
                "notes": {"en": "Lifespan 3–5 years. Males MUST be housed alone (will fight to death). Females can sometimes coexist in 'sorority' tanks (5+ in 75+ L). Bubble nest building is normal healthy behavior.", "ja": "寿命3〜5年。オスは必ず単独飼育（死ぬまで戦う）。メスは「ソロリティ」タンク（75L以上に5匹以上）で共存可能な場合も。泡巣作りは正常な健康行動。"},
            },
            {
                "name": "Marine / Saltwater", "name_ja": "海水魚",
                "temperature": {"en": "24–27°C. Chiller may be needed in summer. Temperature stability even more critical than freshwater — ±1°C fluctuation max.", "ja": "24〜27℃。夏季はクーラーが必要になることも。淡水以上に水温安定が重要 — 変動は±1℃以内。"},
                "housing": {"en": "Minimum 150 L for fish-only, 200+ L for reef. Protein skimmer essential. Live rock for biological filtration. RO/DI water for top-off and salt mixing. Salinity 1.023–1.025 SG.", "ja": "魚のみなら最低150L、サンゴ水槽なら200L以上。プロテインスキマー必須。ライブロックで生物ろ過。RO/DI水で足し水と人工海水。比重1.023〜1.025。"},
                "diet": {"en": "Species-specific: herbivores (nori, spirulina), omnivores (mixed flake + frozen mysis), carnivores (frozen shrimp, silversides). Marine fish often need multiple small feedings per day.", "ja": "種による：草食魚（海苔、スピルリナ）、雑食魚（フレーク＋冷凍ミシスシュリンプ）、肉食魚（冷凍エビ、シルバーサイド）。海水魚は1日複数回の少量給餌が必要なことが多い。"},
                "notes": {"en": "Most expensive and demanding aquarium type. Quarantine ALL new fish (ich/velvet can devastate a tank). Copper medications kill invertebrates. Research extensively before starting — high learning curve.", "ja": "最も費用と手間がかかる水槽タイプ。新しい魚は全て隔離（白点病/ウーディニウムが水槽を壊滅させる）。銅系薬品は無脊椎動物を殺す。始める前に徹底的にリサーチ — 学習曲線が急。"},
            },
        ],
    },
    # =========================================================================
    # その他エキゾチック (Exotic Other)
    # =========================================================================
    "exotic_other": {
        "name": "Other Exotic",
        "name_ja": "その他エキゾチック",
        "temperature": {"en": "Highly species-dependent. Research the specific species' natural habitat to replicate appropriate thermal conditions.", "ja": "種により大きく異なる。飼育する種の自然生息地を調べて適切な温度条件を再現。"},
        "humidity": {"en": "Species-dependent. Match the natural habitat conditions of the specific animal.", "ja": "種による。飼育する動物の自然生息地の条件に合わせる。"},
        "housing": {"en": "Research species-specific requirements thoroughly before acquisition. Provide appropriate space, substrate, and environmental features. Escape prevention critical for all exotic species.", "ja": "飼育前に種固有の要件を徹底的に調査。適切な広さ、床材、環境設備を提供。全てのエキゾチック種で脱走防止が重要。"},
        "diet": {"en": "Highly variable. Consult exotic animal veterinarian and species-specific care guides. Nutritional deficiencies are the most common health issue in exotic pets.", "ja": "種により大きく異なる。エキゾチック動物の獣医と種別飼育ガイドを参照。栄養不足がエキゾチックペットの最も一般的な健康問題。"},
        "enrichment": {"en": "Environmental complexity matching natural habitat. Foraging opportunities. Species-appropriate social grouping. Mental stimulation through novel objects and experiences.", "ja": "自然生息地に合った環境の複雑さ。採食機会。種に適した社会的グループ。新しい物や経験による精神的刺激。"},
        "socialization": {"en": "Research species-specific social needs. Some exotic species are strictly solitary, others require social groups. Improper socialization is a major welfare concern.", "ja": "種固有の社会的ニーズを調査。厳格に単独飼育の種もあれば、群れが必要な種もある。不適切な社会化は重大な福祉問題。"},
        "notes": {"en": "Always check local laws regarding exotic pet ownership. Find an exotic-experienced veterinarian BEFORE acquiring the animal. Many exotic pets have long lifespans — ensure long-term commitment.", "ja": "エキゾチックペットの飼育に関する地域の法律を必ず確認。動物を迎える前にエキゾチック診療経験のある獣医を見つける。長寿の種が多い — 長期飼育の覚悟を。"},
    },
}
