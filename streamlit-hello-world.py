# https://docs.streamlit.io/develop/api-reference
# https://streamlit.io/gallery

import streamlit as st

st.title('Reactive Streamlit App')
number = st.number_input('Insert a number')
st.write('The square of the number is:', number ** 2)