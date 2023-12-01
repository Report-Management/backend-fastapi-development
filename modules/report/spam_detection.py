import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer 
from joblib import load
import os

def spam_or_ham(text):
    df = pd.read_csv('modules\\report\\x_train.csv')
    cv = CountVectorizer()
    df = df.values.flatten()
    cv.fit_transform(df)
    
    # Load model
    model = load('modules\\report\\spam_model.joblib')
    
    text = cv.transform([text])
    results = model.predict(text).flatten()
    if results == 1:
        return True
    return False
