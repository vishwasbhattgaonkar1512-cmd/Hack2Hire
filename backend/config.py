TIME_LIMIT = 60
TERMINATION_SCORE = 40
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔴 fallback (ONLY if env not found)
if not OPENAI_API_KEY:
    OPENAI_API_KEY = "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"
