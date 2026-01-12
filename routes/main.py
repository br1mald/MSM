from flask import Blueprint, render_template

# will need to import jsonify, request and maybe joinedload late, depending

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/search")
def search():
    return render_template("search.html")


@main_bp.route("/log-in")
def log_in():
    return render_template("signin.html")


@main_bp.route("/sign-up")
def sign_up():
    return render_template("signup.html")
