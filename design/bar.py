import streamlit as st
import uuid


def load_sidebar():
    """Manages sidebar chat selection and new chat creation."""
    st.sidebar.title("Chat History")

    # Initialize session state variables
    if "chats" not in st.session_state:
        st.session_state.chats = {}  # Dictionary to store chat history
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = None

    # Button to start a new chat
    if st.sidebar.button("➕ New Chat"):
        chat_id = f"Chat {len(st.session_state.chats) + 1}"
        # chat_id= str(uuid.uuid4().hex[:10])
        st.session_state.chats[chat_id] = []  # Start new empty chat
        st.session_state.current_chat = chat_id  # Set as active chat

    # Show existing chat sessions
    for chat_id in st.session_state.chats.keys():
        if st.sidebar.button(chat_id):
            st.session_state.current_chat = chat_id  # Switch to selected chat

