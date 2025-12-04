import gradio as gr
import yaml
from helpers import * 

import requests

def breed_advisor(*answers):
    return requests.get(f"http://server:8000/which_dog_breed_should_i_choose?text={answers}").text

def breed_score(*answers):
    return requests.get(f"http://server:8000/breed_score?text={join('|',map(str, answers))}").text

# Load questions from the YAML file
with open('steps/step3_questions.yaml', 'r') as file:
    questions_data = yaml.safe_load(file)

# Extract questions and options
questions = []
for category in questions_data['questions']:
    for question in category['questions']:
        q_text = question['question']
        q_answers = question['answers']
        questions.append({'question': q_text, 'options': q_answers})

# # Create Gradio interface
def setup_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### Breed Advisor Questionnaire")
        inputs = []
        for q in questions:
            inputs.append(gr.Radio(q['options'], label=q['question']))
        gr.Button("Get advice").click(breed_advisor, inputs, gr.Textbox(label="Breed Advice"))
        gr.Button("Get score").click(breed_score, inputs, gr.Textbox(label="Breed Score"))
    return demo

app = setup_gradio_interface()

app.launch(server_name="0.0.0.0", share=True)