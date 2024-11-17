from flask import Flask , render_template , request
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

app = Flask(__name__)

def getResponse(input_text , no_words ,aud):
    llm = CTransformers(
        model = "model/llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type = "llama",
        max_tokens = no_words * 2,
        temperature = 0.01    )
    
    template = """Write a detailed, complete story on the topic '{input_text}' for the '{aud}' audience in approximately {no_words} words. Ensure the story has an introduction, middle, and conclusion. Make it engaging and interesting. """


    prompt = PromptTemplate(input_variables=["input_text" , "no_words" , "aud"] , template=template)

    response = llm(prompt.format(input_text= input_text , aud = aud , no_words = no_words ))
    return response


@app.route("/" , methods = ["GET" , "POST"])
def index():
    if request.method == "POST":

        input_text = request.form.get("story")
        words = request.form.get("words")
        aud = request.form.get("audience")

        try:
            words = int(words)
        except ValueError:
            return render_template("index.html" , error = "Please enter a valid no of words count")
        
        response = getResponse(input_text , words , aud)
        return render_template("index.html" , response = response)
    return render_template("index.html" , response = None)


if __name__ == "__main__":
    app.run(debug=True)