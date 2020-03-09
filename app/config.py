import os


basedir = os.path.dirname(os.path.abspath(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = '<Your secret key>'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


title = 'Welcome to SingleSite'

article_range = (10, 140)

posts_per_page = 3
