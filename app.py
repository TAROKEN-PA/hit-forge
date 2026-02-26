# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================================================
#  Master Data
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
                   "p": "Hyper-melodic, orchestral mixed with synths.",
                   "v_base": "Complex structure, frequent modulations."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths, fast piano arpeggios, glitch effects.",
                       "v_base": "Lightning-fast articulation."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass.",
                 "p": "Fretless bass, funky Rhodes, vintage 80s DX7.", "v_base": "Mellow vibes, jazz-pop fusion."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンスフロア。",
                      "p": "Heavy sub-bass, experimental lead synths.",
                      "v_base": "Powerful drop, varied vocal textures."},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。",
                       "p": "Heavy 808s, rhythmic vocal chops.", "v_base": "Trap-influenced sections."},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。",
                     "p": "Catchy pluck leads, organic percussion.", "v_base": "Loop-friendly, high memorability."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes。",
                      "p": "Chill Rhodes, dusty vinyl, boom-bap drums.", "v_base": "Relaxed atmosphere."},
}

KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

LYRIC_FLAVORS = {
    "王道チャート": "Standard catchy phrasing.",
    "詩的・比喩的": "Highly metaphorical, abstract, and poetic imagery.",
    "映画的描写": "Visual storytelling, descriptive scenes.",
    "ストレート/感情剥き出し": "Conversational, direct, emotional, and raw.",
    "哲学的・ダーク": "Philosophical and melancholic."
}

# =========================================================
#  Lux UI Style
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"] { background-color: #101217 !important; border-right: 1px solid #1d212a !important; }
      input, select, textarea, div[data-baseweb="select"] { background-color: #1d212a !important; color: #ffffff !important; border: 1px solid #333 !important; }
      label, p, span, h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
      .app-title h1 { font-size: 2.2rem; font-weight: 900; margin: 0; }
      .gold-underline { display:inline-block; height:4px; width:120px; border-radius:6px; background: linear-gradient(90deg, #e3b341, #f1c84c); margin-bottom: 20px; }
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.2rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; border:none; width:100%; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.15); border:1px solid #e3b341; padding:2px 10px; border-radius: 20px; color: #e3b341 !important; font-size:0.75rem; margin-right:5px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================================================
#  Sidebar (双方向連動ロジック修正)
# =========================================================
with st.sidebar:
    st.header("👤 IDENTITY")
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1, horizontal=True)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2, horizontal=True)

    st.header("📝 PRODUCTION")
    must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
    negative_p = st.text_input("NGワード", placeholder="例: 桜")

    # --- エラー回避用の双方向連動ロジック ---
    st.write("プロンプト文字数制限")
    if "p_limit" not in st.session_state:
        st.session_state.p_limit = 1500


    # 1. 数値入力が変更されたときの処理
    def on_num_change():
        st.session_state.p_limit = st.session_state.num_val


    # 2. スライダーが変更されたときの処理
    def on_sld_change():
        st.session_state.p_limit = st.session_state.sld_val


    limit_val = st.number_input("数値入力", 80, 2500, value=st.session_state.p_limit, key="num_val",
                                on_change=on_num_change, label_visibility="collapsed")
    limit_sld = st.slider("スライダー調整", 80, 2500, value=st.session_state.p_limit, key="sld_val",
                          on_change=on_sld_change, label_visibility="collapsed")

    st.header("🎛️ DNA PRESET")
    genre_key = st.selectbox("GENRE (Preset)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    st.header("🎨 CREATIVE")
    flavor = st.selectbox("Lyricフレーバー (日本語)", list(LYRIC_FLAVORS.keys()))
    lang_opt = st.radio("言語構成", ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（英語混）", "全英語"],
                        horizontal=False)

    manual_on = st.toggle("🔧 手動Override (BPM/Key)")
    if manual_on:
        t_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        t_key = st.selectbox("KEY", KEY_NAMES, index=dna['key'])
    else:
        t_bpm = dna["bpm"];
        t_key = dna["key_name"]

    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================================================
#  Generation
# =========================================================
if st.button("⚡ プロンプトを生成する"):
    compact_struct = "In-V1-PC-C-V2-C-B-C-Out"
    opt_logic = "Intro<15s,1st Chorus<45s.High energy peak." if optimizer else ""

    style_raw = (
        f"Genre:{genre_key}.BPM:{t_bpm}.Key:{t_key}.Energy:{dna['energy']}.Inst:{dna['p']}Vocal:{v_gender}.{'Anthemic boost.' if boost_mode else ''}{opt_logic}{dna['v_base']}Avoid:{negative_p if negative_p else 'none'}.").replace(
        "  ", " ").strip()
    lyrics_raw = (
        f"Lyrics:{genre_key}.Lang:{lang_opt}.POV:{l_pov}.Flavor:{LYRIC_FLAVORS[flavor]}.Theme:{must_have}.Exclude:{negative_p if negative_p else 'none'}.Struct:{compact_struct}.Guide:Sensory details,emotional arc,rhythmic flow with {t_bpm}BPM.Avoid clichés.").replace(
        "  ", " ").strip()

    # セッション状態の値を参照して制限
    current_limit = st.session_state.p_limit
    style_final = style_raw[:current_limit]
    lyrics_final = lyrics_raw[:current_limit]

    st.markdown("### 🧪 生成結果 (DNA-Synced)")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎨 Style Prompt")
    st.text_area("作曲指示", value=style_final, height=140, key="st_ta")
    st.button("📋 Copy Style",
              on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{style_final}")</script>',
                                        unsafe_allow_html=True), key="btn_st")

    st.subheader("✍️ Lyrics Prompt")
    st.text_area("作詞指示", value=lyrics_final, height=200, key="ly_ta")
    st.button("📋 Copy Lyrics",
              on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{lyrics_final}")</script>',
                                        unsafe_allow_html=True), key="btn_ly")

    st.markdown(f"""
        <div style="margin-top:20px;">
            <span class="gold-chip">BPM: {t_bpm}</span><span class="gold-chip">KEY: {t_key}</span>
            <span class="gold-chip">FLAVOR: {flavor}</span>
            <p style='color:#e3b341; margin-top:10px; font-size:0.85rem;'><b>DNA:</b> {dna['logic']}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)