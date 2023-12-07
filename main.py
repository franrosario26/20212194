# main.py
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Rutas
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('bienvenida'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if validate_login(username, password):
            session['username'] = username
            return redirect(url_for('bienvenida'))

    return render_template('login.html')

@app.route('/bienvenida')
def bienvenida():
    if 'username' in session:
        username = session['username']
        return render_template('bienvenida.html', username=username)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not user_exists(username):
            add_user(username, password)
            session['username'] = username
            return redirect(url_for('bienvenida'))

    return render_template('registro.html')

def user_exists(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def validate_login(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

if __name__ == '__main__':
    app.run(debug=True)

