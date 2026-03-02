from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select

from models import (
    CleaningFrequency,
    Employer,
    Schedule,
    User,
    UserStatus,
    Worker,
    db,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("role", "employer")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not all([first_name, last_name, email, phone_number, password, confirm]):
            flash("Tous les champs sont requis")
            return redirect(url_for("auth.register"))

        assert first_name is not None
        assert last_name is not None
        assert email is not None
        assert phone_number is not None
        assert password is not None
        assert confirm is not None

        if password != confirm:
            flash("Les mots de passe ne correspondent pas.")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("Le mot de passe doit contenir au moins 6 caractères.")
            return redirect(url_for("auth.register"))

        stmt = select(User).filter_by(email_address=email)
        existing_user = db.session.execute(stmt).scalars().first()
        if existing_user:
            flash("Cet email est déjà utilisé.")
            return redirect(url_for("auth.register"))

        stmt = select(User).filter_by(phone_number=phone_number)
        existing_phone_number = db.session.execute(stmt).scalars().first()
        if existing_phone_number:
            flash("Ce numéro de téléphone est déjà utilisé.")
            return redirect(url_for("auth.register"))

        user = User(
            first_name=first_name,
            last_name=last_name,
            email_address=email,
            phone_number=phone_number,
        )

        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        if role == "worker":
            worker = Worker(
                user_id=user.id,
                desired_salary=0,
                preferred_schedule=Schedule.FLEXIBLE,
                competences=[],
                description="",
            )
            db.session.add(worker)
        else:
            employer = Employer(
                user_id=user.id,
                address="",
                square_footage=100,
                proposed_salary=0,
                cleaning_frequency=CleaningFrequency.WEEKLY,
            )
            db.session.add(employer)

        db.session.commit()

        session["user_id"] = user.id
        session["role"] = role
        flash("Compte créé avec succès!", "success")
        return redirect(url_for("user.profile"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email et mot de passe requis")
            return redirect(url_for("auth.login"))

        stmt = select(User).filter_by(email_address=email)
        user = db.session.execute(stmt).scalars().first()

        if not user or not user.check_password(password):
            flash("Email ou mot de passe incorrect.")
            return redirect(url_for("auth.login"))

        if user.status == UserStatus.SUSPENDED:
            flash("Votre compte a été suspendu. Contactez le support.")
            return redirect(url_for("auth.login"))

        role = "worker" if user.worker_profile else "employer"

        session["user_id"] = user.id
        session["role"] = role
        session["first_name"] = user.first_name
        session["last_name"] = user.last_name

        if role == "worker":
            return redirect(url_for("user.profile"))
        else:
            return redirect(url_for("user.profile"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Vous êtes déconnecté")
    return redirect(url_for("auth.login"))
