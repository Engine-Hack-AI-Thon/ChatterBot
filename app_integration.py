"""
app_integration.py

Example snippet showing how to integrate usage.py with an existing UI framework.
"""

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Replace with your actual fine-tuned chat model name.
FINE_TUNED_MODEL = "ft:gpt-4o-mini-2024-07-18:personal::BFT1H34c"


def generate_chat_response(messages, max_tokens=150, temperature=0.7):
    """
    Sends a list of chat messages to the ChatCompletion endpoint.
    Returns the assistant's message content.
    """
    response = client.chat.completions.create(model=FINE_TUNED_MODEL,
                                              messages=messages,
                                              max_tokens=max_tokens,
                                              temperature=temperature,
                                              top_p=1.0)
    return response.choices[0].message.content.strip()


def get_user_input():
    """
    Retrieves user input from the command line.
    Returns a dictionary with:
    {
      "task_type": <task>,
      "user_text": <text>
    }
    """
    print("Select a task type:")
    print("1. Fill in the blank")
    print("2. Q&A")
    print("3. Conversation")
    print("4. Vocabulary Matching")
    choice = input("Enter the number of the task type (or 'q' to quit): ").strip()
    if choice.lower() == 'q':
        return None
    task_types = {
        "1": "fill_in_the_blank",
        "2": "q_and_a",
        "3": "conversation",
        "4": "vocabulary_matching"
    }
    task_type = task_types.get(choice, "conversation")
    # For conversation, we don't require initial text.
    if task_type != "conversation":
        user_text = input("Enter your text or question (if applicable): ").strip()
    else:
        user_text = ""
    return {"task_type": task_type, "user_text": user_text}


def display_output(text):
    """
    Displays text to the console.
    Replace this with your actual UI display logic.
    """
    print("\n--- Model Response ---")
    print(text)
    print("----------------------\n")


def verify_answer(task_type, original_task, user_answer):
    """
    Verifies the user's answer by sending both the original task and the user's answer
    to the model, asking for feedback on correctness.
    """
    if task_type == "fill_in_the_blank":
        prompt = (
            f"Task: Fill in the blank (French).\n"
            f"Original exercise: {original_task}\n"
            f"User's answer: {user_answer}\n"
            "Provide feedback on whether the user's answer is correct and explain why."
        )
    elif task_type == "q_and_a":
        prompt = (
            f"Task: Q&A (French).\n"
            f"Question: {original_task}\n"
            f"User's answer: {user_answer}\n"
            "Provide feedback on whether the user's answer is correct and explain briefly."
        )
    elif task_type == "vocabulary_matching":
        prompt = (
            f"Task: Vocabulary Matching (French).\n"
            f"Exercise: {original_task}\n"
            f"User's matching: {user_answer}\n"
            "First, output the correct matching of french words and english words, making sure to say that this is the correct solution. Then, output the solution that the user gave, by assigning each french word to the next english word in the user's response. Then provide detailed feedback for the pairings the user made that do not match the correct matching."
        )
    else:
        prompt = f"User input: {user_answer}\nProvide feedback."

    messages = [
        {"role": "system", "content": "You are a French language tutor who provides detailed feedback."},
        {"role": "user", "content": prompt}
    ]
    feedback = generate_chat_response(messages, max_tokens=200)
    return feedback


def initiate_fill_in_blank(topic):
    """
    Generates a fill-in-the-blank exercise in French.
    """
    messages = [
        {"role": "system",
         "content": "You are a creative French language tutor who generates fill-in-the-blank exercises. Do not reveal the correct answer."},
        {"role": "user",
         "content": f"Generate a French fill-in-the-blank exercise on the topic of {topic} with one blank. Do not reveal the answer."}
    ]
    task = generate_chat_response(messages)
    return task


def initiate_q_and_a(topic):
    """
    Generates an initial Q&A question in French.
    """
    messages = [
        {"role": "system", "content": "You are a French language tutor who generates engaging Q&A questions."},
        {"role": "user",
         "content": f"Ask a simple French question about {topic} to your student. The question should have a one-word answer. Do not reveal the answer."}
    ]
    task = generate_chat_response(messages)
    return task


def initiate_conversation(topic):
    """
    Generates a conversation starter or scene context in French.
    """
    messages = [
        {"role": "system", "content": "You are a friendly French tutor that only speaks French."},
        {"role": "user",
         "content": f"Start a conversation in French on the topic of {topic} by providing a conversation starter or context. Always respond in French. In the event that the student responds in another language, remind them to speak in French only."}
    ]
    starter = generate_chat_response(messages)
    return starter


def initiate_vocabulary_matching(topic):
    """
    Generates a vocabulary matching exercise in French.
    """
    messages = [
        {"role": "system",
         "content": "You are a creative French language tutor who generates vocabulary matching exercises."},
        {"role": "user",
         "content": f"Generate a vocabulary matching exercise in French on the topic of {topic}. Provide a list of 5 French words and an out-of-order list of English translations. Do not reveal the correct matches."}
    ]
    task = generate_chat_response(messages)
    return task


def conversation_loop(initial_context=None):
    """
    Maintains a conversation until the user chooses to quit.
    """
    conversation_history = []
    if initial_context:
        conversation_history.append({"role": "assistant", "content": initial_context})
        print("Conversation starter:")
        print(initial_context)

    print("Type your message in French (or 'quit' to end the conversation).")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            print("Ending conversation.")
            break
        conversation_history.append({"role": "user", "content": user_input})
        response = generate_chat_response(conversation_history)
        conversation_history.append({"role": "assistant", "content": response})
        print("Bot:", response)


def advance_conversation(message, history):
    if message.lower() in ["quit", "exit"]:
        return "Ending conversation", False
    chat_history = [{"role": "system",
                     "content": "You are a friendly French tutor. You will remind your student to use French if they try speaking in a different language."}]
    chat_history.extend(history)
    chat_history.append({"role": "user", "content": message})
    return generate_chat_response(chat_history), True


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
            task = initiate_fill_in_blank()
            print("\n--- Fill-in-the-Blank Task ---")
            print(task)
            user_answer = input("Enter your answer: ").strip()
            feedback = verify_answer("fill_in_the_blank", task, user_answer)
            print("Feedback:", feedback)
            print("-------------------------------")

        elif choice == "2":
            task = initiate_q_and_a()
            print("\n--- Q&A Task ---")
            print("Question:", task)
            user_answer = input("Your answer: ").strip()
            feedback = verify_answer("q_and_a", task, user_answer)
            print("Feedback:", feedback)
            print("----------------")

        elif choice == "3":
            starter = initiate_conversation()
            print("\n--- Conversation Starter ---")
            print(starter)
            print("-----------------------------")
            conversation_loop(initial_context=starter)

        elif choice == "4":
            task = initiate_vocabulary_matching()
            print("\n--- Vocabulary Matching Task ---")
            print(task)
            user_answer = input("Enter your matching (format: frenchword: englishword, ...): ").strip()
            feedback = verify_answer("vocabulary_matching", task, user_answer)
            print("Feedback:", feedback)
            print("-------------------------------")

        elif choice == "5":
            print("Exiting the interface.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
