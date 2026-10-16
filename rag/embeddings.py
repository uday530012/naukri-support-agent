from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded successfully.")

    def encode(self, texts):
        """
        Convert text into vector embeddings.
        """

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )


if __name__ == "__main__":

    embedding_model = EmbeddingModel()

    test_texts = [
        "What is the interview scheduling policy?",
        "What is the notice period policy?"
    ]

    embeddings = embedding_model.encode(test_texts)

    print("\n" + "=" * 60)
    print("EMBEDDING TEST")
    print("=" * 60)

    print(
        f"\nNumber of embeddings: {len(embeddings)}"
    )

    print(
        f"Embedding dimensions: {len(embeddings[0])}"
    )

    print("\nEmbedding generation successful.")
