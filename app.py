import logging
import os
import streamlit as st
from client import OpenAiTextClassifier
from text_examples import AI_TEXT

API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="OpenAI Text Classifier", page_icon="🐙")
st.markdown("""
        <style>
                [data-testid="column"] {
                    width: calc(50% - 1rem);
                }
        </style>
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

if "origin_check_res" not in st.session_state:
    st.session_state.origin_check_res = ""
if "st.session_state.origin_text" not in st.session_state:
    st.session_state.origin_text = ""

detector = OpenAiTextClassifier(API_KEY)
CHECK_RES = "The OpenAI text classifier considers the text to be :{}[**{}**] AI-generated.\n({:.2f}%)"

def get_category_color(category):
    color_dict = {
        'very unlikely': 'green',
        'unlikely': 'violet',
        'unclear if it is': 'blue',
        'possibly': 'orange',
        'likely': 'red'
    }
    return color_dict[category]

def origin_text_on_change():
    st.session_state.origin_check_res = ""

def check(text: str):
    '''
    Use OpenAI text classifier to check if text is AI-Generated.
    '''
    if text == '':
        text = AI_TEXT
    if len(text) < 200:
        st.session_state.origin_check_res = "Text cannot be less than 1000 characters."
        return
    logging.info(f"Checking text...")
    with origin_text_result_placeholder:
        with st.spinner("Please wait while your text is being checked..."):
            rate, category = detector.detect(text)
            st.session_state.origin_check_res = CHECK_RES.format(get_category_color(category), category, rate)


st.header("OpenAI Text Classifier Demo")
st.write(
''' This mini-app show you a demo of using [OpenAI Text Classifier](https://platform.openai.com/ai-text-classifier) client. 
You can access the code on [GitHub](https://github.com/renyilin/OpenAI-Text-Classifier-Client).
''')
origin_text = st.text_area("**Enter your text here:** ", value=st.session_state.origin_text, key="original",
                            height=400, on_change=origin_text_on_change,
                            help="Enter text you want to check. If leave it empty, the default text will be used.",
                            placeholder=AI_TEXT)
_, btn_col, _ = st.columns([1, 8, 1])
with btn_col:
    check_clicked = st.button("**AI-Generated Text Check**", type="primary", use_container_width=True, on_click=check,
                              args=[origin_text])
origin_text_result_placeholder = st.empty()
if st.session_state.origin_check_res:
    with origin_text_result_placeholder:
        st.info(st.session_state.origin_check_res, icon="ℹ️")
