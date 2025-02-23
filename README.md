# **🔍 Chat Search - AI-Powered Chat Retrieval System**  

![GitHub Repo Size](https://img.shields.io/github/repo-size/niladrighosh03/Searcher-in-Chatbot)  
![Python Version](https://img.shields.io/badge/python-3.12+-yellow)  

🚀 **Chat Search** is an AI-powered system that allows users to **search, retrieve, and display past chat conversations** efficiently. It utilizes **ChromaDB** for fast search operations and integrates AI-based responses for seamless interaction.  

---

## **📌 Features**  
✅ **Search Chats Instantly** – Retrieve past conversations with **keyword-based search**.  
✅ **AI-Powered Interaction** – Integrates **Gemini AI** for intelligent responses.  
✅ **YouTube Transcript Search** – Supports **YouTube video transcripts** for enhanced Q&A.  
✅ **Streamlit UI** – A **modern & interactive** web-based interface for smooth navigation.  
✅ **Persistent Storage** – Uses **ChromaDB** for fast and efficient chat storage.  

---

## **🛠️ Tech Stack**  
- **Python 3.12+** 🐍  
- **Streamlit** (Web UI) 🎨  
- **ChromaDB** (Vector Search Engine) 🔍  
- **Gemini AI** (AI Response Generator) 🤖  

---

## **📂 Project Structure**  

```
Searcher-in-Chatbot/
│── chroma_db_/          # Database storage
│── data/
│   ├── search.py        # Search logic for chats
│   ├── store.py         # Data storage handler
│── design/
│   ├── bar.py           # Sidebar UI components
│   ├── chat.py          # Chat handling logic
│   ├── display_chat.py  # Display fetched chat history
│   ├── gemini.py        # AI interaction module
│   ├── youtube_qna.py   # YouTube transcript processing
│── app.py               # Main Streamlit application
│── requirements.txt     # Required Python dependencies
│── .gitignore           # Ignore unnecessary files
│── README.md            # Project documentation
```

---

## **🚀 Installation & Setup**  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/niladrighosh03/Searcher-in-Chatbot.git
cd Searcher-in-Chatbot
```

### **2️⃣ Create a Virtual Environment**  
```bash
python -m venv .venv
source .venv/bin/activate  # For macOS/Linux
# OR
.venv\Scripts\activate  # For Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Application**  
```bash
streamlit run app.py
```

---

## **🖥️ Usage Guide**  
1. **Enter a keyword** in the **Search Chat** box to find past conversations.  
2. **Click on a retrieved chat** to view its full conversation.  
3. **If YouTube transcript search is enabled**, enter the YouTube URL and ask questions.  
4. **Use AI responses** to get context-based answers.  

---



## **💡 Contribution & Support**  
🔹 Found a bug? **Open an issue**  
🔹 Want to improve the project? **Submit a pull request**  
🔹 Need help? **Contact me**  

✨ **Happy Coding!** 🚀  

---

### **📷 Preview Screenshot**  
![Project Structure](pic2.png)
![Project Structure](pic.png)

