from flask import Blueprint, render_template, request
from sqlalchemy import select

# from sqlalchemy.orm import joinedload
from models import Post, db

# will need to import jsonify, request and maybe joinedload later, depending

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/search")
def search():
    q = request.args.get("q")
    if not q:
        return "Query is needed", 400

    stmt = (
        select(Post)
        .where(Post.description.like(q) or Post.title.like(q))
        .limit(20)
        .order_by(Post.created_at.desc())
    )

    results = db.session.execute(stmt).scalars().all()

    return render_template("search.html", results=results)


@main_bp.route("/log-in")
def log_in():
    return render_template("signin.html")


@main_bp.route("/sign-up")
def sign_up():
    return render_template("signup.html")
