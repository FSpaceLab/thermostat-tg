from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
sess = Session()

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    pin_code = Column(Integer)
    permission = Column(Integer)
    session_duration = Column(Integer)

    pin_counter = Column(Integer, default=0)
    pin_matches = Column(Integer, default=0)

    def __repr__(self):
       return f"<User {self.user_id} | permission: {self.permission}>"


class BotSession(Base):
    __tablename__ = 'bot_session'

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    start_session = Column(Integer)
    current_directory = Column(String)

    current_menu = Column(String, default="")

    def __repr__(self):
       return f"<Session {self.session_id} | user: {self.user_id} | " \
              f"start time: {datetime.fromtimestamp(self.start_session)}>"


def create_db():
    Base.metadata.create_all(engine)
