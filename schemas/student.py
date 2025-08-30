from pydantic import BaseModel, Field

# Student schemas for input validation and output shaping


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int

    model_config = {"from_attributes": True}


# Score schemas (for optional future use)

class ScoreBase(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100)
    score: float = Field(..., ge=0.0, le=100.0)


class ScoreCreate(ScoreBase):
    pass


class ScoreOut(ScoreBase):
    id: int
    student_id: int

    model_config = {"from_attributes": True}
