from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os

from recommender.rule_engine import RecommendationEngine
from recommender.groq_chat import ask_groq

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "pfa-final-semester-secret")

engine = RecommendationEngine()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    profile = {
        "name": request.form.get("name", "").strip(),
        "marks": request.form.get("marks", "0"),
        "interests": request.form.getlist("interests"),
        "skills": request.form.getlist("skills"),
        "preferred_work": request.form.get("preferred_work", ""),
        "math_level": request.form.get("math_level", ""),
        "goal": request.form.get("goal", "")
    }

    result = engine.recommend(profile)
    session["last_result"] = result
    session["last_profile"] = profile
    engine.save_history(profile, result)

    return render_template("result.html", profile=profile, result=result)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    profile = session.get("last_profile", {})
    result = session.get("last_result", {})

    if not message:
        return jsonify({"reply": "Please write a question first."})

    reply = ask_groq(message, profile, result)
    return jsonify({"reply": reply})


@app.route("/history")
def history():
    records = engine.load_history()
    return render_template("history.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
