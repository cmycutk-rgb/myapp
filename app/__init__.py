from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.pages import bp as pages_bp
    app.register_blueprint(pages_bp)

    return app