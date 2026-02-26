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
    "J-POP (Main)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78,
                     "logic": "現代の王道ヒット。BPM140超の疾走感。"},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。"},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Energetic drums."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調。"},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths."},
    "Lo-fi": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle."},
}

KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

# フレーバー
LYRIC_FLAVORS = {
    "王道チャート": "Standard catchy phrasing.",
    "詩的・比喩的": "Highly metaphorical imagery.",
    "映画的描写": "Visual storytelling.",
    "ストレート": "Conversational and raw.",
    "ダーク": "Philosophical and melancholic."
}

# =========================================================
#  UI Style (モバイルでの視認性を極限まで高める)
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"] { background-color: #101217 !important; }
      /* ラジオボタンを大きなボタン風にする(キーボード回避策) */
      div[data-testid="stWidgetLabel"] p { font-size: 1rem !important; font-weight: 700 !important; color: #e3b341 !important; }
      .stRadio div[role="radiogroup"] { gap: 10px; }
      /* UIカード */
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.2rem; margin-bottom: 1rem; }
      /* コピーボタン */
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    '<h1 style="color:#e3b341; margin-bottom:0;">🎼 HitForge</h1><div style="height:4px; width:100px; background:#e3b341; margin-bottom:20px;"></div>',
    unsafe_allow_html=True)

# =========================================================
#  Sidebar: キーボードを一切出さない「タップ専用」UI
# =========================================================
with st.sidebar:
    st.header("👤 IDENTITY")
    # キーボードが出る text_input を廃止または最小限に。
    # 代わりにキーワードを「選択」にするか、不要なら消すことも検討できますが、
    # 一旦、文字数制限のみにフォーカスして解決します。

    st.header("📝 PRODUCTION")

    # --- 同期問題の完全解決 ---
    # 同期に悩むより「スライダー1本化」し、その数値を大きく表示する
    st.markdown("### プロンプト文字数制限")
    if "p_limit" not in st.session_state:
        st.session_state.p_limit = 1500

    # スライダーのみを使い、その上に数値を表示。これならキーボードは絶対出ません。
    limit = st.slider("調整", 80, 2500, key="p_limit", label_visibility="collapsed")
    st.markdown(f"<h2 style='text-align:center; color:#e3b341;'>{limit} chars</h2>", unsafe_allow_html=True)

    st.header("🎛️ DNA PRESET")
    # selectboxは環境によりキーボードが出るため、Radioを検討（数が多い場合はスクロール）
    genre_key = st.radio("GENRE", list(DNA_MASTER.keys()), index=0)
    dna = DNA_MASTER[genre_key]

    st.header("🎨 CREATIVE")
    flavor_key = st.radio("LYRIC FLAVOR", list(LYRIC_FLAVORS.keys()), index=0)
    lang_opt = st.radio("LANGUAGE", ["日/英混", "全日本語", "全英語"], index=0)

    st.header("⚙️ OPTIONS")
    boost = st.toggle("Anthemic Boost", True)
    optz = st.toggle("Chart Optimizer", True)

# =========================================================
#  Logic & Display
# =========================================================
if st.button("⚡ GENERATE PROMPT"):
    struct = "In-V1-PC-C-V2-C-B-C-Out"
    style_raw = f"Genre:{genre_key}.BPM:{dna['bpm']}.Key:{dna['key_name']}.Boost:{boost}.Opt:{optz}."
    lyrics_raw = f"Lyrics:{genre_key}.Flavor:{LYRIC_FLAVORS[flavor_key]}.Lang:{lang_opt}.Struct:{struct}."

    s_final = style_raw[:st.session_state.p_limit]
    l_final = lyrics_raw[:st.session_state.p_limit]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style Prompt")
    st.text_area("Copy target", s_final, height=100, key="st_out", label_visibility="collapsed")
    st.button("📋 Copy Style", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{s_final}")</script>',
                                                        unsafe_allow_html=True))

    st.subheader("✍️ Lyrics Prompt")
    st.text_area("Copy target", l_final, height=150, key="ly_out", label_visibility="collapsed")
    st.button("📋 Copy Lyrics", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{l_final}")</script>',
                                                         unsafe_allow_html=True))
    st.markdown('</div>', unsafe_allow_html=True)