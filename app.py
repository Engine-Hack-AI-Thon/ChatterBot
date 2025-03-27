from app_integration import *
import gradio as gr
from enum import Enum


class State(Enum):
    SEND_INITIAL_MESSAGE = 0
    SEND_RESPONSE_TO_USER = 1
    IN_CONVERSATION = 2
    STANDBY = 3


def predict(message, history, session, type, state, task):
    """
    Main prediction function, runs when user sends a new message.
    """
    if state == State.SEND_RESPONSE_TO_USER:
        if type == "Fill in the Blank":
            return {"role": "assistant",
                    "content": verify_answer("fill_in_the_blank", task, message)}, State.STANDBY, None
        elif type == "Q&A":
            return {"role": "assistant",
                    "content": verify_answer("q_and_a", task, message)}, State.STANDBY, None
        elif type == "Vocabulary Matching":
            return {"role": "assistant",
                    "content": verify_answer("vocabulary_matching", task, message)}, State.STANDBY, None
    elif state == State.IN_CONVERSATION:
        response, wants_to_continue = advance_conversation(message, history)
        if not wants_to_continue:
            return {"role": "assistant", "content": response}, State.STANDBY, None
        else:
            return {"role": "assistant", "content": response}, State.IN_CONVERSATION, None
    elif state == State.STANDBY:
        return {"role": "assistant",
                "content": "To continue, click the 'start a new session' button."}, State.STANDBY, None

    return {"role": "assistant", "content": "An internal error has occurred. Please try again later."}


def reset(session, type):
    """
    Runs on start of new session to reset chat history.
    """
    if type == "Fill in the Blank":
        task_description = {"role": "assistant",
                            "content": f"--- Fill-in-the-Blank Task ---\n{initiate_fill_in_blank(session)}"}
        new_state = State.SEND_RESPONSE_TO_USER
    elif type == "Q&A":
        task_description = {"role": "assistant", "content": f"--- Q&A Task ---\n{initiate_q_and_a(session)}"}
        new_state = State.SEND_RESPONSE_TO_USER
    elif type == "Conversation":
        task_description = {"role": "assistant",
                            "content": f"--- Conversation Task ---\n{initiate_conversation(session)}"}
        new_state = State.IN_CONVERSATION
    elif type == "Vocabulary Matching":
        task_description = {"role": "assistant",
                            "content": f"--- Vocabulary Matching Task ---\n{initiate_vocabulary_matching(session)}"}
        new_state = State.SEND_RESPONSE_TO_USER
    history = [task_description]
    return gr.update(value="Start a New Session"), history, history, gr.update(
        visible=True), new_state, task_description


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
                 show_download_button=False,
                 show_share_button=False,
                 scale=0)
        with gr.Column():
            input_session = gr.Textbox(label="What do you want to learn about today?",
                                       placeholder="Type here or leave blank to chose a random topic")
            input_type = gr.Dropdown(["Fill in the Blank", "Q&A", "Conversation", "Vocabulary Matching"],
                                     label="How do you want to practice?")
        start_btn = gr.Button("Start Session", scale=0, elem_id="start_btn")

    current_state = gr.State()
    current_task_description = gr.State()
    bot = gr.Chatbot(type="messages", render=False, show_label=False)
    with gr.Row(visible=False) as row:
        chat = gr.ChatInterface(fn=predict,
                                type="messages",
                                chatbot=bot,
                                additional_inputs=[input_session, input_type, current_state, current_task_description],
                                additional_outputs=[current_state, current_task_description],
                                autofocus=True
                                )
        reset_inputs = [input_session, input_type]
        reset_outputs = [start_btn, bot, chat.chatbot_state, row, current_state, current_task_description]
        input_session.submit(fn=reset, inputs=reset_inputs, outputs=reset_outputs)
        start_btn.click(fn=reset, inputs=reset_inputs, outputs=reset_outputs)
demo.launch()
