from agent.agent_logic import AgentLogic
from rag.rag_pipeline import RAGPipeline


class AgentRAG:

    def __init__(self):
        print("Initializing Agent + RAG...")

        self.agent_logic = AgentLogic()
        self.rag = RAGPipeline()

        print("Agent + RAG initialized successfully.")

    def process(self, user_message):

        # Process message using agent logic
        agent_result = self.agent_logic.process_message(user_message)

        # Get intent
        intent = agent_result["intent"]

        # Ask RAG
        rag_result = self.rag.answer(
            user_message,
            top_k=3
        )

        return {
            "message": user_message,
            "intent": intent,
            "answer": rag_result["answer"],
            "history": agent_result["history"]
        }


def main():

    agent = AgentRAG()

    print("=" * 60)
    print("NAUKRI SUPPORT AGENT - AGENT + RAG TEST")
    print("=" * 60)

    result = agent.process(
        "What is the notice period?"
    )

    print("\nUser:")
    print(result["message"])

    print("\nIntent:")
    print(result["intent"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nConversation History:")
    print("-" * 60)

    for message in result["history"]:
        print(
            f"{message['role'].upper()}: "
            f"{message['content']}"
        )


if __name__ == "__main__":
    main()