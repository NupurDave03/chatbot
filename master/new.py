import pandas as pd
import gradio as gr

# Load your FAQ dataset; update path if needed
faq = pd.read_csv(r'hiring_training_faq.csv')

def get_best_answer(user_query):
    # Exact match
    for i, row in faq.iterrows():
        if user_query.strip().lower() == row['Question'].strip().lower():
            return row['Answer']
    # Keyword overlap match
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

def chatbot_response(chat_history, user_message):
    # Append user message
    chat_history = chat_history or []
    chat_history.append(("You", user_message))
    
    # Get bot answer
    answer = get_best_answer(user_message)
    chat_history.append(("Bot", answer))
    
    return chat_history, ""

with gr.Blocks() as demo:
    gr.Markdown("## Cleardeals Hiring & Training Chatbot")
    
    chatbot = gr.Chatbot(elem_id="chatbot").style(height=450)
    user_input = gr.Textbox(placeholder="Type your question here and hit enter...", show_label=False)
    
    user_input.submit(chatbot_response, inputs=[chatbot, user_input], outputs=[chatbot, user_input])

demo.launch()
