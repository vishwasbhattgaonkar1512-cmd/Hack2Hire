from question_bank import QUESTION_BANK
from resume_parser import extract_skills

questions_queue = []
q_index = 0

def set_field(resume, jd):
    global questions_queue, q_index
    skills = extract_skills(resume)

    questions_queue = []
    for skill in skills:
        if skill in QUESTION_BANK:
            questions_queue.extend(QUESTION_BANK[skill])

    if not questions_queue:
        questions_queue = QUESTION_BANK["technology"]

    q_index = 0

def get_question():
    global q_index
    if q_index >= len(questions_queue):
        return None
    q = questions_queue[q_index]["q"]
    q_index += 1
    return q

def get_expected_answer():
    return questions_queue[q_index - 1]["a"]
