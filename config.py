import os
basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['DATABASE_URL'] = 'mysql+pymysql://root:root@localhost:3306/blog'
os.environ['WEB_RUL'] = 'http://127.0.0.1'
os.environ['WEB_PORT'] = '5000'

class Config():
    # DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    print('config'+os.environ.get('DATABASE_URL', ''))
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    @staticmethod
    def init_app(app):
        pass
