from flask import Flask, render_template, request, jsonify
from models import db, Question, Answer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('Forum.html', questions=questions)

@app.route('/add_question', methods=['POST'])
def add_question():
    text = request.json['text']
    question = Question(text=text)
    db.session.add(question)
    db.session.commit()
    return jsonify({"id": question.id, "text": question.text})

@app.route('/add_answer', methods=['POST'])
def add_answer():
    text = request.json['text']
    question_id = request.json['question_id']
    answer = Answer(text=text, question_id=question_id)
    db.session.add(answer)
    db.session.commit()
    return jsonify({"id": answer.id, "text": answer.text, "question_id": answer.question_id})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
