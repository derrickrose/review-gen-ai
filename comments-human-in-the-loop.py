import streamlit as st
import yaml
from ramda import *

with open('./steps/step9_comments.yaml', 'r') as file:
    comments = yaml.safe_load(file)['comments']

cat_comments = []
ok_comments = []

st.title('Comment Classification')

for comment in comments:
    st.write(f'{comment}')
    if st.radio('Classify Comment', ['ok', 'cat mafia'], key=comment) == 'cat mafia':
        cat_comments.append(comment)
    else:
        ok_comments.append(comment)

st.title('Examples of "cat" comments:')
st.write(join('\n\n', cat_comments))

st.title('Examples of "ok" comments:')
st.write(join('\n\n', ok_comments))
