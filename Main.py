import json
from difflib import get_close_matches
from typing import Optional

# Set your password here
ADMIN_PASSWORD = "Secret.09!"

# Loads existing memory (knowledge base) from file or creates new one
def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"questions": []}  # Safe default

# Saves updated memory to file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Finds closest matching question using fuzzy matching
def find_best_match(user_question: str, questions: list[str]) -> Optional[str]:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Retrieves an answer to a known question
def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# Main chat loop
def chat_bot():
    file_path = 'knowledge_base.json'
    knowledge_base = load_knowledge_base(file_path)

    print("Aether: Hello! Ask me anything. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'quit':
            print("Aether: Goodbye!")
            break

        questions_list = [q["question"] for q in knowledge_base["questions"]]
        best_match = find_best_match(user_input, questions_list)

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Aether: {answer}')
        else:
            print("Aether: I don't know the answer to that. Can you teach me?")
            new_answer = input('Type the answer or "skip" to skip: ').strip()

            if new_answer.lower() != 'skip':
                password_attempt = input("Enter the password to save this new information: ").strip()
                if password_attempt == ADMIN_PASSWORD:
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base(file_path, knowledge_base)
                    print("Aether: Thanks! I've learned something new.")
                else:
                    print("Aether: Incorrect password. I won't save that.")

if __name__ == '__main__':
    chat_bot()
