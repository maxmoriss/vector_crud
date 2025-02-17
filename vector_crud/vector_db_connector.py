import uuid
from datetime import datetime

import chromadb
from chromadb.errors import UniqueConstraintError

from vector_crud.exceptions import ConnectorOperationError


class VectorDBConnector:
    """
    A class that provides CRUD operations on text documents in a Chroma-based vector database.
    """

    def __init__(
        self,
        collection_name: str,
    ):
        self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(name=collection_name)

    def create_collection(
        self, name: str, description: str | None = None
    ) -> chromadb.Collection:
        # Using default model: Sentence Transformers all-MiniLM-L6-v2
        try:
            return self._client.create_collection(
                name=name,
                metadata={"description": description, "created": str(datetime.now())},
            )
        except UniqueConstraintError as e:
            raise ConnectorOperationError(
                f"Collection with name '{name}' already exists."
            ) from e

    def insert_document(self, text: str) -> str:
        if not text:
            raise ValueError("Text to insert cannot be empty.")

        doc_id = str(uuid.uuid4())
        try:
            self._collection.add(documents=[text], ids=[doc_id])
        except Exception as e:
            raise ConnectorOperationError(f"Error while inserting document: {e}") from e
        return doc_id

    def update_document(self, doc_id: str, text: str) -> None:
        if not doc_id:
            raise ValueError("Document ID cannot be empty for update.")

        if not text:
            raise ValueError("Text cannot be empty for update.")

        try:
            self._collection.update(documents=[text], ids=[doc_id])
        except Exception as e:
            raise ConnectorOperationError(f"Error while updating document: {e}") from e

    def delete_document(self, doc_id: str) -> None:
        if not doc_id:
            raise ValueError("Document ID cannot be empty for deletion.")

        try:
            self._collection.delete(ids=[doc_id])
        except Exception as e:
            raise ConnectorOperationError(f"Error while deleting document: {e}") from e

    def retrieve_documents(self, query_text: str, n: int = 5) -> list:
        """
        Retrieves the top-N most relevant documents to the given query text.
        """
        if not query_text:
            raise ValueError("Query text cannot be empty.")

        # If n is greater than total_docs, reduce it to total_docs
        total_docs = self._collection.count()
        n = min(n, total_docs)

        try:
            results = self._collection.query(query_texts=[query_text], n_results=n)
        except Exception as e:
            raise ConnectorOperationError(
                f"Error while retrieving documents: {e}"
            ) from e

        documents = results.get("documents", [])
        return documents[0] if documents else []
