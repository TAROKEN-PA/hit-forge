# -*- coding: utf-8 -*-
import streamlit as st

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================
#  HitForge Master DNA Data
# =========================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": "1 (C#/Db)", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。"},
    "J-POP (Ballad)": {"bpm": 72, "key": "0 (C)", "energy": 0.45, "logic": "ピアノ主体の構成。"},
    "J-Rock": {"bpm": 165, "key": "2 (D)", "energy": 0.85, "logic": "Overdriven guitarsと激しいドラム。"},
    "Anime Song": {"bpm": 175, "key": "1 (C#/Db)", "energy": 0.90, "logic": "高揚感と転調の多用。"},
    "Vocaloid Style": {"bpm": 190, "key": "6 (F#/Gb)", "energy": 0.92, "logic": "超高速/複雑。"},
    "City Pop": {"bpm": 115, "key": "9 (A)", "energy": 0.65, "logic": "80s DX7 synths / Fretless bass."},
    "K-Pop (Dance)": {"bpm": 124, "key": "1 (C#/Db)", "energy": 0.82, "logic": "低音重視ダンスフロア。"},
    "K-Pop (HipHop)": {"bpm": 95, "key": "10 (A#/Bb)", "energy": 0.75, "logic": "重厚Trapビート。"},
    "Global Viral": {"bpm": 105, "key": "7 (G)", "energy": 0.72, "logic": "王道Viral。"},
    "Lo-fi Hip Hop": {"bpm": 85, "key": "5 (F)", "energy": 0.35, "logic": "Vinyl crackle / Rhodes."},
    "Future Bass": {"bpm": 160, "key": "1 (C#/Db)", "energy": 0.85, "logic": "キラキラしたシンセ音。"},
    "Trap": {"bpm": 140, "key": "8 (G#/Ab)", "energy": 0.75, "logic": "808ベースの唸り。"},
}

KEY_LIST = ["0 (C)", "1 (C#/Db)", "2 (D)", "3 (D#/Eb)", "4 (E)", "5 (F)",
            "6 (F#/Gb)", "7 (G)", "8 (G#/Ab)", "9 (A)", "10 (A#/Bb)", "11 (B)"]

