import streamlit as st
import uuid
from data import store
from design import display_chat

def load_sidebar():
    """Manages sidebar chat selection and new chat creation."""
    st.sidebar.title("Chat History")

    # Initialize session state variables
    if "chats" not in st.session_state:
        st.session_state.chats = {}  # Dictionary to store chat history
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = None
    if "search_results" not in st.session_state:
        st.session_state.search_results = []  # Store search results







    # Input field for chat name
    chat_name = st.sidebar.text_input("Enter Chat Name", "")
    # Button to start a new chat
    if st.sidebar.button("➕ New Chat"):        
        chat_name = chat_name.strip()
        if chat_name:
            if store.chat_title_exists(chat_name):  # Check if chat name already exists
                st.sidebar.warning("Chat name already exists! Choose a different name.")
            else:
                st.session_state.chats[chat_name] = []  # Start new empty chat
                st.session_state.current_chat = chat_name  # Set as active chat
                st.sidebar.success(f"New chat '{chat_name}' created!")
        else:
            st.sidebar.error("Please enter a valid chat name.")





    # Search functionality
    search_query = st.sidebar.text_input("Search Chat", "")
    if st.sidebar.button("🔍 Search"):
        search_query = search_query.strip()
        if search_query:
            results = store.search_chat(search_query)  # Fetch list of matching chats
            if results:
                st.session_state.search_results = results  # Store search results
                st.sidebar.success(f"✅ {len(results)} messages(s) found!")
            else:
                st.session_state.search_results = []  # Reset search results
                st.sidebar.warning("⚠️ No matching chats found!")



    # Display search results with clickable chat names
    if st.session_state.search_results:
        st.sidebar.markdown("### 🔎 Search Results")
        for chat, chat_time in st.session_state.search_results:
            if st.sidebar.button(f"{chat.chat_title} 🕒 {chat_time}", key=f"search_{chat.chat_id}"):

                display_chat.search_chats(chat.chat_id)  # Display selected chat
                # st.session_state.current_chat = chat.chat_title  # Set selected chat
                # st.session_state.search_results = []  # Clear search results
                # st.session_state.chats[chat.chat_title] = store.get_chat_messages(chat.chat_title)  # Load messages







    # Show existing chat sessions
    chats_to_delete = []
    for chat_title in list(st.session_state.chats.keys()):
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            if st.button(chat_title, key=chat_title):
                st.session_state.current_chat = chat_title  # Switch to selected chat
        with col2:
            if st.button("❌", key=f"del_{chat_title}"):
                chats_to_delete.append(chat_title)

    # Delete chats outside the loop to avoid modifying the dictionary during iteration
    for chat_title in chats_to_delete:
        if st.session_state.current_chat == chat_title:
            st.session_state.current_chat = None  # Reset current chat if deleted
        
        del st.session_state.chats[chat_title]  # Remove from UI
        store.delete_chat(chat_title)  # Remove from Database  ✅ Added this line

        st.rerun()  # Refresh UI ✅ Added this to reflect changes instantly





    # Display the selected chat
    display_chat.show_chats()

