# -*- coding: utf-8 -*-

from datetime import date

from app import db


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(90), unique=True, nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self):
        return '<Post: {}, user_id: {}>'.format(self.author, self.id)
