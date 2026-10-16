from agent.memory import ConversationMemory


memory = ConversationMemory()

memory.add_user_message(
    "What is the notice period policy?"
)

memory.add_agent_message(
    "Employees should disclose their expected notice period during recruitment."
)

memory.add_user_message(
    "What if I am currently employed?"
)

print("=" * 60)
print("CONVERSATION MEMORY TEST")
print("=" * 60)

for message in memory.get_history():
    print(f"{message['role'].upper()}: {message['content']}")