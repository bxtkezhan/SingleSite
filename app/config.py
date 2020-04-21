import os


basedir = os.path.dirname(os.path.abspath(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = '<Your secret key>'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


title = 'Welcome to SingleSite'

post_title_range = (1, 32)
post_body_range  = (32, 1024)
post_categories = [
    'python',
    'c/c++',
]

posts_per_page = 3
