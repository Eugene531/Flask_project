from flask import Flask, render_template, request, flash, g, abort
import sqlite3
import os

from FDataBase import FDataBase

# config
DATABASE = 'flsite.db'
DEBUG = True
SECRET_KEY = 'qiRuYh34u#$%^@!#weyafg35#%$'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 0:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Error adding a message', category='error')
            else:
                flash('A message was added successfully', category='success')
        else:
            flash('Error adding a message', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Adding a message")


@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route('/')
def home():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('home.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


if __name__ == '__main__':
    create_db()
    app.run()
