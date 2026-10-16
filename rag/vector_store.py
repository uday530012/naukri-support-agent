import chromadb

from rag.load_documents import load_documents
from rag.chunking import (
    fixed_size_chunking,
    sentence_based_chunking
)
from rag.embeddings import EmbeddingModel


CHROMA_PATH = "./chroma_db"


def create_vector_store():

    print("=" * 60)
    print("CREATING CHROMADB VECTOR STORE")
    print("=" * 60)

    # Load documents
    documents = load_documents()

    print(f"\nDocuments loaded: {len(documents)}")

    # Load embedding model
    embedding_model = EmbeddingModel()

    # Create ChromaDB client
    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    # Create separate collections
    fixed_collection = client.get_or_create_collection(
        name="fixed_size_collection"
    )

    sentence_collection = client.get_or_create_collection(
        name="sentence_collection"
    )

    fixed_texts = []
    fixed_ids = []
    fixed_metadatas = []

    sentence_texts = []
    sentence_ids = []
    sentence_metadatas = []

    # Create chunks
    for document in documents:

        document_id = document["document_id"]
        filename = document["filename"]
        text = document["text"]

        # Fixed-size chunks
        fixed_chunks = fixed_size_chunking(
            text,
            chunk_size=300,
            overlap=50
        )

        for index, chunk in enumerate(fixed_chunks):

            fixed_texts.append(chunk)

            fixed_ids.append(
                f"fixed_{document_id}_{index}"
            )

            fixed_metadatas.append({
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
                "chunking_strategy": "fixed_size"
            })

        # Sentence-based chunks
        sentence_chunks = sentence_based_chunking(text)

        for index, chunk in enumerate(sentence_chunks):

            sentence_texts.append(chunk)

            sentence_ids.append(
                f"sentence_{document_id}_{index}"
            )

            sentence_metadatas.append({
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
                "chunking_strategy": "sentence_based"
            })

    print(
        f"\nFixed-size chunks: {len(fixed_texts)}"
    )

    print(
        f"Sentence chunks: {len(sentence_texts)}"
    )

    # Generate embeddings
    print("\nGenerating fixed-size embeddings...")

    fixed_embeddings = embedding_model.encode(
        fixed_texts
    ).tolist()

    print("Generating sentence embeddings...")

    sentence_embeddings = embedding_model.encode(
        sentence_texts
    ).tolist()

    # Store fixed-size chunks
    print("\nStoring fixed-size chunks...")

    fixed_collection.upsert(
        ids=fixed_ids,
        documents=fixed_texts,
        embeddings=fixed_embeddings,
        metadatas=fixed_metadatas
    )

    # Store sentence chunks
    print("Storing sentence chunks...")

    sentence_collection.upsert(
        ids=sentence_ids,
        documents=sentence_texts,
        embeddings=sentence_embeddings,
        metadatas=sentence_metadatas
    )

    print("\n" + "=" * 60)
    print("VECTOR STORE CREATION COMPLETED")
    print("=" * 60)

    print(
        f"\nFixed-size collection count: "
        f"{fixed_collection.count()}"
    )

    print(
        f"Sentence collection count: "
        f"{sentence_collection.count()}"
    )

    print(f"\nChromaDB location: {CHROMA_PATH}")


if __name__ == "__main__":
    create_vector_store()
