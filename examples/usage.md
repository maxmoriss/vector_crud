### A sample file to be used for demonstrating the CRUD operations.

```python
from vector_crud.vector_db_connector import VectorDBConnector

# Initialize
vector_db = VectorDBConnector(collection_name="my_collection")

# Create a new collection
vector_db.create_collection(
    name="documents",
    description="Collection for storing text documents"
)

# Insert documents
vector_db.insert_document("Python is a great programming language")
vector_db.insert_document("I love to write unit tests")
doc_id = vector_db.insert_document("JavaScript is popular for web")

# Update the document
vector_db.update_document(doc_id, "JavaScript is popular for web development")

# Retrieve documents similar to a query
query_results = vector_db.retrieve_documents(query_text="programming", n=2)
print(f"Retrieved documents: {query_results}")

# Delete the document
vector_db.delete_document(doc_id)
print(f"Deleted document with ID: {doc_id}")
```
