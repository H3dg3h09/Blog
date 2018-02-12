#!/usr/bin/env python
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import Article, ArticleType, User,\
    Menu, Comment, BlogInfo, Source

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def deploy(deploy_type):
    from flask_migrate import upgrade
    from app.models import Article, ArticleType, User,\
        Menu, Comment, BlogInfo, Source

    # upgrade database to the latest version
   # upgrade()

    if deploy_type == 'product':
        # step_1:insert basic blog info
        BlogInfo.insert_blog_info()
        # step_2:insert admin account
        User.insert_admin(email='blog_test@163.com', username='admin', password='admin')
        # step_3:insert system default setting
        # ArticleTypeSetting.insert_system_setting()
        # step_4:insert default article sources
        # Source.insert_sources()
        # step_5:insert default articleType
        ArticleType.insert_system_articleType()
        # step_6:insert system plugin
        # Plugin.insert_system_plugin()
        # step_7:insert blog view
        # BlogView.insert_view()

    # You must run `python manage.py deploy(product)` before run `python manage.py deploy(test_data)`
    if deploy_type == 'test_data':
        # step_1:insert navs
        Menu.insert_menus()
        # step_2:insert articleTypes
        ArticleType.insert_articleTypes()
        Source.insert_sources()
        # generate User
        User.generate_fake(100)
        # step_3:generate random articles
        Article.generate_fake(100)
        # step_4:generate random comments
        Comment.generate_fake(300)
        # step_5:generate random replies
        # Comment.generate_fake_replies(100)
        # step_4:generate random comments
        # Comment.generate_fake(300)

@manager.command
def init_db():
    db.create_all(app=app)



if __name__ == '__main__':
    manager.run()

