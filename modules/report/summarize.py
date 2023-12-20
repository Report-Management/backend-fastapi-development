import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

def summary_by_gemini(text_info: str) -> str:
    try:
        load_dotenv()
        genai.configure(api_key="AIzaSyDBNL6Na06RSz3KURODchvC0vuyGzbokrk")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("summary make it short then original: {}".format(text_info))
        return response.text
    except:
        return None


