import streamlit as st
import validators
from design import youtube_qna as ai
from data import store


    
def load_chat():    
    if st.session_state.current_chat:
        st.subheader(st.session_state.current_chat)  # Show chat title

        
        # YouTube URL input
        youtube_url = st.text_input("Enter YouTube URL video having Transcript:", 
                                   st.session_state.get("youtube_urls", {}).get(st.session_state.current_chat, ""))
        
        st.button("Submit YouTube URL")
        if youtube_url:
            # Validate the URL
            if validators.url(youtube_url) and "youtube.com" in youtube_url or "youtu.be" in youtube_url:
                st.session_state.setdefault("youtube_urls", {})[st.session_state.current_chat] = youtube_url
                st.write(f"**YouTube Video:** {youtube_url}")
                st.video(youtube_url)
            else:
                st.error("Invalid YouTube URL. Please enter a valid YouTube link.")        


        # Display chat history
        for message in st.session_state.chats[st.session_state.current_chat]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle user input
        if prompt := st.chat_input("Type your query..."):
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get response from AI model
            # response = ai.get_response(prompt) #for gemini
            with st.spinner("Thinking..."):
                response = ai.get_response(youtube_url,prompt) #for youtube

            with st.chat_message("assistant"):
                st.markdown(response)

            # Save chat to database
            store.add_chat(st.session_state.current_chat, youtube_url, prompt, response)

            # Save chat history
            st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
            st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": response})

    else:
        st.markdown("### ✨ **Start a new chat** from the **sidebar** :sparkles:")
