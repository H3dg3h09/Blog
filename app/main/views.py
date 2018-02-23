from . import main
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify, session

from flask_login import login_user, login_required, logout_user
from ..models import ArticleType, Article, User, Source,\
    Comment, Menu

from .form import SignInForm, ChangePwdForm, CommonForm, LoginForm
from .. import db, login_manager

#
# @main.route('/')
# def home_page():
#     return render_template('index.html')

@main.route('/')
def home_page():

    page = request.args.get('page', 1, type=int)
    article_type = request.args.get('type', type=int)
    article_source = request.args.get('source', type=int)

    data = db.session.query(Article.id, Article.title,Article.create_time, Article.summary,
                            Article.num_of_view, ArticleType.name.label('article_name'),
                            Source.name.label('source_name')).\
        join(ArticleType, ArticleType.id == Article.articleType_id, isouter=True).\
        join(Source, Source.id == Article.source_id, isouter=True)

    if article_type:
        data = data.filter(Article.articleType_id == article_type)
    if article_source:
        data = data.filter(Article.source_id == article_source)

    data = data.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)

    return render_template('index.html', articles=data, currentPage=data.page, totalPages=data.total)


@main.route('/article_list', methods=['GET'])
def get_article_list():
    """index article list"""
    page = request.args.get('page', 1, type=int)
    article_type = request.args.get('type' ,type=int)
    article_source = request.args.get('source', type=int)

    data = db.session.query(Article.title, Article.summary,
                            Article.create_time, Article.update_time, Article.id,
                            Article.num_of_view,
                            ArticleType.name.label('type_name'),
                            Source.name.label('source_name'))

    if article_type:
        data = data.filter(Article.articleType_id == article_type)
    if article_source:
        data = data.filter(Article.source_id == article_source)

    data = data.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)

    res = []

    for i in data.items:
        one = {
            'id': i.id,
            'title': i.title,
            'summary': i.summary,
            'create_time': i.create_time,
            'view_num': i.num_of_view,
            'update_time': i.update_time,
            'type_name': i.type_name,
            'source_name': i.source_name,
        }
        res.append(one)
    dic_res = {'data': res,
               'currentPage':data.page,
               'totalPages': data.total}
    return jsonify(dic_res)


@main.route('/article/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)

    if article:
        source = Source.query.get_or_404(article.source_id)
        article.content = str(article.content).split(r'\n')
    else:
        return redirect('/')

    # article_id = request.args.get('article_id')
    com = db.session.query(Comment.content, Comment.timestamp, Comment.avatar_hash, User.username).join(User,
                                                                                                         User.id == Comment.author_id,
                                                                                                         isouter=True).filter(
        Comment.article_id == article_id).all()
    for i in com:
        print(i.content)

    return render_template('blog_text.html', User=User, article=article, source=source, com=com)


@main.route('/comment', methods=['GET', 'POST'])
def get_comment():
    article_id = request.args.get('article_id')
    cont = db.session.query(Comment.content, Comment.timestamp, Comment.avatar_hash, User.username).join(User, User.id==Comment.author_id, isouter=True).filter(Comment.article_id == article_id).all()



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
