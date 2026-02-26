# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================
#  HitForge Master DNA Data & Statistics
# =========================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。"},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。"},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars/Energetic drums."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調の多用。"},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。"},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンスフロア。"},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。"},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。"},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes."},
    "Future Bass": {"bpm": 160, "key": 1, "key_name": "C#", "energy": 0.85, "logic": "キラキラしたシンセ音。"},
    "Trap": {"bpm": 140, "key": 8, "key_name": "Ab", "energy": 0.75, "logic": "808ベースの唸り。"},
}

KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

# --- UI Styles (Browser Neutral Fix) ---
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"] { background-color: #101217 !important; border-right: 1px solid #1d212a !important; }
      input, select, textarea, div[data-baseweb="select"] { background-color: #1d212a !important; color: #ffffff !important; }
      label, p, span, h1, h2, h3 { color: #ffffff !important; }
      .app-title h1 { font-size: 2.6rem; font-weight: 900; margin: 0; }
      .gold-underline { display:inline-block; height:6px; width:160px; border-radius:6px; background: linear-gradient(90deg, #e3b341, #f1c84c); margin-bottom: 20px; }
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; border:none; width:100%; height: 3.2rem; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.15); border:1px solid #e3b341; padding:2px 10px; border-radius: 20px; color: #e3b341 !important; font-size:0.8rem; margin-right:5px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================
#  Sidebar (Controls)
# =========================
with st.sidebar:
    st.header("👤 IDENTITY")
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.header("📝 PRODUCTION")
    must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
    negative_p = st.text_input("NGワード", placeholder="例: 卒業, 桜")

    st.write("プロンプト文字数制限")
    c1, c2 = st.columns([2, 1])
    with c1:
        limit_sl = st.slider("Slider", 80, 2500, 1500, 10, label_visibility="collapsed")
    with c2:
        limit = st.number_input("Value", 80, 2500, value=limit_sl, label_visibility="collapsed")

    st.header("🎛️ DNA PRESET")
    genre_key = st.selectbox("GENRE (Preset Selection)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    # --- 📊 統計ヒストグラム表示ボタン ---
    if st.button("📊 Show DNA Histogram"):
        st.markdown(f"**DNA Statistics: {genre_key}**")

        # 1. BPM Histogram (X: BPM, Y: Frequency)
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)  # 選択ジャンルをピークにした分布
        bpm_df = pd.DataFrame({'BPM (X-axis)': bpm_bins.astype(int), 'Frequency (Y-axis)': bpm_dist})
        st.caption("BPM Distribution (Hit-Rate)")
        st.bar_chart(bpm_df.set_index('BPM (X-axis)'))

        # 2. KEY Histogram (X: Scale/Note, Y: Frequency)
        key_dist = [0.1] * 12
        key_dist[dna['key']] = 0.9  # 選択されたKeyを強調
        key_df = pd.DataFrame({'Scale (X-axis)': KEY_NAMES, 'Popularity (Y-axis)': key_dist})
        st.caption("Key Popularity (Musical Scale)")
        st.bar_chart(key_df.set_index('Scale (X-axis)'))

    manual_on = st.toggle("🔧 Manual Overide (手動調整)")
    if manual_on:
        t_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        t_key = st.selectbox("KEY", KEY_NAMES, index=dna['key'])
    else:
        t_bpm = dna["bpm"]
        t_key = dna["key_name"]

    lang_opt = st.selectbox("言語構成",
                            ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================
#  Generation Logic
# =========================
if st.button("⚡ Generate Hit-DNA Production Prompt"):
    inst_detail = "Modern J-POP production."
    if "Ballad" in genre_key:
        inst_detail = "Grand Piano, emotional strings, delicate live percussion."
    elif "Rock" in genre_key:
        inst_detail = "Driving overdriven guitars, energetic bass, real acoustic drums."
    elif "City Pop" in genre_key:
        inst_detail = "Fretless bass, funky Rhodes, vintage 80s DX7 synth pads."
    elif "Lo-fi" in genre_key:
        inst_detail = "Chill Rhodes, dusty vinyl crackle, boom-bap drums."
    elif "Vocaloid" in genre_key:
        inst_detail = "Aggressive digital synths, fast piano arpeggios, glitch effects."

    opt_logic = f"Hit-Logic:Intro<15s,1st Chorus<45s.High loudness,peak energy at chorus." if optimizer else ""

    style_raw = (
        f"Genre:{genre_key}.BPM:{t_bpm}.Key:{t_key}.Energy:{dna['energy']}.Inst:{inst_detail}Vocal:{v_gender}.{'Anthemic soaring chorus boost.' if boost_mode else ''}{opt_logic}Avoid:{negative_p if negative_p else 'none'}.").replace(
        "  ", " ").strip()
    lyrics_raw = (
        f"Professional lyrics for {genre_key}.Language:{lang_opt}.POV:{l_pov}.Theme:{must_have}.Exclude:{negative_p if negative_p else 'none'}.Structure:[Intro][Verse1][Pre-Chorus][Chorus][Verse2][Chorus][Bridge][Chorus][Outro].Guidelines:Emotional imagery,rhythmic alignment with {t_bpm}BPM.").replace(
        "  ", " ").strip()

    style_final = style_raw[:limit]
    lyrics_final = lyrics_raw[:limit]

    st.markdown("### 🧪 生成結果 (DNA-Synced)")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style / Composition Prompt")
    st.text_area("作曲指示", value=style_final, height=150, key="st_ta")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("作詞指示", value=lyrics_final, height=220, key="ly_ta")

    all_output = f"【STYLE】\n{style_final}\n\n【LYRICS】\n{lyrics_final}"
    st.download_button("⬇️ プロンプトを保存", data=all_output, file_name="hitforge_production.txt")

    st.subheader("🧠 DNA Analysis")
    st.markdown(
        f"""<div style="margin-top:10px;"><span class="gold-chip">BPM: {t_bpm}</span><span class="gold-chip">KEY: {t_key}</span><span class="gold-chip">ENERGY: {dna['energy']}</span><p style='color:#e3b341; margin-top:10px;'>Logic: {dna['logic']}</p></div>""",
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)