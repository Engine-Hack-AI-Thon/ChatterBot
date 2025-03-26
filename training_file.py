import json

# Define a list of training examples.
# You can extend or modify this list based on your textbook or assignment inputs.
# Here, we include examples for English-French and English-Italian.
examples = [
    {
        "prompt": "English-French: I don't has any idea what to do.",
        "completion": "I don't have any idea what to do. Explanation: Use 'have' with the pronoun 'I' instead of 'has'. In French, it would be: 'Je n'ai aucune idée de quoi faire.'"
    },
    {
        "prompt": "English-Italian: She go to school every day.",
        "completion": "She goes to school every day. Explanation: Add an 's' to 'go' for third-person singular. In Italian, this translates to: 'Lei va a scuola ogni giorno.'"
    },
    {
        "prompt": "English-French: He do not like pizza.",
        "completion": "He does not like pizza. Explanation: Use 'does not' with the singular subject 'he' instead of 'do not'. In French, you would say: 'Il n'aime pas la pizza.'"
    },
    {
        "prompt": "English-Italian: They is reading a book.",
        "completion": "They are reading a book. Explanation: Use 'are' with the plural subject 'they' instead of 'is'. In Italian, this is: 'Loro stanno leggendo un libro.'"
    }
]

# Write the examples to a JSONL file.
output_file = "chatterbot_training_data.jsonl"
with open(output_file, "w", encoding="utf8") as f:
    for example in examples:
        json_line = json.dumps(example, ensure_ascii=False)
        f.write(json_line + "\n")

print(f"JSONL training file '{output_file}' has been created with {len(examples)} examples.")