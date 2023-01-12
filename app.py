from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avar.db'
db = SQLAlchemy()

# таблицы с вопросами в базе данных нет, потому что в задании это был лишь рекомендуемый дизайн, а не обязательный,
# к тому же, я измучилась с вытаскиванием вопросов из бд и решила просто прописать их в html

class Answers(db.Model): # таблица с ответами
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


class User(db.Model): # таблица с информацией про пользователя: пол, образование и возраст
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)

db.init_app(app) # соединяем базу и приложение

@app.before_first_request # создаем бд
def db_creation():
    db.create_all()

@app.route('/') # я не знала, каким контентом наполнить страницу, так что скопировала информацию с каких-то разных сайтов и добавила ссылки на дополнительные материалы, зато сделала кастомные буллет-поинты
@app.route('/main') # это добавила, чтобы была возможность возвращаться на главную страницу при нажатии соответствующей кнопки
def index():
    return render_template("main.html")


@app.route('/questions') # вопросы, я решила что лучше их просто прописать в html, чтобы они выглядели так, как я хотела
def question_page():
    return render_template(
        'questions.html'
    )


@app.route('/process', methods=['get']) # сбор всей информации при ответе, просто взяла из конспектов
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    
    gender = request.args.get('gender') # изначально я хотела выводить на странице со статистикой пол, но потом передумала, пусть это будет доступно только владельцу и будет доставаться с помощью sql-запроса
    education = request.args.get('education') # здесь та же история, что с полом, кажется, будто не очень обязательно просто пользователю 
    age = request.args.get('age')
    
    user = User(
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user) # подгрузка информации о пользователе в бд
    
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
    # подгрузка информации об ответе на опрос в бд
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10)
    db.session.add(answer)
    db.session.commit()
    
    return render_template("answer.html") # это просто чтобы не сразу перекидывало на страницу со статой, будто ничего не произошло, флажочек, что все ок


@app.route('/stats') # подсчет статистики по пройденному опросу, я не писала что-то сверх конспекта, потому что не вижу в этом смысла
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0] # средний возраст респондентов
    all_info['age_min'] = age_stats[1] # минимальный возраст
    all_info['age_max'] = age_stats[2] # максимальный возраст
    all_info['total_count'] = User.query.count() # подсчет количества людей, прошедших опрос
# далее однотипный подсчет средней оценки предложений из опроса
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