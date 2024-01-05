import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

def summary_by_gemini(text_info: str) -> str:
    try:
        genai.configure(api_key="AIzaSyDBNL6Na06RSz3KURODchvC0vuyGzbokrk")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Summary this text and make it short than original: {}".format(text_info))
        return response.text
    except Exception as e:
        print(e)
        return None


