import chromadb

from rag.embeddings import EmbeddingModel


class RetrievalOnly:

    def __init__(self):

        print("Initializing Retrieval-Only RAG...")

        self.embedding_model = EmbeddingModel()

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.fixed_collection = self.client.get_collection(
            "fixed_size_collection"
        )

        self.sentence_collection = self.client.get_collection(
            "sentence_collection"
        )

        print("Retrieval-only RAG initialized successfully.")

    def retrieve(self, question, top_k=3):

        query_embedding = self.embedding_model.encode(
            [question]
        ).tolist()

        results = []

        # Search fixed-size collection
        fixed_results = self.fixed_collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        # Search sentence collection
        sentence_results = self.sentence_collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        # Collect fixed-size results
        if fixed_results["documents"]:

            documents = fixed_results["documents"][0]
            distances = fixed_results["distances"][0]

            for document, distance in zip(
                documents, distances
            ):
                results.append({
                    "document": document,
                    "distance": distance
                })

        # Collect sentence results
        if sentence_results["documents"]:

            documents = sentence_results["documents"][0]
            distances = sentence_results["distances"][0]

            for document, distance in zip(
                documents, distances
            ):
                results.append({
                    "document": document,
                    "distance": distance
                })

        # Remove duplicate documents
        unique_results = {}

        for result in results:

            document = result["document"]

            if document not in unique_results:

                unique_results[document] = result

        # Sort by relevance
        sorted_results = sorted(
            unique_results.values(),
            key=lambda x: x["distance"]
        )

        # Return only the best results
        return sorted_results[:top_k]


def main():

    rag = RetrievalOnly()

    question = "What is the notice period?"

    results = rag.retrieve(
        question,
        top_k=3
    )

    print("\n" + "=" * 60)
    print("IMPROVED RAG RETRIEVAL TEST")
    print("=" * 60)

    print("\nQuestion:")
    print(question)

    print("\nTop Retrieved Information:")
    print("-" * 60)

    for i, result in enumerate(results, 1):

        print(f"\nResult {i}")
        print(f"Distance: {result['distance']:.4f}")
        print("Document:")
        print(result["document"])


if __name__ == "__main__":
    main()