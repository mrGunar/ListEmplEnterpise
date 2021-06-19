import sqlite3
import os

from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from FDataBase import FDataBase

DATABASE = 'dbase.db'
SECRET_KEY = '325gid8gdwsgiwfied234fj094fwje412if82334g8fi3wjgfewr98fg0dwgvdvhjsdvk'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'dbase.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/departament", methods=['GET', 'POST'])
def departament():
    if not session.get('username', None):
        return redirect(url_for('authorization'))
    context = {
        'departments': dbase.getDepartments(),
    }
    if request.method == 'GET':
        return render_template('departament.html', **context)
    else:
        form_name = request.form['title']
        form_parent = request.form['parent']
        if form_name:
            dbase.addDepartment(form_name, form_parent)
            flash('Отдел добавлен', category='success')
            return render_template('departament.html', **context)
        else:
            flash('Ошибка при добавлении', category='error')
            return render_template('departament.html', **context)


@app.route("/person", methods=['GET', 'POST'])
def person():
    if not session.get('username', None):
        return redirect(url_for('authorization'))
    context = {
        'positions': dbase.getPosition(),
        'persons': dbase.getPersons(),
        'departments': dbase.getDepartments()
    }
    if request.method == 'GET':
        return render_template('person.html', **context)
    else:
        form_name = request.form['username']
        form_dep = request.form['department']
        form_pos = request.form['position']
        if form_name:
            res = dbase.addPerson(form_name, form_dep, form_pos)
            if res:
                flash('Сотрудник добавлен', category='success')
            else:
                flash('Ошибка при добавлении', category='error')
        else:
            flash('Имя не может быть пустым', category='error')
        return render_template('person.html', **context)


@app.route("/statistic", methods=['GET', 'POST'])
def statistic():
    if not session.get('username', None):
        return redirect(url_for('authorization'))
    arr = []  # список из выбранного отдела и его дочерних отделов
    data = {}  # словарь ключ - название отдела, значение - список сотрудников

    def get_child(n: int) -> None:
        for ch in dbase.getDepartmentChild(n):
            arr.append(ch)
            if dbase.getDepartmentChild(ch['id']):
                get_child(ch['id'])

    if request.method == 'POST':
        form_dep_id = request.form['departments']
        dep = dbase.getDepartment(form_dep_id)
        dep_id = dep[0]
        arr.append(dep)
        get_child(dep_id)

        for el in arr:
            data[el['title']] = []
            pers = dbase.getPersonsFromDepartments(el['id'])
            if pers:
                for per in pers:
                    data[el['title']].append(per['name'])

    context = {
        'departments': dbase.getDepartments(),
        'data': data,
    }
    return render_template('statistic.html', **context)


@app.route("/setting")
def setting():
    if not session.get('username', None):
        return redirect(url_for('authorization'))
    arr = {}
    for person in dbase.getPersons():
        pos_title = dbase.getPersonPosition(person['position_id'])[0]['title']
        dep_title = dbase.getPersonDepartments(person['department_id'])
        if not dep_title:
            dep_title = 'нет отдела'
            arr[person['name']] = [dep_title]
        else:
            arr[person['name']] = [dep_title[0]['title']]

        arr[person['name']].append(pos_title)

    context = {
        'persons': dbase.getPersons(),
        'arrs': arr,
    }
    return render_template('setting.html', **context)


@app.route("/setting/<username>", methods=["GET", "POST"])
def change_user(username):
    if not session.get('username', None):
        return redirect(url_for('authorization'))
    current_user = dbase.getPerson(username)
    current_pos = current_user['position_id']
    current_dep = current_user['department_id']

    if current_dep:
        dep = dbase.getPersonDepartments(current_dep)[0]['title']
    else:
        dep = 'Нет отдела'

    context = {
        'username': username,
        'department': dep,
        'position': dbase.getPersonPosition(current_pos)[0]['title'],
        'positions': dbase.getPosition(),
        'departments': dbase.getDepartments()
    }
    if request.method == "POST":
        pk = current_user['id']
        form_name = request.form['user']
        form_pos = request.form['change-pos']
        form_dep = request.form['change-dep']
        print(pk, form_name, form_pos, form_dep)
        dbase.updatePerson(pk, form_name, form_pos, form_dep)
        return redirect(url_for('change_user', username=form_name))

    return render_template('change_user_profile.html', **context)


@app.route("/setting/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    if not session.get('username', None):
        return redirect(url_for('authorization'))
    context = {
        'user': username,
    }
    if request.method == "POST":
        dbase.deletePerson(username)
        return redirect(url_for('setting'))
    return render_template('delete_user.html', **context)


@app.route("/authorization", methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        name = request.form['username']
        pas = request.form['password']
        if pas == '12345':
            session['username'] = name
            return redirect(url_for('index'))
        else:
            flash('Неверный пароль', category='error')
    return render_template('authorization.html')


@app.route('/logout')
def logout():
    if session.get('username', None):
        session['username'] = []
    return render_template('authorization.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
