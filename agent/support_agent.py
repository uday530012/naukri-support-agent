from agent.memory import ConversationMemory
from rag.rag_pipeline import RAGPipeline


class NaukriSupportAgent:

    def __init__(self):
        print("Initializing Naukri Support Agent...")

        self.memory = ConversationMemory()

        self.rag = RAGPipeline()

        print("Naukri Support Agent initialized successfully.")

    def add_user_message(self, message):
        self.memory.add_user_message(message)

    def add_agent_message(self, message):
        self.memory.add_agent_message(message)

    def get_conversation_history(self):
        return self.memory.get_history()

    def ask(self, question):

        # Store user message
        self.add_user_message(question)

        # Get answer from RAG
        result = self.rag.answer(
            question,
            top_k=3
        )

        answer = result["answer"]

        # Store agent response
        self.add_agent_message(answer)

        return {
            "question": question,
            "answer": answer
        }


if __name__ == "__main__":

    agent = NaukriSupportAgent()

    question = "What is the notice period policy?"

    result = agent.ask(question)

    print("\n" + "=" * 70)
    print("NAUKRI SUPPORT AGENT")
    print("=" * 70)

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nConversation History:")
    print("=" * 70)

    for message in agent.get_conversation_history():
        print(
            f"{message['role'].upper()}: "
            f"{message['content']}"
        )