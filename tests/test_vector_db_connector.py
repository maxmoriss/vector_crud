import pytest
from chromadb.errors import UniqueConstraintError

from vector_crud.vector_db_connector import VectorDBConnector
from vector_crud.exceptions import ConnectorOperationError


VECTOR_DB_CONNECTOR_PATH = "vector_crud.vector_db_connector"


@pytest.fixture
def mock_collection(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_client(mocker, mock_collection):
    mock_client = mocker.Mock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client.create_collection.return_value = mock_collection
    return mock_client


@pytest.fixture
def vector_db(mocker, mock_client):
    mocker.patch(
        f"{VECTOR_DB_CONNECTOR_PATH}.chromadb.Client", return_value=mock_client
    )
    return VectorDBConnector(collection_name="test_collection")


def test_init(vector_db, mock_client, mock_collection):
    assert vector_db._client == mock_client
    assert vector_db._collection == mock_collection
    mock_client.get_or_create_collection.assert_called_once_with(name="test_collection")


def test_create_collection_success(vector_db, mock_client):
    collection = vector_db.create_collection(name="new_collection", description="Test")
    mock_client.create_collection.assert_called_once()
    assert collection is not None


def test_create_collection_unique_constraint_error(mocker, vector_db, mock_client):
    mock_client.create_collection.side_effect = UniqueConstraintError("Duplicate")

    with pytest.raises(
        ConnectorOperationError,
        match="Collection with name 'new_collection' already exists.",
    ):
        vector_db.create_collection(name="new_collection")


def test_insert_document_success(mocker, vector_db, mock_collection):
    mock_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mocker.patch(f"{VECTOR_DB_CONNECTOR_PATH}.uuid.uuid4", return_value=mock_uuid)

    doc_id = vector_db.insert_document("Test document")

    mock_collection.add.assert_called_once_with(
        documents=["Test document"], ids=[mock_uuid]
    )
    assert doc_id == mock_uuid


def test_insert_document_empty_text(vector_db):
    with pytest.raises(ValueError, match="Text to insert cannot be empty."):
        vector_db.insert_document("")


def test_insert_document_error(mocker, vector_db, mock_collection):
    mock_collection.add.side_effect = Exception("Insert failure")

    with pytest.raises(
        ConnectorOperationError, match="Error while inserting document: Insert failure"
    ):
        vector_db.insert_document("Test document")


def test_update_document_success(vector_db, mock_collection):
    doc_id = "test_doc"
    text = "Updated text"

    vector_db.update_document(doc_id, text)
    mock_collection.update.assert_called_once_with(documents=[text], ids=[doc_id])


def test_update_document_empty_doc_id(vector_db):
    with pytest.raises(ValueError, match="Document ID cannot be empty for update."):
        vector_db.update_document("", "Some text")


def test_update_document_empty_text(vector_db):
    with pytest.raises(ValueError, match="Text cannot be empty for update."):
        vector_db.update_document("test_doc", "")


def test_update_document_error(mocker, vector_db, mock_collection):
    mock_collection.update.side_effect = Exception("Update failure")

    with pytest.raises(
        ConnectorOperationError, match="Error while updating document: Update failure"
    ):
        vector_db.update_document("test_doc", "Updated text")


def test_delete_document_success(vector_db, mock_collection):
    doc_id = "test_doc"
    vector_db.delete_document(doc_id)
    mock_collection.delete.assert_called_once_with(ids=[doc_id])


def test_delete_document_empty_doc_id(vector_db):
    with pytest.raises(ValueError, match="Document ID cannot be empty for deletion."):
        vector_db.delete_document("")


def test_delete_document_error(mocker, vector_db, mock_collection):
    mock_collection.delete.side_effect = Exception("Delete failure")

    with pytest.raises(
        ConnectorOperationError, match="Error while deleting document: Delete failure"
    ):
        vector_db.delete_document("test_doc")


def test_retrieve_documents_success(mocker, vector_db, mock_collection):
    mock_collection.query.return_value = {"documents": [["Doc1", "Doc2"]]}
    mock_collection.count.return_value = 2

    documents = vector_db.retrieve_documents("query", n=2)

    mock_collection.query.assert_called_once_with(query_texts=["query"], n_results=2)
    assert documents == ["Doc1", "Doc2"]


def test_retrieve_documents_empty_query(vector_db):
    with pytest.raises(ValueError, match="Query text cannot be empty."):
        vector_db.retrieve_documents("")


def test_retrieve_documents_limited_by_total_docs(vector_db, mock_collection):
    mock_collection.count.return_value = 3
    mock_collection.query.return_value = {"documents": [["Doc1", "Doc2", "Doc3"]]}

    documents = vector_db.retrieve_documents(
        "query", n=10
    )  # Requesting 10 but only 3 exist

    mock_collection.query.assert_called_once_with(query_texts=["query"], n_results=3)
    assert documents == ["Doc1", "Doc2", "Doc3"]


def test_retrieve_documents_no_results(vector_db, mock_collection):
    mock_collection.query.return_value = {"documents": []}
    mock_collection.count.return_value = 0

    documents = vector_db.retrieve_documents("query", n=2)
    assert documents == []


def test_retrieve_documents_error(mocker, vector_db, mock_collection):
    mock_collection.query.side_effect = Exception("Query failure")
    mock_collection.count.return_value = 0

    with pytest.raises(
        ConnectorOperationError, match="Error while retrieving documents: Query failure"
    ):
        vector_db.retrieve_documents("query text", n=5)
