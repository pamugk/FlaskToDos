from sqlalchemy import Column, ForeignKey, UniqueConstraint, Integer, String, Text
from FlaskToDos.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def __repr__(self):
        return '<Пользователь %r>' % (self.login)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(Text)
    __table_args__ = (UniqueConstraint('user_id', 'title', name='_user_task_uc'),)

    def __init__(self, id, user_id, title, description):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Задача \'%r\'>' % (self.title)
