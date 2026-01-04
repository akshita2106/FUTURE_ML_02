import streamlit as st
import joblib
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Spotify Churn Analysis",
    page_icon="🎧",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
}
h1, h2 { color: #1DB954; }
.stButton button {
    background-color: #1DB954;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
.footer {
    text-align:center;
    font-size:12px;
    color:#888;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model/spotify_churn_model.pkl")
feature_names = joblib.load("model/feature_names.pkl")
# ---------------- HEADER ----------------
st.markdown("""
<h1>🎧 Spotify Churn Analytics Dashboard</h1>
<p>AI-powered churn prediction using engagement, satisfaction & monetization signals</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("👤 User Behaviour Profile")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Age", 10, 70, 25)
    music_freq = st.selectbox(
        "Music Listening Frequency",
        ["Rarely", "Occasionally", "Frequently", "Daily"]
    )

with col2:
    rating = st.slider("Recommendation Satisfaction", 1, 5, 3)
    podcast_freq = st.selectbox(
        "Podcast Listening Frequency",
        ["Never", "Rarely", "Occasionally", "Frequently"]
    )

with col3:
    premium = st.selectbox("Premium Willingness", ["Yes", "No"])

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FEATURE ENGINEERING ----------------
low_music = 1 if music_freq in ["Rarely", "Occasionally"] else 0
low_podcast = 1 if podcast_freq in ["Never", "Rarely"] else 0
low_rating = 1 if rating <= 2 else 0
no_premium = 1 if premium == "No" else 0

engagement_score = low_music + low_podcast
satisfaction_score = low_rating
monetization_score = no_premium
churn_pressure = 0.5*engagement_score + 0.3*satisfaction_score + 0.2*monetization_score

# ---------------- BUILD INPUT ----------------
input_dict = {col: 0 for col in feature_names}

# Age buckets
if age <= 12:
    input_dict["Age_6-12"] = 1
elif 20 <= age <= 35:
    input_dict["Age_20-35"] = 1
elif 36 <= age <= 60:
    input_dict["Age_35-60"] = 1
else:
    input_dict["Age_60+"] = 1

input_dict.update({
    "low_music_engagement": low_music,
    "low_podcast_engagement": low_podcast,
    "low_recommendation_rating": low_rating,
    "no_premium_interest": no_premium,
    "music_recc_rating": rating,
    "engagement_score": engagement_score,
    "satisfaction_score": satisfaction_score,
    "monetization_score": monetization_score,
    "churn_pressure": churn_pressure
})

input_df = pd.DataFrame([input_dict])

# ---------------- PREDICTION ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Churn Risk Assessment")

if st.button("Run Churn Analysis"):
    prob = model.predict_proba(input_df)[0][1]

    c1, c2, c3 = st.columns(3)
    c1.metric("Churn Probability", f"{prob:.2%}")
    c2.metric("Engagement Risk", engagement_score)
    c3.metric("Monetization Risk", monetization_score)

    if prob >= 0.65:
        st.error("🚨 High churn risk — Immediate retention action recommended")
    elif prob >= 0.4:
        st.warning("⚠️ Moderate churn risk — Engagement optimization needed")
    else:
        st.success("✅ Low churn risk — User is healthy")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div class="footer">
Spotify Churn Prediction System • Machine Learning Internship Project
</div>
""", unsafe_allow_html=True)
