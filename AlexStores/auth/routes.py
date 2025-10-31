from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import db
from models.user import User
from forms import LoginForm, RegistrationForm # NOVO

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm() # NOVO: Instancia o formulário
    if form.validate_on_submit(): # NOVO: Valida no envio (POST)
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("product_bp.list_products"))
        flash("Usuário ou senha incorretos.")
    return render_template("auth/login.html", form=form) # NOVO: Passa o form

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm() # NOVO: Instancia o formulário
    if form.validate_on_submit(): # NOVO: Valida no envio (POST)
        # Os dados já foram validados pelo WTForms, incluindo unicidade
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form) # NOVO: Passa o form

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso!")
    return redirect(url_for("auth.login"))