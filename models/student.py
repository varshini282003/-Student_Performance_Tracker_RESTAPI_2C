from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from database.session import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)

    # Relationship to scores
    scores = relationship("Score", back_populates="student",
                          cascade="all, delete-orphan")


class Score(Base):
    __tablename__ = "scores"
    __table_args__ = (
        UniqueConstraint("student_id", "subject", name="uq_student_subject"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey(
        "students.id", ondelete="CASCADE"), nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    score = Column(Float, nullable=False)

    student = relationship("Student", back_populates="scores")
