# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================================================
#  HitForge Master DNA (元のロジックを完全継承)
# =========================================================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。",
                           "p": "Modern J-POP production, rich layers, hybrid synths.",
                           "v_base": "First Hook <40s. High production value."},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。",
                       "p": "Grand Piano, emotional strings, delicate live percussion.",
                       "v_base": "Slow build, emotional peak at chorus."},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars/Energetic drums.",
               "p": "Driving electric guitars, energetic bass, real acoustic drums.",
               "v_base": "High energy, aggressive mix."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調の多用。",
                   "p": "Hyper-melodic, fast-paced, orchestral elements mixed with synths.",
                   "v_base": "Complex structure, frequent modulations."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths, fast piano arpeggios, glitch effects.",
                       "v_base": "Lightning-fast articulation, robotic precision."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass.",
                 "p": "Fretless bass, funky Rhodes, vintage 80s DX7 synth pads, clean electric guitar.",
                 "v_base": "Mellow vibes, sophisticated jazz-pop fusion."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンスフロア。",
                      "p": "Heavy sub-bass, experimental sound design, sharp lead synths.",
                      "v_base": "Powerful drop, varied vocal textures."},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。",
                       "p": "Heavy 808s, rhythmic vocal chops, dark atmospheric pads.",
                       "v_base": "Trap-influenced, aggressive rap sections."},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。",
                     "p": "Catchy pluck leads, simple but effective bass, organic percussion.",
                     "v_base": "Loop-friendly, high memorability."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes.",
                      "p": "Chill Rhodes, dusty vinyl crackle, boom-bap drums, sampled aesthetic.",
                      "v_base": "Relaxed atmosphere, nostalgic mood."},
}

KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {
    "Standard": "Standard catchy phrasing.",
    "Poetic": "Highly metaphorical, abstract, and poetic imagery.",
    "Cinematic": "Visual storytelling, descriptive scenes.",
    "Street/Raw": "Conversational, direct, emotional, and raw.",
    "Deep/Dark": "Philosophical and melancholic."
}

# =========================================================
#  Lux UI Style (色化け対策済み)
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"] { background-color: #101217 !important; border-right: 1px solid #1d212a !important; }
      input, select, textarea, div[data-baseweb="select"] { background-color: #1d212a !important; color: #ffffff !important; border: 1px solid #333 !important; }
      label, p, span, h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
      .app-title h1 { font-size: 2.6rem; font-weight: 900; margin: 0; }
      .gold-underline { display:inline-block; height:6px; width:160px; border-radius:6px; background: linear-gradient(90deg, #e3b341, #f1c84c); margin-bottom: 20px; }
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; width:100%; height: 3.2rem; border:none; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.15); border:1px solid #e3b341; padding:2px 10px; border-radius: 20px; color: #e3b341 !important; font-size:0.8rem; margin-right:5px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================================================
#  Sidebar (双方向連動ロジック)
# =========================================================
with st.sidebar:
    st.header("👤 IDENTITY")
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.header("📝 PRODUCTION")
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光")
    negative_p = st.text_input("NGワード", placeholder="例: 卒業, 桜")

    # --- スライダーとBOXの数値連動設定 ---
    st.write("プロンプト文字数制限")
    if "prompt_limit" not in st.session_state:
        st.session_state.prompt_limit = 1500


    def update_slider():
        st.session_state.prompt_limit = st.session_state.num_input


    def update_num():
        st.session_state.prompt_limit = st.session_state.slider_input


    c1, c2 = st.columns([2, 1])
    with c1:
        limit = st.slider("Slider", 80, 2500, key="slider_input", on_change=update_num,
                          value=st.session_state.prompt_limit, label_visibility="collapsed")
    with c2:
        limit = st.number_input("Value", 80, 2500, key="num_input", on_change=update_slider,
                                value=st.session_state.prompt_limit, label_visibility="collapsed")

    st.header("🎛️ DNA PRESET")
    genre_key = st.selectbox("GENRE (Preset)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    if st.button("📊 Show DNA Histogram"):
        st.markdown(f"**DNA: {genre_key}**")
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)))
        key_dist = [0.1] * 12;
        key_dist[dna['key']] = 0.9
        st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES))

    manual_on = st.toggle("🔧 Manual Override")
    if manual_on:
        t_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        t_key = st.selectbox("KEY", KEY_NAMES, index=dna['key'])
    else:
        t_bpm = dna["bpm"];
        t_key = dna["key_name"]

    st.header("🎨 CREATIVE")
    flavor = st.selectbox("Lyric Flavor", list(LYRIC_FLAVORS.keys()))
    lang_opt = st.selectbox("言語構成",
                            ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================================================
#  Logic & Result
# =========================================================
if st.button("⚡ Generate Hit-DNA Production Prompt"):
    compact_struct = "In-V1-PC-C-V2-C-B-C-Out"
    opt_logic = "Intro<15s,1st Chorus<45s.High loudness,peak energy at chorus." if optimizer else ""

    style_raw = (
        f"Genre:{genre_key}.BPM:{t_bpm}.Key:{t_key}.Energy:{dna['energy']}.Inst:{dna['p']}Vocal:{v_gender}.{'Anthemic soaring chorus boost.' if boost_mode else ''}{opt_logic}{dna['v_base']}Avoid:{negative_p if negative_p else 'none'}.").replace(
        "  ", " ").strip()
    lyrics_raw = (
        f"Lyrics:{genre_key}.Lang:{lang_opt}.POV:{l_pov}.Flavor:{LYRIC_FLAVORS[flavor]}.Theme:{must_have}.Exclude:{negative_p if negative_p else 'none'}.Struct:{compact_struct}.Guide:Sensory details,emotional arc,rhythmic flow with {t_bpm}BPM.Avoid clichés.").replace(
        "  ", " ").strip()

    # 制限文字数でカット
    style_final = style_raw[:st.session_state.prompt_limit]
    lyrics_final = lyrics_raw[:st.session_state.prompt_limit]

    st.markdown("### 🧪 生成結果 (DNA-Synced)")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎨 Style / Composition Prompt")
    st.text_area("作曲指示", value=style_final, height=140, key="st_ta")
    st.button("📋 Copy Style Prompt",
              on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{style_final}")</script>',
                                        unsafe_allow_html=True), key="copy_st")

    st.write("---")

    st.subheader("✍️ Lyrics Prompt")
    st.text_area("作詞指示", value=lyrics_final, height=200, key="ly_ta")
    st.button("📋 Copy Lyrics Prompt",
              on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{lyrics_final}")</script>',
                                        unsafe_allow_html=True), key="copy_ly")

    st.markdown(f"""
        <div style="margin-top:20px;">
            <span class="gold-chip">BPM: {t_bpm}</span><span class="gold-chip">KEY: {t_key}</span>
            <span class="gold-chip">ENERGY: {dna['energy']}</span><span class="gold-chip">FLAVOR: {flavor}</span>
            <p style='color:#e3b341; margin-top:15px; font-size:0.9rem;'><b>DNA Logic:</b> {dna['logic']}<br/><b>Optimized Structure:</b> {compact_struct}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)