# -*- coding: utf-8 -*-
import streamlit as st

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================
#  HitForge Master DNA Data
# =========================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": "1 (C#/Db)", "energy": 0.78, "mode": "Major",
                           "logic": "現代の王道ヒットチャート。"},
    "J-POP (Ballad)": {"bpm": 72, "key": "0 (C)", "energy": 0.45, "mode": "Major", "logic": "ピアノ主体の構成。"},
    "J-Rock": {"bpm": 165, "key": "2 (D)", "energy": 0.85, "mode": "Minor", "logic": "疾走感のあるバンドサウンド。"},
    "Anime Song": {"bpm": 175, "key": "1 (C#/Db)", "energy": 0.90, "mode": "Major", "logic": "高揚感と情報量重視。"},
    "Vocaloid Style": {"bpm": 190, "key": "6 (F#/Gb)", "energy": 0.92, "mode": "Minor",
                       "logic": "超高速かつ複雑な転回。"},
    "City Pop": {"bpm": 115, "key": "9 (A)", "energy": 0.65, "mode": "Major7th", "logic": "洗練されたメロウな響き。"},
    "K-Pop (Dance)": {"bpm": 124, "key": "1 (C#/Db)", "energy": 0.82, "mode": "Minor",
                      "logic": "低音重視ダンスフロア仕様。"},
    "K-Pop (HipHop)": {"bpm": 95, "key": "10 (A#/Bb)", "energy": 0.75, "mode": "Minor", "logic": "重厚なTrapビート。"},
    "Global Viral": {"bpm": 105, "key": "7 (G)", "energy": 0.72, "mode": "Major",
                     "logic": "キャッチーで踊りやすい王道。"},
    "Lo-fi Hip Hop": {"bpm": 85, "key": "5 (F)", "energy": 0.35, "mode": "Minor", "logic": "究極の作業用BGM。"},
    "Future Bass": {"bpm": 160, "key": "1 (C#/Db)", "energy": 0.85, "mode": "Major", "logic": "シンセと重低音。"},
    "Trap": {"bpm": 140, "key": "8 (G#/Ab)", "energy": 0.75, "mode": "Minor", "logic": "808ベースの現代定番。"},
}

KEY_LIST = ["0 (C)", "1 (C#/Db)", "2 (D)", "3 (D#/Eb)", "4 (E)", "5 (F)",
            "6 (F#/Gb)", "7 (G)", "8 (G#/Ab)", "9 (A)", "10 (A#/Bb)", "11 (B)"]

# --- UI Styles (Lux UI + Visual Fixes) ---
st.markdown(
    """
    <style>
      :root{
        --bg: #0a0b0e; --panel: #101217; --card: #111418; --border: #1d212a;
        --text: #ffffff; --muted: #ffffffcc; --gold: #e3b341; --gold-strong: #f1c84c;
      }
      html, body, .block-container, .stApp { background: var(--bg); color: var(--text); }
      .app-title h1{ font-size: 2.6rem; font-weight: 900; color: var(--text); margin-bottom: .8rem; }
      .gold-underline{ display:inline-block; height:6px; width:160px; border-radius:6px; background: linear-gradient(90deg, var(--gold), var(--gold-strong)); }
      .card{ background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 1.2rem; margin-bottom: 1rem; }
      .stButton > button{ background: linear-gradient(135deg, #1b1e25 0%, rgba(227,179,65,.95) 100%); color:#0a0b0e; font-weight: 900; border-radius: 12px; border:none; width:100%; }
      .gold-chip{ display:inline-flex; gap:.35rem; align-items:center; background: rgba(227,179,65,0.15); border:1px solid rgba(227,179,65,0.3); padding:0.2rem 0.6rem; border-radius: 999px; color: var(--gold); font-size:0.85rem; font-weight:700; margin-right:5px; }
      pre, code, textarea { color: #ffffff !important; }
      /* 見にくい入力項目の色を強制修正 */
      label, p, span, h1, h2, h3, div[data-baseweb="select"] span, input { color: #ffffff !important; }
      .stNumberInput input, .stSelectbox div { background-color: #1d212a !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================
#  Sidebar UI (Inputs)
# =========================
with st.sidebar:
    st.markdown('### 👤 IDENTITY & POV')
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.markdown('### 📝 LYRICS CONTROL')
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光, 運命のドア")
    negative_p = st.text_input("ネガティブプロンプト", placeholder="例: 卒業, 桜 (避けるべき単語)")

    # 文字数制限の連動改善
    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        limit_slider = st.slider("文字数上限", 80, 2000, 420, 10)
    with col_l2:
        limit = st.number_input("数値入力", 80, 2000, value=limit_slider)

    st.markdown('### 🎛️ DNA PRESET')
    genre_key = st.selectbox("GENRE (Hit-DNA)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    manual_override = st.toggle("🔧 Manual Override (手動調整)")
    if manual_override:
        target_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        target_key = st.selectbox("KEY", KEY_LIST, index=KEY_LIST.index(dna["key"]))
    else:
        target_bpm = dna["bpm"]
        target_key = dna["key"]

    lang_opt = st.selectbox("言語構成", ["日本語（サビのみ英語可）", "全日本語", "韓国語（サビのみ英語可）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================
#  Original Logic Restoration
# =========================
if st.button("⚡ Start / 開始 (Generate Hit-DNA Prompt)"):
    # 作曲プロンプト生成 (元の構造を維持)
    opt_text = "Optimizer ON: Intro <15s, First Hook <40s." if optimizer else ""
    style_prompt = (
        f"Genre: {genre_key}. BPM: {target_bpm}. Key: {target_key}. "
        f"Energy: {dna['energy']}. Mode: {dna['mode']}. Vocal: {v_gender}. "
        f"{'Anthemic Lift ON.' if boost_mode else ''} {opt_text}"
    )

    # 作詞プロンプト生成 (元の厳格な制約を維持)
    lyrics_prompt = (
        f"Write lyrics for a {genre_key} song. Language: {lang_opt}. "
        f"POV: {l_pov}. Theme/Keywords: {must_have}. "
        f"Constraint: Must NOT use these words: {negative_p}. "
        f"Length: Strictly under {limit} characters. "
        f"Structure: [Intro] -> [Verse 1] -> [Pre-Chorus] -> [Chorus] -> [Verse 2] -> [Chorus] -> [Bridge] -> [Outro]."
    )

    # --- Result Display ---
    st.markdown("### 🧪 生成結果 (DNA-Synced)")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # 作曲セクション
    st.subheader("🎨 Style / Composition Prompt")
    st.text_area("作曲指示", value=style_prompt, height=100)

    # 作詞セクション
    st.subheader(f"✍️ Lyrics Prompt (Limit: {limit})")
    st.text_area("作詞指示", value=lyrics_prompt, height=200)

    st.download_button("⬇️ プロンプトを保存", data=f"STYLE:\n{style_prompt}\n\nLYRICS:\n{lyrics_prompt}",
                       file_name="hitforge_dna.txt")

    # ロジック解説
    st.subheader("🧠 ロジック解説 (Selected DNA)")
    st.markdown(f"""
        <div style="margin-top:10px;">
            <span class="gold-chip">BPM</span> {target_bpm}
            <span class="gold-chip">Key</span> {target_key}
            <span class="gold-chip">Energy</span> {dna['energy']}
            <span class="gold-chip">Logic</span> {dna['logic']}
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("⚔️ 黄金比を反映したプロンプトを正常に生成しました！")