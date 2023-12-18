import base64

import requests
import streamlit as st
import streamlit_mermaid as stmd
from langchain.callbacks import get_openai_callback

from langchain_helper import generate_mermaid_code

st.title("🦜🔗 Flowchart Generator App")
st.caption("🚀 A streamlit :red[Flowchart Generator App] powered by :blue[Langchain]")


# Method to display flowchart from mermaid code
def generate_flowchart_image(graph):
    graph_bytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    img_url = "https://mermaid.ink/img/" + base64_string
    page = requests.get(img_url)
    file_name = "flowchart.png"
    with open(file_name, 'wb') as file:
        file.write(page.content)
    image = open(file_name, "rb")
    st.download_button(
        label="Download image",
        data=image,
        file_name=file_name,
        mime="image/png")


with st.sidebar:
    st.header("Choose Model Parameters")
    model_name = st.selectbox(
        'Model',
        ('text-davinci-003', 'gpt-3.5-turbo'))
    st.write('You selected:', model_name)
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.1
    )
    st.write('Temperature:', temperature)
    max_tokens = st.slider(
        "Max tokens", min_value=1, max_value=1000, value=800,
    )
    st.write('Max tokens:', max_tokens)
    prompt_type = st.selectbox(
        'Prompt Type',
        ('Zero-shot', 'Few-shot'))
    st.write('You selected:', prompt_type)

form = st.form("Form", clear_on_submit=True)

input_text = form.text_input("Enter your input text to generate flow chart")

if form.form_submit_button("Generate Flowchart Diagram"):
    with st.spinner("Generating Mermaid Code"):
        with get_openai_callback() as cb:
            # calling the function to get the generated mermaid code
            response_code = generate_mermaid_code(input_text, model_name, temperature, max_tokens, prompt_type)
            generate_flowchart_image(response_code)
            with st.expander("See Cost Calculation Info"):
                st.text(cb)
        with st.expander("See Generated Flowchart Mermaid Code"):
            st.code(response_code)

        st.subheader("Flowchart Diagram")
        st.caption(input_text)
        stmd.st_mermaid(response_code, height=800)
