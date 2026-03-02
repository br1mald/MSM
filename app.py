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

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.user import user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.template_filter("stars")
    def stars_filter(rating):
        """Convert numeric rating to star string"""
        full_stars = int(rating)
        return "★" * full_stars + "☆" * (5 - full_stars)

    @app.template_filter("schedule_display")
    def schedule_display_filter(schedule):
        """Convert schedule enum to user-friendly French text"""
        schedule_map = {
            "mornings": "Matins",
            "afternoons": "Après-midis",
            "evenings": "Soirs",
            "weekends": "Week-ends",
            "flexible": "Horaires flexibles",
        }
        # Handle both enum and string values
        schedule_value = schedule.value if hasattr(schedule, "value") else str(schedule)
        return schedule_map.get(schedule_value.lower(), schedule_value)

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
