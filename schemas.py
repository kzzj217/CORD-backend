from pydantic import BaseModel
from typing import List
"""
class Author(BaseModel):
    first: str
    middle: List[str]
    last: str
    suffix: str
    email: str
    affiliation: str

class BodyText(BaseModel):
    paper_id: str
    content: str

class Citation(BaseModel):
    paper_id: str
    content: str
"""
class Answer(BaseModel):
    doi: str
    doc_score: str
    doc_date: str
    title: str
    sents: List[str]

class Abstract(BaseModel):
    doi: str
    paper_id: str
    title: str
    authors: List[str]
    text: List[str]
    sciwingTags: List[str]

class Paper(BaseModel):
    abstract: Abstract
    body_text: str
 #   citation: List[Citation]
