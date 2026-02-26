# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================================================
#  1. Master DNA Data (すべてのロジックをここに濃縮)
# =========================================================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。", "p": "Modern J-POP production, rich layers.",
                           "v_base": "First Hook <40s."},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。",
                       "p": "Grand Piano, emotional strings.", "v_base": "Slow build."},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars.",
               "p": "Driving electric guitars, real drums.", "v_base": "High energy."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調の多用。",
                   "p": "Hyper-melodic, orchestral mixed synths.", "v_base": "Complex structure."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths, glitch effects.", "v_base": "Lightning-fast."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths.",
                 "p": "Fretless bass, funky Rhodes.", "v_base": "Mellow vibes."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes。",
                      "p": "Chill Rhodes, dusty vinyl.", "v_base": "Relaxed."},
}

KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {
    "王道チャート": "Standard catchy phrasing.",
    "詩的・比喩的": "Highly metaphorical imagery.",
    "映画的描写": "Visual storytelling.",
    "ストレート": "Conversational and raw.",
    "哲学的・ダーク": "Philosophical and melancholic."
}

# =========================================================
#  2. Lux UI Style (色化け・キーボード対策)
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"] { background-color: #101217 !important; border-right: 1px solid #1d212a !important; }
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.5rem; border:none; width:100%; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.15); border:1px solid #e3b341; padding:2px 10px; border-radius: 20px; color: #e3b341 !important; font-size:0.8rem; margin-right:5px; }
      /* ポップアップ(Popover)内の文字色修正 */
      div[data-testid="stPopoverBody"] { background-color: #1d212a !important; color: white !important; border: 1px solid #e3b341; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    '<h1 style="color:#e3b341; margin-bottom:0;">🎼 HitForge</h1><div style="height:6px; width:150px; background:linear-gradient(90deg, #e3b341, #f1c84c); border-radius:6px; margin-bottom:20px;"></div>',
    unsafe_allow_html=True)

# =========================================================
#  3. Sidebar (ボタン集約 & 文字数シンクロ復活)
# =========================================================
with st.sidebar:
    st.header("👤 IDENTITY")
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1, horizontal=True)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2, horizontal=True)

    st.header("📝 PRODUCTION")
    must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")

    # 文字数シンクロ復活
    if "p_limit" not in st.session_state: st.session_state.p_limit = 1500


    def sync_n(): st.session_state.p_limit = st.session_state.n_in


    def sync_s(): st.session_state.p_limit = st.session_state.s_in


    st.write("プロンプト文字数制限")
    l_num = st.number_input("Value", 80, 2500, key="n_in", on_change=sync_n, value=st.session_state.p_limit,
                            label_visibility="collapsed")
    l_sld = st.slider("Slider", 80, 2500, key="s_in", on_change=sync_s, value=st.session_state.p_limit,
                      label_visibility="collapsed")

    st.header("🎛️ CONFIG (Popups)")
    # --- ジャンル選択ポップアップ ---
    with st.popover("🎹 ジャンルを選択"):
        genre_key = st.radio("DNA Genre", list(DNA_MASTER.keys()), index=0)
        dna = DNA_MASTER[genre_key]
        st.info(f"Logic: {dna['logic']}")

    # --- フレーバー＆言語ポップアップ ---
    with st.popover("🎨 表現・言語設定"):
        flavor = st.radio("Lyricフレーバー", list(LYRIC_FLAVORS.keys()), index=0)
        lang_opt = st.radio("言語構成", ["日本語/英語混", "全日本語", "全英語"], index=0)

    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Chart Optimizer", value=True)

# =========================================================
#  4. Main Content (DNAグラフ復活)
# =========================================================
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown(f"### 📊 DNA Stats: {genre_key}")
    bpm_bins = np.linspace(60, 200, 15)
    bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
    st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=200)

with c2:
    st.markdown("### 🎹 Key Popularity")
    key_dist = [0.1] * 12;
    key_dist[dna['key']] = 0.9
    st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES), height=200)

if st.button("⚡ GENERATE PROMPT"):
    compact_struct = "In-V1-PC-C-V2-C-B-C-Out"
    opt_logic = "Intro<15s,1st Chorus<45s.High energy peak." if optimizer else ""

    # 元の複雑な指示をすべて復元して結合
    style_raw = (
        f"Genre:{genre_key}.BPM:{dna['bpm']}.Key:{dna['key_name']}.Energy:{dna['energy']}.Inst:{dna['p']}Vocal:{v_gender}.{'Anthemic boost.' if boost_mode else ''}{opt_logic}{dna['v_base']}").replace(
        "  ", " ").strip()
    lyrics_raw = (
        f"Lyrics:{genre_key}.Lang:{lang_opt}.POV:{l_pov}.Flavor:{LYRIC_FLAVORS[flavor]}.Theme:{must_have}.Struct:{compact_struct}.Guide:Sensory details,emotional arc,rhythmic flow with {dna['bpm']}BPM.Avoid clichés.").replace(
        "  ", " ").strip()

    s_final = style_raw[:st.session_state.p_limit]
    l_final = lyrics_raw[:st.session_state.p_limit]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style Prompt")
    st.text_area("Style", s_final, height=120, label_visibility="collapsed")
    st.button("📋 Copy Style", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{s_final}")</script>',
                                                        unsafe_allow_html=True), key="cp_s")

    st.subheader("✍️ Lyrics Prompt")
    st.text_area("Lyrics", l_final, height=180, label_visibility="collapsed")
    st.button("📋 Copy Lyrics", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{l_final}")</script>',
                                                         unsafe_allow_html=True), key="cp_l")
    st.markdown('</div>', unsafe_allow_html=True)
    st.success(f"DNA Mixed: {genre_key} x {flavor}")