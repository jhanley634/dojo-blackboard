from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(url="sqlite:////tmp/blackboard.db")


def get_session() -> Session:
    return sessionmaker(bind=engine)()
