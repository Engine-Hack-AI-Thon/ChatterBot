"""
app_integration.py

Example snippet showing how to integrate usage.py with an existing UI framework.
"""

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load your fine-tuned chat model.
# Replace this with your actual fine-tuned model name.
FINE_TUNED_MODEL = "ft:gpt-4o-mini-2024-07-18:personal::BFT1H34c"


def generate_chat_response(messages, max_tokens=150, temperature=0.7):
    """
    Sends a list of chat messages to the ChatCompletion endpoint.
    Returns the assistant's message.
    """
    response = client.chat.completions.create(model=FINE_TUNED_MODEL,
    messages=messages,
    max_tokens=max_tokens,
    temperature=temperature,
    top_p=1.0)
    return response.choices[0].message.content.strip()


def initiate_fill_in_blank():
    """
    Generates a fill-in-the-blank task in French.
    The generated output should include a sentence with a blank
    and the correct answer (hidden from the user).
    We assume the assistant returns a message with the blank and an explanation.
    """
    messages = [
        {"role": "system",
         "content": "You are a creative French language tutor who generates fill-in-the-blank exercises. Do not reveal the answer to the user."},
        {"role": "user",
         "content": "Generate a French fill-in-the-blank sentence. The exercise should include one or more blanks and a hidden answer."}
    ]
    task = generate_chat_response(messages)
    return task


def initiate_q_and_a():
    """
    Generates an initial Q&A task in French.
    The assistant generates a question that expects a single-word or short answer.
    """
    messages = [
        {"role": "system", "content": "You are a French language tutor who creates engaging Q&A questions."},
        {"role": "user", "content": "Generate a simple French question that requires a one-word answer."}
    ]
    task = generate_chat_response(messages)
    return task


def initiate_conversation():
    """
    Generates a conversation starter or context.
    Returns the initial conversation message from the system.
    """
    messages = [
        {"role": "system",
         "content": "You are a friendly French tutor. Initiate a conversation by providing a conversation starter or a scene context in French."},
        {"role": "user", "content": "Start a conversation in French."}
    ]
    starter = generate_chat_response(messages)
    return starter


def initiate_vocabulary_matching():
    """
    Generates a vocabulary matching task.
    The assistant should generate a list of French words and a scrambled list of English translations.
    """
    messages = [
        {"role": "system",
         "content": "You are a creative French language tutor who generates vocabulary matching exercises."},
        {"role": "user",
         "content": "Generate a vocabulary matching task in French. Provide a list of French words and a scrambled list of English translations. Do not reveal which pair is correct."}
    ]
    task = generate_chat_response(messages)
    return task


def conversation_loop(initial_context=None):
    """
    Continues a conversation until the user chooses to end it.
    Maintains conversation history.
    """
    conversation_history = []
    if initial_context:
        conversation_history.append({"role": "assistant", "content": initial_context})
        print("Conversation starter:")
        print(initial_context)

    print("Type your message in French (or type 'quit' to end the conversation).")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            print("Ending conversation.")
            break
        conversation_history.append({"role": "user", "content": user_input})
        # Get response while preserving the conversation history.
        response = generate_chat_response(conversation_history)
        conversation_history.append({"role": "assistant", "content": response})
        print("Bot:", response)


def main():
    print("Welcome to the ChatterBot language learning interface!")
    while True:
        print("\nSelect an option:")
        print("1. Start a new Fill-in-the-Blank task")
        print("2. Start a new Q&A task")
        print("3. Start a new Conversation")
        print("4. Start a new Vocabulary Matching task")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            # Generate and display a fill-in-the-blank exercise.
            task = initiate_fill_in_blank()
            print("\n--- Fill-in-the-Blank Task ---")
            print(task)
            # Optionally, you can now ask the user to input their answer and verify it.
            answer = input("Enter your answer: ").strip()
            # In a real application, you might compare 'answer' to a stored correct answer.
            print("Your answer was:", answer)
            print("-------------------------------")

        elif choice == "2":
            # Generate and display a Q&A task.
            task = initiate_q_and_a()
            print("\n--- Q&A Task ---")
            print("Question:", task)
            answer = input("Your answer: ").strip()
            print("You answered:", answer)
            print("----------------")

        elif choice == "3":
            # Start a new conversation. Generate an initial conversation starter.
            starter = initiate_conversation()
            print("\n--- Conversation Starter ---")
            print(starter)
            print("-----------------------------")
            conversation_loop(initial_context=starter)

        elif choice == "4":
            # Generate and display a vocabulary matching exercise.
            task = initiate_vocabulary_matching()
            print("\n--- Vocabulary Matching Task ---")
            print(task)
            # In a full implementation, you'd allow the user to match words and then verify.
            input("Press Enter when you are done reviewing the task...")
            print("-------------------------------")

        elif choice == "5":
            print("Exiting the interface.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()