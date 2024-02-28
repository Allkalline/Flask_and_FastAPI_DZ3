# Задание №4
# Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
# содержать следующие поля:
# ○ Имя пользователя (обязательное поле)
# ○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
# ○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
# ○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
# После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
# и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
# заполнено или данные не прошли валидацию, то должно выводиться соответствующее
# сообщение об ошибке.
# Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
# базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
# об ошибке.


from flask import Flask, request, render_template
from models_for_task4 import db, User
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyuiopasdfghjklzxcvbnm'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/task4', methods=['GET', 'POST'])
def task4():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return 'Пользователь успешно зарегистрирован!'
    return render_template('task4.html', form=form)
