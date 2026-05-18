from flask import Blueprint, render_template, request, redirect, session
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin
            return redirect("/admin" if user.is_admin else "/")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"]),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")