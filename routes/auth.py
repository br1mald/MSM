from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select

from models import User, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("Email est requis")
            return redirect(url_for("auth.register"))

        password = request.form.get("password")
        if not password:
            flash("Mot de passe est requis")
            return redirect(url_for("auth.register"))

        first_name = request.form.get("first_name")
        if not first_name:
            flash("Prénom est requis")
            return redirect(url_for("auth.register"))

        last_name = request.form.get("last_name")
        if not last_name:
            flash("Nom est requis")
            return redirect(url_for("auth.register"))

        phone_number = request.form.get("phone_number")
        if not phone_number:
            flash("Numéro de téléphone est requis")
            return redirect(url_for("auth.register"))

        stmt = select(User).filter_by(email_address=email)
        existing_user = db.session.execute(stmt).scalars().first()
        if existing_user:
            flash("Cet email est déjà inscrit")
            return redirect(url_for("auth.register"))

        user = User(
            email_address=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect(url_for("user.profile"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("Email requis")
            return redirect(url_for("auth.login"))
        password = request.form.get("password")
        if not password:
            flash("Mot de passe requis")
            return redirect(url_for("auth.login"))

        stmt = select(User).filter_by(email_address=email)
        user = db.session.execute(stmt).scalars().first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("user.profile"))

        flash("Email ou mot de passe invalide")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
