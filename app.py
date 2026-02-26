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
    "J-POP (Ballad)": {"bpm": 72, "key": "0 (C)", "energy": 0.45, "mode": "Major",
                       "logic": "ピアノ主体のエモーショナルな構成。"},
    "J-Rock": {"bpm": 165, "key": "2 (D)", "energy": 0.85, "mode": "Minor", "logic": "疾走感のあるバンドサウンド。"},
    "Anime Song": {"bpm": 175, "key": "1 (C#/Db)", "energy": 0.90, "mode": "Major", "logic": "異常な高揚感と情報量。"},
    "Vocaloid Style": {"bpm": 190, "key": "6 (F#/Gb)", "energy": 0.92, "mode": "Minor",
                       "logic": "超高速かつ複雑な転回。"},
    "City Pop": {"bpm": 115, "key": "9 (A)", "energy": 0.65, "mode": "Major7th", "logic": "洗練されたメロウな響き。"},
    "K-Pop (Dance)": {"bpm": 124, "key": "1 (C#/Db)", "energy": 0.82, "mode": "Minor",
                      "logic": "低音重視、ダンスフロア仕様。"},
    "K-Pop (HipHop)": {"bpm": 95, "key": "10 (A#/Bb)", "energy": 0.75, "mode": "Minor",
                       "logic": "重厚なTrapビートが中心。"},
    "Global Viral": {"bpm": 105, "key": "7 (G)", "energy": 0.72, "mode": "Major",
                     "logic": "キャッチーで踊りやすい王道。"},
    "Lo-fi Hip Hop": {"bpm": 85, "key": "5 (F)", "energy": 0.35, "mode": "Minor", "logic": "究極の作業用・リラックス。"},
    "Future Bass": {"bpm": 160, "key": "1 (C#/Db)", "energy": 0.85, "mode": "Major",
                    "logic": "キラキラしたシンセと重低音。"},
    "Trap": {"bpm": 140, "key": "8 (G#/Ab)", "energy": 0.75, "mode": "Minor", "logic": "808ベースが唸る現代の定番。"},
}

KEY_LIST = ["0 (C)", "1 (C#/Db)", "2 (D)", "3 (D#/Eb)", "4 (E)", "5 (F)",
            "6 (F#/Gb)", "7 (G)", "8 (G#/Ab)", "9 (A)", "10 (A#/Bb)", "11 (B)"]

# --- UI Styles (Lux UI) ---
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
      .hero, .card{ background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 1.2rem; margin-bottom: 1rem; }
      .stButton > button{ background: linear-gradient(135deg, #1b1e25 0%, rgba(227,179,65,.95) 100%); color:#0a0b0e; font-weight: 900; border-radius: 12px; }
      .gold-chip{ display:inline-flex; gap:.35rem; align-items:center; background: rgba(227,179,65,.15); border:1px solid rgba(227,179,65,.3); padding:.2rem .6rem; border-radius: 999px; color: var(--gold); font-size:.85rem; font-weight:700; margin-right:5px; }
      pre, code { white-space: pre-wrap !important; word-break: break-word !important; color: #ffffff !important; }
      /* Text items forced white */
      label, p, span, h1, h2, h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================
#  Sidebar UI
# =========================
with st.sidebar:
    st.markdown('<div class="section-title">👤 IDENTITY & POV</div>', unsafe_allow_html=True)
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.markdown('<div class="section-title">📝 LYRICS CONTROL</div>', unsafe_allow_html=True)
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光, 運命のドア")

    # 文字数制限の改善：数値入力とスライダーを連動
    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        limit_slider = st.slider("文字数上限", 80, 2000, 420, 10)
    with col_l2:
        limit = st.number_input("数値入力", 80, 2000, value=limit_slider)

    st.markdown('<div class="section-title">🎛️ DNA PRESET</div>', unsafe_allow_html=True)
    genre_key = st.selectbox("GENRE (Hit-DNA)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    # マニュアル調整トグル
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
#  Generation Logic
# =========================
if st.button("⚡ Start / 開始 (Generate DNA Prompt)"):
    # プロンプト構築
    optimizer_block = ""
    if optimizer:
        optimizer_block = "Hit Optimizer: First chorus ≤ 0:40; hook ≤ 0:15; high perceived loudness; Duration 3:20-3:50."

    final_prompt = (
        f"Language: {lang_opt}. Genre: {genre_key}. BPM: {target_bpm}. Key: {target_key}. "
        f"Energy Level: {dna['energy']}. Mode: {dna['mode']}. "
        f"Vocal: {v_gender}. POV: {l_pov}. Must include: {must_have}. "
        f"{'Anthemic Boost ON: Soaring chorus lift.' if boost_mode else ''} "
        f"{optimizer_block}"
    ).strip()

    # 表示
    st.markdown("### 🧪 生成結果")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎨 DNA-Synced Style & Lyrics Prompt")
    st.text_area("そのままコピペ可", value=final_prompt[:limit], height=300)

    st.subheader("🧠 ロジック解説 (Selected DNA)")
    st.markdown(f"""
        <div style="margin-top:10px;">
            <span class="gold-chip">BPM</span> {target_bpm}<br/>
            <span class="gold-chip">Key</span> {target_key}<br/>
            <span class="gold-chip">Energy</span> {dna['energy']}<br/>
            <span class="gold-chip">Logic</span> {dna['logic']}
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success(f"⚔️ {genre_key} の黄金比に基づいたプロンプトが完成しました！")