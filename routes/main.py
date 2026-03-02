from flask import Blueprint, render_template, request
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models import User, UserStatus, Worker, WorkerSearchForm, db

# will need to import jsonify, request and maybe joinedload later, depending

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():

    stmt = (
        select(Worker)
        .order_by(Worker.average_rating.desc())
        .limit(3)
        .options(joinedload(Worker.user))
    )
    best_workers = db.session.execute(stmt).scalars().all()

    return render_template("index.html", best_workers=best_workers)


@main_bp.route("/search")
def search():
    form = WorkerSearchForm(request.args, meta={"csrf": False})

    query = (
        db.session.query(User, Worker)
        .join(Worker, User.id == Worker.user_id)
        .filter(User.status == UserStatus.VALIDATED)
    )

    if form.competence.data:
        query = query.filter(Worker.competences.contains(form.competence.data))

    if form.dispo.data:
        query = query.filter(Worker.preferred_schedule == form.dispo.data)

    if form.note_min.data and form.note_min.data != "0":
        note_min = int(form.note_min.data)
        query = query.filter(Worker.average_rating >= note_min)

    workers = query.order_by(Worker.average_rating.desc()).all()

    return render_template(
        "search.html",
        form=form,
        workers=workers,
        page_title="Rechercher une aide ménagère",
    )


@main_bp.route("/log-in")
def log_in():
    return render_template("signin.html")


@main_bp.route("/sign-up")
def sign_up():
    return render_template("signup.html")
