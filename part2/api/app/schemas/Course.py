# course.py
from pydantic import BaseModel
from typing import Optional, List

class Course(BaseModel):
    """
    The Course Python object that can be converted into Pydantic for a little easier structure.
    """
    title: str # e.g.: "MLOps"
    semester: int # e.g.: 5 --> Year 3, semester 1
    weight: int # e.g.: 10 (where to be in a sorted array)
    tags: List[str] # e.g.: ["Kubernetes", "CI/CD", "AutomatedAI"]
    pillar: str # e.g.: "code" --> The MCT pillar to classify this course in.
    tracks: Optional[List[str]] # e.g.: ["ai-engineer"] --> The MCT tracks this course is taught in
    preview: str # e.g.: "In de module MLOps leren we AI modellen deployen."
    basename: str # e.g.: "mlops" A short name