from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Text, ForeignKey, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import event
from sqlalchemy import or_
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




def search_chat(search_term):
    """
    Searches for a chat record based on a search term across multiple columns using the LIKE operation.

    Parameters:
        search_term (str): The term to search for.

    Returns:
        list of tuples: [(Chat object, timestamp), ...] if found, else an empty list.
    """
    session = Session()
    search_pattern = f"%{search_term}%"

    chat_records = session.query(Chat).filter(
        or_(
            Chat.chat_title.like(search_pattern),
            Chat.user_query.like(search_pattern),  # Assuming there's a content field
            Chat.ai_reply.like(search_pattern)  # Assuming there's a user_name field
        )
    ).all()

    session.close()

    if chat_records:
        return [(chat, chat.created_at) for chat in chat_records]
    else:
        print("No matching chats found.")
        return []





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


def get_chat_by_id(chat_id):
    """
    Fetches a chat record by its ID.
    
    Parameters:
        chat_id (int): The ID of the chat to fetch.
    
    Returns:
        Chat: The chat record if found, else None.
    """
    return session.query(Chat).filter_by(chat_id=chat_id).first()



print("Listening for new messages inserts...")

# Keep the script running indefinitely to listen for modifications
# while True:
#     time.sleep(1)  # Sleep for 1 second before checking for modifications