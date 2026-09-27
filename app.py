import os
import sqlite3

from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "development-only-change-me")

DB_NAME = "site.db"
GAMES = [
    {
        "slug": "neon-drift",
        "title": "Neon Drift",
        "genre": "Racing",
        "description": "Thread your way through a synthwave city at impossible speed.",
        "players": "1,248",
        "accent": "pink",
    },
    {
        "slug": "void-strike",
        "title": "Void Strike",
        "genre": "Action",
        "description": "Clear hostile sectors and climb the weekly combat leaderboard.",
        "players": "892",
        "accent": "blue",
    },
    {
        "slug": "pixel-forge",
        "title": "Pixel Forge",
        "genre": "Strategy",
        "description": "Build an unstoppable crew, craft rare gear, and outsmart rivals.",
        "players": "641",
        "accent": "gold",
    },
]


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        conn.commit()


@app.route('/')
def home():
    return render_template('index.html', messages=get_flashed_messages())


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()

    if not name or not email or not password:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('home'))

    if len(password) < 6:
        flash('Password must contain at least 6 characters.', 'error')
        return redirect(url_for('home'))

    conn = get_db()
    existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    if existing:
        conn.close()
        flash('An account with that email already exists.', 'error')
        return redirect(url_for('home'))

    hashed_password = generate_password_hash(password)
    conn.execute(
        'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
        (name, email, hashed_password)
    )
    conn.commit()
    conn.close()

    flash('Signup successful! Please log in.', 'success')
    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()

    if not email or not password:
        flash('Email and password are required.', 'error')
        return redirect(url_for('home'))

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user['password'], password):
        flash('Invalid email or password.', 'error')
        return redirect(url_for('home'))

    session['user_id'] = user['id']
    session['user_name'] = user['name']
    session['user_email'] = user['email']

    flash('Login successful!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('home'))

    return render_template(
        'dashboard.html',
        user_name=session['user_name'],
        games=GAMES,
    )


@app.route('/game/<slug>')
def game(slug):
    if 'user_id' not in session:
        flash('Please log in to play.', 'error')
        return redirect(url_for('home'))

    selected_game = next((item for item in GAMES if item["slug"] == slug), None)
    if selected_game is None:
        flash('That game is not available.', 'error')
        return redirect(url_for('dashboard'))

    return render_template('game.html', game=selected_game, user_name=session['user_name'])


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


init_db()


if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
