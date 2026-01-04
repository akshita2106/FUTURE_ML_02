import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Spotify Churn Analytics",
    page_icon="🎧",
    layout="wide" # Changed to wide for better dashboard feel
)

# ---------------- CUSTOM CSS (Spotify Dark Mode) ----------------
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #121212 0%, #000000 100%);
        color: white;
    }
    .stMetric {
        background-color: #181818;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #282828;
    }
    div.stButton > button {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        border: none !important;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #1ed760 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def create_gauge(probability):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Churn Probability %", 'font': {'color': "#1DB954", 'size': 20}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "white"},
            'bar': {'color': "#1DB954"},
            'bgcolor': "#282828",
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70},
            'steps': [
                {'range': [0, 40], 'color': '#1a4a2a'},
                {'range': [40, 70], 'color': '#4a4a1a'},
                {'range': [70, 100], 'color': '#4a1a1a'}]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"}, height=300)
    return fig

# ---------------- LOAD MODEL ----------------
# Use @st.cache_resource to prevent reloading model on every click
@st.cache_resource
def load_assets():
    with open("model/spotify_churn_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/feature_names.pkl", "rb") as f:
        features = pickle.load(f)
    return model, features

try:
    model, feature_names = load_assets()
except Exception as e:
    st.error("Error loading models. Please ensure model files exist in the /model folder.")
    st.stop()

# ---------------- SIDEBAR / HEADER ----------------
st.title("🎧 Spotify Churn Prediction")
st.markdown("Use this dashboard to analyze user behavior and predict attrition risk.")

# ---------------- MAIN LAYOUT ----------------
col_input, col_viz = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("👤 User Profile Metrics")
    
    with st.container():
        age = st.number_input("Age", 10, 80, 25)
        music_freq = st.select_slider(
            "Listening Frequency",
            options=["Rarely", "Occasionally", "Frequently", "Daily"],
            value="Frequently"
        )
        premium = st.radio("Current Premium Interest", ["Yes", "No"], horizontal=True)
        rating = st.slider("Recommendation Rating", 1, 5, 4)
        podcast = st.checkbox("Active Podcast Listener")

    # Feature Engineering Logic
    low_music = 1 if music_freq in ["Rarely", "Occasionally"] else 0
    no_premium = 1 if premium == "No" else 0
    low_rating = 1 if rating <= 2 else 0
    
    # Prep Input DataFrame
    input_dict = {col: 0 for col in feature_names}
    if age <= 12: input_dict["Age_6-12"] = 1
    elif 20 <= age <= 35: input_dict["Age_20-35"] = 1
    elif 36 <= age <= 60: input_dict["Age_35-60"] = 1
    else: input_dict["Age_60+"] = 1
    
    input_dict.update({
        "low_music_engagement": low_music,
        "no_premium_interest": no_premium,
        "low_recommendation_rating": low_rating,
        "low_podcast_engagement": 0 if podcast else 1,
        "music_recc_rating": rating
    })
    
    input_df = pd.DataFrame([input_dict])
    
    predict_btn = st.button("RUN ANALYSIS")

with col_viz:
    if predict_btn:
        prob = model.predict_proba(input_df)[0][1]
        
        # Display Gauge
        st.plotly_chart(create_gauge(prob), use_container_width=True)
        
        # Risk Assessment Logic
        if prob >= 0.7:
            st.error("### 🔴 HIGH RISK")
            st.info("**Key Drivers:** Low app rating and infrequent listening sessions detected.")
        elif prob >= 0.4:
            st.warning("### 🟡 MEDIUM RISK")
            st.info("**Note:** Consider targeted promotions for New Releases.")
        else:
            st.success("### 🟢 LOW RISK (RETAINED)")
            st.info("**Strategy:** Keep user engaged with personalized Year-in-Review content.")
            
    else:
        st.info("👈 Adjust parameters and click 'Run Analysis' to see results.")
        # Placeholder image for visual balance
        st.image("https://images.unsplash.com/photo-1614680376593-902f74cc0d41?w=800&auto=format&fit=crop&q=60", use_container_width=True)

# ---------------- FOOTER ----------------
st.divider()
st.caption("Internal Retention Tool v2.0 • Data refreshed daily")