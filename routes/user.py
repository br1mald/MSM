from flask import Blueprint, render_template, session
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models import Employer, User, Worker, db

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return "User id is required", 400

    stmt = select(User).filter_by(user_id=User.id)
    user = db.session.execute(stmt).scalars().first()

    return render_template("profile.html", user=user)


@user_bp.route("/history")
def history():
    user_id = session.get("user_id")
    if not user_id:
        return "User_id is required", 400

    stmt = (
        select(User)
        .filter_by(id=user_id)
        .options(
            joinedload(User.worker_profile).joinedload(Worker.employments),
            joinedload(User.employer_profile).joinedload(Employer.employments),
        )
    )
    user = db.session.execute(stmt).scalars().first()
    if not user:
        return "User not found", 404

    employments = []

    if user.worker_profile:
        employments.extend(user.worker_profile.employments)
    if user.employer_profile:
        employments.extend(user.employer_profile.employments)

    employments.sort(key=lambda e: e.created_at, reverse=True)

    return render_template("history.html", employments=employments, user=user)


@user_bp.route("/reviews")
def reviews():
    user_id = session.get("user_id")
    if not user_id:
        return "User id is needed", 400

    stmt = (
        select(User)
        .filter_by(id=user_id)
        .options(
            joinedload(User.worker_profile).joinedload(Worker.ratings),
            joinedload(User.employer_profile).joinedload(Employer.ratings),
        )
    )
    user = db.session.execute(stmt).scalars().first()

    if not user:
        return "User not found", 404

    worker_average = None
    employer_average = None

    if user.worker_profile:
        worker_ratings = user.worker_profile.ratings
        if worker_ratings:
            worker_average = sum(worker_ratings) / len(worker_ratings)

    if user.employer_profile:
        employer_ratings = user.employer_profile.ratings
        if employer_ratings:
            employer_average = sum(employer_ratings) / len(employer_ratings)

    return render_template(
        "reviews.html",
        user=user,
        worker_average=worker_average,
        employer_average=employer_average,
    )
