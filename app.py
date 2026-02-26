# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================================================
#  1. Master DNA Data (完全復元)
# =========================================================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78, "logic": "BPM140超の疾走感。"},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。"},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調。"},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。"},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths."},
    "Lo-fi": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle."},
}
KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {"王道チャート": "Standard", "詩的・比喩的": "Metaphorical", "映画的描写": "Cinematic",
                 "ストレート": "Raw", "哲学的・ダーク": "Deep"}

# =========================================================
#  2. 視認性改善 CSS (文字色・アイコンを強制白に)
# =========================================================
st.markdown(
    """
    <style>
      /* 全体の背景と文字色 */
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { 
        background-color: #0a0b0e !important; color: #ffffff !important; 
      }
      /* サイドバーの背景と文字色 */
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { 
        background-color: #101217 !important; color: #ffffff !important; 
      }
      /* サイドバーを閉じる/開くアイコンを白く強制 */
      button[kind="header"] svg { fill: #ffffff !important; stroke: #ffffff !important; }

      /* 入力フォーム類の背景と文字色 */
      input, select, textarea, div[data-baseweb="select"] { 
        background-color: #1d212a !important; color: #ffffff !important; border: 1px solid #333 !important;
      }
      /* ボタンのデザイン */
      .stButton > button { 
        background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; 
        color:#000000 !important; font-weight: 900 !important; border-radius: 12px !important;
      }
      /* ポップアップ(Popover)内 */
      div[data-testid="stPopoverBody"] { background-color: #1d212a !important; color: white !important; border: 1px solid #e3b341 !important; }
      h1, h2, h3, p, span, label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

# =========================================================
#  3. Sidebar (文字数同期 & ポップアップ設定)
# =========================================================
with st.sidebar:
    st.markdown('<h2 style="color:#e3b341;">👤 IDENTITY</h2>', unsafe_allow_html=True)
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1, horizontal=True)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2, horizontal=True)

    st.markdown('<h2 style="color:#e3b341;">📝 PRODUCTION</h2>', unsafe_allow_html=True)
    must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")

    # --- 文字数同期 ---
    if "p_limit" not in st.session_state: st.session_state.p_limit = 1500


    def sync_n(): st.session_state.p_limit = st.session_state.n_in


    def sync_s(): st.session_state.p_limit = st.session_state.s_in


    st.write("プロンプト文字数制限")
    st.number_input("数値", 80, 2500, key="n_in", on_change=sync_n, value=st.session_state.p_limit,
                    label_visibility="collapsed")
    st.slider("スライダー", 80, 2500, key="s_in", on_change=sync_s, value=st.session_state.p_limit,
              label_visibility="collapsed")

    st.markdown('<h2 style="color:#e3b341;">🎛️ CONFIG</h2>', unsafe_allow_html=True)

    # ジャンルとグラフを一つのポップアップに集約
    with st.popover("🎹 ジャンル・DNA分析"):
        genre_key = st.radio("DNA Genre", list(DNA_MASTER.keys()), index=0)
        dna = DNA_MASTER[genre_key]
        st.write(f"**Logic:** {dna['logic']}")

        # グラフをポップアップ内に配置
        st.caption("BPM Distribution")
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=150)

        st.caption("Key Popularity")
        key_dist = [0.1] * 12;
        key_dist[dna['key']] = 0.9
        st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES), height=150)

    with st.popover("🎨 表現・言語設定"):
        flavor = st.radio("Lyricフレーバー", list(LYRIC_FLAVORS.keys()), index=0)
        lang_opt = st.radio("言語構成", ["日本語/英語混", "全日本語", "全英語"], index=0)

    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Chart Optimizer", value=True)

# =========================================================
#  4. Main Display
# =========================================================
st.markdown(
    '<h1 style="color:#e3b341; margin-bottom:0;">🎼 HitForge</h1><div style="height:4px; width:150px; background:#e3b341; border-radius:6px; margin-bottom:20px;"></div>',
    unsafe_allow_html=True)

if st.button("⚡ GENERATE HIT-DNA PROMPT"):
    compact_struct = "In-V1-PC-C-V2-C-B-C-Out"
    style_raw = f"Genre:{genre_key}.BPM:{dna['bpm']}.Energy:{dna['energy']}.Vocal:{v_gender}.{'Anthemic boost.' if boost_mode else ''}{'Chart Optz.' if optimizer else ''}"
    lyrics_raw = f"Lyrics:{genre_key}.Flavor:{LYRIC_FLAVORS[flavor]}.Lang:{lang_opt}.POV:{l_pov}.Theme:{must_have}.Struct:{compact_struct}."

    s_final = style_raw[:st.session_state.p_limit]
    l_final = lyrics_raw[:st.session_state.p_limit]

    st.markdown('<div style="background:#111418; border:1px solid #1d212a; border-radius:14px; padding:1.5rem;">',
                unsafe_allow_html=True)
    st.subheader("🎨 Style Prompt")
    st.text_area("Style", s_final, height=120, label_visibility="collapsed")
    st.button("📋 Copy Style", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{s_final}")</script>',
                                                        unsafe_allow_html=True), key="cp_s")

    st.subheader("✍️ Lyrics Prompt")
    st.text_area("Lyrics", l_final, height=180, label_visibility="collapsed")
    st.button("📋 Copy Lyrics", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{l_final}")</script>',
                                                         unsafe_allow_html=True), key="cp_l")
    st.markdown('</div>', unsafe_allow_html=True)