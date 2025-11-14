from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import uuid

app = Flask(__name__)
app.secret_key = "Suamãeaquelagostosa"

# Criar pastas se não existirem
os.makedirs("data/fichas", exist_ok=True)

from markupsafe import Markup

@app.template_filter('nl2br')
def nl2br(text):
    return Markup(text.replace("\n", "<br>"))

# =============================== ARQUETIPOS ===============================

arquetipos = {
    # (todo o seu dicionário gigante aqui, mantive intacto)
}
    
# =============================== HOME ===============================

@app.route("/")
def index():
    return render_template("index.html")

# =============================== ETAPA 1 – ATRIBUTOS ===============================

@app.route("/criar_ficha/atributos", methods=["GET", "POST"])
def criar_ficha_atributos():
    if request.method == "POST":
        session["ficha"] = {
            "poder": request.form["poder"],
            "habilidade": request.form["habilidade"],
            "resistencia": request.form["resistencia"]
        }
        return redirect(url_for("criar_ficha_arquetipos"))

    return render_template("criar_ficha_atributos.html")

# =============================== ETAPA 2 – ARQUETIPOS ===============================

@app.route("/criar_ficha/arquetipos", methods=["GET", "POST"])
def criar_ficha_arquetipos():
    if "ficha" not in session:
        return redirect(url_for("criar_ficha_atributos"))

    if request.method == "POST":
        session["ficha"]["arquetipo"] = request.form["arquetipo"]
        return redirect(url_for("criar_ficha_final"))

    return render_template("criar_ficha_arquetipos.html", arquetipos=arquetipos)

# =============================== ETAPA 3 – TOQUES FINAIS ===============================

@app.route("/criar_ficha/final", methods=["GET", "POST"])
def criar_ficha_final():
    if "ficha" not in session:
        return redirect(url_for("criar_ficha_atributos"))

    if request.method == "POST":
        ficha_id = str(uuid.uuid4())

        ficha = session["ficha"]
        ficha["id"] = ficha_id
        ficha["nome"] = request.form["nome"]
        ficha["idade"] = request.form["idade"]
        ficha["pericias"] = request.form["pericias"]
        ficha["vantagens"] = request.form["vantagens"]
        ficha["historico"] = request.form["historico"]

        with open(f"data/fichas/{ficha_id}.json", "w", encoding="utf-8") as f:
            json.dump(ficha, f, indent=4, ensure_ascii=False)

        session.pop("ficha", None)
        return redirect(url_for("fichas"))

    return render_template("criar_ficha_final.html", ficha=session["ficha"])

# =============================== LISTAR FICHAS ===============================

@app.route("/fichas")
def fichas():
    lista = []
    for arquivo in os.listdir("data/fichas"):
        if arquivo.endswith(".json"):
            with open(f"data/fichas/{arquivo}", "r", encoding="utf-8") as f:
                lista.append(json.load(f))
    return render_template("fichas.html", fichas=lista)

# =============================== VER FICHA ===============================

@app.route("/ficha/<id>")
def ficha(id):
    caminho = f"data/fichas/{id}.json"
    if not os.path.exists(caminho):
        return "Ficha não encontrada", 404

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return render_template("ver_ficha.html", ficha=dados)

# =============================== OUTRAS PÁGINAS ===============================

@app.route("/npc")
def npc():
    return render_template("npc.html")

@app.route("/campanha")
def campanha():
    return render_template("campanha.html")

@app.route("/homebrew_editor")
def homebrew_editor():
    return render_template("homebrew_editor.html")

# =============================== RUN ===============================

if __name__ == "__main__":
    app.run(debug=True)

# ----------------------------- RUN -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
