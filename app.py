from flask import Flask, request, session, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps
import re
import time

app = Flask(__name__)

# Demo-only secret. Do not use real secrets in a public repository.
app.secret_key = "demo-secret-change-in-production"

# Secure session configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

# Demo in-memory user store.
# Passwords are stored only as secure hashes.
users = {}

# Simple in-memory login rate limiter for the lab.
login_attempts = {}
MAX_ATTEMPTS = 5
WINDOW_SECONDS = 60


def valid_username(username):
    return (
        isinstance(username, str)
        and 3 <= len(username) <= 30
        and re.fullmatch(r"[A-Za-z0-9_]+", username) is not None
    )


def valid_password(password):
    return isinstance(password, str) and 8 <= len(password) <= 128


def rate_limited(username):
    now = time.time()
    attempts = login_attempts.get(username, [])

    attempts = [
        timestamp
        for timestamp in attempts
        if now - timestamp < WINDOW_SECONDS
    ]

    if len(attempts) >= MAX_ATTEMPTS:
        login_attempts[username] = attempts
        return True

    attempts.append(now)
    login_attempts[username] = attempts
    return False


def login_required(view):
    @wraps(view)
    def wrapped():
        if "username" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return view()

    return wrapped


@app.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not valid_username(username) or not valid_password(password):
        return jsonify({"error": "Invalid registration data"}), 400

    if username in users:
        return jsonify({"error": "Registration failed"}), 400

    users[username] = generate_password_hash(password)

    return jsonify({"message": "Registration successful"}), 201


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not valid_username(username) or not isinstance(password, str):
        return jsonify({"error": "Invalid username or password"}), 401

    if rate_limited(username):
        return jsonify({"error": "Too many login attempts"}), 429

    stored_hash = users.get(username)

    if not stored_hash or not check_password_hash(stored_hash, password):
        # Generic error prevents username enumeration.
        return jsonify({"error": "Invalid username or password"}), 401

    session.clear()
    session.permanent = True
    session["username"] = username

    return jsonify({"message": "Login successful"}), 200


@app.get("/profile")
@login_required
def profile():
    return jsonify({"username": session["username"]})


@app.post("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run()
