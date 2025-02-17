from fastapi import Query
from pydantic import BaseModel


class Collection(BaseModel):
    name: str
    description: str | None = None


class Document(BaseModel):
    text: str


class RetrieveQueryParams(BaseModel):
    query_text: str = Query(..., description="The text to match against documents.")
    n: int = Query(5, description="Number of top documents to retrieve.")


class MessageResponse(BaseModel):
    message: str


class DocumentResponse(BaseModel):
    doc_id: str
    message: str


class RetrievedDocumentsResponse(BaseModel):
    documents: list[str]


class ErrorResponse(BaseModel):
    detail: str
