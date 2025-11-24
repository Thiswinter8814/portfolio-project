
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict

class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, description="사용자 이름")
    email: EmailStr = Field(..., description="유효한 이메일 주소")
    password: str = Field(..., min_length=8, description="8자 이상의 비밀번호")

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class ProjectCreateSchema(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    link: Optional[str] = None

class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    link: Optional[str] = None

class PortfolioUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birthdate: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None
    specialties: Optional[List[str]] = None
    part_time_jobs: Optional[List[dict]] = None
    education: Optional[List[dict]] = None
    certificates: Optional[List[dict]] = None
    accounts: Optional[Dict[str, str]] = None
    skills: Optional[List[str]] = None

class SkillSchema(BaseModel):
    skill: str = Field(..., min_length=1, description="기술 스택 이름")
