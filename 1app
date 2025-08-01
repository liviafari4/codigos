from flask import Flask, request, url_for, redirect
from flask import render_template

import sqlite3
from database import obter_conexao

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personagens/novo', methods=['GET', 'POST'])
def novo_personagem():
    if request.method == "POST":
        nome = request.form['nome']
        jogo = request.form['jogo']
        habilidade = request.form['habilidade']

        conn = obter_conexao()
        sql = "INSERT INTO personagens (nome, jogo_origem, habilidade_principal) VALUES (?, ?, ?)"
        conn.execute(sql, (nome, jogo, habilidade))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_personagens'))

    return render_template('novo_personagem.html')

@app.route('/personagens')
def listar_personagens():
    conn = obter_conexao()
    sql = "SELECT * FROM personagens"
    lista = conn.execute(sql).fetchall()
    conn.close()

    return render_template('listar_personagens.html', lista=lista)

if __name__ == '__main__':
    app.run(debug=True)
