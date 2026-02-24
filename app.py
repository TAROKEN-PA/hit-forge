# -*- coding: utf-8 -*-
import streamlit as st

APP_TITLE = "HitForge"  # バージョン表記は不要
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================
# CSS（可読性最優先のライト系トーン）
# =========================
st.markdown(
    """
    <style>
      /* ベース */
      html, body, .block-container {
        background: #f7f8fb;  /* 明るい背景 */
        color: #111;          /* 充分なコントラスト */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Meiryo", Arial, sans-serif;
      }
      /* タイトルを特大に */
      .app-title h1 {
        font-size: 2.4rem;
        line-height: 1.25;
        font-weight: 800;
        letter-spacing: 0.2px;
        margin: 0.3rem 0 1.0rem 0;
        color: #0f172a; /* 濃紺寄りで視認性UP */
      }
      /* セクション見出し */
      .section-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0.5rem;
        letter-spacing: 0.2px;
      }
      /* カード風コンテナ */
      .card {
        background: #ffffff;
        border: 1px solid #e6e8ee;
        border-radius: 12px;
        padding: 1.0rem 1.0rem;
        box-shadow: 0 1px 2px rgba(16,24,40,0.04);
        margin-bottom: 1rem;
      }
      /* コードブロックの視認性 */
      pre, code {
        background: #0b1020;
        color: #e6edf7;
        border-radius: 10px !important;
      }
      /* ボタン */
      .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.0rem;
        font-weight: 700;
        letter-spacing: 0.3px;
      }
      .stButton > button:hover {
        filter: brightness(1.05);
      }
      /* サイドバー背景 */
      section[data-testid="stSidebar"] {
        background: #f3f4f8 !important;
        border-right: 1px solid #e6e8ee;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# データベース（カテゴリ/ジャンル拡充）
# p: 楽曲スタイル / v_base: ボーカル基調 / l_base: 歌詞基調 / boost: サビ強化要素 / logic: 背景ロジック
# =========================
db = {
    # --- 新設: USチャート向け ---
    "US Chart Playbook": {
        "Pop Rap (Melodic)": {
            "p": "Pop-rap, 88–100 BPM, punchy 808, crisp hats, bright synth layers, hooky topline.",
            "v_base": "Conversational rhythmic phrasing, mid-high register, catchy ad-libs.",
            "l_base": "Braggadocious vs introspection balance, simple quotable lines.",
            "boost": "Layered gang-vocals + octave-doubled hook; sub-bass lift on chorus.",
            "logic": "2024年はHip-hop/rapがHot 100 Top10で最大シェア（38%）。ラップ×ポップの勘所を押さえる構成が依然強力。[1](https://www.billboard.com/pro/hip-hop-top-hit-songs-deconstructed-hot-100-top-10-report-2024/)",
        },
        "Pop Anthem (Female)": {
            "p": "Modern Pop, 118–128 BPM, tight drums, wide synths, low acousticness, high loudness.",
            "v_base": "High register belt + stacked harmonies.",
            "l_base": "Empowerment / romance clarity, memorable chorus phrase.",
            "boost": "Pre-chorus lift → soaring chorus; post-chorus chant.",
            "logic": "上位曲はラウドネス高・適度なダンサビリティ・明快な構造（2024分析）。[2](https://cnsmaryland.org/2024/04/16/what-makes-a-hit-a-look-into-2024s-top-charting-songs/)",
        },
        "Country‑Pop Crossover": {
            "p": "Country‑pop, 86–100 BPM, acoustic/electric blend, steady kick, pop mix.",
            "v_base": "Warm storytelling tone, slight twang.",
            "l_base": "Everyday narratives + vivid imagery.",
            "boost": "Final chorus key/energy lift; stacked gang choir.",
            "logic": "2024年の年末Hot 100ではCountry/Popクロスの躍進が顕著（例: Shaboozey, Post Malone ft. Morgan Wallen）。[3](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2024)",
        },
        "R&B‑Pop Slowbounce": {
            "p": "R&B‑pop, 80–95 BPM, lush pads, clean snaps, sub‑focused low end.",
            "v_base": "Breathy intimate lead + doubles.",
            "l_base": "Introspective love/solitude.",
            "boost": "Melodic leap on chorus with airy harmonies.",
            "logic": "内省的テーマの増加、曲尺は近年やや長めへ回帰（平均3:40）。[4](https://www.hitsongsdeconstructed.com/hsd_wire/the-state-of-the-hot-100-top-10-2024-trend-report/)",
        },
    },

    # --- 新設: JPチャート向け ---
    "JP Chart Playbook": {
        "Anime OP（王道）": {
            "p": "Anime OP, 168–178 BPM, brass hits, galloping drums, rock orchestra.",
            "v_base": "Power belts (男女可), tight ensemble chorus.",
            "l_base": "夢/勇気/スケール大の語彙、比喩濃度高め。",
            "boost": "Dynamic soaring hook + cinematic explosion.",
            "logic": "2024年のJAPAN Hot 100年間1位はアニメOP系の楽曲（Creepy Nuts “BBBB”）。[5](https://www.billboard.com/music/chart-beat/billboard-japan-2024-year-end-charts-creepy-nuts-snow-man-mrs-green-apple-1235846923/)",
        },
        "Vocaloid‑Influenced J‑Pop": {
            "p": "Fast J‑Pop, 160–175 BPM, dense piano, syncopated phrases, EDM hybrid.",
            "v_base": "Agile high‑pitch, precise diction.",
            "l_base": "ネット文化語彙＋高速言い回し。",
            "boost": "Hook repetition + shoutable tags.",
            "logic": "日本では動画/UGCとの親和が高い高速系・反復タグが波及しやすい（J Hot100動向）。[6](https://billboard-japan.com/charts/detail?a=hot100_year&year=2024)",
        },
        "City Pop 2.0": {
            "p": "City Pop, 112–122 BPM, slap bass/DX7, funk guitar, smooth chords.",
            "v_base": "Sophisticated airy tone.",
            "l_base": "都会ノスタルジー/夜景/ドライブ。",
            "boost": "Sparkling synth top‑line + falsetto lifts.",
            "logic": "City Pop再評価は世界的な配信駆動で継続中。[7](https://musicindustryweekly.com/japanese-city-pop-global-comeback-streaming-2024/)",
        },
        "J‑Ballad Modern": {
            "p": "Modern ballad, 70–82 BPM, strings/piano, modern drum support.",
            "v_base": "Emotional vibrato, intimate storytelling.",
            "l_base": "情景描写＋心情の起伏。",
            "boost": "Final double chorus + ad‑lib expansion.",
            "logic": "国内配信/カラオケ指標で粘るスローテンポ曲の地力は依然強い（総合指標型チャートの性質）。[8](https://billboard-japan.com/charts/year_end?year=2024)",
        },
        "J‑Rock Anthem": {
            "p": "J‑Rock, 140–160 BPM, overdriven guitar, solid bass, live‑feel drums.",
            "v_base": "Raspy male/female, strong vibrato.",
            "l_base": "青春/疾走/群像。",
            "boost": "Guitar‑driven hook + unison shout.",
            "logic": "バンド楽曲はライブ映え×サビ同唱で長期浸透（年末チャートにも古参曲が並ぶ傾向）。[6](https://billboard-japan.com/charts/detail?a=hot100_year&year=2024)",
        },
    },

    # --- 新設: KRチャート向け ---
    "KR Chart Playbook": {
        "K‑Pop Girl Group Dance": {
            "p": "K‑Pop dance, 120–132 BPM, moombahton/reggaeton touches, tight brass/synth stabs.",
            "v_base": "Highly harmonized + chantable group shouts.",
            "l_base": "Confident, bilingual hooks (Korean main + Eng hook).",
            "boost": "Post‑chorus hook（歌orインスト）＋ダンスブレイク。",
            "logic": "K‑Popはポストコーラス/ダンスブレイク/セクション多様化が定石。[9](https://www.mtna.org/downloads/GP3/Handouts/2022/K-POP%20Presentation.pdf)[10](https://kpopalypse.com/2016/09/13/kpopalypse-explains-common-song-structures-in-k-pop/)",
        },
        "K‑Pop Boy Group Anthem": {
            "p": "Hybrid pop/EDM/rock, 140–160 BPM, big toms, EDM drops.",
            "v_base": "Powerful belts + rap breaks.",
            "l_base": "Unity/resolve/ambition.",
            "boost": "Build→Drop（anti‑chorus含む）＋最後にキー感リフト。",
            "logic": "サビ前のリフトとドロップの二段構えで映像/振付の見せ場を最大化。[9](https://www.mtna.org/downloads/GP3/Handouts/2022/K-POP%20Presentation.pdf)",
        },
        "K‑R&B": {
            "p": "Alt R&B, 78–92 BPM, minimal beats, silky chords, sub‑bass.",
            "v_base": "Smooth falsetto/airy head voice.",
            "l_base": "Intimate urban romance.",
            "boost": "Falsetto lift + stacked airy harmonies.",
            "logic": "KR配信市場でR&Bは継続強含み（Circleの総合はストリーミング/ダウンロード複合）。[11](https://en.wikipedia.org/wiki/Circle_Digital_Chart)",
        },
        "Trot‑Pop Hybrid": {
            "p": "Modern trot‑pop, 70–95 BPM, shinobue/brass option, big room claps.",
            "v_base": "Dramatic vibrato, wide dynamics.",
            "l_base": "人生譚/情愛/誓い。",
            "boost": "Key up + call & response.",
            "logic": "国内デジタル総合でトロットも定期的に存在感（年次チャートでも顕在）。[12](https://www.soompi.com/article/1715673wpp/circle-chart-reveals-year-end-album-and-digital-charts-for-2024)",
        },
    },

    # 既存ワールド系（拡充例）
    "World / Urban Heat": {
        "Afrobeats (Tropical)": {
            "p": "Afrobeats, 100–110 BPM, organic perc, marimba/plucks, warm pads.",
            "v_base": "Soulful relaxed melodic.",
            "l_base": "Groovy repetitive sunny metaphors.",
            "boost": "Syncopated catchy rhythm, lush ad‑libs.",
            "logic": "US/Globalで継続的にプレイリスト主軸。[13](https://billboard-japan.com/charts/detail?a=uhot100_year&year=2024)",
        },
        "Reggaeton Pop": {
            "p": "Reggaeton‑pop, 90–100 BPM, dembow groove, synth brass.",
            "v_base": "Rhythmic phrasing + doubles.",
            "l_base": "Flirty/nightlife themes.",
            "boost": "Hook repetition + pitch‑drop FX.",
            "logic": "英語圏チャートでもクロスオーバー常連。[13](https://billboard-japan.com/charts/detail?a=uhot100_year&year=2024)",
        },
    },

    # 既存実験系（サンプル）
    "Experimental / Anime": {
        "Future Bass (Sparkle)": {
            "p": "Future Bass, 150–165 BPM, super‑saw chords, LFO wobble, vocal chops.",
            "v_base": "Cute high‑pitch female, airy style.",
            "l_base": "Digital love, sparkle, high‑speed phrases.",
            "boost": "Massive wobble drop + vocal climax.",
            "logic": "ポップ×EDMの王道路線でサビ昇圧が効く。"
        },
        "王道アニソンOP（熱血）": {
            "p": "Anime OP, 170–178 BPM, brass hits, galloping drums, rock orchestra.",
            "v_base": "Power belts, hot‑blooded.",
            "l_base": "Dreams, courage, epic scale.",
            "boost": "Dynamic soaring hook, cinematic explosion.",
            "logic": "開幕からの掴みを最大化し、視聴継続率を上げる。"
        },
    },
}

# =========================
# 生成ロジック
# =========================
def generate_strategy(cat, genre, v_gender, l_pov, lang_opt, must_have, negative_p, limit, boost_mode, optimizer):
    d = db[cat][genre]

    # 1) Identity（性別/視点）
    v_f = f"{v_gender} vocal, {d['v_base']}"
    l_f = f"{l_pov}, {d['l_base']}"

    # 2) 言語構成
    lang_map = {
        "日本語（サビのみ英語可）": "Main Lang: Japanese. Catchy English only in chorus.",
        "全日本語": "Language: 100% Japanese.",
        "韓国語（サビのみ英語可）": "Main Lang: Korean. Catchy English only in chorus.",
        "全英語": "Language: English."
    }
    l_ins = lang_map[lang_opt]

    # 3) 構造/サビ強化
    struct = "Short verses, fast transition to chorus. No long intros."
    bst = d["boost"] if boost_mode else ""

    # 4) 歌詞キーワード制御
    focus_ins = f"Lyrics must include: {must_have}" if must_have else ""
    neg_ins = f"NO (lyrics): {negative_p}" if negative_p else ""

    # 5) Top-Chart Optimizer（米/日/韓のヒット傾向注入）
    optimizer_block = ""
    if optimizer:
        optimizer_lines = [
            # 早いコーラス到達（平均~0:42/19%目安）
            "Hit Optimizer: First chorus ≤ 0:40, hook within first 0:15. Strong pre-chorus lift → chorus. [14](https://www.hitsongsdeconstructed.com/hsd_wire/hit-song-choruses/)",
            # ラウドネスと適度なダンサビリティ（2024分析）
            "Mix Target: High perceived loudness, moderate-high danceability/energy; avoid high acousticness for pop crossovers. [2](https://cnsmaryland.org/2024/04/16/what-makes-a-hit-a-look-into-2024s-top-charting-songs/)",
            # 曲尺傾向（2024は平均3:40）
            "Duration: Aim around ~3:20–3:50 with distinct post-chorus/payoff moments. [4](https://www.hitsongsdeconstructed.com/hsd_wire/the-state-of-the-hot-100-top-10-2024-trend-report/)",
            # K‑Popのセクション作法
            "K-Style Options: Post-chorus hook / dance break, multi-section variety without losing core hook. [9](https://www.mtna.org/downloads/GP3/Handouts/2022/K-POP%20Presentation.pdf)"
        ]
        optimizer_block = " ".join(optimizer_lines)

    # 6) 統合プロンプト
    full_p = f"{l_ins} {struct} {bst} {focus_ins} Vocal: {v_f} POV & Phrasing: {l_f}. {neg_ins} {optimizer_block}"
    return full_p[:limit], d


# =========================
# UI
# =========================
st.markdown(f"""
<div class="app-title">
  <h1>🔥 {APP_TITLE}</h1>
</div>
""", unsafe_allow_html=True)

# レイアウト：サイドバー
with st.sidebar:
    st.markdown('<div class="section-title">🎯 IDENTITY & POV</div>', unsafe_allow_html=True)
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary / Neutral"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.markdown('<div class="section-title">🔑 LYRICS CONTROL</div>', unsafe_allow_html=True)
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光, 運命のドア")
    negative_p = st.text_input("歌詞除外設定 (Negative)", placeholder="例: 暴力表現, あいまいな一般論")

    st.markdown('<div class="section-title">⚙️ PRODUCTION</div>', unsafe_allow_html=True)
    limit = st.slider("文字数上限", 80, 1200, 360, 10)
    lang_opt = st.selectbox("言語構成", ["日本語（サビのみ英語可）", "全日本語", "韓国語（サビのみ英語可）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost（サビ強化ON）", value=True)
    optimizer = st.toggle("Top‑Chart Optimizer（米/日/韓データ注入）", value=True)

    c_col, g_col = st.columns(2)
    with c_col:
        cat = st.selectbox("CATEGORY", list(db.keys()))
    with g_col:
        genre = st.selectbox("GENRE", list(db[cat].keys()))

# 実行ボタン
run = st.button("Start / 開始 (Generate)")

if run:
    final_p, d_info = generate_strategy(
        cat=cat, genre=genre, v_gender=v_gender, l_pov=l_pov,
        lang_opt=lang_opt, must_have=must_have, negative_p=negative_p,
        limit=limit, boost_mode=boost_mode, optimizer=optimizer
    )

    st.markdown("### ✅ 出力", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📣 Styleプロンプト（楽曲/ボーカル設定）")
        st.code(f"{d_info['p']} {d_info['boost'] if boost_mode else ''} Vocal: {v_gender}. {d_info['v_base']}  NO (lyrics): {negative_p if negative_p else '—'}")

        st.subheader(f"✍️ 歌詞指示プロンプト（{len(final_p)} / {limit} 文字）")
        st.code(final_p)

        st.subheader("🧠 徹底ロジカル解説")
        st.markdown(
            f"""
- **音楽的背景**：{d_info['logic']}
- **言語主権**：AIの“勝手な言語変更”を抑止し、指定言語＋サビのみ英語等の運用を徹底。  
- **構造強制**：Short verses → 早期コーラス到達。**ポストコーラス**で2段目のカタルシスを設計。[14](https://www.hitsongsdeconstructed.com/hsd_wire/hit-song-choruses/)  
- **ミックス目標**：ラウドネス強め／ダンサビリティ中〜高／アコースティック成分は控えめ（ポップ系）。[2](https://cnsmaryland.org/2024/04/16/what-makes-a-hit-a-look-into-2024s-top-charting-songs/)  
- **曲尺ガイド**：~3:20–3:50 目安（2024年はTop10平均3:40）。[4](https://www.hitsongsdeconstructed.com/hsd_wire/the-state-of-the-hot-100-top-10-2024-trend-report/)
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.success(f"⚔️ {genre.upper()} – 最強プロンプト生成が完了しました！")
