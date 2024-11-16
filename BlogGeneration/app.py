from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
import streamlit as st


# Function to get response from Llama 2 model
def getLlamaResponse(input_text, no_words, blog_style):

    # Initialize the Llama model
    llm = CTransformers(
        model="model/llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        config={"max_new_tokens": 256, "temperature": 0.01}
    )

    # Define the template
    template = """
    Write a blog for {style} job profile for a topic {text}
    within {n_words} words.
    """

    prompt = PromptTemplate(input_variables=["style", "text", "n_words"], template=template)

    # Generate the response
    response = llm(prompt.format(style=blog_style, text=input_text, n_words=no_words))
    print(response)
    return response


st.set_page_config(page_title="Generate Blog", page_icon=":smile:", layout="centered", initial_sidebar_state="collapsed")
st.header("Generate Blogs")

# User input fields
input_text = st.text_input("Enter the Blog Topic")

# Creating two columns for additional fields
col1, col2 = st.columns([5, 5])
with col1:
    no_words = st.text_input("No of Words")

with col2:
    blog_style = st.selectbox("Writing the blog for", ("Researchers", "Data Scientists", "Common People"), index=0)


submit = st.button("Generate")

# Final Response
if submit:
    st.write(getLlamaResponse(input_text, no_words, blog_style))
