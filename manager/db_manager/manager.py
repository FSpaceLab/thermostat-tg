from manager.db_manager import User, BotSession, Base, engine, sess as db
from sqlalchemy import desc
from datetime import datetime


def create_db():
    Base.metadata.create_all(engine)


def add_user(user_id, pin_code, permission, session_duration):
    user = User(user_id=user_id, pin_code=pin_code, permission=permission, session_duration=session_duration)
    db.add(user)
    db.commit()


def add_session(user_id: int, current_directory: str = "~/"):
    session = BotSession(user_id=user_id, start_session=int(datetime.now().timestamp()),
                         current_directory=current_directory)
    db.add(session)
    db.commit()


def get_user(id: int):
    return db.query(User).filter_by(user_id=id).first()


def get_pin_data(id: int, update_pin_counter: int = 2,
                 update_pin_matches: int = 2) -> "pin_code, pin_counter, pin_matches":
    """
    :param id: user telegram id
    :param update_pin_counter: 2 - without update; 1 - increment pin counter; 0 - nullify pin counter
    :param update_pin_matches: 2 - without update; 1 - increment pin matches; 0 - nullify pin matches
    :return: pin code, pin counter and pin matches
    """
    user = db.query(User).filter_by(user_id=id).first()

    if update_pin_counter < 2:
        # increment or nullify pin counter
        user.pin_counter = (user.pin_counter + 1 if update_pin_counter else 0)
        db.commit()

    if update_pin_matches < 2:
        # increment or nullify pin matches
        user.pin_matches = (user.pin_matches + 1 if update_pin_matches else 0)
        db.commit()

    return user.pin_code, user.pin_counter, user.pin_matches


def get_last_session(id: int):
    return db.query(BotSession).filter_by(user_id=id).order_by(desc(BotSession.start_session)).first()


def update_bot_session(id: int, path: str = "~/"):
    session = get_last_session(id)
    session.current_directory = path
    db.commit()
    return session

def update_current_menu(id:int, menu: str = ""):
    session = get_last_session(id)
    session.current_menu = menu
    db.commit()
    return session

def get_current_menu(id:int):
    session = get_last_session(id)
    return session.current_menu
