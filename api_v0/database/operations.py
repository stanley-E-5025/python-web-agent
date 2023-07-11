from sqlmodel import Session

from .settings import engine
from .models import User

def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
