from datetime import date, datetime
from enum import Enum as PyEnum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class PostType(PyEnum):
    JOBSEARCH = "jobsearch"
    JOBOFFER = "joboffer"


class EmploymentStatus(PyEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Schedule(PyEnum):
    MORNINGS = "mornings"
    AFTERNOONS = "afternoons"
    EVENINGS = "evenings"
    WEEKENDS = "weekends"
    FLEXIBLE = "flexible"


class CleaningFrequency(PyEnum):
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTHLY = "monthly"
    ONE_TIME = "one-time"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(unique=True)
    email_address: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()

    worker_profile: Mapped["Worker | None"] = relationship(
        back_populates="user", uselist=False
    )
    employer_profile: Mapped["Employer | None"] = relationship(
        back_populates="user", uselist=False
    )
    posts: Mapped[list["Post | None"]] = relationship(back_populates="author")

    def __init__(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email_address: str,
        password_hash: str = "",
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email_address = email_address
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Worker(db.Model):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), unique=True)
    desired_salary: Mapped[int]
    preferred_schedule: Mapped[Schedule] = mapped_column(Enum(Schedule))
    ratings: Mapped[list[float] | None] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(back_populates="worker_profile")
    employments: Mapped[list["Employment"]] = relationship(back_populates="worker")

    def __init__(
        self,
        id: int,
        user_id: int,
        desired_salary: int,
        preferred_schedule: Schedule,
        ratings: list[float | None],
    ):
        self.id = id
        self.user_id = user_id
        self.desired_salary = desired_salary
        self.preferred_schedule = preferred_schedule
        self.ratings = []


class Employer(db.Model):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), unique=True)
    address: Mapped[str]
    square_footage: Mapped[int] = mapped_column(CheckConstraint("square_footage > 0"))
    proposed_salary: Mapped[int]
    cleaning_frequency: Mapped[CleaningFrequency] = mapped_column(
        Enum(CleaningFrequency)
    )
    ratings: Mapped[list[float] | None] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(back_populates="employer_profile")
    employments: Mapped[list["Employment"]] = relationship(back_populates="employer")

    def __init__(
        self,
        id: int,
        user_id: int,
        address: str,
        square_footage: int,
        proposed_salary: int,
        cleaning_frequency: CleaningFrequency,
        ratings: list[float | None],
    ):
        self.id = id
        self.user_id = user_id
        self.address = address
        self.square_footage = square_footage
        self.proposed_salary = proposed_salary
        self.cleaning_frequency = cleaning_frequency
        self.ratings = []


class Employment(db.Model):
    __tablename__ = "employments"

    id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(db.ForeignKey("employers.id"))
    worker_id: Mapped[int] = mapped_column(db.ForeignKey("workers.id"))
    salary: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    start_date: Mapped[date] = mapped_column(db.Date)
    end_date: Mapped[date] = mapped_column(db.Date, nullable=True)
    status: Mapped[EmploymentStatus] = mapped_column(
        Enum(EmploymentStatus), default=EmploymentStatus.PENDING
    )

    worker: Mapped["Worker"] = relationship(back_populates="employments")
    employer: Mapped["Employer"] = relationship(back_populates="employments")

    def __init__(
        self,
        id: int,
        employer_id: int,
        worker_id: int,
        salary: int,
        created_at: datetime,
        start_date: date,
        end_date: date,
        status: EmploymentStatus,
    ):
        self.id = id
        self.employer_id = employer_id
        self.worker_id = worker_id
        self.salary = salary
        self.created_at = created_at
        self.start_date = start_date
        self.end_date = end_date
        self.status = status


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    type: Mapped[PostType] = mapped_column(Enum(PostType))
    title: Mapped[str]
    description: Mapped[str]

    author: Mapped["User"] = relationship(back_populates="posts")

    def __init__(
        self,
        id: int,
        created_at: datetime,
        type: PostType,
        title: str,
        description: str,
    ):
        self.id = id
        self.created_at = created_at
        self.type = type
        self.title = title
        self.description = description