# =========================
#  Lux UI Style (配色・視認性修正)
# =========================
st.markdown(
    """
    <style>
      :root {
        --bg: #0a0b0e; --panel: #101217; --card: #111418; --border: #1d212a;
        --text: #ffffff; --gold: #e3b341;
      }
      html, body, [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
      .app-title h1 { font-size: 2.6rem; font-weight: 900; color: var(--text); margin: 0; }
      .gold-underline { display:inline-block; height:6px; width:160px; border-radius:6px; background: linear-gradient(90deg, var(--gold), #f1c84c); margin-bottom: 20px; }
      .card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }

      /* 入力BOXの視認性改善：背景を少し明るく、文字を白に固定 */
      input, select, textarea { background-color: #1d212a !important; color: white !important; border: 1px solid #333 !important; }
      div[data-baseweb="select"] > div { background-color: #1d212a !important; color: white !important; }
      label, p, span, .stMarkdown { color: #ffffff !important; }

      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, rgba(227,179,65,1) 100%); color:#000 !important; font-weight: 900; border-radius: 12px; width:100%; border:none; height: 3.2rem; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.15); border:1px solid var(--gold); padding:2px 10px; border-radius: 20px; color: var(--gold); font-size:0.8rem; margin-right:5px; margin-top:5px;}
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

    st.header("📝 PRODUCTION CONTROL")
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光, 運命のドア")
    negative_p = st.text_input("ネガティブプロンプト(避ける語)", placeholder="例: 卒業, 桜")

    # プロンプト文字数制限 (スライダーと数値入力を同期)
    st.write("プロンプト文字数制限 (Length Limit)")
    c1, c2 = st.columns([2, 1])
    with c1:
        limit_sl = st.slider("Slider", 80, 2500, 1500, 10, label_visibility="collapsed")
    with c2:
        limit = st.number_input("Value", 80, 2500, value=limit_sl, label_visibility="collapsed")

    st.header("🎛️ DNA PRESET")
    genre_key = st.selectbox("GENRE (Preset Selection)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    # 手動上書きトグル
    manual_on = st.toggle("🔧 Manual Overide (BPM/Key調整)")
    if manual_on:
        t_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        t_key = st.selectbox("KEY", KEY_LIST, index=KEY_LIST.index(dna["key"]))
    else:
        t_bpm = dna["bpm"]
        t_key = dna["key"]

    lang_opt = st.selectbox("言語構成",
                            ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================
#  Original Prompt Logic (完全復元版)
# =========================
if st.button("⚡ Generate Hit-DNA Production Prompt"):

    # --- 作曲(Style)プロンプトの構築 ---
    # 元のファイルにあった各ジャンルの楽器・構成ロジックを正確に反映
    inst_detail = "Modern J-POP production with rich instrument layers."
    if "Ballad" in genre_key:
        inst_detail = "Emotional Grand Piano, soaring strings, delicate live percussion."
    elif "Rock" in genre_key:
        inst_detail = "Driving overdriven electric guitars, energetic bassline, real acoustic drums."
    elif "City Pop" in genre_key:
        inst_detail = "Fretless bass, funky Rhodes piano, vintage 80s DX7 synth pads, clean electric guitar."
    elif "Lo-fi" in genre_key:
        inst_detail = "Chill Rhodes, dusty vinyl crackle, boom-bap drums, sampled aesthetic."
    elif "Vocaloid" in genre_key:
        inst_detail = "Aggressive digital synths, lightning-fast piano arpeggios, heavy glitch effects."

    # オプティマイザー（サビのタイミング等）
    opt_logic = ""
    if optimizer:
        opt_logic = "Hit-Logic: Intro <15s, 1st Chorus starts <45s. High loudness, high energy peak at chorus."

    style_raw = (
        f"Genre: {genre_key}. BPM: {t_bpm}. Key: {t_key}. Energy Level: {dna['energy']}. "
        f"Instruments: {inst_detail}. Vocal: {v_gender}. "
        f"{'Effect: Anthemic soaring chorus boost.' if boost_mode else ''} {opt_logic} "
        f"Avoid: {negative_p if negative_p else 'none'}."
    )

    # --- 作詞(Lyrics)プロンプトの構築 ---
    lyrics_raw = (
        f"Write professional lyrics for a {genre_key} song. Language: {lang_opt}. "
        f"Vocal POV: {l_pov}. Key Theme: {must_have}. "
        f"Negative Constraint: Strictly NOT use these words: {negative_p if negative_p else 'none'}. "
        f"Song Structure: [Intro] -> [Verse 1] -> [Pre-Chorus] -> [Chorus] -> [Verse 2] -> [Chorus] -> [Bridge] -> [Chorus] -> [Outro]. "
        f"Guidelines: Emotional imagery, catchy rhymes, rhythmic alignment with {t_bpm} BPM."
    )

    # 指定された「プロンプト自体の文字数制限」を適用
    style_final = style_raw[:limit]
    lyrics_final = lyrics_raw[:limit]

    # --- 結果表示 ---
    st.markdown("### 🧪 生成結果 (Production Ready)")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎨 Style / Composition Prompt (作曲指示)")
    st.text_area("Copy this for Music AI Tools", value=style_final, height=160, key="style_ta")

    st.subheader("✍️ Lyrics Prompt (作詞指示)")
    st.text_area("Copy this for Lyrics/LLM Tools", value=lyrics_final, height=220, key="lyrics_ta")

    # ダウンロードボタン
    all_output = f"【STYLE PROMPT】\n{style_final}\n\n【LYRICS PROMPT】\n{lyrics_final}"
    st.download_button("⬇️ プロンプトを保存", data=all_output, file_name="hitforge_production_prompt.txt")

    # DNAロジックの可視化
    st.subheader("🧠 Hit-DNA Logic Analysis")
    st.markdown(f"""
        <div style="margin-top:10px;">
            <span class="gold-chip">BPM: {t_bpm}</span>
            <span class="gold-chip">KEY: {t_key}</span>
            <span class="gold-chip">ENERGY: {dna['energy']}</span>
            <br/><br/>
            <p style='color:#e3b341'>Preset Logic: {dna['logic']}</p>
            <p style='color:#ffffffcc'>Arrangement: {inst_detail}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("⚔️ 黄金比データの注入が完了しました！")