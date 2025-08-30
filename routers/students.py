from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database.session import get_db
from models.student import Student
from schemas.student import StudentCreate, StudentOut

router = APIRouter()


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(name=payload.name.strip(),
                      department=payload.department.strip())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=List[StudentOut])
def list_students(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    stmt = select(Student).offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return rows


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    obj = db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    obj = db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(obj)
    db.commit()
    return None


@router.get("/search/", response_model=List[StudentOut])
def search_students(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    like_pattern = f"%{name}%"
    stmt = select(Student).where(func.lower(
        Student.name).like(func.lower(like_pattern)))
    rows = db.execute(stmt).scalars().all()
    return rows
