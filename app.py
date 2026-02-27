import streamlit as st
import plotly.graph_objects as go


def display_futuristic_metrics(dna_data):
    # dna_data には {'bpm': 148, 'key': 'C#', 'energy': 0.85, ...} が入る想定だお

    # 1. BPM ゲージ（円形ネオン）
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=dna_data['bpm'],
        title={'text': "TARGET BPM", 'font': {'color': "#c9a050", 'size': 20}},
        number={'font': {'color': "#ffffff", 'size': 50}},
        gauge={
            'axis': {'range': [60, 200], 'tickwidth': 1, 'tickcolor': "#c9a050"},
            'bar': {'color': "#c9a050"},  # 黄金のバー
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [60, 100], 'color': 'rgba(201, 160, 80, 0.1)'},
                {'range': [100, 160], 'color': 'rgba(201, 160, 80, 0.2)'},
                {'range': [160, 200], 'color': 'rgba(201, 160, 80, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': dna_data['bpm']
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#ffffff"},
        height=300,
        margin=dict(l=30, r=30, t=50, b=20)
    )

    return fig

# --- アプリ内での呼び出しイメージ ---
# current_dna = DNA_MASTER[selected_genre]
# st.plotly_chart(display_futuristic_metrics(current_dna))