from FlaskToDos.database import db_session
from FlaskToDos.models import *
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

def add_task (user_id, title, description):
    db_session.add(Task(None, user_id, title, description))
    db_session.commit()

def add_user(login, password):
    db_session.add(User(None, login, generate_password_hash(password, salt_length=64)))
    db_session.commit()

def check_user_password(user, password):
    return check_password_hash(user.password, password)

def get_task_by_id(id, user_id):
    return Task.query.filter(Task.id == id and Task.user_id == user_id).first()

def get_task_by_title(title, user_id):
    return Task.query.filter(Task.title == title and Task.user_id == user_id).first()

def get_tasks_by_user_id(id):
    return Task.query.filter(Task.user_id == id).order_by(Task.id)

def get_user_by_id(id):
    return User.query.filter(User.id == id).first()

def get_user_by_login(login):
    return User.query.filter(User.login == login).first()

def remove_task(user_id, task_id):
    task = get_task_by_id(task_id, user_id)
    if (task == None):
        return
    db_session.delete(task)

def validate_login(login):
    forbiddenchars = set('@')
    return login.strip() != '' and not any((c in forbiddenchars) for c in login)

def validate_password(password):
    forbiddenchars = set('@')
    return password.strip() != '' and not any((c in forbiddenchars) for c in password)

def validate_task_title(title):
    return title.strip() != ''

def update_task(user_id, task_id, title, description):
    task = get_task_by_id(task_id, user_id)
    if (task == None):
        return None
    task.title = title
    task.description = description
    db_session.commit()
    return task