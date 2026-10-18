from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory


# ============================================================
# SESSION STORE
# ============================================================

session_store = {}


# ============================================================
# GET SESSION HISTORY
# ============================================================

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Return the conversation history for a session.

    A new session gets a new in-memory history.
    The same session_id retrieves the existing conversation.
    """

    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()

    return session_store[session_id]


# ============================================================
# SIMPLE RESPONSE FUNCTION
# ============================================================

def respond_with_context(input_data):
    """
    Demonstration response function.

    It receives the current user message and the previous
    conversation history.
    """

    question = input_data["question"]
    history = input_data.get("history", [])

    # Convert history into readable text
    previous_messages = []

    for message in history:
        previous_messages.append(
            f"{message.type}: {message.content}"
        )

    # Demonstrate that previous conversation is available
    if previous_messages:
        return (
            f"Current question: {question}\n"
            f"Previous conversation:\n"
            + "\n".join(previous_messages)
        )

    return f"Current question: {question}\nNo previous conversation."


# ============================================================
# BASE RUNNABLE
# ============================================================

base_chain = RunnableLambda(respond_with_context)


# ============================================================
# MEMORY-ENABLED CHAIN
# ============================================================

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
