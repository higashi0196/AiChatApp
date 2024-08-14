import os
from flask import Flask, request, redirect, url_for, render_template
import openai
import re

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは賢いAIです。"},
                {"role": "user", "content": f"{animal}の名前を3個考えてください"}
            ],
            temperature=0.6,
        )
        
        tempresult = response.choices[0].message['content']
        result_text = re.sub(r'(\d+)\.', r'\n\1.', tempresult)

        return redirect(url_for("index", result=result_text))
    
    result = request.args.get("result","")
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(port=5001, debug=True)