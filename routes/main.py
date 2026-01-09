from flask import Blueprint, render_template

# will need to import jsonify, request and maybe joinedload late, depending

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/profile")
def profile():
    return render_template("profile.html")
