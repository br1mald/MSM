# MSM — Marketplace de Services Ménagers

Plateforme web mettant en relation des employeurs (particuliers) et des aides ménagères : publication d’annonces, recherche de profils, réservation, paiement, et système d’avis bidirectionnel. Application Flask avec SQLAlchemy.

Démo en ligne : https://msm-marketplace-de-services-menagers.onrender.com/

>Projet académique (L2 GLSI — ESP/UCAD), réalisé en équipe de 2.

## Fonctionnalités

- Authentification — inscription/connexion, mots de passe hachés (Werkzeug), sessions, accès protégé par décorateur ‎`login_required`

- Deux rôles — profils worker (aide ménagère) et employer (employeur), chacun avec son tableau de bord

- Annonces — publication d’offres d’emploi et de recherches d’emploi (‎`jobsearch` / ‎`joboffer`)

- Recherche & réservation — un employeur réserve une aide ménagère validée, puis confirme le paiement

- Cycle de vie d’un emploi — statuts ‎`pending → active → completed / cancelled` (annulation possible uniquement en attente)

- Avis bidirectionnels — employeur et travailleur se notent (1–5), un seul avis par emploi, recalcul automatique de la moyenne

- Validation des comptes — statut utilisateur ‎`pending / validated / suspended`

## Stack

- Backend : Python, Flask (blueprints ‎`auth` / ‎`main` / ‎`user`)

- ORM : SQLAlchemy (mapping typé ‎`Mapped` / ‎`mapped_column`, relations, contraintes ‎`CheckConstraint`)

- Sécurité : hachage de mots de passe Werkzeug, gestion de session, contrôle d’accès par rôle

- Frontend : templates Jinja2, HTML/CSS

- Déploiement : Render (gunicorn)

## Modèle de données

‎`User` (1–1 vers ‎`Worker` ou ‎`Employer`) · ‎`Post` · ‎`Employment` (relie employeur et travailleur, avec statut) · ‎`Review` (liée à un emploi, notation 1–5 contrainte en base).

## Lancer le projet en local

```bash
pip install -r requirements.txt   # ou : uv sync
python seed.py                     # (optionnel) données de démonstration
python app.py
```

L’application démarre sur ‎`http://localhost:5000`.

## Auteurs

- Ibrahima Sory Diallo - [@br1mald](https://github.com/br1mald)
- Véronique Sylva - [@VeroS06](https://github.com/VeroS06)
