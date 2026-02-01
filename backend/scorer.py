def evaluate_answer(user_answer, expected_answer, time_left):
    user = user_answer.lower()
    expected = expected_answer.lower()

    keyword_match = sum(1 for w in expected.split() if w in user)

    accuracy = min(keyword_match * 5, 30)
    clarity = 20 if len(user.split()) >= 6 else 10
    depth = 20 if len(user) > 60 else 10
    relevance = 20 if keyword_match >= 2 else 10
    time_score = 10 if time_left > 0 else 0

    return accuracy + clarity + depth + relevance + time_score
