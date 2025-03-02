import streamlit as st
from data import store

def show_chats():
    """
    Fetch existing chat names and their content from the database,
    then display them in the sidebar, grouping messages by chat_title.
    """
    show_stored_chats = st.sidebar.checkbox("Show Existing Chats")
    if show_stored_chats:
        stored_chats = store.get_all_chats()  # Fetch all stored chats
        chat_groups = {}

        # Group chats by chat_title
        for chat in stored_chats:
            if chat.chat_title not in chat_groups:
                chat_groups[chat.chat_title] = []
            chat_groups[chat.chat_title].append(chat)

        if chat_groups:
            for chat_title, messages in chat_groups.items():
                if st.sidebar.button(chat_title, key=f"stored_{chat_title}"):
                    st.session_state.current_chat = chat_title
                    st.session_state.chats[chat_title] = []

                    # Store all messages under the same chat title
                    for msg in messages:
                        st.session_state.chats[chat_title].append({"role": "user", "content": msg.user_query})
                        st.session_state.chats[chat_title].append({"role": "assistant", "content": msg.ai_reply})

                    # Store the latest video's URL (assuming the last message's video_url is the most relevant)
                    st.session_state.setdefault("youtube_urls", {})[chat_title] = messages[-1].video_url
        else:
            st.sidebar.info("No stored chats found.")



def search_chats(chat_id):
    """
    Fetch existing chat names and their content from the database. If a chat_id is provided,
    display that specific chat; otherwise, list all stored chats in the sidebar.
    """
    if chat_id:
        chat = store.get_chat_by_id(chat_id)  # Fetch the specific chat using chat_id
        if chat:
            st.session_state.current_chat = chat.chat_title
            st.session_state.chats[chat.chat_title] = [
                {"role": "user", "content": chat.user_query},
                {"role": "assistant", "content": chat.ai_reply}
            ]
            st.session_state.setdefault("youtube_urls", {})[chat.chat_title] = chat.video_url
        else:
            st.error("Chat not found.")
    else:
        show_stored_chats = st.sidebar.checkbox("Show Existing Chats")
        if show_stored_chats:
            stored_chats = store.get_all_chats()  # Fetch stored chats from ORM
            if stored_chats:
                for chat in stored_chats:
                    if st.sidebar.button(chat.chat_title, key=f"stored_{chat.chat_id}"):
                        st.session_state.current_chat = chat.chat_title
                        st.session_state.chats[chat.chat_title] = [
                            {"role": "user", "content": chat.user_query},
                            {"role": "assistant", "content": chat.ai_reply}
                        ]
                        st.session_state.setdefault("youtube_urls", {})[chat.chat_title] = chat.video_url
            else:
                st.sidebar.info("No stored chats found.")
