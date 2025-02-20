import streamlit as st 
from gemini import Gemini

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot search")

import streamlit as st

with st.chat_message("user"):
    st.write("Hello 👋")
    
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        
if prompt := st.chat_input("Type your query..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})