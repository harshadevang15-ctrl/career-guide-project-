from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask("__name__")
app.secret_key = 'supersecretkey'

# Initialize DB
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        qualification TEXT,
        category TEXT,
        work_status TEXT,
        experience TEXT,
        interested_fields TEXT,
        course_completion TEXT,
        password TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def dashboard_1():
    return render_template('dashboard1.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'skills': request.form['skills'],
            'qualification': request.form['qualification'],
            'category': request.form['category'],
            'work_status': request.form['work_status'],
            'experience': request.form.get('experience', ''),
            'interested_fields': request.form['interested_fields'],
            'course_completion': request.form.get('course_completion', ''),
            'password': request.form['password'],
            'confirm_password': request.form['confirm_password']
        }

        if data['password'] != data['confirm_password']:
            return "Passwords do not match!"

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO users (
                username, first_name, last_name, email, phone, skills,
                qualification, category, work_status, experience,
                interested_fields, course_completion, password
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (data['username'], data['first_name'], data['last_name'], data['email'], data['phone'],
                       data['skills'], data['qualification'], data['category'], data['work_status'],
                       data['experience'], data['interested_fields'], data['course_completion'], data['password']))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard_2'))
        else:
            return "Invalid credentials!"

    return render_template('login.html')

@app.route('/dashboard2')
def dashboard_2():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user details from the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (session['username'],))
    user = c.fetchone()
    conn.close()

    if user:
        # Get the user details
        username = user[1]  # Username is the 2nd column in the 'users' table
        first_name = user[2]  # First Name is the 3rd column
        email = user[4]  # Email is the 5th column
        phone = user[5]  # Phone is the 6th column
        skills = user[6]  # Skills are in the 7th column
        qualification = user[7]  # Qualification is in the 8th column
        work_status = user[9]  # Work Status is in the 10th column
        experience = user[10]  # Experience is in the 11th column
        interested_fields = user[11]  # Interested fields are in the 12th column
        course_completion = user[12]  # Course Completion is in the 13th column
        category = user[8]  # Category is in the 9th column (either 'technical' or 'non-technical')

        return render_template('dashboard2.html', first_name=first_name, username=username, email=email, 
                               phone=phone, skills=skills, qualification=qualification, work_status=work_status, 
                               experience=experience, interested_fields=interested_fields, 
                               course_completion=course_completion, category=category)
    return "User not found!"

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (session['username'],))
    user = c.fetchone()
    conn.close()

    if request.method == 'POST':
        updated_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'skills': request.form['skills'],
            'qualification': request.form['qualification'],
            'work_status': request.form['work_status'],
            'experience': request.form.get('experience', ''),
            'interested_fields': request.form['interested_fields'],
            'course_completion': request.form.get('course_completion', ''),
        }

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''UPDATE users SET first_name=?, last_name=?, email=?, phone=?, skills=?, qualification=?, 
                    work_status=?, experience=?, interested_fields=?, course_completion=? WHERE username=?''',
                  (updated_data['first_name'], updated_data['last_name'], updated_data['email'], updated_data['phone'],
                   updated_data['skills'], updated_data['qualification'], updated_data['work_status'], updated_data['experience'],
                   updated_data['interested_fields'], updated_data['course_completion'], session['username']))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard_2'))

    # Pre-fill the form with current data
    if user:
        first_name = user[2]
        last_name = user[3]
        email = user[4]
        phone = user[5]
        skills = user[6]
        qualification = user[7]
        work_status = user[9]
        experience = user[10]
        interested_fields = user[11]
        course_completion = user[12]
        
        return render_template('edit_profile.html', first_name=first_name, last_name=last_name, email=email,
                               phone=phone, skills=skills, qualification=qualification, work_status=work_status,
                               experience=experience, interested_fields=interested_fields, 
                               course_completion=course_completion)
    return "User not found!"

@app.route('/view_skills')
def view_skills():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch user details from the database to view skills
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT skills FROM users WHERE username=?', (session['username'],))
    user = c.fetchone()
    conn.close()

    if user:
        skills = user[0]  # Skills are in the 7th column
        return render_template('view_skills.html', skills=skills)
    return "User not found!"

############################################
from flask import Flask, render_template, request, redirect, session, url_for
import google.generativeai as genai
import re
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

@app.route('/skillset', methods=['GET', 'POST'])
def skillset():
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

    # Determine the recommendation based on the score
    if score <= 10:
        recommendation = "Your score indicates that you need to review the basics more thoroughly. Focus on improving your foundational skills and practice more. Don't get discouraged; progress comes with consistent effort."
    elif score <= 20:
        recommendation = "You're doing well! Your score suggests that you're on the right path, but there is still room for improvement. Consider reviewing the areas you struggled with to improve further."
    else:
        recommendation = "Excellent work! Your score shows a strong understanding of the material. Keep up the great work and continue challenging yourself with more advanced topics."

    return render_template('skill_result.html', results=results, score=score, total=len(questions), career_guidance=recommendation)

@app.route('/recommendation/<category>')
def recommendation(category):
    recommendations = {
        'skillset': {
            'message': "Here are some resources to help you improve your skill set. Review the basics and practice more.",
            'courses': [
                "Introduction to Programming (Udemy)",
                "Android Application (Udemy)",
                "Python for Beginners (Coursera)",
                "React for Beginners (Coursera)",
                "Basic Web Development (freeCodeCamp)",
                "UI/UX (freeCodeCamp)"
            ]
        },
        'technical': {
            'message': "Based on your results, you should focus on improving your technical knowledge. Consider taking more technical courses.",
            'courses': [
                "Data Structures and Algorithms (Udemy)",
                "Advanced Python Programming (Coursera)",
                "Full Stack Web Development (freeCodeCamp)",
                "Data Science (Udemy)",
                "Data Analysis(Coursera)",
                "Data Mining (freeCodeCamp)"
            ]
        },
        'non-technical': {
            'message': "Based on your results, you might want to focus on improving your non-technical skills, such as communication and management.",
            'courses': [
                "Effective Communication Skills (LinkedIn Learning)",
                "Leadership and Management (Coursera)",
                "Time Management for Professionals (Udemy)",
                "Personal Skill Development (LinkedIn Learning)",
                "Attitude Management (Coursera)",
                "Client Satisfaction (Udemy)"
                
            ]
        },
        'High School': {
            'message': "Based on your results, you might want to focus on improving your non-technical skills, such as communication and management.",
            'courses': [
                "Computer Science",
                "Computer With Maths",
                "B.E/B.Tech",
                "B.SC",
                "B.Com",
                "B.A"
                
            ]
        }
    }

    category_recommendation = recommendations.get(category, None)
    if category_recommendation is None:
        return render_template('recommendation.html', category=category, recommendation="Invalid category.")

    recommendation_message = category_recommendation['message']
    courses = category_recommendation['courses']

    return render_template('recommendation.html', category=category, recommendation=recommendation_message, courses=courses)

############################################


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if" __name__ "== '__main__':
    app.run(debug=True)
