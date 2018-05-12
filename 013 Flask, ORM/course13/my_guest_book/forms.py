# -*- coding: utf-8 -*-

from wtforms_alchemy import ModelForm

from models import Guest


class PostForm(ModelForm):
    class Meta:
        model = Guest
        include = ['id']