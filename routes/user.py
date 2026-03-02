from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models import (
    Employer,
    Employment,
    Review,
    ReviewType,
    Schedule,
    User,
    UserStatus,
    Worker,
    db,
)
from utils import login_required

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile")
@login_required
def profile():
    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id:
        return "User id is required", 400

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

    if role == "worker":
        return render_worker_dashboard(user)
    else:
        return render_employer_dashboard(user)


def render_worker_dashboard(user):
    worker = user.worker_profile
    if not worker:
        return redirect(url_for("user.complete_profile"))

    employments = worker.employments
    total_employments = len(employments)

    stmt = (
        select(Review)
        .filter_by(reviewee_id=user.id, review_type=ReviewType.WORKER)
        .order_by(Review.created_at.desc())
        .limit(5)
    )
    recent_reviews = db.session.execute(stmt).scalars().all()

    return render_template(
        "worker_dashboard.html",
        user=user,
        worker=worker,
        employments=employments,
        total_employments=total_employments,
        recent_reviews=recent_reviews,
    )


def render_employer_dashboard(user):
    employer = user.employer_profile
    if not employer:
        return redirect(url_for("user.complete_profile"))

    employments = employer.employments

    return render_template(
        "employer_dashboard.html",
        user=user,
        employer=employer,
        employments=employments,
    )


