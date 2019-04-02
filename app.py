
# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

sqlite_path = 'db/todo.db'


def get_db_connection():
    connection = sqlite3.connect(sqlite_path)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def index():
    # connection = get_db_connection()
    # cursor = connection.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, name TEXT, number INTEGER, price INTEGER)")
    #
    # cursor.execute("INSERT INTO todo VALUES (1, 'カレー', 2, 300)")
    # cursor.execute("INSERT INTO todo VALUES (2, 'パン', 3, 100)")
    # res = cursor.execute('SELECT * FROM todo')
    # connection.commit()
    # todo_list=res.fetchall()

    return render_template('index1.html')

@app.route("/show", methods=["GET"])
def show_task():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, name TEXT, number INTEGER, price INTEGER)")
    res = cursor.execute('SELECT * FROM todo')
    return render_template('show.html', todo_list=res.fetchall())

@app.route("/choice", methods=["GET","POST"])
def choice_task():
    connection = get_db_connection()
    cursor = connection.cursor()
    choi = cursor.execute('SELECT * FROM todo ORDER BY RANDOM()')
    connection.commit()
    return render_template('index.html', food=choi.fetchone() )


@app.route("/decide", methods=["POST"])
def decide_food():
    food_name = request.form['food_incle']
    food_name = food_name[:-3]
    print(food_name)
    connection = sqlite3.connect(sqlite_path)
    cursor = connection.cursor()
    cursor.execute('UPDATE todo SET number = number - 1 WHERE name = ?',(food_name,))
    connection.commit()
    math_in = cursor.execute('SELECT number FROM todo WHERE name = ?', (food_name, ))
    math_in1 = math_in.fetchone()
    print(math_in1[0])
    if math_in1[0] == 0:
        connection = sqlite3.connect(sqlite_path)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM todo WHERE name = ?', (food_name, ))
        print(food_name + "を削除しました")
        connection.commit()


    return render_template('index.html', decide=food_name, math_out=math_in1[0])

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == 'GET':
        todo = {}
        return render_template('edit.html', type='add', todo=todo)
    else:
        connection = get_db_connection()
        cursor = connection.cursor()
        error = []

        if not request.form['name']:
            error.append('購入したものを入力してください')
        if not request.form['number']:
            error.append('個数を入力してください')

        if error:
            todo = request.form.to_dict()
            return render_template('edit.html', type='add', todo=todo, error_list=error)

        cursor.execute('INSERT INTO todo(name, number, price) VALUES(?, ?, ?)',
                      (request.form['name'],
                       request.form['number'],
                       request.form['price']))

        connection.commit()
        return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM todo WHERE id = ?', (id,))
    connection.commit()
    return redirect(url_for('show_task'))

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    res = cursor.execute('SELECT * FROM todo WHERE id = ? ', (id, ))
    return render_template('edit.html', type='edit', todo=res.fetchone())

# @app.route("/update/<int:id>", methods=["POST"])
# def update_task(id):
#     error = []
#
#     if not request.form['name']:
#         error.append('食品名を入力してください')
#
#     if not request.form['number']:
#         error.append('購入数を入力してください')
#
#     if error:
#         todo = request.form.to_dict()
#         todo['id'] = id
#         return render_template('edit.html', type='edit', todo=todo, error_list=error)
#
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute('UPDATE todo set name = ? , number = ? , price = ? where id = ?',
#                   (request.form['name'],
#                    request.form['number'],
#                    request.form['price'],
#                    id))
#     connection.commit()
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
