from . import main
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify
from flask_login import login_required, current_user

from ..models import ArticleType, Article, User, Source,\
    Comment, Menu

from .form import SignInForm, ChangePwdForm, CommonForm
from .. import db
import json

@main.route('/')
def home_page():
    return render_template('index.html')


@main.route('/article/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get_or_404(id)

    if article:
        source = Source.query.get_or_404(article.source_id)
        article.content = str(article.content).split(r'\n')
    else:
        source = Source()

    return render_template('blog_text.html', User=User, article=article, source=source)


@main.route('/content/<int:article_id>')
def get_countent(article_id):
    cont = db.session.query(Comment.content, Comment.timestamp, Comment.avatar_hash, User.username).join(User, User.id==Comment.author_id, isouter=True).filter(Comment.article_id == article_id).all()
    res = []
    for i in cont:
        one = {
            'content': i.content,
            'autor': i.username,
            'time': str(i.timestamp)
        }
        res.append(one)

    return jsonify(json.dumps(res))



