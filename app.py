from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/language-selection")
def language_selection():
    return render_template("language_selection.html")

@app.route("/learn/<language>")
def learn(language):
    if language not in ['dari', 'pashto']:
        return render_template("coming_soon.html", language=language)
    return render_template("learn.html", language=language)

@app.route("/advanced")
def advanced():
    return render_template("advanced_language_selection.html")

@app.route("/advanced/<language>")
def advanced_language(language):
    if language not in ['dari']:
        return render_template("coming_soon.html", language=language)
    return render_template("advanced.html", language=language)

@app.route("/suggestions", methods=["POST"])
def suggestions():
    try:
        data = request.get_json()
        sentence = data["sentence"]
        word = data["word"]

        prompt = (
            f'Given the sentence "{sentence}" where the word "{word}" is underlined, '
            "generate five new sentences by replacing that word with a word from a different semantic category. "
            "Keep them grammatical and meaningful, and return each on its own line."
        )

        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        text = resp.choices[0].message.content.strip()
        suggestions = [line.strip().strip('"') for line in text.splitlines() if line.strip()]

        return jsonify({"suggestions": suggestions})

    except Exception as e:
        app.logger.exception("Error in /suggestions")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
