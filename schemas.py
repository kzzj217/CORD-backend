from pydantic import BaseModel
from typing import List, Dict, Tuple

class AbstractTag(BaseModel):
    sciwing: List[str]
    coda19: List[str]

class Abstract(BaseModel):
    text: List[str]
    tags: AbstractTag

class BioNerTag(BaseModel):
    sciwingI2B2: Dict[str, str]

class SectionHeader(BaseModel):
    original: List[str]
    generic: List[str]

class BodyText(BaseModel):
    section_header: SectionHeader
    text: List[str]
    tags: BioNerTag

class Answer(BaseModel):
    score: str
    sents: List[str]
    sent_section: List[str]

# TODO: side column to show similar paper
class PaperInfo(BaseModel):
    paper_id: str
    doi: str
    title: str
    doc_date: str
    authors: List[str]
    summary: str
    abstract: Abstract
    bodyText: BodyText
    url: str

class GeneralAns(BaseModel):
    answer: Answer
    paper_id: str
    doi: str
    title: str
    doc_date: str
    authors: List[str]
    summary: str
    abstract: Abstract
    bodyText: BodyText
    url: str

    #   citation: List[Citation]
class GraphUnit(BaseModel):
    num: int
    articles: List[PaperInfo]

class Graph(BaseModel):
    Xtype: str
    Ytype: str
    Xaxis: List[str]
    Yaxis: List[str]
    numbers:List[List[int]]
    values: Dict[str , GraphUnit]