# https://www.gradio.app/docs/interface
# https://www.gradio.app/custom-components/gallery

import gradio as gr

def greet(name):
    return "Hello " + name + "!"

app = gr.Interface(fn=greet, inputs="text", outputs="text")
app.launch(share=True, server_name="0.0.0.0")
