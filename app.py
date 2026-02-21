import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Set Page Config
st.set_page_config(page_title="Movie Success Predictor", layout="centered")

# Title and Description
st.title("🎬 Movie Success Predictor")
st.markdown("""
Predict if a movie will be a **Hit**, **Average**, or **Flop** financially.
* **Flop:** Revenue < Budget (Loss)
* **Average:** Revenue 1x - 2x Budget
* **Hit:** Revenue > 2x Budget
""")

# Load Model and Artifacts
@st.cache_resource
def load_artifacts():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('label_encoder_genre.pkl', 'rb') as f:
        le_genre = pickle.load(f)
    return model, scaler, le_genre

try:
    model, scaler, le_genre = load_artifacts()
except FileNotFoundError:
    st.error("Model files not found. Please run the notebook/script first.")
    st.stop()


# Tab for Prediction (Removed tabs to simplify)
# Main Prediction Logic
# Input Fields
st.subheader("Movie Parameters")
col1, col2 = st.columns(2)

with col1:
    genres = list(le_genre.classes_)
    genre = st.selectbox("Genre", genres)
    
    budget = st.number_input("Budget ($)", min_value=0, value=10000000, step=1000000, format="%d")
    
    # Re-introducing IMDB Score Slider
    imdb_score = st.slider("IMDB Score (Optional - for Verdict)", 0.0, 10.0, 6.5, 0.1)

with col2:
    year = st.number_input("Release Year", min_value=1900, max_value=2030, value=2016)
    
    fb_likes = st.number_input("Cast Total Facebook Likes", min_value=0, value=5000)

# Prediction Logic
if st.button("Predict Financial Outcome"):
    # Preprocess
    genre_encoded = le_genre.transform([genre])[0]
    features = np.array([[genre_encoded, fb_likes, budget, year]])
    features_scaled = scaler.transform(features)
    
    # Predict
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)
    
    # Display
    st.markdown("---")
    st.subheader("Prediction Result")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown("#### 💰 Financial Prediction")
        outcome_color = {'Hit': 'green', 'Average': 'orange', 'Flop': 'red'}
        color = outcome_color.get(prediction, 'blue')
        st.markdown(f"The model predicts: :{color}[**{prediction}**]")
        if prediction == 'Flop':
            st.caption("Likely to lose money (Revenue < Budget).")
        elif prediction == 'Hit':
            st.caption("Likely to be highly profitable!")
            
    with col_res2:
        st.markdown("#### ⭐ IMDB Verdict")
        def classify_imdb(score):
            if score < 5.0: return 'Flop', 'red'
            elif score < 7.0: return 'Average', 'orange'
            else: return 'Hit', 'green'
            
        imdb_verdict, imdb_color = classify_imdb(imdb_score)
        st.markdown(f"Based on Score ({imdb_score}): :{imdb_color}[**{imdb_verdict}**]")
        st.caption("Flop < 5.0 | Average 5.0-7.0 | Hit > 7.0")

    # Graph
    st.write("### Financial Probability Breakdown")
    classes = model.classes_
    probs = probabilities[0]
    
    prob_df = pd.DataFrame({
        'Outcome': classes,
        'Probability': probs
    })
    
    st.bar_chart(prob_df.set_index('Outcome')['Probability'])

