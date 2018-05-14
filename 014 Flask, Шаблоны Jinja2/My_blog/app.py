# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms_alchemy import ModelForm
from datetime import date

app = Flask(__name__, template_folder='templates')
app.config.update(
    DEBUG=True,
    SECRET_KEY='asdfsdfssf asf dsgsdg',

    # Database settings:
    SQLALCHEMY_DATABASE_URI='sqlite:///myblog.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    WTF_CSRF_ENABLED=False
)

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    article_url = db.Column(db.String(350), unique=True, nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.Date, default=date.today)

    def __str__(self):
        return '<Article {}>'.format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    article_id = db.Column(
        db.Integer,
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )
    article = db.relationship(Article, foreign_keys=[article_id, ])
    content = db.Column(db.String(3000), nullable=False)
    data_created = db.Column(db.Date, default=date.today)

    def __str__(self):
        return '<Comment {} to Article:{}>'.format(self.title, self.article.title)


class ArticleForm(ModelForm):
    class Meta:
        model = Article


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        include = [
            'article_id',
        ]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = ArticleForm(request.form)
        if form.validate():
            article = Article(**form.data)
            db.session.add(article)
            db.session.commit()

            article.article_url = str(article.id)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('errors.html', errors_text=str(form.errors))

    all_articles = Article.query.all()

    return render_template('index.html', articles=all_articles, date_today=date.today())


@app.route('/article/<article_url>', methods=['GET', 'POST'])
def new_article(article_url):
    form = CommentForm(request.form)
    article = Article.query.filter_by(article_url=article_url).first()
    if request.method == 'POST':
        print(request.form)
        if form.validate():
            comm = Comment(**form.data)
            db.session.add(comm)
            db.session.commit()
        else:
            return render_template('errors.html', errors_text=str(form.errors))

    all_comments = Comment.query.filter_by(article=article)
    return render_template('article.html', comments=all_comments, article=article,
                           date_today=date.today())


@app.route('/delete')
def delete():
    Article.query.delete()
    Comment.query.delete()
    db.session.commit()
    return render_template('report.txt')


if __name__ == '__main__':
    db.create_all()

    app.run()
