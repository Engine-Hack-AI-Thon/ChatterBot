import gradio as gr

"""
    Main prediction function, runs when user sends a new message.
"""
def predict(message, history, session):
    return f"message={message}, session={session}"

"""
    Runs on start of new session to reset chat history.
"""
def reset(session):
    history = [{"role": 'assistant', "content": f'Hello! Do you want to learn about {session} in French?'}]
    return history, history

with gr.Blocks() as demo:
    gr.Markdown(f"<h1 style='text-align: center; margin-bottom: 1rem'>ChatterBot</h1>")
    with gr.Row():
        input_session = gr.Textbox(show_label=False, scale=1, placeholder="What do you want to learn about today?")
        start_btn = gr.Button("Start Session", scale = 0)

    bot = gr.Chatbot(type="messages", render=False)
    chat = gr.ChatInterface(fn=predict, type="messages", chatbot=bot, additional_inputs=input_session)
    start_btn.click(fn=reset, inputs=[input_session], outputs=[bot, chat.chatbot_state])

demo.launch()
