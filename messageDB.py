from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    username = Column(String(100))
    IP_address = Column(String(100))

    @staticmethod
    def add_user(username, IP_address, engine):
        new_user = Users(username=username, IP_address=IP_address)
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        session.add(new_user)
        session.commit()
        #print("Message added successfully!")
        session.close()

    @staticmethod
    def get_users(engine):
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        allUsers = session.query(Users).all()
        session.close()
        return allUsers

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    sender = Column(String(100))
    recipient = Column(String(100))
    message = Column(String(500))
    time = Column(DateTime, default=func.now())
    sent_status = Column(Integer)

    # Function to add a new message to the database
    @staticmethod
    def add_message(sender, recipient, message, sent_status, engine):
        new_message = Message(sender=sender, recipient=recipient, message=message, sent_status=sent_status)
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        session.add(new_message)
        session.commit()
        #print("Message added successfully!")
        session.close()

    # Function to retrieve messages from the database
    @staticmethod
    def get_messages(engine, otherUsername):
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        messages = session.query(Message).filter_by(recipient=otherUsername, sent_status=0).all()
        session.close()
        return messages
    
    @staticmethod
    def change_message_status(engine, otherUsername):
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        messages = session.query(Message).filter_by(recipient=otherUsername, sent_status=0).all()
        
        for message in messages:
            message.sent_status = 1
        session.commit()
        #messages = session.query(Message).all()
        session.close()



