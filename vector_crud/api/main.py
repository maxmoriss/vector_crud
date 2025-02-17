from fastapi import FastAPI, Depends, HTTPException

from vector_crud.vector_db_connector import VectorDBConnector
from vector_crud.exceptions import ConnectorOperationError
from vector_crud.api.models import (
    Collection,
    Document,
    RetrieveQueryParams,
    MessageResponse,
    DocumentResponse,
    RetrievedDocumentsResponse,
)

app = FastAPI()
vector_db = VectorDBConnector(collection_name="my_collection")


@app.exception_handler(ValueError)
async def handle_value_error_exception(request, e: ValueError):
    raise HTTPException(status_code=400, detail=str(e))


@app.exception_handler(ConnectorOperationError)
async def handle_connector_operation_exception(request, e: ConnectorOperationError):
    raise HTTPException(status_code=400, detail=str(e))


@app.post("/create-collection", response_model=MessageResponse)
async def create_collection(collection: Collection) -> MessageResponse:
    vector_db.create_collection(
        name=collection.name, description=collection.description
    )
    return MessageResponse(message=f"Collection '{collection.name}' created")


@app.post("/insert", response_model=DocumentResponse)
async def insert_document(doc: Document) -> DocumentResponse:
    doc_id = vector_db.insert_document(doc.text)
    return DocumentResponse(doc_id=doc_id, message="Document inserted successfully.")


@app.put("/update/{doc_id}", response_model=MessageResponse)
async def update_document(doc_id: str, doc: Document) -> MessageResponse:
    vector_db.update_document(doc_id, doc.text)
    return MessageResponse(message=f"Document with ID {doc_id} updated successfully.")


@app.delete("/delete/{doc_id}", response_model=MessageResponse)
async def delete_document(doc_id: str) -> MessageResponse:
    vector_db.delete_document(doc_id)
    return MessageResponse(message=f"Document with ID {doc_id} deleted successfully.")


@app.get("/retrieve/", response_model=RetrievedDocumentsResponse)
async def retrieve_documents(
    params: RetrieveQueryParams = Depends(),
) -> RetrievedDocumentsResponse:
    docs = vector_db.retrieve_documents(query_text=params.query_text, n=params.n)
    return RetrievedDocumentsResponse(documents=docs)
