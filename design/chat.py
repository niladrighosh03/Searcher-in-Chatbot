import streamlit as st
from design import ai


def load_chat():    
    if st.session_state.current_chat:
        st.subheader(st.session_state.current_chat)  # Show chat title

        # Display chat history
        for message in st.session_state.chats[st.session_state.current_chat]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle user input
        if prompt := st.chat_input("Type your query..."):
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get response from AI model
            response = ai.get_response(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)

            # Save chat history
            st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
            st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": response})

    else:
        st.write("Start a new chat from the sidebar.")

