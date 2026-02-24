# -*- coding: utf-8 -*-
import streamlit as st

APP_TITLE = "HitForge"  # バージョン表記は不要
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================================================
#  Lux UI: Black & Gold Premium Theme + Icons/Illustrations
#  - 高コントラストの黒基調に金色アクセント
#  - HeroバナーはインラインSVG（外部依存なし）
#  - テキストは白系に統一（--text:#ffffff / --muted:#ffffffcc）
#  - コード/テキストの折り返しを有効化（プロンプト全文表示）
# =========================================================
st.markdown(
    """
    <style>
      :root{
        --bg: #0a0b0e;        /* 背景（黒） */
        --panel: #101217;     /* パネル（濃紺寄りの黒） */
        --card: #111418;      /* カード（黒） */
        --border: #1d212a;    /* 枠線 */

        /* ▼テキストを白に統一 ▼*/
        --text: #ffffff;          /* メイン文字 */
        --muted: #ffffffcc;       /* サブ文字（半透明の白） */

        --gold: #e3b341;      /* ゴールド */
        --gold-strong: #f1c84c;
        --gold-soft: rgba(227,179,65,0.25);
        --accent: #7c4dff;    /* 差し色（控えめ） */
      }
      html, body, .block-container{
        background: var(--bg);
        color: var(--text);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Meiryo", Arial, sans-serif;
      }
      /* タイトル（特大 & ゴールド装飾） */
      .app-title h1{
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: .4px;
        line-height: 1.2;
        color: var(--text);
        margin: .25rem 0 .8rem 0;
      }
      .app-title .gold-underline{
        display:inline-block; height:6px; width:160px; border-radius:6px;
        background: linear-gradient(90deg, var(--gold), var(--gold-strong));
        margin-top:.2rem;
      }

      /* ヒーロー・カード群 */
      .hero, .card{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 4px 18px rgba(0,0,0,.28), inset 0 0 0 1px rgba(255,255,255,.02);
      }
      .hero{ padding: 0; overflow: hidden; }
      .hero-top{ padding: 1rem 1.2rem 0.6rem 1.2rem; }
      .hero-svg{
        width: 100%; height: 160px;
        background: radial-gradient(1200px 240px at 20% 0%, rgba(227,179,65,0.18), transparent 60%),
                    radial-gradient(900px 220px at 80% 0%, rgba(124,77,255,0.20), transparent 60%);
        border-top: 1px solid var(--border);
      }

      /* サイドバー（黒×ゴールド） */
      section[data-testid="stSidebar"]{
        background: var(--panel) !important;
        border-right: 1px solid var(--border);
      }
      .section-title{
        font-size: .98rem; font-weight: 800; color: var(--text);
        letter-spacing: .25px; display:flex; align-items:center; gap:.5rem;
        margin:.2rem 0 .2rem 0;
      }
      .section-title .badge{
        display:inline-flex; align-items:center; justify-content:center;
        width:22px; height:22px; border-radius:7px; font-size:.8rem;
        background: linear-gradient(135deg, rgba(227,179,65,.12), rgba(227,179,65,.05));
        border: 1px solid rgba(227,179,65,.22);
        color: var(--gold);
      }

      /* ボタン（黒→ゴールドのグラデ） */
      .stButton > button{
        background: linear-gradient(135deg, #1b1e25 0%, rgba(227,179,65,.95) 100%);
        color:#0a0b0e; font-weight: 900; letter-spacing: .4px;
        border:none; border-radius: 12px; padding: .65rem 1.05rem;
        box-shadow: 0 10px 22px rgba(227,179,65,.18);
      }
      .stButton > button:hover{ filter: brightness(1.05); }

      /* 入力/セレクト類の強調枠 */
      .stSelectbox, .stTextInput, .stRadio, .stSlider, .stToggle{ background: transparent !important; }
      .stTextInput > div > div > input,
      .stTextArea textarea{
        background: #0d1016 !important;
        color: var(--text) !important;
        border:1px solid var(--border) !important;
        border-radius: 10px !important;
      }
      .stSelectbox div[data-baseweb="select"] > div{
        background:#0d1016; border:1px solid var(--border); border-radius:10px; color: var(--text);
      }

      /* コード/プレの折り返し（←コレが重要） */
      pre, code, .element-container .stCode pre{
        white-space: pre-wrap !important;       /* 折り返し */
        word-break: break-word !important;
        overflow-x: hidden !important;
        color: var(--text) !important;
      }

      /* 情報ボックス */
      .meta{ color: var(--muted); font-size:.92rem; margin-top:.25rem; }
      .gold-chip{
        display:inline-flex; gap:.35rem; align-items:center;
        background: linear-gradient(135deg, rgba(227,179,65,.18), rgba(227,179,65,.08));
        border:1px solid rgba(227,179,65,.28);
        padding:.25rem .55rem; border-radius: 999px; color: var(--gold);
        font-weight:700; letter-spacing:.2px; font-size:.86rem;
      }
      .subtle{ color: var(--muted); font-size:.92rem; letter-spacing:.2px; margin-bottom:.6rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 強制ホワイト化の上書きパッチ（優先度をさらに上げる） ---
st.markdown(
    """
    <style>
      /* =============================
         強制ホワイト化パッチ（上書き用・最後勝ち）
         ============================= */
      html, body, .block-container, .stApp, .stMarkdown, .stText, .stWrite, .stSpinner,
      .stExpander, .stTabs, .stTab, .stCheckbox, .stRadio, .stSelectbox, .stDateInput,
      .stSlider, .stMultiSelect, .stTextInput, .stTextArea, .stNumberInput, .stDownloadButton,
      section[data-testid="stSidebar"], header[tabindex="0"] * {
        color: #ffffff !important;
      }
      label, .st-bx, .st-bb, .st-bc, .st-bd, .st-be, .st-af, .st-ag, .st-ah { color: #ffffff !important; }
      p, span, li, h1, h2, h3, h4, h5, h6, small, strong, em { color: #ffffff !important; }
      section[data-testid="stSidebar"] * { color: #ffffff !important; }
      input, textarea, [data-baseweb="input"], [data-baseweb="textarea"] { color: #ffffff !important; }
      input::placeholder, textarea::placeholder { color: #ffffffcc !important; }
      div[data-baseweb="select"] * { color: #ffffff !important; }
      div[data-baseweb="select"] svg { fill: #ffffff !important; }
      pre, code, .element-container .stCode pre {
        color: #ffffff !important; white-space: pre-wrap !important; word-break: break-word !important; overflow-x: hidden !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
#  Hero（インラインSVGの“金色サウンドウェーブ”）
# =========================
st.markdown(
    f"""
    <div class=\"app-title\">
      <h1>🎼 {APP_TITLE}</h1>
      <span class=\"gold-underline\"></span>
    </div>
    <div class=\"hero\">
      <div class=\"hero-top\">
        <div class=\"meta\</div>
      </div>
      <div class=\"hero-svg\">
        <!-- 波形っぽいライン（装飾） -->
        <svg width=\"100%\" height=\"100%\" xmlns=\"http://www.w3.org/2000/svg\" preserveAspectRatio=\"none\">
          <defs>
            <linearGradient id=\"goldGrad\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\">
              <stop offset=\"0%\" stop-color=\"#b9902e\" />
              <stop offset=\"100%\" stop-color=\"#f1c84c\" />
            </linearGradient>
          </defs>
          <path d=\"M0,100 C150,60 250,140 400,100 C550,60 650,140 800,100 L1200,100\"
                stroke=\"url(#goldGrad)\" stroke-width=\"3\" fill=\"transparent\" opacity=\"0.9\"/>
          <path d=\"M0,120 C150,80 250,160 400,120 C550,80 650,160 800,120 L1200,120\"
                stroke=\"url(#goldGrad)\" stroke-width=\"2\" fill=\"transparent\" opacity=\"0.55\"/>
          <path d=\"M0,140 C150,100 250,180 400,140 C550,100 650,180 800,140 L1200,140\"
                stroke=\"url(#goldGrad)\" stroke-width=\"1.5\" fill=\"transparent\" opacity=\"0.35\"/>
        </svg>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# データベース（主要プレイブック）
# =========================
db = {
    "US Chart Playbook": {
        "Pop Rap (Melodic)": {
            "p": "Pop-rap, 88–100 BPM, punchy 808, bright synth, hooky topline.",
            "v_base": "Conversational rhythmic phrasing, mid-high register, catchy ad-libs.",
            "l_base": "Braggadocious vs introspection, quotable lines.",
            "boost": "Layered gang-vocals + octave hook; sub-bass lift on chorus.",
            "logic": "USトップ10でHip-hop/rap の存在感が大きい年度を踏まえた構造設計。",
        },
        "Pop Anthem (Female)": {
            "p": "Modern Pop, 118–128 BPM, tight drums, wide synths, low acousticness, high loudness.",
            "v_base": "High register belt + stacked harmonies.",
            "l_base": "Empowerment / romance clarity, memorable hook phrase.",
            "boost": "Pre-chorus lift → soaring chorus; post-chorus chant.",
            "logic": "高ラウドネス＆中〜高ダンサビリティの王道アンセム構成。",
        },
        "Country‑Pop Crossover": {
            "p": "Country‑pop, 86–100 BPM, acoustic/electric blend, steady kick, pop mix.",
            "v_base": "Warm storytelling tone.",
            "l_base": "Everyday narratives + vivid imagery.",
            "boost": "Final chorus energy/key lift; stacked choir.",
            "logic": "クロスオーバー楽曲の王道：語り×キャッチーなコーラス。",
        },
    },
    "JP Chart Playbook": {
        "Anime OP（王道）": {
            "p": "Anime OP, 168–178 BPM, brass hits, galloping drums, rock orchestra.",
            "v_base": "Power belts (男女可), tight ensemble chorus.",
            "l_base": "夢/勇気/スケール大の語彙、比喩濃度高め。",
            "boost": "Dynamic soaring hook + cinematic explosion.",
            "logic": "アニメ主題歌系の“早い掴み”×“大サビ”で最大化。",
        },
        "City Pop 2.0": {
            "p": "City Pop, 112–122 BPM, slap bass/DX7, funk guitar, smooth chords.",
            "v_base": "Sophisticated airy tone.",
            "l_base": "都会ノスタルジー/夜景/ドライブ。",
            "boost": "Sparkling synth top‑line + falsetto lifts.",
            "logic": "配信での再評価文脈を反映。",
        },
        "J‑Rock Anthem": {
            "p": "J‑Rock, 140–160 BPM, overdriven guitar, solid bass, live‑feel drums.",
            "v_base": "Raspy male/female, strong vibrato.",
            "l_base": "青春/疾走/同唱感。",
            "boost": "Guitar‑driven hook + unison shout.",
            "logic": "ライブ映え×コーラス同唱で浸透力を上げる。",
        },
    },
    "KR Chart Playbook": {
        "K‑Pop Girl Group Dance": {
            "p": "K‑Pop dance, 120–132 BPM, moombahton touches, sharp synth stabs.",
            "v_base": "Highly harmonized + chantable shouts.",
            "l_base": "Confident, bilingual hooks.",
            "boost": "Post‑chorus hook（歌orインスト）＋ダンスブレイク。",
            "logic": "セクション多様化とポストコーラスで映像的ハイライトを設計。",
        },
        "K‑Pop Boy Group Anthem": {
            "p": "Hybrid pop/EDM/rock, 140–160 BPM, big toms, EDM drop.",
            "v_base": "Power belts + rap breaks.",
            "l_base": "Unity/resolve/ambition.",
            "boost": "Build→Drop（anti‑chorus可）＋終盤リフト。",
            "logic": "2段カタルシス構造で拡散性を最適化。",
        },
    },
    "World / Urban Heat": {
        "Afrobeats (Tropical)": {
            "p": "Afrobeats, 100–110 BPM, organic perc, marimba/plucks, warm pads.",
            "v_base": "Soulful relaxed melodic.",
            "l_base": "Groovy repetitive sunny metaphors.",
            "boost": "Syncopated catchy rhythm, lush ad‑libs.",
            "logic": "グローバル・プレイリスト常連の躯体。",
        }
    },
    "Experimental / Anime": {
        "Future Bass (Sparkle)": {
            "p": "Future Bass, 150–165 BPM, super‑saw chords, LFO wobble, vocal chops.",
            "v_base": "Cute high‑pitch, airy style.",
            "l_base": "Digital love, sparkle, hi‑speed phrases.",
            "boost": "Massive wobble drop + vocal climax.",
            "logic": "EDM色強めのサビ爆上げ設計。",
        }
    },
}

# =========================
# 生成ロジック
# =========================
def generate_strategy(cat, genre, v_gender, l_pov, lang_opt, must_have, negative_p, limit, boost_mode, optimizer):
    d = db[cat][genre]

    # 1) Identity
    v_f = f"{v_gender} vocal, {d['v_base']}"
    l_f = f"{l_pov}, {d['l_base']}"

    # 2) 言語構成
    lang_map = {
        "日本語（サビのみ英語可)": "Main Lang: Japanese. Catchy English only in chorus.",
        "日本語（サビのみ英語可）": "Main Lang: Japanese. Catchy English only in chorus.",
        "全日本語": "Language: 100% Japanese.",
        "韓国語（サビのみ英語可)": "Main Lang: Korean. Catchy English only in chorus.",
        "韓国語（サビのみ英語可）": "Main Lang: Korean. Catchy English only in chorus.",
        "全英語": "Language: English."
    }
    l_ins = lang_map.get(lang_opt, "Language: 100% Japanese.")

    # 3) 構造/サビ
    struct = "Short verses, fast transition to chorus. No long intros."
    bst = d["boost"] if boost_mode else ""

    # 4) キーワード制御
    focus_ins = f"Lyrics must include: {must_have}" if must_have else ""
    neg_ins = f"NO (lyrics): {negative_p}" if negative_p else ""

    # 5) Top‑Chart Optimizer
    optimizer_block = ""
    if optimizer:
        optimizer_block = (
            "Hit Optimizer: First chorus ≤ 0:40; hook ≤ 0:15; strong pre-chorus lift → chorus; "
            "Post-chorus hook or drop for second payoff; Mix: high perceived loudness, "
            "moderate-high danceability; Duration ~3:20–3:50."
        )

    # 6) 統合
    full_p = (
        f"{l_ins} {struct} {bst} {focus_ins} Vocal: {v_f} "
        f"POV & Phrasing: {l_f}. {neg_ins} {optimizer_block}"
    ).strip()

    # 文字数上限
    return full_p[:limit], d

# =========================
# サイドバー UI（アイコン増量）
# =========================
with st.sidebar:
    st.markdown('<div class="section-title"><span class="badge">👤</span>IDENTITY & POV</div>', unsafe_allow_html=True)
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary / Neutral"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.markdown('<div class="section-title"><span class="badge">📝</span>LYRICS CONTROL</div>', unsafe_allow_html=True)
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光, 運命のドア")
    negative_p = st.text_input("歌詞除外設定 (Negative)", placeholder="例: 暴力表現, あいまいな一般論")

    st.markdown('<div class="section-title"><span class="badge">⚙️</span>PRODUCTION</div>', unsafe_allow_html=True)
    limit = st.slider("文字数上限", 80, 2000, 420, 10)
    lang_opt = st.selectbox("言語構成", ["日本語（サビのみ英語可）", "全日本語", "韓国語（サビのみ英語可）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost（サビ強化ON）", value=True)
    optimizer = st.toggle("Top‑Chart Optimizer（ヒット傾向注入）", value=True)

    st.markdown('<div class="section-title"><span class="badge">🎛️</span>CATEGORY / GENRE</div>', unsafe_allow_html=True)
    c_col, g_col = st.columns(2)
    with c_col:
        cat = st.selectbox("CATEGORY", list(db.keys()))
    with g_col:
        genre = st.selectbox("GENRE", list(db[cat].keys()))

# =========================
# 実行ボタン
# =========================
run = st.button("⚡ Start / 開始 (Generate)")

# =========================
# 出力
# =========================
if run:
    final_p, d_info = generate_strategy(
        cat=cat, genre=genre, v_gender=v_gender, l_pov=l_pov,
        lang_opt=lang_opt, must_have=must_have, negative_p=negative_p,
        limit=limit, boost_mode=boost_mode, optimizer=optimizer
    )

    st.markdown("### 🧪 生成結果", unsafe_allow_html=True)

    # スタイル・プロンプト（折り返し表示）
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Styleプロンプト（楽曲/ボーカル設定）")
    style_prompt = f"{d_info['p']} {d_info['boost'] if boost_mode else ''} Vocal: {v_gender}. {d_info['v_base']}  NO (lyrics): {negative_p if negative_p else '—'}"
    st.text_area(
        "（折り返し表示）",
        value=style_prompt.strip(),
        height=140,
        key="style_prompt_area"
    )

    # 歌詞プロンプト（折り返し表示・全文が見える）
    st.subheader(f"✍️ 歌詞指示プロンプト（{len(final_p)} / {limit} 文字）")
    st.text_area(
        "（折り返し表示・そのままコピペ可）",
        value=final_p,
        height=260,
        key="lyrics_prompt_area"
    )
    st.download_button("⬇️ プロンプトを保存（.txt）", data=final_p, file_name="hitforge_prompt.txt")

    # ロジック解説（アイコン&金色アクセント）
    st.subheader("🧠 ロジック解説")
    st.markdown(
        f"""
        <div class=\"meta\">
          <span class=\"gold-chip\">構成</span> Short verses → 早期コーラス到達。<br/>
          <span class=\"gold-chip\">サビ</span> {d_info['boost']}<br/>
          <span class=\"gold-chip\">アイデンティティ</span> {v_gender} × {l_pov}（{d_info['v_base']}）<br/>
          <span class=\"gold-chip\">歌詞基調</span> {d_info['l_base']}<br/>
          <span class=\"gold-chip\">背景</span> {d_info['logic']}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.success(f"⚔️ {genre.upper()} – 最強プロンプトの生成が完了しました！")
