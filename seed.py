from datetime import datetime, timedelta

from sqlalchemy.orm.attributes import flag_modified
from werkzeug.security import generate_password_hash

from app import create_app
from models.models import (
    CleaningFrequency,
    Employer,
    Employment,
    EmploymentStatus,
    Review,
    ReviewType,
    Schedule,
    User,
    UserStatus,
    Worker,
    db,
)


def seed_database():
    """Seed the database with test data"""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Clear existing data
        print("Clearing existing data...")
        Review.query.delete()
        Employment.query.delete()
        Worker.query.delete()
        Employer.query.delete()
        User.query.delete()
        db.session.commit()

        print("Creating test users...")

        # Create Workers
        workers_data = [
            {
                "first_name": "Aminata",
                "last_name": "Ndiaye",
                "email_address": "aminata@example.com",
                "phone_number": "+221771234567",
                "competences": ["Nettoyage", "Garde d'enfant", "Repassage", "Cuisine"],
                "description": "Expérience de 8 ans dans le ménage. Très organisée et ponctuelle. Adore les enfants.",
                "desired_salary": 150000,
                "preferred_schedule": Schedule.MORNINGS,
            },
            {
                "first_name": "Maguette",
                "last_name": "Diop",
                "email_address": "maguette@example.com",
                "phone_number": "+221772345678",
                "competences": [
                    "Nettoyage",
                    "Cuisine",
                    "Garde d'enfant",
                    "Repassage",
                    "Courses",
                    "Baby-sitting",
                ],
                "description": "15 ans d'expérience. Spécialisée en cuisine sénégalaise. Références disponibles.",
                "desired_salary": 160000,
                "preferred_schedule": Schedule.FLEXIBLE,
            },
            {
                "first_name": "Coumba",
                "last_name": "Cissé",
                "email_address": "coumba@example.com",
                "phone_number": "+221773456789",
                "competences": [
                    "Nettoyage",
                    "Cuisine",
                    "Garde d'enfant",
                    "Repassage",
                    "Courses",
                ],
                "description": "Professionnelle sérieuse avec 10 ans d'expérience. Diplôme en hygiène et nutrition.",
                "desired_salary": 140000,
                "preferred_schedule": Schedule.AFTERNOONS,
            },
            {
                "first_name": "Fatou",
                "last_name": "Sall",
                "email_address": "fatou@example.com",
                "phone_number": "+221774567890",
                "competences": ["Nettoyage", "Repassage", "Cuisine"],
                "description": "Aide ménagère dynamique et motivée. 5 ans d'expérience avec des familles expatriées.",
                "desired_salary": 135000,
                "preferred_schedule": Schedule.MORNINGS,
            },
            {
                "first_name": "Aissatou",
                "last_name": "Ba",
                "email_address": "aissatou@example.com",
                "phone_number": "+221775678901",
                "competences": [
                    "Garde d'enfant",
                    "Baby-sitting",
                    "Cuisine",
                    "Nettoyage",
                ],
                "description": "Spécialisée en garde d'enfants. Formation en puériculture. Douce et patiente.",
                "desired_salary": 145000,
                "preferred_schedule": Schedule.FLEXIBLE,
            },
        ]

        workers = []
        for data in workers_data:
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email_address=data["email_address"],
                phone_number=data["phone_number"],
                password_hash=generate_password_hash("password123"),
            )
            user.status = UserStatus.VALIDATED
            user.is_verified = True
            db.session.add(user)
            db.session.flush()

            worker = Worker(
                user_id=user.id,
                competences=data["competences"],
                description=data["description"],
                desired_salary=data["desired_salary"],
                preferred_schedule=data["preferred_schedule"],
            )
            db.session.add(worker)
            workers.append((user, worker))

        # Create Employers
        employers_data = [
            {
                "first_name": "Moussa",
                "last_name": "Diallo",
                "email_address": "moussa@example.com",
                "phone_number": "+221776789012",
                "address": "Point E, Dakar",
                "square_footage": 120,
                "proposed_salary": 155000,
                "cleaning_frequency": CleaningFrequency.WEEKLY,
            },
            {
                "first_name": "Khady",
                "last_name": "Faye",
                "email_address": "khady@example.com",
                "phone_number": "+221777890123",
                "address": "Sacré-Cœur, Dakar",
                "square_footage": 150,
                "proposed_salary": 165000,
                "cleaning_frequency": CleaningFrequency.BI_WEEKLY,
            },
            {
                "first_name": "Omar",
                "last_name": "Sy",
                "email_address": "omar@example.com",
                "phone_number": "+221778901234",
                "address": "Mermoz, Dakar",
                "square_footage": 100,
                "proposed_salary": 145000,
                "cleaning_frequency": CleaningFrequency.WEEKLY,
            },
        ]

        employers = []
        for data in employers_data:
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email_address=data["email_address"],
                phone_number=data["phone_number"],
                password_hash=generate_password_hash("password123"),
            )
            user.status = UserStatus.VALIDATED
            user.is_verified = True
            db.session.add(user)
            db.session.flush()

            employer = Employer(
                user_id=user.id,
                address=data["address"],
                square_footage=data["square_footage"],
                proposed_salary=data["proposed_salary"],
                cleaning_frequency=data["cleaning_frequency"],
            )
            db.session.add(employer)
            employers.append((user, employer))

        db.session.commit()
        print(f"Created {len(workers)} workers and {len(employers)} employers")

        # Create Employments
        print("Creating employments...")
        employments_data = [
            {
                "worker": workers[0][1],  # Aminata
                "employer": employers[0][1],  # Moussa
                "start_date": datetime.now().date() - timedelta(days=180),
                "salary": 150000,
                "status": EmploymentStatus.COMPLETED,
            },
            {
                "worker": workers[1][1],  # Maguette
                "employer": employers[0][1],  # Moussa
                "start_date": datetime.now().date() - timedelta(days=60),
                "salary": 160000,
                "status": EmploymentStatus.ACTIVE,
            },
            {
                "worker": workers[2][1],  # Coumba
                "employer": employers[1][1],  # Khady
                "start_date": datetime.now().date() - timedelta(days=90),
                "salary": 140000,
                "status": EmploymentStatus.COMPLETED,
            },
            {
                "worker": workers[3][1],  # Fatou
                "employer": employers[1][1],  # Khady
                "start_date": datetime.now().date() - timedelta(days=30),
                "salary": 135000,
                "status": EmploymentStatus.ACTIVE,
            },
            {
                "worker": workers[4][1],  # Aissatou
                "employer": employers[2][1],  # Omar
                "start_date": datetime.now().date() - timedelta(days=5),
                "salary": 145000,
                "status": EmploymentStatus.PENDING,
            },
            {
                "worker": workers[0][1],  # Aminata
                "employer": employers[2][1],  # Omar
                "start_date": datetime.now().date() - timedelta(days=120),
                "salary": 150000,
                "status": EmploymentStatus.COMPLETED,
            },
        ]

        employments = []
        for data in employments_data:
            end_date = None
            if data["status"] == EmploymentStatus.COMPLETED:
                end_date = data["start_date"] + timedelta(days=90)

            employment = Employment(
                worker_id=data["worker"].id,
                employer_id=data["employer"].id,
                start_date=data["start_date"],
                end_date=end_date,
                salary=data["salary"],
                status=data["status"],
            )
            db.session.add(employment)
            employments.append(employment)

        db.session.commit()
        print(f"Created {len(employments)} employments")

        # Create Reviews
        print("Creating reviews...")
        reviews_data = [
            {
                "employment": employments[0],  # Aminata worked for Moussa
                "reviewer": employers[0][0],  # Moussa reviews
                "reviewee": workers[0][0],  # Aminata is reviewed
                "review_type": ReviewType.WORKER,
                "rating": 5,
                "comment": "Excellente aide ménagère ! Très professionnelle et ponctuelle. Je la recommande vivement.",
            },
            {
                "employment": employments[2],  # Coumba worked for Khady
                "reviewer": employers[1][0],  # Khady reviews
                "reviewee": workers[2][0],  # Coumba is reviewed
                "review_type": ReviewType.WORKER,
                "rating": 5,
                "comment": "Travail impeccable et très bonne cuisinière. Ma maison n'a jamais été aussi propre !",
            },
            {
                "employment": employments[5],  # Aminata worked for Omar
                "reviewer": employers[2][0],  # Omar reviews
                "reviewee": workers[0][0],  # Aminata is reviewed
                "review_type": ReviewType.WORKER,
                "rating": 4,
                "comment": "Très bon service. Quelques retards occasionnels mais globalement très satisfait.",
            },
            {
                "employment": employments[0],  # Reverse review: Aminata reviews Moussa
                "reviewer": workers[0][0],  # Aminata reviews
                "reviewee": employers[0][0],  # Moussa is reviewed
                "review_type": ReviewType.EMPLOYER,
                "rating": 5,
                "comment": "Excellent employeur, respectueux et ponctuel pour les paiements.",
            },
            {
                "employment": employments[2],  # Reverse review: Coumba reviews Khady
                "reviewer": workers[2][0],  # Coumba reviews
                "reviewee": employers[1][0],  # Khady is reviewed
                "review_type": ReviewType.EMPLOYER,
                "rating": 5,
                "comment": "Famille très agréable, conditions de travail excellentes.",
            },
        ]

        for data in reviews_data:
            review = Review(
                employment_id=data["employment"].id,
                reviewer_id=data["reviewer"].id,
                reviewee_id=data["reviewee"].id,
                review_type=data["review_type"],
                rating=data["rating"],
                comment=data["comment"],
            )
            review.created_at = datetime.now() - timedelta(days=10)
            db.session.add(review)

            # Update ratings based on review type
            if data["review_type"] == ReviewType.WORKER:
                worker = data["employment"].worker
                worker.add_rating(data["rating"])
                # Mark the ratings field as modified so SQLAlchemy saves it
                flag_modified(worker, "ratings")
            else:
                employer = data["employment"].employer
                employer.add_rating(data["rating"])
                # Mark the ratings field as modified so SQLAlchemy saves it
                flag_modified(employer, "ratings")

        db.session.commit()
        print(f"Created {len(reviews_data)} reviews")

        # Update average ratings
        print("Calculating average ratings...")
        for user, worker in workers:
            worker.recalculate_average()
            # Mark the ratings field as modified
            flag_modified(worker, "ratings")

        for user, employer in employers:
            employer.recalculate_average()
            # Mark the ratings field as modified
            flag_modified(employer, "ratings")

        db.session.commit()

        print("\n✅ Database seeding completed successfully!")
        print("\nTest credentials:")
        print("=" * 50)
        print("\n👷 Workers (email / password):")
        for user, _ in workers:
            print(f"  • {user.email_address} / password123")
        print("\n👔 Employers (email / password):")
        for user, _ in employers:
            print(f"  • {user.email_address} / password123")
        print("\n" + "=" * 50)
        print("\nTotal created:")
        print(f"  • {len(workers)} workers")
        print(f"  • {len(employers)} employers")
        print(f"  • {len(employments)} employments")
        print(f"  • {len(reviews_data)} reviews")


if __name__ == "__main__":
    seed_database()
