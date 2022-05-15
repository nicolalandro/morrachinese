import asyncio
import streamlit as st
import time
# st.set_page_config(layout="wide")
if not hasattr(st, 'static_state'):
    st.static_state = {'update': 'Nothing to update'}

async def watch(test):
    while True:
        test.markdown(st.static_state['update'])
        r = await asyncio.sleep(1)

st.title('Sasso Carta Forbici')
name = st.text_input("UserName", "")
if st.button('click'):
    st.static_state['update'] = name + 'clicked'

test = st.empty()

asyncio.run(watch(test))