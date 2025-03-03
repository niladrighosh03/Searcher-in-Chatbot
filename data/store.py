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

'''The parent class for all ORM models.'''
Base = declarative_base()

# Define a class to map to the 'chats' table
class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_title = Column(String(255), nullable=False)
    video_url = Column(Text, nullable=True)
    user_query = Column(Text, nullable=False)
    ai_reply = Column(Text, nullable=False)
    user = Column(String(255), nullable=False)  # New column
    feedback = Column(Text, nullable=True)  # New column
    feedback_rating = Column(Integer, nullable=True)  # New column
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

# Define a function to handle modifications to the 'chats' table after insertion
def chats_table_insert_listener(mapper, connection, target):
    print("New record inserted into 'chats' table!")

# Attach the event listener to the 'after_insert' event for the Chat class
event.listen(Chat, 'after_insert', chats_table_insert_listener)

# Create a session to use the listener
Session = sessionmaker(bind=engine)
from sqlalchemy.orm import scoped_session
session = scoped_session(sessionmaker(bind=engine))

def add_chat(chat_title, video_url, user_query, ai_reply, user, feedback=None, feedback_rating=None):
    """
    Inserts a new chat record into the 'chats' table.
    """
    new_chat = Chat(
        chat_title=chat_title,
        video_url=video_url,
        user_query=user_query,
        ai_reply=ai_reply,
        user=user,
        feedback=feedback,
        feedback_rating=feedback_rating
    )
    session.add(new_chat)
    session.commit()
    print(f"New chat record inserted: {chat_title}")

def search_chat(search_term):
    """
    Searches for a chat record based on a search term across multiple columns using the LIKE operation.
    """
    session = Session()
    search_pattern = f"%{search_term}%"
    chat_records = session.query(Chat).filter(
        or_(
            Chat.chat_title.like(search_pattern),
            Chat.user_query.like(search_pattern),
            Chat.ai_reply.like(search_pattern),
            Chat.user.like(search_pattern),
            Chat.feedback.like(search_pattern)
        )
    ).all()
    session.close()
    return [(chat, chat.created_at) for chat in chat_records] if chat_records else []

def get_all_chats():
    """Fetches all chats from the database."""
    session = Session()
    chats = session.query(Chat).order_by(Chat.created_at.desc()).all()
    session.close()
    return chats

def delete_chat(chat_title):
    """Deletes a chat from the 'chats' table based on its title."""
    session.query(Chat).filter(Chat.chat_title == chat_title).delete()
    session.commit()
    print(f"Chat '{chat_title}' deleted successfully.")

def get_chat_by_id(chat_id):
    """Fetches a chat record by its ID."""
    return session.query(Chat).filter_by(chat_id=chat_id).order_by(Chat.created_at.asc()).all()

def chat_title_exists(chat_title):
    """Checks if a chat with the given title exists in the database."""
    session_obj = Session()
    exists = session_obj.query(Chat).filter(Chat.chat_title == chat_title).first() is not None
    session_obj.close()
    return exists

def save_feedback(chat_title, feedback, feedback_rating):
    """
    Updates the feedback and feedback rating for the latest chat record with the given title.
    """
    session_obj = Session()
    chat_record = session_obj.query(Chat).filter_by(chat_title=chat_title).order_by(Chat.created_at.desc()).first()
    
    if chat_record:
        chat_record.feedback = feedback
        chat_record.feedback_rating = feedback_rating
        session_obj.commit()
        print(f"Feedback updated for chat title '{chat_title}' (Chat ID: {chat_record.chat_id})")
    else:
        print(f"No chat found with title '{chat_title}'")
    
    session_obj.close()




def get_top_bottom_feedbacks():
    """
    Fetch top 4 highest-rated and bottom 4 lowest-rated feedbacks.
    """
    session_obj = Session()

    top_feedbacks = session_obj.query(Chat).filter(Chat.feedback_rating.isnot(None)) \
        .order_by(Chat.feedback_rating.desc()).limit(4).all()

    bottom_feedbacks = session_obj.query(Chat).filter(Chat.feedback_rating.isnot(None)) \
        .order_by(Chat.feedback_rating.asc()).limit(4).all()

    session_obj.close()
    
    return top_feedbacks, bottom_feedbacks


print("Listening for new messages inserts...")
