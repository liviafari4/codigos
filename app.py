# ======================= APP.PY =======================

"""
Aluno: Lívia Faria
Prova de PSI - Flask
Versão do Flask: 2.x.x
Projeto: Sistema de Login com Área Protegida
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta_123'

# FLASK-LOGIN SETUP
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# SIMULAÇÃO DE BANCO DE DADOS
usuarios = {}  # exemplo: {'joao': {'senha': '123'}}

# CLASSE DE USUÁRIO
class Usuario(UserMixin):
    def __init__(self, id):
        self.id = id

# FUNÇÃO QUE CARREGA O USUÁRIO
@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

# ROTA INICIAL
@app.route('/')
def home():
    return render_template('home.html')

# ROTA DE CADASTRO
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        if nome in usuarios:
            flash("Usuário já existe.")
        else:
            usuarios[nome] = {'senha': senha}
            flash("Cadastro realizado com sucesso!")
            return redirect(url_for('login'))
    return render_template('cadastro.html')

# ROTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        if nome in usuarios and usuarios[nome]['senha'] == senha:
            user = Usuario(nome)
            login_user(user)
            session['usuario'] = nome

            # SALVA O NOME DO USUÁRIO EM COOKIE
            resp = make_response(redirect(url_for('painel')))
            resp.set_cookie('ultimo_usuario', nome)
            flash("Login realizado com sucesso!")
            return resp
        else:
            flash("Usuário ou senha inválidos.")
    return render_template('login.html')

# ROTA PROTEGIDA
@app.route('/painel')
@login_required
def painel():
    usuario = current_user.id
    return render_template('painel.html', usuario=usuario)

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.")
    return redirect(url_for('login'))

# EXECUTA O SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)





# ======================= BASE.HTML =======================

"""
templates/base.html
"""

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Sistema{% endblock %}</title>
</head>
<body>
    <h1>{% block header %}Sistema de Login{% endblock %}</h1>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
</body>
</html>





# ======================= HOME.HTML =======================

"""
templates/home.html
"""

{% extends 'base.html' %}

{% block title %}Página Inicial{% endblock %}

{% block content %}
  <p>Bem-vindo! Escolha uma opção:</p>
  <a href="{{ url_for('login') }}">Login</a> |
  <a href="{{ url_for('cadastro') }}">Cadastro</a>
{% endblock %}





# ======================= LOGIN.HTML =======================

"""
templates/login.html
"""

{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
  <form method="POST">
    <label>Usuário:</label>
    <input type="text" name="usuario" required><br>
    <label>Senha:</label>
    <input type="password" name="senha" required><br>
    <input type="submit" value="Entrar">
  </form>
{% endblock %}





# ======================= CADASTRO.HTML =======================

"""
templates/cadastro.html
"""

{% extends 'base.html' %}

{% block title %}Cadastro{% endblock %}

{% block content %}
  <form method="POST">
    <label>Usuário:</label>
    <input type="text" name="usuario" required><br>
    <label>Senha:</label>
    <input type="password" name="senha" required><br>
    <input type="submit" value="Cadastrar">
  </form>
{% endblock %}





# ======================= PAINEL.HTML =======================

"""
templates/painel.html
"""

{% extends 'base.html' %}

{% block title %}Painel{% endblock %}

{% block content %}
  <p>Bem-vindo, {{ usuario }}! Esta é uma área protegida.</p>
  <a href="{{ url_for('logout') }}">Sair</a>
{% endblock %}
