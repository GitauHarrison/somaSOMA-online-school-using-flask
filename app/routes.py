from app import app
from flask import render_template


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html', title='Login')


@app.route('/login', methods=['GET', 'POST'])
def register_parent():
    return render_template(
        'auth/parent_registration.html',
        title='Register As A Parent')
