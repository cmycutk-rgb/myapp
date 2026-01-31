#Flaskアプリ本題を組み立てる場所
#アプリの初期設定・ルーティング（URL登録）をまとめるため

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'any-random-string-12345'

    from .routes import pages
    app.register_blueprint(pages.bp)

    return app