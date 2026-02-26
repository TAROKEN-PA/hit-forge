# -*- coding: utf-8 -*-
import streamlit as st

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================
#  HitForge Master DNA Data (静的データ)
# =========================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": "1 (C#/Db)", "energy": 0.78, "logic": "現代の王道。"},
    "J-POP (Ballad)": {"bpm": 72, "key": "0 (C)", "energy": 0.45, "logic": "ピアノ主体のエモーショナル。"},
    "J-Rock": {"bpm": 165, "key": "2 (D)", "energy": 0.85, "logic": "疾走感。"},
    "Anime Song": {"bpm": 175, "key": "1 (C#/Db)", "energy": 0.90, "logic": "高揚感。"},
    "Vocaloid Style": {"bpm": 190, "key": "6 (F#/Gb)", "energy": 0.92, "logic": "複雑な転回。"},
    "City Pop": {"bpm": 115, "key": "9 (A)", "energy": 0.65, "logic": "洗練されたメロウ。"},
    "K-Pop (Dance)": {"bpm": 124, "key": "1 (C#/Db)", "energy": 0.82, "logic": "低音重視。"},
    "K-Pop (HipHop)": {"bpm": 95, "key": "10 (A#/Bb)", "energy": 0.75, "logic": "重厚Trap。"},
    "Global Viral": {"bpm": 105, "key": "7 (G)", "energy": 0.72, "logic": "王道Viral。"},
    "Lo-fi Hip Hop": {"bpm": 85, "key": "5 (F)", "energy": 0.35, "logic": "究極Chill。"},
    "Future Bass": {"bpm": 160, "key": "1 (C#/Db)", "energy": 0.85, "logic": "シンセ/重低音。"},
    "Trap": {"bpm": 140, "key": "8 (G#/Ab)", "energy": 0.75, "logic": "808ベース。"},
}

KEY_LIST = ["0 (C)", "1 (C#/Db)", "2 (D)", "3 (D#/Eb)", "4 (E)", "5 (F)",
            "6 (F#/Gb)", "7 (G)", "8 (G#/Ab)", "9 (A)", "10 (A#/Bb)", "11 (B)"]

