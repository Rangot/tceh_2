import random
from flask import Flask, request, url_for
from flask.json import jsonify

from flask_wtf import FlaskForm
from wtforms import IntegerField, validators


FLASK_RANDOM_SEED = random.seed(1)
Guessed_numbers = {}


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='This key must be secret!',
    WTF_CSRF_ENABLED=False,
)


class ContactForm(FlaskForm):
    guess = IntegerField(validators=[
        validators.NumberRange(min=1, max=99, message='Введите число от 1 до 99')
    ])


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        home.numb_of_game = 0
        home.number = random.randint(0, 100)
        print(home.number)
        return 'Число загадано', 200


@app.route('/guess', methods=['POST'])
def guessing():
    form = ContactForm(request.form)
    status_output = {0: 'Загаданное число больше', 1: 'Загаданное число меньше',
                     3: 'Вы угадали! Новое число создано'}
    if request.method == 'POST':
        if form.validate():
            user_guess = form.data['guess']
            result = user_guessing(user_guess)
            status_check = jsonify(status_output[result])
            return status_check
        else:
            return str(form.errors['guess'])
    else:
        return url_for('home')


def user_guessing(user_guess):
    if user_guess < home.number:
        return 0
    elif user_guess > home.number:
        return 1
    elif user_guess == home.number:
        home.numb_of_game += 1
        Guessed_numbers[home.numb_of_game] = home.number
        home.number = random.randint(0, 100)
        print(Guessed_numbers)
        print(len(Guessed_numbers))
        print(home.number)
        return 3


if __name__ == '__main__':
    app.run()

