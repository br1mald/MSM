from flask import Blueprint, jsonify, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")
