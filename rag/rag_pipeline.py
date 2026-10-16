import chromadb

from rag.embeddings import EmbeddingModel
from rag.generator import AnswerGenerator


CHROMA_PATH = "./chroma_db"


class RAGPipeline:

    def __init__(self):

        print("Initializing RAG pipeline...")

        # Connect to ChromaDB
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        # Get both collections
        self.fixed_collection = (
            self.client.get_collection(
                name="fixed_size_collection"
            )
        )

        self.sentence_collection = (
            self.client.get_collection(
                name="sentence_collection"
            )
        )

        # Load embedding model
        self.embedding_model = EmbeddingModel()

        # Load Gemini generator
        self.generator = AnswerGenerator()

        print("RAG pipeline initialized successfully.")

    def retrieve(
        self,
        question,
        collection,
        top_k=3
    ):
        """
        Retrieve the most relevant chunks
        from a ChromaDB collection.
        """

        query_embedding = (
            self.embedding_model
            .encode([question])
            .tolist()
        )

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        return results

    def build_context(self, results):
        """
        Convert retrieved documents into
        a context string for Gemini.
        """

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        context_parts = []

        for i, document in enumerate(documents):

            filename = "Unknown"

            if i < len(metadatas):
                filename = metadatas[i].get(
                    "filename",
                    "Unknown"
                )

            context_parts.append(
                f"[Source: {filename}]\n"
                f"{document}"
            )

        return "\n\n".join(context_parts)

    def answer(
        self,
        question,
        top_k=3
    ):
        """
        Retrieve information from both
        chunking strategies and generate
        a grounded answer.
        """

        # Retrieve from fixed-size collection
        fixed_results = self.retrieve(
            question,
            self.fixed_collection,
            top_k
        )

        # Retrieve from sentence collection
        sentence_results = self.retrieve(
            question,
            self.sentence_collection,
            top_k
        )

        # Build contexts
        fixed_context = self.build_context(
            fixed_results
        )

        sentence_context = self.build_context(
            sentence_results
        )

        # Combine contexts
        context = (
            "FIXED-SIZE RETRIEVAL:\n"
            + fixed_context
            + "\n\n"
            + "SENTENCE-BASED RETRIEVAL:\n"
            + sentence_context
        )

        # Generate final answer
        answer = self.generator.generate_answer(
            question,
            context
        )

        return {
            "question": question,
            "answer": answer,
            "context": context
        }


if __name__ == "__main__":

    pipeline = RAGPipeline()

    questions = [
        "What is the notice period policy?",
        "How are interviews scheduled?",
        "Can employees work remotely?"
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print("QUESTION")
        print("=" * 70)

        print(question)

        result = pipeline.answer(
            question,
            top_k=3
        )

        print("\nANSWER")
        print("=" * 70)

        print(result["answer"])

        print("\n")
