from backend.gemini_service import ask_gemini


def generate_quiz(topic, difficulty, num_questions):
    prompt = f"""
You are an expert teacher.

Generate {num_questions} multiple-choice questions.

Topic: {topic}

Difficulty: {difficulty}

Rules:

1. Each question should have four options:
A)
B)
C)
D)

2. Mention the correct answer after each question.

3. Explain the correct answer in one sentence.

4. Format the quiz neatly.
"""

    return ask_gemini(prompt)