# 🎯 Skill Assessment & Career Guidance System

An AI-powered web application designed to help students identify their skills, evaluate their knowledge, and discover suitable career opportunities through intelligent skill assessments and personalized career recommendations.

The system uses Google's Gemini AI to generate dynamic multiple-choice questions (MCQs), evaluate user performance, and provide career guidance based on assessment results.

## 🚀 Project Overview

Choosing the right career path can be challenging for students and fresh graduates. This project aims to simplify career planning by providing an interactive skill assessment platform that evaluates users' knowledge and helps them identify suitable career paths.

Users can register, log in, complete skill-based assessments, view their scores, and receive AI-powered career and course recommendations.

## ✨ Key Features

- **User Authentication:** Secure user registration and login system.
- **Skill Assessment:** Interactive skill-based assessments to evaluate user knowledge.
- **AI Question Generation:** Automatically generates 25 MCQs using Google Gemini AI.
- **Dynamic Quiz System:** Displays questions and manages answers through interactive quiz sessions.
- **Automated Evaluation:** Calculates assessment scores based on submitted answers.
- **Career Guidance:** Provides career recommendations based on assessment performance.
- **Course Recommendations:** Suggests relevant learning courses to improve users' skills.
- **Session Management:** Maintains quiz progress and user responses using Flask sessions.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| AI Integration | Google Gemini API |
| Database | SQLite |
| Template Engine | Jinja2 |
| Session Management | Flask Sessions |
| Text Processing | Python Regex |

## 🏗️ Project Architecture

The application follows a client-server architecture.

1. **User Interface:** Users interact with the application through HTML, CSS, and JavaScript.
2. **Flask Backend:** Handles authentication, application routes, quiz logic, and user requests.
3. **Gemini AI Integration:** Generates skill-based assessment questions and supports career guidance.
4. **Quiz Evaluation:** Processes submitted answers and calculates assessment scores.
5. **Database:** SQLite stores user information.
6. **Result Generation:** Displays assessment results and relevant career and course recommendations.

## 📂 Project Structure

```text
Career-Guidance-System/
│
├── app.py
│
├── templates/
│   ├── skill_index.html
│   ├── skill_quiz.html
│   └── skill_result.html
│
├── static/
│   ├── css/
│   │   └──
