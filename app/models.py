# -*- coding:utf-8 -*-
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
import os



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    @staticmethod
    def insert_admin(email, username, password):
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise ArithmeticError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()


    def set_url(self, size=40, default='identicon', rating='g'):
        url = os.environ.get('WEB_RUL','http://127.0.0.1') + \
              os.environ.get('WEB_PORT', '5000')

        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()

        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()

        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.name.full_name(),
                     password=generate_password_hash(forgery_py.basic.password()))
            db.session.add(u)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def __repr__(self):
        return '<User %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ArticleType(db.Model):
    __tablename__ = 'articleTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    introduction = db.Column(db.Text, server_default=None)
    articles = db.relationship('Article', backref='articleType', lazy='dynamic')
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    # setting_id = db.Column(db.Integer, db.ForeignKey('articleTypeSettings.id'))

    @staticmethod
    def insert_system_articleType():
        articleType = ArticleType(name=u'未分类',
                                  introduction=u'系统默认分类，不可删除。')
        db.session.add(articleType)
        db.session.commit()

    @staticmethod
    def insert_articleTypes():
        articleTypes = ['Python', 'Java', 'JavaScript', 'Django',
                        'CentOS', 'Ubuntu', 'MySQL', 'Redis',
                        u'Linux成长之路', u'Linux运维实战', u'其它',
                        u'思科网络技术', u'生活那些事', u'学校那些事',
                        u'感情那些事', 'Flask']
        for name in articleTypes:
            articleType = ArticleType(name=name)
            db.session.add(articleType)
        db.session.commit()

    @property
    def is_protected(self):
        if self.setting:
            return self.setting.protected
        else:
            return False

    @property
    def is_hide(self):
        if self.setting:
            return self.setting.hide
        else:
            return False

    def __repr__(self):
        return '<ArticleType %r>' % self.name


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True,
                            default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True,
                            default=datetime.utcnow)
    num_of_view = db.Column(db.Integer, default=0)
    articleType_id = db.Column(db.Integer, db.ForeignKey('articleTypes.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        articleType_count = ArticleType.query.count()
        source_count = Source.query.count()

        for i in range(count):
            aT = ArticleType.query.offset(randint(0, articleType_count - 1)).first()
            s = Source.query.offset(randint(0, source_count - 1)).first()
            a = Article(title=forgery_py.lorem_ipsum.title(randint(3, 5)),
                        content=forgery_py.lorem_ipsum.sentences(randint(15, 35)),
                        summary=forgery_py.lorem_ipsum.sentences(randint(2, 5)),
                        num_of_view=randint(100, 15000),
                        articleType=aT, source=s)
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_view(article, db):
        article.num_of_view += 1
        db.session.add(article)
        db.session.commit()
    def __repr__(self):
        return '<Article %r>' % self.title


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer)
    author_email = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.today)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    avatar_hash = db.Column(db.String(32))
    disabled = db.Column(db.Boolean, default=False)
    comment_type = db.Column(db.String(64), default='comment')
    reply_to = db.Column(db.String(128), default='notReply')

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        if self.author_email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.author_email.encode('utf-8')).hexdigest()

    def set_url(self, size=40, default='identicon', rating='g'):

        url = os.environ.get('WEB_URL', '127.0.0.1') + \
            os.environ.get('WEB_PORT', 5000)

        hash = self.avatar_hash or hashlib.md5(
            self.author_email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        article_count = Article.query.count()
        for i in range(count):
            a = Article.query.offset(randint(0, article_count - 1)).first()
            c = Comment(content=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
                        timestamp=forgery_py.date.date(True),
                        author_id = randint(0,100),
                        author_email=forgery_py.internet.email_address(),
                        article=a)
            db.session.add(c)
        try:
            db.session.commit()
        except Exception as e:
            print("error:\n{}".format(e))
            db.session.rollback()

    # @staticmethod
    # def generate_fake_replies(count=100):
    #     from random import seed, randint
    #     import forgery_py
    #
    #     seed()
    #     comment_count = Comment.query.count()
    #     for i in range(count):
    #         followed = Comment.query.offset(randint(0, comment_count - 1)).first()
    #         c = Comment(content=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
    #                     author_email=forgery_py.internet.email_address(),
    #                     timestamp=forgery_py.date.date(True),
    #                     author_id = randint(0,100),
    #                     article=followed.article, comment_type='reply',
    #                     )
    #         f = Follow(follower=c, followed=followed)
    #         db.session.add(f)
    #         db.session.commit()

    def is_reply(self):
        if self.followed.count() == 0:
            return False
        else:
            return True
    # to confirm whether the comment is a reply or not

    def followed_name(self):
        if self.is_reply():
            return self.followed.first().followed.author_name


class Menu(db.Model):
    """导航栏内容"""
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    types = db.relationship('ArticleType', backref='menu', lazy='dynamic')
    order = db.Column(db.Integer, default=0, nullable=False)

    def sort_delete(self):
        for menu in Menu.query.order_by(Menu.order).offset(self.order).all():
            menu.order -= 1
            db.session.add(menu)

    @staticmethod
    def insert_menus():
        menus = ['HTML5', 'Linux', 'JAVA', 'PHP',
                 'Python', 'JavaScript', 'C++', 'Others']

        for name in menus:
            menu = Menu(name=name)
            db.session.add(menu)
            db.session.commit()
            menu.order = menu.id
            db.session.add(menu)
            db.session.commit()

    @staticmethod
    def return_menus():
        menus = [(m.id, m.name) for m in Menu.query.all()]
        menus.append((-1, u'不选择导航（该分类将单独成一导航）'))
        return menus

    def __repr__(self):
        return '<Menu %r>' % self.name


class BlogInfo(db.Model):
    __tablename__ = 'blog_info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    signature = db.Column(db.Text)
    navbar = db.Column(db.String(64))

    @staticmethod
    def insert_blog_info():
        blog_info = BlogInfo(title=u'Blog-FLV',
                             signature=u'Created By FLV',
                             navbar='inverse')
        db.session.add(blog_info)
        db.session.commit()


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='source', lazy='dynamic')

    @staticmethod
    def insert_sources():
        sources = (u'原创',
                   u'转载',
                   u'翻译')
        for s in sources:
            source = Source.query.filter_by(name=s).first()
            if source is None:
                source = Source(name=s)
            db.session.add(source)
        db.session.commit()

    def __repr__(self):
        return '<Source %r>' % self.name