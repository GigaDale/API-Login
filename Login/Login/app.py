from flask import Flask, render_template, request, make_response, session, redirect
from jinja2.exceptions import TemplateNotFound

import secrets
import middlewares.db_middleware as db
import middlewares.utils_middleware as utils

app = Flask("login")
app.secret_key = secrets.token_hex()

# Página principal
@app.route("/", methods=['GET'])
def home():
    try:
        return render_template("home.html"), 200
    except TemplateNotFound:
        return render_template("pagina_nao_encontrada.html"), 404


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        users_json = request.get_json()
        users_json['senha'] = utils.gen_hash(users_json, 'senha')
        if db.validation_login(users_json['usuario'], users_json['senha']) == 1:
            session['usuario'] = users_json['usuario']
            return render_template("logado.html", name=session['usuario']), 200
        else:
            return "<h1>Usuário não encontrado</h1>"
    else:
        return render_template("pagina_nao_encontrada.html"), 404
    
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('usuario', None)
    return render_template("logout.html")

@app.route("/register", methods=['POST'])
def register():
    register_json = request.get_json()
    register_json['senha'] = utils.gen_hash(register_json, 'senha')
    if db.validation_login(register_json['usuario'], register_json['senha']) == 1:
        return "<h1>Usuário já existente, use outro nome</h1>"
    db.create_login(register_json['usuario'], register_json['senha'])
    return render_template("cadastro_sucesso.html", name=register_json['usuario'])

if __name__ == "__main__":
    app.run(debug=True) # Tirar debug antes de dar deploy