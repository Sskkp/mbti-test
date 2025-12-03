import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load dataset
df = pd.read_csv("mbti_1.csv")

# Clean text function
def clean_text(text):
    text = text.lower()
    text = ''.join([ch for ch in text if ch.isalpha() or ch.isspace()])
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Apply cleaning
df['clean_posts'] = df['posts'].apply(clean_text)

# Encode MBTI labels
le = LabelEncoder()
df["type_label"] = le.fit_transform(df["type"])

# Create training pipeline
pipe = Pipeline([
    ("vectorizer", TfidfVectorizer(max_features=1000)),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Fit the model
pipe.fit(df["clean_posts"], df["type_label"])

# Save model and encoder
joblib.dump(pipe, "mbti_pipe.pkl")
joblib.dump(le, "mbti_label_encoder.pkl")

print("✅ Retraining complete. Model and encoder saved.")

