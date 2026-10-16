from agent.memory import ConversationMemory
from agent.intent_classifier import classify_intent


class AgentLogic:

    def __init__(self):
        self.memory = ConversationMemory()
        self.last_intent = None

    def process_message(self, user_message):

        # Store user message
        self.memory.add_user_message(user_message)

        # Detect intent
        detected_intent = classify_intent(user_message)

        # If the new question is general,
        # use the previous intent when available
        if detected_intent == "general" and self.last_intent is not None:
            intent = self.last_intent
        else:
            intent = detected_intent

        # Save the current intent
        self.last_intent = intent

        # Get recent conversation
        history = self.memory.get_recent_history(5)

        return {
            "message": user_message,
            "intent": intent,
            "history": history
        }


def main():

    agent = AgentLogic()

    print("=" * 60)
    print("NAUKRI SUPPORT AGENT - CONTEXT AWARE TEST")
    print("=" * 60)

    # First question
    result1 = agent.process_message(
        "What is the notice period?"
    )

    print("\nUser:")
    print(result1["message"])

    print("\nDetected Intent:")
    print(result1["intent"])

    # Follow-up question
    result2 = agent.process_message(
        "Can I reduce it?"
    )

    print("\nUser:")
    print(result2["message"])

    print("\nDetected Intent:")
    print(result2["intent"])

    print("\nConversation History:")
    print("-" * 60)

    for message in result2["history"]:
        print(f"{message['role'].upper()}: {message['content']}")


if __name__ == "__main__":
    main()