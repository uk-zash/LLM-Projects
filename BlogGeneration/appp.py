from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

app = Flask(__name__)

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
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve input from the form
        input_text = request.form.get("input_text")
        no_words = request.form.get("no_words")
        blog_style = request.form.get("blog_style")

        # Ensure valid number of words
        try:
            no_words = int(no_words)
        except ValueError:
            return render_template("index.html", error="Please enter a valid number for the word count.")

        # Ensure blog style is valid
        if blog_style not in ["Researchers", "Data Scientists", "Common People"]:
            blog_style = "Researchers"  # Default to "Researchers" if invalid

        # Generate the blog response
        response = getLlamaResponse(input_text, no_words, blog_style)
        return render_template("index.html", response=response)

    return render_template("index.html", response=None)

if __name__ == "__main__":
    app.run(debug=True)
