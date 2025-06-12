"""Simple chat dashboard with user login."""

import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from zero_system import ZeroSystem


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me")


login_manager = LoginManager(app)
login_manager.login_view = "index"


# In-memory user store
USERS = {
    "demo": {"password": "demo", "name": "Demo User"},
}


class User(UserMixin):
    def __init__(self, username: str):
        self.id = username
        self.name = USERS[username]["name"]


@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None


system = ZeroSystem()

# Chat history per user (stored in memory)
history = {}


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("chat.html", history=history.get(current_user.id, []))
    return render_template("login.html")


@app.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in USERS and USERS[username]["password"] == password:
        login_user(User(username))
    return redirect(url_for("index"))


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.post("/chat")
@login_required
def chat():
    text = request.json.get("message", "")
    profile = {"id": current_user.id, "name": USERS[current_user.id]["name"]}
    resp = system.interact(text, profile)
    history.setdefault(current_user.id, []).append(
        {"user": text, "bot": resp["output"]}
    )
    return jsonify({"response": resp["output"]})


if __name__ == "__main__":
    app.run(debug=True)
