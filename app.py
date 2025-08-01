import streamlit as st
import joblib

model = joblib.load("model.pkl")

st.title("📧 Email Spam Detector")
email_text = st.text_area("Enter email text here:")

if st.button("Classify"):
    if email_text:
        label = model.predict([email_text])[0]
        st.success("Spam 🚫" if label else "Legit ✅")
    else:
        st.warning("Please enter some text to classify.")
