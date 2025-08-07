# services/chat_history.py

from collections import defaultdict

# In-memory chat history store
chat_history_store = defaultdict(list)

def get_chat_history(conversation_id: str):
    return chat_history_store[conversation_id]

def add_to_chat_history(conversation_id: str, question: str, answer: str):
    chat_history_store[conversation_id].append((question, answer))

def reset_chat_history(conversation_id: str):
    chat_history_store[conversation_id] = []
