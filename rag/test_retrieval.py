import chromadb

from rag.embeddings import EmbeddingModel


CHROMA_PATH = "./chroma_db"


def search_collection(
    collection,
    embedding_model,
    query,
    top_k=3
):
    """
    Search a ChromaDB collection using
    semantic similarity.
    """

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results


def display_results(
    collection_name,
    results
):
    """
    Display retrieved chunks.
    """

    print("\n" + "=" * 70)
    print(f"{collection_name.upper()} RESULTS")
    print("=" * 70)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        print("No results found.")
        return

    for i, document in enumerate(documents):

        print(f"\nResult {i + 1}")
        print("-" * 70)

        print("Document:")
        print(document)

        if i < len(metadatas):
            print("\nMetadata:")
            print(metadatas[i])

        if i < len(distances):
            print(
                f"\nDistance: {distances[i]:.4f}"
            )


def main():

    print("=" * 70)
    print("RAG RETRIEVAL TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Connect to ChromaDB
    # --------------------------------------------------------

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    fixed_collection = client.get_collection(
        name="fixed_size_collection"
    )

    sentence_collection = client.get_collection(
        name="sentence_collection"
    )

    # --------------------------------------------------------
    # Load embedding model
    # --------------------------------------------------------

    embedding_model = EmbeddingModel()

    # --------------------------------------------------------
    # Test questions
    # --------------------------------------------------------

    questions = [
        "What is the notice period policy?",
        "How are interviews scheduled?",
        "What is the policy for remote work?"
    ]

    # --------------------------------------------------------
    # Run retrieval
    # --------------------------------------------------------

    for question in questions:

        print("\n\n" + "#" * 70)
        print(f"QUESTION: {question}")
        print("#" * 70)

        # Fixed-size retrieval
        fixed_results = search_collection(
            fixed_collection,
            embedding_model,
            question,
            top_k=3
        )

        display_results(
            "Fixed-Size Collection",
            fixed_results
        )

        # Sentence-based retrieval
        sentence_results = search_collection(
            sentence_collection,
            embedding_model,
            question,
            top_k=3
        )

        display_results(
            "Sentence-Based Collection",
            sentence_results
        )


if __name__ == "__main__":
    main()
