from flask import Flask, render_template, request, redirect, session, url_for
import google.generativeai as genai
import re



# API/SkillSet.py
from flask import Blueprint, render_template

# Create a Blueprint for SkillSet
skillset_blueprint = Blueprint('skillset', __name__)







app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure Gemini API
genai.configure(api_key="AIzaSyClwCo8aIpV8gieeDQ5HsjiASODhGkxt-0")

# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Generate 25 MCQs based on skill set. Each question must have options (a-d) and clearly state the correct answer like 'Answer: b'"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        skill_set = request.form['skill']
        chat = model.start_chat()
        response = chat.send_message(
            f"My skill set is: {skill_set}. Please create 25 MCQ questions with 4 options (a to d) and include the correct answer like 'Answer: b' after each question."
        )
        raw_quiz = response.text
        lines = raw_quiz.splitlines()

        questions = []
        answer_key = []
        current_question = None

        for line in lines:
            line = line.strip()
            if re.match(r"^\d+\.", line):
                if current_question:
                    questions.append(current_question)
                current_question = {"question": line, "options": []}
            elif re.match(r"^[a-dA-D]\)", line):
                if current_question:
                    current_question["options"].append(line)
            elif line.lower().startswith("answer:"):
                answer = line.split(":")[1].strip().lower()
                answer_key.append(answer)

        if current_question:
            questions.append(current_question)

        session['questions'] = questions[:25]
        session['answer_key'] = answer_key[:25]
        session['user_answers'] = []
        session['current_q'] = 0

        return redirect(url_for('quiz'))

    return render_template('skill_index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session or 'current_q' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        answer = request.form.get('answer', '').lower()
        if answer in ['a', 'b', 'c', 'd']:
            session['user_answers'].append(answer)
            session['current_q'] += 1

    current_q_index = session['current_q']
    if current_q_index >= len(session['questions']):
        return redirect(url_for('result'))

    question = session['questions'][current_q_index]
    return render_template('skill_quiz.html', index=current_q_index + 1, question=question)


@app.route('/result')
def result():
    questions = session.get('questions', [])
    user_answers = session.get('user_answers', [])
    answer_key = session.get('answer_key', [])
    score = 0
    results = []

    for i, (user, correct) in enumerate(zip(user_answers, answer_key)):
        is_correct = user == correct
        if is_correct:
            score += 1
        results.append({
            'q_num': i + 1,
            'your_answer': user,
            'correct_answer': correct,
            'is_correct': is_correct
        })

    return render_template('skill_result.html', results=results, score=score, total=len(questions))


if __name__ == '__main__':
    app.run(debug=True)
