# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy

import config as config

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    from models import Guest

    posts = Guest.query.all()
    for post in posts:
        user_id = post.id
        print(user_id)

    return render_template('home.txt', posts=posts)


@app.route('/create', methods=['POST'])
def create():
    from models import Guest
    from forms import PostForm

    if request.method == 'POST':
        print(request.form)
        form = PostForm(request.form)

        if form.validate():
            post = Guest(**form.data)
            db.session.add(post)
            db.session.commit()

            flash('Post created!')
        else:
            flash('Form is not valid! Post was not created.')
            flash(str(form.errors))

    return index()


if __name__ == '__main__':
    from models import *
    db.create_all()

    posted = Guest.query.all()
    print(list(map(str, posted)))

    app.run()
