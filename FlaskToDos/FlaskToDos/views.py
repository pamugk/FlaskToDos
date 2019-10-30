"""
Routes and views for the flask application.
"""

from flask import Flask, render_template, request, redirect, url_for, session
from FlaskToDos import app
from FlaskToDos.logic import *

@app.route('/about')
def about():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = get_user_by_id(user_id)
    return render_template('pages/about.html', page_title='О сайте | Манагер задач', user=user)

@app.route('/')
@app.route('/home')
def home():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = get_user_by_id(user_id)
    return render_template('pages/index.html', page_title='Манагер задач', user=user)

@app.route('/login', methods=['GET'])
def login():
    return render_template('pages/login.html', page_title='Вход | Манагер задач')

@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход | Манагер задач'
    
    if not request.form['login']:
        return render_template('pages/login.html', page_title=page_title, error="Требуется ввести логин")
    
    user = get_user_by_login(request.form['login'])
    if not user:
        return render_template('pages/login.html', page_title=page_title, error="Пользователя с таким логином не существует")
   
    if not request.form['password'] or request.form['login'].strip() == '':
        return render_template('pages/login.html', page_title=page_title, error="Требуется ввести пароль")
    
    if not check_user_password(user, request.form['password']):
        return render_template('pages/login.html', page_title=page_title, error="Неверный пароль")
    
    session['user_id'] = user.id
    return redirect(url_for('home'))

@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация | Манагер задач')

@app.route('/registration', methods=['POST'])
def registration_action():
    page_title = 'Регистрация | Манагер задач'
    
    if not request.form['login']:
        return render_template('pages/registration.html', page_title=page_title, error="Требуется ввести логин")
   
    if not validate_login(request.form['login']):
        return render_template('pages/registration.html', page_title=page_title, error="Введённый логин пуст или содержит запрещённые символы")
    
    if get_user_by_login(request.form['login']):
        return render_template('pages/registration.html', page_title=page_title, error="Этот логин уже занят")
    
    if not request.form['password']:
        return render_template('pages/registration.html', page_title=page_title, error="Требуется ввести пароль")
    
    if not validate_password(request.form['password']):
        return render_template('pages/registration.html', page_title=page_title, error="Введённый пароль пуст или содержит запрещённые символы")

    if not request.form['password2']:
        return render_template('pages/registration.html', page_title=page_title, error="Требуется ввести повтор пароля")
    
    if request.form['password'] != request.form['password2']:
        return render_template('pages/registration.html', page_title=page_title, error="Пароли не совпадают")
    
    add_user(request.form['login'], request.form['password'])
    return redirect(url_for('home'))

@app.route('/tasks', methods=['GET'])
def tasks(): 
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    tasks = get_tasks_by_user_id(user_id)
    return render_template('pages/tasks.html', page_title='Задачи | Манагер задач', user=user, tasks=tasks)

@app.route('/tasks', methods=['POST'])
def tasks_action():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    error = None
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    tasks = get_tasks_by_user_id(user_id)

    if not request.form['title']:
        eror="Требуется ввести заголовок задачи"
    elif not validate_task_title(request.form['title']):
        error="Заголовок задачи пуст или содержит запрещённые символы"
    elif get_task_by_title(request.form['title'], session['user_id']):
        error="Задача с таким заголовком уже используется"
    else:
        add_task(session['user_id'], request.form['title'], request.form['description'])

    return render_template('pages/tasks.html', page_title='Задачи | Манагер задач', user=user, error=error, tasks=tasks)

@app.route('/tasks/<id>', methods=['GET'])
def task(id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    task = get_task_by_id(id)
    return render_template('pages/task.html', page_title='Задача | Манагер задач', user=user, task=task)

@app.route('/tasks/<id>', methods=['POST'])
def task_update(id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    error = None
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    task = get_task_by_id(id)

    if not task:
        eror="Задача не найдена"
    elif not request.form['title']:
        eror="Требуется ввести заголовок задачи"
    elif not validate_task_title(request.form['title']):
        error="Заголовок задачи пуст или содержит запрещённые символы"
    else:
        someTask = get_task_by_title(request.form['title'], session['user_id'])
        if someTask.id != task.id:
            error="Задача с таким заголовком уже используется"
        else:
            task = update_task(user_id, task, request.form['title'], request.form['description'])
    if not error:
        return redirect(url_for('tasks'))
    else:
        return render_template('pages/task.html', page_title='Задача | Манагер задач', user=user, error=error, task=task)

@app.route('/tasks/<id>/delete', methods=['POST'])
def task_remove(id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    remove_task(user_id, id)
    tasks = get_tasks_by_user_id(user_id)
    return render_template('pages/tasks.html', page_title='Задачи | Манагер задач', user=user, tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('home'))
