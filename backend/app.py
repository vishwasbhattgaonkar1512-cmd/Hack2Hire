from flask import Flask, request, jsonify
from flask_cors import CORS
from interviewer import get_question, get_expected_answer, set_field
from scorer import evaluate_answer
from openai_api import ai_api   # ✅ OpenAI API import

app = Flask(__name__)
CORS(app)

# ✅ Register OpenAI blueprint (NEW API)
app.register_blueprint(ai_api)

# =========================
# Interview State
# =========================
state = {
    "attempts": 0,
    "total_score": 0,
    "max_questions": 3,
    "active": True
}

# =========================
# Hiring Badge Logic
# =========================
def get_hiring_badge(accuracy):
    if accuracy >= 90:
        return "🟢 Strong Hire"
    elif accuracy >= 75:
        return "🟡 Hire with Training"
    elif accuracy >= 50:
        return "🟠 Average"
    else:
        return "🔴 Not Ready"

# =========================
# Start Interview (ORIGINAL)
# =========================
@app.route("/start", methods=["POST"])
def start():
    data = request.json
    set_field(data.get("resume", ""), data.get("jd", ""))
    state.update({
        "attempts": 0,
        "total_score": 0,
        "max_questions": 3,
        "active": True
    })
    return jsonify({"status": "Interview started"})

# =========================
# Get Question (ORIGINAL)
# =========================
@app.route("/question", methods=["GET"])
def question():
    if not state["active"]:
        return jsonify({"question": "Interview Ended"})

    if state["attempts"] >= state["max_questions"]:
        return jsonify({"question": "Interview Completed"})

    q = get_question()
    if q is None:
        state["active"] = False
        return jsonify({"question": "No more questions available"})

    return jsonify({"question": q})

# =========================
# Submit Answer (ORIGINAL)
# =========================
@app.route("/answer", methods=["POST"])
def answer():
    if not state["active"]:
        return jsonify({"message": "Interview Ended"})

    data = request.json
    expected = get_expected_answer()

    if not data.get("answer", "").strip():
        score = 0
    else:
        score = evaluate_answer(data["answer"], expected, data.get("time", 0))

    state["attempts"] += 1
    state["total_score"] += score

    accuracy = round(
        (state["total_score"] / (state["attempts"] * 100)) * 100, 2
    )

    if state["attempts"] == 3:
        if accuracy >= 85:
            state["max_questions"] = 7
        elif accuracy >= 50:
            state["max_questions"] = 5
        else:
            state["active"] = False

    if state["attempts"] == 7 and accuracy >= 90:
        state["max_questions"] = 17

    completed = False
    if state["attempts"] >= state["max_questions"]:
        completed = True
        state["active"] = False

    return jsonify({
        "score": score,
        "accuracy": accuracy,
        "badge": get_hiring_badge(accuracy),
        "completed": completed
    })

# =========================
# Run Server
# =========================
if __name__ == "__main__":
    app.run(debug=True)
