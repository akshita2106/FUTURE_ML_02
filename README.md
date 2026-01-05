# 🎧 Spotify User Churn Prediction System

A machine learning–based churn prediction system that identifies users likely to stop using a music streaming service.  
The project combines **predictive modeling**, an **interactive dashboard**, and **actionable business insights** to support data-driven retention strategies.


## 📌 Project Overview

Customer churn is a major challenge for subscription-based platforms like Spotify. Retaining existing users is far more cost-effective than acquiring new ones.
This project predicts **churn probability per user**, visualizes **churn risk segments**, and highlights **key behavioral drivers of churn** through an analytics dashboard.


## 🎯 Objectives

- Predict user churn probability using machine learning
- Segment users into churn risk levels (Low / Medium / High)
- Visualize churn insights in an interactive dashboard
- Provide actionable business recommendations for retention


## 🧠 Machine Learning Approach

- **Algorithm Used:** XGBoost Classifier  
- **Target Variable:** `churn` (0 = Active, 1 = Churned)
- **Class Imbalance Handling:** `scale_pos_weight`
- **Model Output:** Churn probability (0–1)

### Key Features Used

- User engagement signals  
- Recommendation satisfaction  
- Premium subscription interest  
- Monetization behavior  

## 📊 Dashboard & Insights

An interactive **Power BI dashboard** was built to present insights for business stakeholders.

### Dashboard Highlights:
- Total Users & Churn Rate KPIs
- Active vs Churned user distribution
- Churn risk segmentation based on probabilities
- Key churn drivers analysis
- Clear explanation of churn assessment logic


## 💡 Business Recommendations

- Improve recommendation quality for users with low satisfaction scores
- Proactively engage low-engagement users through personalized content
- Offer targeted premium trials to high-risk users
- Focus on retention strategies even when overall churn appears low


## 🛠️ Tools & Technologies

- **Python** – Data analysis & modeling  
- **Pandas, NumPy** – Data preprocessing  
- **Scikit-learn** – Model evaluation  
- **XGBoost** – Churn prediction model  
- **Power BI** – Dashboard & visualization  
- **Streamlit** – Web app deployment  


## 📁 Project Structure
ChurnPredictionSystem/
│
├── data/
│ └── spotify_model_ready.csv
| └── spotify_processed.csv
│ └── spotify_raw.csv
|
├── notebooks/
│ ├── 01_data_exploration.ipynb
│ ├── 02_feature_engineering.ipynb
│ └── 03_model_training.ipynb
│
├── model/
│ ├── spotify_churn_model.pkl
│ └── feature_names.pkl
│
├── app.py
├── requirements.txt

## 🚀 How to Run the Project

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/FUTURE_ML_02.git
2. pip install -r requirements.txt
3. streamlit run app.py

## 📈 Results Summary

Total Users: 224
Churned Users: 16
Churn Rate: ~7%
The model successfully identifies high-risk users despite low current churn.

##  Conclusion

This project demonstrates how machine learning can be effectively combined with data visualization to create business-ready churn prediction systems.
It emphasizes not just model accuracy, but interpretability, insights, and real-world decision support.

## 📬 Author
Akshita
Machine Learning Intern | AI & ML Enthusiast