@user_bp.route("/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():
    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id or not role:
        flash("Session invalide")
        return redirect(url_for("auth.login"))

    stmt = (
        select(User)
        .filter_by(id=user_id)
        .options(
            joinedload(User.worker_profile),
            joinedload(User.employer_profile),
        )
    )
    user = db.session.execute(stmt).scalars().first()

    if not user:
        return "User not found", 404

    if request.method == "POST":
        if role == "worker":
            return update_worker_profile(user)
        else:
            return update_employer_profile(user)

    return render_template("complete_profile.html", user=user, role=role)


def update_worker_profile(user):
    worker = user.worker_profile

    if not worker:
        flash("Profil introuvable")
        return redirect(url_for("user.profile"))

    desired_salary = request.form.get("desired_salary", type=int) or 0
    competences_str = request.form.get("competences", "")
    description = request.form.get("description", "")
    schedule = request.form.get("schedule", "flexible")

    competences = [c.strip() for c in competences_str.split(",") if c.strip()]

    try:
        schedule_enum = Schedule[schedule.upper()]
    except KeyError:
        schedule_enum = Schedule.FLEXIBLE

    worker.desired_salary = desired_salary
    worker.competences = competences
    worker.description = description
    worker.preferred_schedule = schedule_enum

    db.session.commit()
    flash("Profil mis à jour avec succès!", "success")
    return redirect(url_for("user.profile"))


def update_employer_profile(user):
    employer = user.employer_profile

    if not employer:
        flash("Profil introuvable")
        return redirect(url_for("user.profile"))

    address = request.form.get("address", "")
    square_footage = request.form.get("square_footage", type=int) or 100

    employer.address = address
    employer.square_footage = square_footage

    db.session.commit()
    flash("Profil mis à jour avec succès!", "success")
    return redirect(url_for("user.profile"))


@user_bp.route("/employment/<int:employment_id>/review", methods=["POST"])
@login_required
def add_review(employment_id):
    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id:
        flash("Session invalide")
        return redirect(url_for("auth.login"))

    stmt = select(Employment).filter_by(id=employment_id)
    employment = db.session.execute(stmt).scalars().first()

    if not employment:
        flash("Emploi introuvable")
        return redirect(url_for("user.profile"))

    if role == "employer" and employment.employer.user_id != user_id:
        flash("Non autorisé")
        return redirect(url_for("user.profile"))

    rating = request.form.get("rating", type=float)
    comment = request.form.get("comment", "")

    if not rating or rating < 1 or rating > 5:
        flash("Note invalide (1-5)")
        return redirect(url_for("user.profile"))

    existing_review = (
        db.session.execute(
            select(Review).filter_by(employment_id=employment_id, reviewer_id=user_id)
        )
        .scalars()
        .first()
    )

    if existing_review:
        flash("Vous avez déjà laissé un avis pour cet emploi")
        return redirect(url_for("user.profile"))

    if role == "employer":
        reviewee_id = employment.worker.user_id
        review_type = ReviewType.WORKER
    else:
        reviewee_id = employment.employer.user_id
        review_type = ReviewType.EMPLOYER

    review = Review(
        employment_id=employment_id,
        reviewer_id=user_id,
        reviewee_id=reviewee_id,
        review_type=review_type,
        rating=rating,
        comment=comment,
    )

    db.session.add(review)

    if review_type == ReviewType.WORKER:
        worker = employment.worker
        worker.add_rating(rating)
    else:
        employer = employment.employer
        employer.add_rating(rating)

    db.session.commit()
    flash("Avis ajouté avec succès!", "success")
    return redirect(url_for("user.profile"))


@user_bp.route("/employment/<int:employment_id>/cancel", methods=["POST"])
@login_required
def cancel_employment(employment_id):
    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id:
        flash("Session invalide")
        return redirect(url_for("auth.login"))

    stmt = select(Employment).filter_by(id=employment_id)
    employment = db.session.execute(stmt).scalars().first()

    if not employment:
        flash("Emploi introuvable")
        return redirect(url_for("user.profile"))

    from models import EmploymentStatus

    if employment.status != EmploymentStatus.PENDING:
        flash("Seuls les emplois en attente peuvent être annulés")
        return redirect(url_for("user.profile"))

    if role == "employer" and employment.employer.user_id != user_id:
        flash("Non autorisé")
        return redirect(url_for("user.profile"))

    employment.status = EmploymentStatus.CANCELLED
    db.session.commit()

    flash("Emploi annulé", "success")
    return redirect(url_for("user.profile"))


@user_bp.route("/book/<int:worker_id>", methods=["GET", "POST"])
@login_required
def book_worker(worker_id):
    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id or role != "employer":
        flash("Seuls les employeurs peuvent réserver")
        return redirect(url_for("auth.login"))

    stmt = select(Worker).filter_by(id=worker_id).options(joinedload(Worker.user))
    worker = db.session.execute(stmt).scalars().first()

    if not worker or worker.user.status != UserStatus.VALIDATED:
        flash("Travailleur introuvable ou non validé")
        return redirect(url_for("main.search"))

    if request.method == "POST":
        start_date_str = request.form.get("start_date")
        duration = request.form.get("duration")
        salary = request.form.get("salary", type=int) or worker.desired_salary

        if not start_date_str or not duration:
            flash("Tous les champs sont requis")
            return render_template("book_worker.html", worker=worker)

        from datetime import datetime as dt

        try:
            start_date = dt.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Date invalide")
            return render_template("book_worker.html", worker=worker)

        stmt = (
            select(User)
            .filter_by(id=user_id)
            .options(joinedload(User.employer_profile))
        )
        user = db.session.execute(stmt).scalars().first()

        if not user or not user.employer_profile:
            flash("Profil employeur introuvable")
            return redirect(url_for("user.profile"))

        employment = Employment(
            employer_id=user.employer_profile.id,
            worker_id=worker.id,
            salary=salary,
            start_date=start_date,
        )

        db.session.add(employment)
        db.session.commit()

        return redirect(url_for("user.payment", employment_id=employment.id))

    from datetime import date

    return render_template(
        "book_worker.html", worker=worker, today=date.today().strftime("%Y-%m-%d")
    )


@user_bp.route("/payment/<int:employment_id>", methods=["GET", "POST"])
@login_required
def payment(employment_id):
    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id or role != "employer":
        flash("Non autorisé")
        return redirect(url_for("user.profile"))

    stmt = (
        select(Employment)
        .filter_by(id=employment_id)
        .options(
            joinedload(Employment.worker).joinedload(Worker.user),
            joinedload(Employment.employer),
        )
    )
    employment = db.session.execute(stmt).scalars().first()

    if not employment or employment.employer.user_id != user_id:
        flash("Emploi introuvable")
        return redirect(url_for("user.profile"))

    if request.method == "POST":
        from models import EmploymentStatus

        employment.status = EmploymentStatus.ACTIVE

        db.session.commit()

        flash("Paiement confirmé avec succès!", "success")
        return redirect(url_for("user.profile"))

    return render_template("payment.html", employment=employment)
