from flask import Blueprint, render_template

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile")
def profile():
    return render_template("profile.html")


@user_bp.route("/history")
def history():
    return render_template("history.html")


@user_bp.route("/reviews")
def reviews():
    return render_template("reviews.html")
