from datetime import date, datetime
from enum import Enum as PyEnum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    # will add authentication later

    worker_profile: Mapped["Worker | None"] = relationship(
        back_populates="user", uselist=False
    )
    employer_profile: Mapped["Employer | None"] = relationship(
        back_populates="user", uselist=False
    )
    posts: Mapped[list["Post | None"]] = relationship(back_populates="author")


class Worker(db.Model):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), unique=True)
    desired_salary: Mapped[int]
    preferred_schedule: Mapped[Schedule] = mapped_column(Enum(Schedule))
    ratings: Mapped[list[float] | None] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(back_populates="worker_profile")
    employments: Mapped[list["Employment"]] = relationship(back_populates="worker")


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


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    type: Mapped[PostType] = mapped_column(Enum(PostType))
    title: Mapped[str]
    description: Mapped[str]

    author: Mapped["User"] = relationship(back_populates="posts")
