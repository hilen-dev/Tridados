from flask import Flask, render_template, request

app = Flask(__name__)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Criar Ficha
@app.route("/criar_ficha", methods=["GET", "POST"])
def criar_ficha():
    if request.method == "POST":
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        pericias = request.form.get("pericias")
        poder = request.form.get("poder")
        habilidade = request.form.get("habilidade")
        resistencia = request.form.get("resistencia")
        vantagens = request.form.get("vantagens")
        historico = request.form.get("historico")

        print("FICHA RECEBIDA:", nome)  # Teste temporário

        # Depois vamos salvar em TXT, JSON ou Banco de Dados
        # Por enquanto só mostra mensagem

    return render_template("criar_ficha.html")

# Fichas criadas
@app.route("/fichas")
def fichas():
    return render_template("fichas.html")

# Criar NPC
@app.route("/npc", methods=["GET", "POST"])
def npc():
    return render_template("npc.html")

# Criar Campanha
@app.route("/campanha", methods=["GET", "POST"])
def campanha():
    return render_template("campanha.html")

# Editor Homebrew
@app.route("/homebrew_editor", methods=["GET", "POST"])
def homebrew_editor():
    return render_template("homebrew_editor.html")

if __name__ == "__main__":
    app.run(debug=True)