# =========================
#  Lux UI Style (色化け修正)
# =========================
st.markdown(
    """
    <style>
      :root {
        --bg: #0a0b0e; --panel: #101217; --card: #111418; --border: #1d212a;
        --text: #ffffff; --muted: #ffffffcc; --gold: #e3b341;
      }
      html, body, [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
      .app-title h1 { font-size: 2.6rem; font-weight: 900; color: var(--text); margin: 0; }
      .gold-underline { display:inline-block; height:6px; width:160px; border-radius:6px; background: linear-gradient(90deg, var(--gold), #f1c84c); margin-bottom: 20px; }
      .card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }

      /* ▼入力フォームの色修正（背景色と文字色のコントラストを確保）▼ */
      input, select, textarea, [data-baseweb="select"] { background-color: #1d212a !important; color: white !important; }
      label, p, span { color: #ffffff !important; font-weight: 500; }
      div[data-baseweb="select"] > div { background-color: #1d212a !important; color: white !important; border: 1px solid #e3b34166 !important; }
      .stNumberInput input { background-color: #1d212a !important; color: white !important; }

      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, rgba(227,179,65,1) 100%); color:#000; font-weight: 900; border-radius: 12px; width:100%; border:none; height: 3rem; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.2); border:1px solid var(--gold); padding:2px 10px; border-radius: 20px; color: var(--gold); font-size:0.8rem; margin-right:5px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================
#  Sidebar (Input Logic)
# =========================
with st.sidebar:
    st.header("👤 IDENTITY")
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.header("📝 LYRICS & DNA")
    must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
    negative_p = st.text_input("NGワード", placeholder="例: 卒業, 桜")

    # プロンプト文字数制限（スライダーと数値入力を同期）
    st.write("プロンプト文字数制限")
    c1, c2 = st.columns([2, 1])
    with c1:
        limit_sl = st.slider("Slider", 80, 2000, 1000, 10, label_visibility="collapsed")
    with c2:
        limit = st.number_input("Value", 80, 2000, value=limit_sl, label_visibility="collapsed")

    st.header("🎛️ DNA PRESET")
    genre_key = st.selectbox("GENRE (Preset)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    # 手動設定
    manual_on = st.toggle("🔧 Manual Overide (手動調整)")
    if manual_on:
        t_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        t_key = st.selectbox("KEY", KEY_LIST, index=KEY_LIST.index(dna["key"]))
    else:
        t_bpm = dna["bpm"]
        t_key = dna["key"]

    lang_opt = st.selectbox("言語", ["日本語（サビ英語）", "全日本語", "韓国語", "全英語"])
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================
#  Original Prompt Logic (添付ファイル再現)
# =========================
if st.button("⚡ Generate Production Prompt"):

    # --- 1. 作曲(Style)プロンプトの構築 (元の楽器指示・タイミングを維持) ---
    # 元のファイルにあった get_dna_info 相当の楽器指示をジャンル別に再現
    inst_logic = "Modern J-POP arrangement, rich layers, hybrid synths."
    if "Ballad" in genre_key:
        inst_logic = "Grand piano, emotional strings, delicate percussion."
    elif "Rock" in genre_key:
        inst_logic = "Overdriven electric guitars, energetic real drums, driving bass."
    elif "City Pop" in genre_key:
        inst_logic = "Fretless bass, funky Rhodes, vintage 80s DX7 synths."
    elif "Lo-fi" in genre_key:
        inst_logic = "Vinyl crackle, sampled Rhodes, relaxed boombap drums."

    opt_logic = ""
    if optimizer:
        opt_logic = "Structure: Intro <15s, 1st Chorus <45s. High perceived loudness. High production value."

    style_prompt = (
        f"Genre: {genre_key}. BPM: {t_bpm}. Key: {t_key}. Energy: {dna['energy']}. "
        f"{inst_logic} Vocal: {v_gender}. "
        f"{'Boost: Anthemic soaring chorus.' if boost_mode else ''} {opt_logic} "
        f"NO: {negative_p if negative_p else 'none'}."
    )

    # --- 2. 作詞(Lyrics)プロンプトの構築 (元の構成・制約を維持) ---
    lyrics_main = (
        f"Task: Write professional lyrics. Genre: {genre_key}. Lang: {lang_opt}. POV: {l_pov}. "
        f"Theme: {must_have}. NOT use: {negative_p}. "
        f"Structure: [Intro] [Verse 1] [Pre-Chorus] [Chorus] [Verse 2] [Chorus] [Bridge] [Chorus] [Outro]. "
        f"Focus: Emotional depth and catchy rhymes."
    )

    # 「プロンプトの文字数制限」を適用
    style_final = style_prompt[:limit]
    lyrics_final = lyrics_main[:limit]

    # =========================
    #  Display Results
    # =========================
    st.markdown("### 🧪 生成結果")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎨 Style / Composition Prompt (作曲指示)")
    st.text_area("Copy for AI Music Tools", value=style_final, height=150)

    st.subheader("✍️ Lyrics Prompt (作詞指示)")
    st.text_area("Copy for AI Lyrics Tools", value=lyrics_final, height=200)

    # ダウンロード
    all_p = f"【STYLE】\n{style_final}\n\n【LYRICS】\n{lyrics_final}"
    st.download_button("⬇️ プロンプトを保存", data=all_p, file_name="hitforge_production.txt")

    # ロジック表示
    st.subheader("🧠 DNA Logic Check")
    st.markdown(f"""
        <div style="margin-top:10px;">
            <span class="gold-chip">BPM: {t_bpm}</span>
            <span class="gold-chip">KEY: {t_key}</span>
            <span class="gold-chip">ENERGY: {dna['energy']}</span><br/><br/>
            <p style='color:#e3b341'>Logic: {dna['logic']} / {inst_logic}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)