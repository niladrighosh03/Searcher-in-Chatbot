from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Text, ForeignKey, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import event
import time


# Database connection details
username = 'nigo'
password = 'admin'
hostname = 'localhost'
port = '3306'
database_name = 'chatdb'

# Connect to MySQL database
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database_name}')

'''the parent class for all ORM models.'''
Base = declarative_base()


# Define a class to map to the 'chats' table
class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_title = Column(String(255), nullable=False)
    video_url = Column(Text, nullable=True)
    user_query = Column(Text, nullable=False)
    ai_reply = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


# Define a function to handle modifications to the 'chats' table after insertion
def chats_table_insert_listener(mapper, connection, target):
    print("New record inserted into 'chats' table!")

# Attach the event listener to the 'after_insert' event for the Book class
event.listen(Chat, 'after_insert', chats_table_insert_listener)

# Create a session to use the listener
Session = sessionmaker(bind=engine)
session = Session()



def add_chat(chat_title, video_url, user_query, ai_reply):
    """
    Inserts a new chat record into the 'chats' table.
    
    Parameters:
        chat_title (str): The title of the chat.
        video_url (str): The URL of the related video (can be None).
        user_query (str): The query asked by the user.
        ai_reply (str): The AI's response to the query.
    """
    new_chat = Chat(
        chat_title=chat_title,
        video_url=video_url,
        user_query=user_query,
        ai_reply=ai_reply
    )

    session.add(new_chat)
    session.commit()
    print(f"New chat record inserted: {chat_title}")



def search_chat(chat_title):
    """
    Searches for a chat record by chat_title and returns both chat details & timestamp.

    Parameters:
        chat_title (str): The title of the chat to search for.

    Returns:
        tuple: (Chat object, timestamp) if found, else (None, None).
    """
    session = Session()
    chat_record = session.query(Chat).filter(Chat.chat_title == chat_title).first()
    session.close()

    if chat_record:
        return chat_record, chat_record.created_at  # Returning both chat object and timestamp
    else:
        print("Chat title not found.")
        return None, None





def get_all_chats():
    """
    Fetches all chats from the database.

    Returns:
        list: A list of Chat objects.
    """
    session = Session()
    # chats = session.query(Chat).all()
    chats = session.query(Chat).order_by(Chat.created_at.desc()).all()  # Sort by latest

    session.close()
    return chats



def delete_chat(chat_title):
    """
    Deletes a chat record from the 'chats' table by chat_title.

    Parameters:
        chat_title (str): The title of the chat to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    session = Session()
    chat_record = session.query(Chat).filter(Chat.chat_title == chat_title).first()

    if chat_record:
        session.delete(chat_record)
        session.commit()
        session.close()
        print(f"Chat '{chat_title}' deleted successfully.")
        return True
    else:
        session.close()
        print(f"Chat '{chat_title}' not found.")
        return False





print("Listening for new messages inserts...")

# Keep the script running indefinitely to listen for modifications
# while True:
#     time.sleep(1)  # Sleep for 1 second before checking for modifications