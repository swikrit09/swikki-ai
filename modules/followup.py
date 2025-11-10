# modules/followup.py

def suggest_followup_question(chat_history, model):
    """
    Generate a follow-up question based on existing chat history
    when the assistant lacks enough context to proceed.
    """
    prompt = "You are a helpful assistant. Here's the conversation so far:\n\n"
    for msg in chat_history:
        role = msg["role"].capitalize()
        content = msg["content"]
        prompt += f"{role}: {content}\n"

    prompt += "\nThe assistant couldn't complete the last request. What is a good follow-up question the assistant could ask the user to gather the needed context?"

    result = model.invoke(prompt)
    return result.content.strip()

def suggest_answer(chat_history, model,query):
    """
    Generate a suggested answer based on existing chat history
    when the assistant has enough context to proceed.
    """
    prompt = "You are a helpful assistant. Here's the conversation so far:\n\n"
    for msg in chat_history[:-1]:  
        role = msg["role"].capitalize()
        content = msg["content"]
        prompt += f"{role}: {content}\n"

    prompt += f"\nAbove is the context. What is the answer for {query}?"

    result = model.invoke(prompt)
    return result.content.strip()