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


    # Input field for chat name
    chat_name = st.sidebar.text_input("Enter Chat Name", "")
  

    # Button to start a new chat
    if st.sidebar.button("➕ New Chat"):        
        if chat_name.strip():  # Ensure chat name is not empty
            if chat_name in st.session_state.chats:
                st.sidebar.warning("Chat name already exists! Choose a different name.")
            else:
                st.session_state.chats[chat_name] = []  # Start new empty chat
                st.session_state.current_chat = chat_name  # Set as active chat
                st.session_state.chat_name_input = ""  # Reset input field
        else:
            st.sidebar.error("Please enter a valid chat name.")
    


    # Show existing chat sessions
    chats_to_delete = []
    for chat_name in list(st.session_state.chats.keys()):
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            if st.button(chat_name, key=chat_name):
                st.session_state.current_chat = chat_name  # Switch to selected chat
        with col2:
            if st.button("❌", key=f"del_{chat_name}"):
                chats_to_delete.append(chat_name)
    
    # Delete chats outside the loop to avoid modifying the dictionary during iteration
    for chat_name in chats_to_delete:
        if st.session_state.current_chat == chat_name:
            st.session_state.current_chat = None  # Reset current chat if deleted
        del st.session_state.chats[chat_name]