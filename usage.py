"""
usage.py

Script to load and query the fine-tuned model for different language-learning tasks.
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_fine_tuned_model(model_name):
    """
    Simple placeholder function in case you want
    to store the model name or load custom logic.
    """
    return model_name

def generate_response(model_name, user_prompt, max_tokens=100):
    """
    Sends the user_prompt to the fine-tuned model and returns the response.
    """
    response = client.completions.create(model=model_name,
    prompt=user_prompt,
    max_tokens=max_tokens,
    temperature=0.5,
    top_p=1.0)
    return response.choices[0].text.strip()

def main():
    # Example usage
    # Suppose your fine-tuned model name is "davinci:ft-your-org--lingua-activities-2023-xx-xx"
    fine_tuned_model = "davinci:ft-your-org--lingua-activities-2023-xx-xx"
    loaded_model = load_fine_tuned_model(fine_tuned_model)

    # A sample user prompt: fill in the blank
    user_prompt = (
        "Task: Fill in the blank (French)\n"
        "Sentence: Je __ un chat.\n"
        "Possible words: [ai, suis, vas]\n"
        "Question: Which word correctly fills in the blank?\n"
        "Answer with explanation in French.\n"
        "Answer:"
    )

    response_text = generate_response(loaded_model, user_prompt)
    print("Model Response:\n", response_text)

if __name__ == "__main__":
    main()