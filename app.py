from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avar.db'
db = SQLAlchemy()

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)


db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        with open('Questions.txt', 'r', encoding='utf-8') as questions_file:
            for line in questions_file:
                question = Questions(question_text=line)
                db.session.add(question)
                db.session.commit()
    except:
        pass

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/questions', methods=['get'])
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    
    user = User(
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    q8 = request.args.get('q8')
    q9 = request.args.get('q9')
    q10 = request.args.get('q10')
    
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10)
    db.session.add(answer)
    db.session.commit()
    
    return 'Ok'


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()

    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    all_info['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0]
    all_info['q3_mean'] = db.session.query(func.avg(Answers.q3)).one()[0]
    all_info['q4_mean'] = db.session.query(func.avg(Answers.q4)).one()[0]
    all_info['q5_mean'] = db.session.query(func.avg(Answers.q5)).one()[0]
    all_info['q6_mean'] = db.session.query(func.avg(Answers.q6)).one()[0]
    all_info['q7_mean'] = db.session.query(func.avg(Answers.q7)).one()[0]
    all_info['q8_mean'] = db.session.query(func.avg(Answers.q8)).one()[0]
    all_info['q9_mean'] = db.session.query(func.avg(Answers.q9)).one()[0]
    all_info['q10_mean'] = db.session.query(func.avg(Answers.q10)).one()[0]

    return render_template('stats.html', all_info=all_info)

if __name__ == "__main__":
    app.run()