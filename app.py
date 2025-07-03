from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        curso = request.form.get('curso')
        resp = make_response(redirect(url_for('perfil', curso=curso)))
        resp.set_cookie('nome', nome, max_age=120)
        return resp

    return render_template('cadastro.html')

@app.route('/perfil')
def perfil():
    curso = request.args.get('curso')
    nome = request.cookies.get('nome', 'Visitante')
    return render_template('perfil.html', curso=curso, nome=nome)

if __name__ == '__main__':
    app.run(debug=True)