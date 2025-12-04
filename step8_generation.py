from helpers import * 
from pydantic import BaseModel, constr
from enum import Enum

import outlines

@outlines.prompt
def generate_comment_prompt(topic):
    """Generate social comment about {{ topic }}."""

names = Enum('names', ['Alice', 'Bob', 'Claire'])
class Comment(BaseModel):
    name: names
    comment: constr(min_length=10, max_length=200)
    

generate_comment = outlines.Function(
    generate_comment_prompt,
    Comment,
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

import streamlit as st
from ramda import *

def main():
    themes = ['Cats instincts', 'Cats behavior', 'Cats health', 'Cats nutrition', 'Cats training', 'Dogs instincts', 'Dogs behavior', 'Dogs health', 'Dogs nutrition', 'Dogs training']
    selected_theme = st.selectbox('Select a theme', themes)
    if st.button('Generate'):
        generated_comment = generate_comment(selected_theme)
        st.write(generated_comment)

if __name__ == '__main__':
    main()




