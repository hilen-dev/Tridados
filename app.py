from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/npc")
def npc():
    return render_template("npc.html")

@app.route("/campanha")
def campanha():
    return render_template("campanha.html")

@app.route("/homebrew_editor")
def homebrew_editor():
    return render_template("homebrew_editor.html")

@app.route('/criar_ficha', methods=['GET', 'POST'])
def criar_ficha():
    if request.method == 'POST':
        # Aqui depois vamos salvar no banco ou em arquivo
        nome = request.form['nome']
        idade = request.form['idade']
        pericias = request.form['pericias']
        poder = request.form['poder']
        habilidade = request.form['habilidade']
        resistencia = request.form['resistencia']
        vantagens = request.form['vantagens']
        historico = request.form['historico']

        print("FICHA RECEBIDA:", nome)  # só pra testar

    return render_template('criar_ficha.html')


if __name__ == '__main__':
    app.run(debug=True)
