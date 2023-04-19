from flask import Flask, render_template, request, make_response, session, redirect, flash
from jinja2.exceptions import TemplateNotFound

import secrets
import middlewares.db_middleware as db
import middlewares.utils_middleware as utils

app = Flask(__name__)
app.secret_key = secrets.token_hex()

# Página principal
@app.route("/", methods=['GET'])
def home():
    try:
        return render_template("html/home.html"), 200
    except TemplateNotFound:
        return render_template("html/pagina_nao_encontrada.html"), 404


@app.route("/login", methods=['POST', 'GET'])
def login():
    try:
        if request.method == "POST":
            username = request.form.get('username')
            password = utils.gen_hash(request.form.get('password'))
            if db.validation_login(username, password) == 1:
                session['username'] = username
                return render_template("html/logado.html", name=session['username'])
            else:
                flash('Usuário e/ou senha incorretos.')
                return redirect('/login')
        return render_template("html/login.html")
    except TemplateNotFound:
        return render_template("html/pagina_nao_encontrada.html"), 404
    
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('usuario', None)
    return render_template("html/logout.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = utils.gen_hash(request.form.get('password'))
        if db.validation_login(username, password) == 0:
            db.create_user(username, password)
            session['username'] = username
            return redirect(f'/success')
        else:
            flash('Usuário já existe. Tente novamente.')
            return redirect('/register')
    return render_template("html/cadastro.html")
    
@app.route("/success", methods=['POST', 'GET'])
def success():
    return render_template("html/cadastro_sucesso.html", name=session['username'])

if __name__ == "__main__":
    app.run(debug=True) # Tirar debug antes de dar deploy