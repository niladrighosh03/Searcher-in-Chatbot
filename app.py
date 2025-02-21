import streamlit as st 
from design import bar,chat, gemini #module defined

st.title("💬 YouTube Video Q&A Chatbot")
st.caption("🚀 A Streamlit chatbot search")

    
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        
bar.load_sidebar()
chat.load_chat()