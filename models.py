from typing import List
from pydantic import BaseModel
print("loading models")


class User(BaseModel):
    id: int
    name: str
    skills: List[str] 
class Project(BaseModel):
    id: int
    title: str
    required_skills: List[str] 
