from flask import Flask, render_template, request, redirect, url_for
import os
import json
import uuid

app = Flask(__name__)
app.secret_key = "Suamãeaquelagostosa"

# Criar pastas se não existirem
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/fichas"):
    os.makedirs("data/fichas")
    
    from markupsafe import Markup

@app.template_filter('nl2br')
def nl2br(text):
    return Markup(text.replace("\n", "<br>"))

arquetipos = {
    "Humano": {
        "custo": 0,
        "descricao": "Adaptáveis, impulsivos e versáteis.",
        "vantagens": ["Mais Além (Ganho 1 vez por cena por 2PM)"],
        "desvantagens": []
    },
    "Aberrante": {
        "custo": 1,
        "descricao": "Criaturas mutantes, bizarras, fora da realidade.",
        "vantagens": [
            "Deformidade (+1 no atributo ligado a perícia escolhida)",
            "Teratismo (1 Técnica Comum)"
        ],
        "desvantagens": ["Monstruoso"]
    },
    "Abissal": {
        "custo": 1,
        "descricao": "Demônios e seres infernais.",
        "vantagens": [
            "Ágil",
            "Desfavor (3PM, alvo sofre Perda)",
        ],
        "desvantagens": ["Infame"]
    },

    # (continua com TODOS — posso incluir o bloco completo se quiser agora)
}


# ----------------------------- ROTAS BÁSICAS -----------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------- CRIAR FICHA -----------------------------

@app.route("/criar_ficha", methods=["GET", "POST"])
def criar_ficha():
    if request.method == "POST":
        ficha_id = str(uuid.uuid4())  # ID único

        ficha = {
            "id": ficha_id,
            "nome": request.form["nome"],
            "idade": request.form["idade"],
            "pericias": request.form["pericias"],
            "poder": request.form["poder"],
            "habilidade": request.form["habilidade"],
            "resistencia": request.form["resistencia"],
            "vantagens": request.form["vantagens"],
            "historico": request.form["historico"]
        }

        # salvar JSON
        caminho = f"data/fichas/{ficha_id}.json"
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(ficha, f, indent=4, ensure_ascii=False)

        return redirect(url_for("fichas"))

    return render_template("criar_ficha.html")


# ----------------------------- LISTAR FICHAS -----------------------------

@app.route("/fichas")
def fichas():
    fichas_list = []

    for arquivo in os.listdir("data/fichas"):
        if arquivo.endswith(".json"):
            with open(f"data/fichas/{arquivo}", "r", encoding="utf-8") as f:
                dado = json.load(f)
                fichas_list.append(dado)

    return render_template("fichas.html", fichas=fichas_list)

#------------------------------ ARQUETIPOS ----------------------------------

@app.route("/arquetipos")
def pagina_arquetipos():
    return render_template("arquetipos.html", arquetipos=arquetipos)

#------------------------------ SALVAR NO JSON ------------------------------

@app.route("/escolher_arquetipo", methods=["POST"])
def escolher_arquetipo():
    escolha = request.form["arquetipo"]

    session["ficha"] = session.get("ficha", {})
    session["ficha"]["arquetipo"] = escolha

    return redirect(url_for("toques_finais"))

#------------------------------ TOQUES FINAIS -------------------------------

@app.route("/toques_finais")
def toques_finais():
    return render_template("toques_finais.html", ficha=session.get("ficha", {}))

# ----------------------------- VISUALIZAR FICHA -----------------------------

@app.route("/ficha/<id>")
def ficha(id):
    caminho = f"data/fichas/{id}.json"

    if not os.path.exists(caminho):
        return "Ficha não encontrada!", 404

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return render_template("ver_ficha.html", ficha=dados)


# ----------------------------- OUTRAS PÁGINAS -----------------------------

@app.route("/npc")
def npc():
    return render_template("npc.html")

@app.route("/campanha")
def campanha():
    return render_template("campanha.html")

@app.route("/homebrew_editor")
def homebrew_editor():
    return render_template("homebrew_editor.html")


# ----------------------------- RUN -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
