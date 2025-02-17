import spacy
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Spacy English model
nlp = spacy.load('en_core_web_sm')

# Sample knowledge base with intents and responses
knowledge_base = {
    'greeting': ['Hello!', 'Hi there!', 'Greetings!', 'How can I help you today?'],
    'farewell': ['Goodbye!', 'See you later!', 'Take care!', 'Until next time!'],
    'thanks': ['You\'re welcome!', 'No problem!', 'Glad I could help!', 'Anytime!'],
    'about_python': ['Python is a high-level programming language.', 
                   'Python is known for its simplicity and readability.',
                   'Python is widely used in data science and AI.'],
    'about_nlp': ['Natural Language Processing helps computers understand human language.',
                'NLP combines computational linguistics with machine learning.',
                'Common NLP tasks include sentiment analysis and named entity recognition.'],
    'about_chatbot': ['I\'m a chatbot built with Spacy and Python.',
                    'I was created as part of a CODTECH internship task.',
                    'I use NLP techniques to understand and respond to your queries.'],
    'default': ['I\'m not sure I understand.', 
              'Could you rephrase that?', 
              'I\'m still learning. Can you try asking differently?'],
}

# Define sample texts for each intent for training
intent_examples = {
    'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings'],
    'farewell': ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit'],
    'thanks': ['thank you', 'thanks', 'appreciate it', 'thank you so much'],
    'about_python': ['what is python', 'tell me about python', 'python programming', 'python language'],
    'about_nlp': ['what is nlp', 'natural language processing', 'how does nlp work', 'explain nlp'],
    'about_chatbot': ['who are you', 'what are you', 'tell me about yourself', 'chatbot information']
}

# Preprocessing with Spacy
def preprocess(text):
    doc = nlp(text.lower())
    # Get lemmatized tokens, excluding stop words and punctuation
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

# Function to determine intent
def get_intent(user_input):
    # Preprocess user input
    processed_input = preprocess(user_input)
    
    # Prepare examples for all intents
    all_examples = []
    intent_list = []
    
    for intent, examples in intent_examples.items():
        for example in examples:
            all_examples.append(preprocess(example))
            intent_list.append(intent)
    
    # Add user input to create the TF-IDF matrix
    all_examples.append(processed_input)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_examples)
    
    # Calculate cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Find the most similar example
    best_match_idx = np.argmax(similarity_scores)
    
    # If similarity is too low, return default intent
    if similarity_scores.max() < 0.2:
        return 'default'
    
    return intent_list[best_match_idx]

def get_response(intent):
    # Return a random response for the given intent
    return random.choice(knowledge_base[intent])

def chatbot():
    print("Spacy Chatbot: Hello! I'm your NLP chatbot. Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in intent_examples['farewell']:
            print("Spacy Chatbot: Goodbye! Thanks for chatting with me.")
            break
        
        intent = get_intent(user_input)
        response = get_response(intent)
        print(f"Spacy Chatbot: {response}")

if __name__ == "__main__":
    # Make sure to have the spacy model installed with:
    # python -m spacy download en_core_web_sm
    chatbot()
