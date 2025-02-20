import google.generativeai as genai
import streamlit as st

key='AIzaSyDE_ldK9alrl9f0QkgrchtwpGMILTVr2qQ'
genai.configure(api_key=key)

def response(prompt):
    if "gemini_model" not in st.session_state:
        st.session_state["gemini_model"] = "gemini-pro"

    model = genai.GenerativeModel(st.session_state["gemini_model"])
    chat = model.start_chat()
    answer_to_prompt= chat.send_message(prompt)

    return answer_to_prompt.text