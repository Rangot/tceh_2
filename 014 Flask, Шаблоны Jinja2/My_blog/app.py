# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms_alchemy import ModelForm

app = Flask(__name__, template_folder='templates')
app.config.update(
    DEBUG=True,
    SECRET_KEY='asdfsdfssf asf dsgsdg',

    # Database settings:
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    WTF_CSRF_ENABLED=False
)

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    article_data = db.Column(db.String(3000), nullable=False)

    def __str__(self):
        return '<Article {}>'.format(self.article_data)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    article_id = db.Column(
        db.Integer,
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )
    article = db.relationship(Article, foreign_keys=[article_id, ])

    data = db.Column(db.String(120))

    def __str__(self):
        return '<Comment {}>'.format(self.data)


class ArticleForm(ModelForm):
    class Meta:
        model = Article


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        include = [
            'article_id',
        ]


@app.route('/article', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = ArticleForm(request.form)
        if form.validate():
            article = Article(**form.data)
            db.session.add(article)
            db.session.commit()

            flash('Article created!')
        else:
            flash('Article is not valid! Article was not created.')
            flash(str(form.errors))

    articles = Article.query.all()
    for article in articles:
        art_id = article.id
        article = Article.query.filter_by(id=art_id).first()
        print(article.id, article.title, article)

    return render_template('report.txt', articles=articles)

# app.jinja_env.globals.update(some_var='value')


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate():
            comm = Comment(**form.data)
            db.session.add(comm)
            db.session.commit()

            flash('Comment created!')
        else:
            flash('Comment is not valid! Comment was not created.')
            flash(str(form.errors))

    articles = Article.query.all()
    comments = Comment.query.all()
    return render_template('report.txt', comments=comments, articles=articles)


@app.route('/delete')
def delete():
    Article.query.delete()
    Comment.query.delete()
    db.session.commit()
    return render_template('report.txt')


if __name__ == '__main__':
    db.create_all()

    app.run()

'''
    a = Article(title='Article')
    db.session.add(a)

    c = Comment(article=a, data='some_data')

    db.session.add(c)
    db.session.commit()


    all_comments = Comment.query.all()
    for comment in all_comments:
        print(comment.id, comment.data)
        print(comment.id, comment.first.name, comment.first.id)
        print()
'''