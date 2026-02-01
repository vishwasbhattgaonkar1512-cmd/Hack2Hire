from flask import Blueprint, request, jsonify
import os
from openai import OpenAI, RateLimitError

ai_api = Blueprint("ai_api", __name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create client only if key exists
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

@ai_api.route("/ai-question", methods=["POST"])
def ai_question():
    data = request.json or {}
    prompt = data.get("prompt", "Ask a technical interview question")

    # 🔴 If no API key
    if not client:
        return jsonify({
            "question": "What is Python and why is it used in AI development?",
            "mode": "no_api_key_fallback"
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI interviewer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=80
        )

        return jsonify({
            "question": response.choices[0].message.content.strip(),
            "mode": "openai"
        })

    except RateLimitError:
        # 🟡 QUOTA EXCEEDED → fallback
        return jsonify({
            "question": "Explain OOP concepts in Python with example.",
            "mode": "quota_fallback"
        })

    except Exception as e:
        return jsonify({
            "question": "What is the difference between list and tuple in Python?",
            "mode": "error_fallback",
            "error": str(e)
        })
