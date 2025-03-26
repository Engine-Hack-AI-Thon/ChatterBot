import gradio as gr

"""
    Main prediction function, runs when user sends a new message.
"""


def predict(message, history, session, type):
    return f"message={message}, session={session}, type={type}"


"""
    Runs on start of new session to reset chat history.
"""


def reset(session, type):
    history = [{"role": 'assistant',
                "content": f"Hello! I'd be happy to practice {session} in French with you through {type}!"}]
    return gr.update(value="Start a New Session"), history, history, gr.update(visible=True)


CSS = """
    .gradio-container { background-color: #fbf3e2; }
    .contain { display: flex; flex-direction: column; }
    #start_btn { height: 175px; }
    #start_btn:hover { background-color: #124BDB; color: #FFFFFF }
    """

with gr.Blocks(css=CSS) as demo:
    with gr.Row():
        gr.Image("logo-sized.jpeg",
                 container=False,
                 height="175px",
                 show_label=False,
                 show_fullscreen_button=False,
                 show_download_button=False, scale=0)
        with gr.Column():
            input_session = gr.Textbox(label="What do you want to learn about today?",
                                       placeholder="Type here or leave blank to chose a random topic")
            input_type = gr.Dropdown(["Fill in the Blanks", "Translate"], label="How do you want to practice?")
        start_btn = gr.Button("Start Session", scale=0, elem_id="start_btn")

    bot = gr.Chatbot(type="messages", render=False, show_label=False)
    with gr.Row(visible=False) as row:
        chat = gr.ChatInterface(fn=predict,
                                type="messages",
                                chatbot=bot,
                                additional_inputs=[input_session, input_type],
                                autofocus=True,
                                )
        input_session.submit(fn=reset, inputs=[input_session, input_type],
                             outputs=[start_btn, bot, chat.chatbot_state, row])
        start_btn.click(fn=reset, inputs=[input_session, input_type], outputs=[start_btn, bot, chat.chatbot_state, row])
demo.launch()
