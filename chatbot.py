import pandas as pd

# Load your FAQ data
faq = pd.read_csv('hiring_training_faq.csv')

def get_best_answer(user_query):
    # Try exact match first
    for i, row in faq.iterrows():
        if user_query.strip().lower() == row['Question'].strip().lower():
            return row['Answer']
    # Keyword match: Return the answer to the question that shares the most words
    max_overlap = 0
    best_answer = "Sorry, I don't have an answer for that. Please contact hiring@cleardeals.com."
    user_words = set(user_query.lower().split())
    for i, row in faq.iterrows():
        question_words = set(str(row['Question']).lower().split())
        overlap = len(user_words & question_words)
        if overlap > max_overlap:
            max_overlap = overlap
            best_answer = row['Answer']
    return best_answer

# Simple command-line test loop (try it!)
if __name__ == '__main__':
    print("Cleardeals Hiring & Training Chatbot (type 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break
        print("Bot:", get_best_answer(query))




