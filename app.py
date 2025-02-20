import streamlit as st 
from gemini import Gemini
import ai #module defined

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot search")

    
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

    # '''Response to the user prompt'''
    answer_to_prompt=ai.response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer_to_prompt)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer_to_prompt})

