from . import main
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify, session

from flask_login import login_user, login_required, logout_user
from ..models import ArticleType, Article, User, Source,\
    Comment, Menu

from .form import SignInForm, ChangePwdForm, CommonForm, LoginForm
from .. import db, login_manager


@main.route('/')
def home_page():
    return render_template('index.html')


@main.route('/article_list', methods=['GET'])
def get_article_list():
    """index article list"""
    page = request.args.get('page', 1, type=int)
    article_type = request.args.get('type' ,type=int)
    article_source = request.args.get('source', type=int)

    data = Article.query
    if article_type:
        data = data.filter(Article.articleType_id == article_type)
    if article_source:
        data = data.filter(Article.source_id == article_source)

    data = data.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)

    res = []
    for i in data.items:
        one = {
            'title': i.title,
            'summary': i.summary,
            'create_time': i.create_time,
            'view_num': i.num_of_view,
            'update_time': i.update_time,
            'articleType_id': i.articleType_id,
            'source_id': i.source_id
        }
        res.append(one)

    return jsonify(res)


@main.route('/article/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get_or_404(id)

    if article:
        source = Source.query.get_or_404(article.source_id)
        article.content = str(article.content).split(r'\n')
    else:
        source = Source()

    return render_template('blog_text.html', User=User, article=article, source=source)


@main.route('/content', methods=['GET', 'POST'])
def get_countent():
    article_id = request.args.get('article_id')
    cont = db.session.query(Comment.content, Comment.timestamp, Comment.avatar_hash, User.username).join(User, User.id==Comment.author_id, isouter=True).filter(Comment.article_id == article_id).all()
    res = []
    for i in cont:
        one = {
            'content': i.content,
            'autor': i.username,
            'time': str(i.timestamp)
        }
        res.append(one)

    return jsonify(res)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@main.route('/login', methods=["POST"])
def login():
    """Login in"""
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email", type=str, default=None)
        password = request.form.get("password", type=str, default=None)
        remember_me = request.form.get('remember_me', False)

        user = User.query.filter_by(email=email).first()
        is_right = user.check_password(password) if user else False

        if is_right:
            #into session
            login_user(user, remember=remember_me)

        res = {'success': is_right,
               'message': 'Welcome, {}'.format(user.username) if is_right else 'Your email or password is wrong!'}

        return jsonify(res)


@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@main.route('/signin', methods=['POST'])
def signin():
    pass
