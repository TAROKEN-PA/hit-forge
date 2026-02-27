import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- 1. プリセットデータの準備 (たろけんぱさんのデータに合わせて書き換えてお) ---
data = {
    'Genre': ['J-POP', 'City Pop', 'HipHop', 'Rock', 'Lofi'],
    'BPM': [158, 115, 95, 135, 80],
    'Energy': [0.85, 0.65, 0.75, 0.90, 0.30],
    'Danceability': [0.60, 0.80, 0.90, 0.50, 0.40],
    'Key_Match': [95, 80, 70, 85, 60] # ヒット曲とのKey一致率(想定)
}
df = pd.DataFrame(data)

st.title("🎧 HitForge | Global DNA Analysis")

# --- 2. メイン：レーダーチャート（全要素を一度に比較） ---
# これが一番「分析してる感」が出るお！
fig_radar = go.Figure()

for i, row in df.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=[row['Energy'], row['Danceability'], row['Key_Match']/100, row['BPM']/200, row['Energy']],
        theta=['Energy','Danceability','Key Accuracy','Tempo Scale','Energy'],
        fill='toself',
        name=row['Genre']
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(201,160,80,0.2)"),
        bgcolor="rgba(0,0,0,0)"
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#ffffff"),
    title="Multi-Genre DNA Structure",
    showlegend=True
)

st.plotly_chart(fig_radar, use_container_width=True)

# --- 3. サブ：BPM比較バーチャート（黄金のグラデーション） ---
st.markdown("### 📊 BPM Distribution by Genre")
fig_bar = go.Figure(go.Bar(
    x=df['Genre'],
    y=df['BPM'],
    marker=dict(color=df['BPM'], colorscale=[[0, '#050609'], [1, '#c9a050']]),
    text=df['BPM'],
    textposition='auto',
))

fig_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#ffffff"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
)

st.plotly_chart(fig_bar, use_container_width=True)