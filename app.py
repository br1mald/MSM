from flask import Flask
from flask_session import Session

from models import db


def create_app():
    app = Flask("__name__")

    app.config["SECRET_KEY"] = ""
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///msm.db"

    db.init_app(app)
    Session(app)

    from routes.user import user_bp

    # from routes.auth import auth_bp
    app.register_blueprint(user_bp)
    # app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
