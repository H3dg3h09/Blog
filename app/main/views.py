#-*- coding:UTF-8 -*-
from . import main
from flask import render_template, redirect, flash, \
    url_for, request, current_app
from flask_login import login_required, current_user

from ..models import ArticleType, Article, User, Source,\
    Comment, Menu

from .form import SignInForm, ChangePwdForm, CommonForm
from .. import db


@main.route('/')
def home_page():
    return render_template('index.html')


@main.route('/article/<int:id>', methods=['GET'])
def article_content(id):
    article = Article.query.get_or_404(id)

    if article:
        source = Source.query.get_or_404(article.source_id)
        article.content = str(article.content).split(r'\n')
    else:
        source = Source()

    return render_template('blog_text.html', User=User, article=article, source=source)

