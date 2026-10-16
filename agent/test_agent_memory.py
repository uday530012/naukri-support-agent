from agent.memory import ConversationMemory


def main():

    memory = ConversationMemory()

    print("=" * 60)
    print("NAUKRI SUPPORT AGENT - MEMORY TEST")
    print("=" * 60)

    # First conversation
    memory.add_user_message(
        "What is the notice period?"
    )

    memory.add_agent_message(
        "The notice period is 30 days."
    )

    # Second conversation
    memory.add_user_message(
        "Can I work remotely?"
    )

    memory.add_agent_message(
        "Remote work depends on the applicable company policy."
    )

    print("\nConversation History:")
    print("-" * 60)

    for message in memory.get_history():
        print(f"{message['role'].upper()}: {message['content']}")

    print("\nRecent History:")
    print("-" * 60)

    for message in memory.get_recent_history(2):
        print(f"{message['role'].upper()}: {message['content']}")


if __name__ == "__main__":
    main()