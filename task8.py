# Задание №8
# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email",
# "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе
# данных, а пароль должен быть зашифрован.

from flask import Flask, request, render_template
from models_for_task8 import db, User
from forms import RegistrationForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash



app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyuiopasdfghjklzxcvbnm'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_for_task8.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/task8', methods=['GET', 'POST'])
def task8():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return 'Пользователь успешно зарегистрирован!'
    return render_template('task8.html', form=form)