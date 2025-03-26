"""
data_preparation.py

Generates a JSONL file that includes examples of:
 - Fill-in-the-blank questions
 - Simple Q&A / conversation
 - Vocabulary matching
 - Other custom activities

We focus on French in this example, but you can add other languages.
"""
import json

def create_chat_dataset(output_file="lingua_activities_chat.jsonl"):
    """
    Creates a JSONL dataset with multiple language-learning activity types in chat format.
    Each line contains a 'messages' key with a list of chat messages.
    """
    examples = [
        # 1) Fill in the blank (original)
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Fill in the blank: Je __ un chat. Possible words: [ai, suis, vas]. Which word correctly fills in the blank? Answer with explanation in French."},
                {"role": "assistant", "content": "ai\nExplanation: In French, 'J'ai un chat' is correct."}
            ]
        },
        # 2) Simple Q&A (original)
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Q&A: Comment dit-on 'apple' en français? Answer in a single word."},
                {"role": "assistant", "content": "pomme"}
            ]
        },
        # 3) Short conversation (original)
        {
            "messages": [
                {"role": "system", "content": "You are a friendly French tutor."},
                {"role": "user", "content": "Bonjour, comment ça va?"},
                {"role": "assistant", "content": "Ça va très bien, merci! Et toi?"}
            ]
        },
        # 4) Vocabulary matching (original)
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Vocabulary matching: Here are the pairs: 1) cat, 2) dog, 3) house, 4) city. French words: [maison, chien, chat, ville]. Match each English word with the correct French word."},
                {"role": "assistant", "content": "1) cat - chat\n2) dog - chien\n3) house - maison\n4) city - ville"}
            ]
        },
        # 5) Fill in the blank (variation, original)
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Fill in the blank: Nous ____ au supermarché. Possible words: [allons, avez, suis]. Which word correctly fills in the blank? Answer with a brief explanation in English."},
                {"role": "assistant", "content": "allons\nExplanation: 'Nous allons' means 'We are going.'" }
            ]
        },
        # 6) Additional Fill in the blank
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Fill in the blank: Il __ un livre intéressant. Possible words: [lit, lis, lire]. Which word is correct? Answer with explanation in French."},
                {"role": "assistant", "content": "lit\nExplanation: 'Il lit un livre intéressant' is correct because 'lit' is the third person singular form of 'lire' in the present tense."}
            ]
        },
        # 7) Additional Q&A
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Q&A: Quelle est la capitale de la France? Answer in a single word."},
                {"role": "assistant", "content": "Paris"}
            ]
        },
        # 8) Additional Short Conversation
        {
            "messages": [
                {"role": "system", "content": "You are a friendly French tutor."},
                {"role": "user", "content": "Salut, que fais-tu ce weekend?"},
                {"role": "assistant", "content": "Je vais visiter un musée et prendre un café avec des amis."}
            ]
        },
        # 9) Additional Vocabulary Matching
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Vocabulary matching: Match the English words with their French equivalents. English words: [water, bread, milk, cheese]. French words: [eau, pain, lait, fromage]."},
                {"role": "assistant", "content": "water - eau\nbread - pain\nmilk - lait\ncheese - fromage"}
            ]
        },
        # 10) Additional Fill in the blank (another variation)
        {
            "messages": [
                {"role": "system", "content": "You are a helpful French language tutor."},
                {"role": "user", "content": "Fill in the blank: Ils ___ au cinéma ce soir. Possible words: [vont, vonts, vontre]. Which word is correct? Answer with explanation in French."},
                {"role": "assistant", "content": "vont\nExplanation: 'Ils vont au cinéma ce soir' is correct because 'vont' is the correct third person plural form of 'aller'."}
            ]
        }
    ]

    with open(output_file, "w", encoding="utf8") as f:
        for example in examples:
            json_line = json.dumps(example, ensure_ascii=False)
            f.write(json_line + "\n")

    print(f"Chat dataset created: {output_file} with {len(examples)} examples.")

if __name__ == "__main__":
    create_chat_dataset()