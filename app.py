from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import uuid
import logging
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = "Suamãeaquelagostosa"

# logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar pastas
os.makedirs("data/fichas", exist_ok=True)

# Filtro para quebra de linha (usado nos templates)
@app.template_filter('nl2br')
def nl2br(text):
    if text is None:
        return ""
    return Markup(str(text).replace("\n", "<br>"))

# ---------------- ARQUETIPOS (mantido como você já tinha) ----------------
arquetipos = {
    "Humano": {
        "custo": 0,
        "descricao": "Versáteis, impulsivos e adaptáveis. Podem ser qualquer coisa.",
        "vantagens": [
            "Mais Além (1 vez por cena, gastar 2PM para ter Ganho em um teste)"
        ],
        "desvantagens": []
    },

    "Aberrante": {
        "custo": 1,
        "descricao": "Seres distorcidos, mutados ou alienados da realidade.",
        "vantagens": [
            "Deformidade (+1 no atributo em uma perícia escolhida)",
            "Teratismo (Recebe 1 Técnica Comum)"
        ],
        "desvantagens": [
            "Monstruoso"
        ]
    },

    "Abissal": {
        "custo": 1,
        "descricao": "Demônios e infernais vindos de planos malignos.",
        "vantagens": [
            "Ágil",
            "Desfavor (3PM, força um alvo a testar Resistência; se falhar sofre Perda)",
        ],
        "desvantagens": ["Infame"]
    },

    "Alien": {
        "custo": 1,
        "descricao": "Seres estrangeiros, de outras épocas, planetas ou dimensões.",
        "vantagens": [
            "Talento (Ágil, Carismático, Forte, Gênio, Resoluto ou Vigoroso)",
            "Xenobiologia (Vantagens custam metade em PM)"
        ],
        "desvantagens": ["Inculto"]
    },

    "Anão": {
        "custo": 1,
        "descricao": "Baixos, robustos, teimosos e resistentes.",
        "vantagens": [
            "Abascanto (Ganho em testes de Resistência contra efeitos)",
            "A Ferro e Fogo (+1 quando testar Máquinas; Infravisão)"
        ],
        "desvantagens": ["Lento"]
    },

    "Anfíbio": {
        "custo": 1,
        "descricao": "Seres aquáticos que vivem bem dentro e fora da água.",
        "vantagens": [
            "Imune (Anfíbio – respira e age normalmente na água)",
            "Vigoroso"
        ],
        "desvantagens": ["Ambiente"]
    },

    "Celestial": {
        "custo": 1,
        "descricao": "Seres angelicais de planos superiores, nobres e radiantes.",
        "vantagens": [
            "Carismático",
            "Arrebatar (3PM para conceder Ganho a um aliado até o próximo turno)"
        ],
        "desvantagens": ["Código"]
    },

    "Centauro": {
        "custo": 2,
        "descricao": "Criaturas táuricas com grande força e resistência.",
        "vantagens": [
            "Corpo Táurico (1PM para crítico com 5-6 em testes de P físico ou corrida)",
            "Vigoroso"
        ],
        "desvantagens": ["Diferente"]
    },

    "Ciborgue": {
        "custo": 2,
        "descricao": "Metade máquina, metade orgânico.",
        "vantagens": [
            "Construto Vivo (pode ser curado ou consertado)",
            "Imune (Abiótico, Doenças, Resiliente)"
        ],
        "desvantagens": ["Diretriz"]
    },

    "Construto": {
        "custo": 1,
        "descricao": "Seres artificiais, feitos de metal, cristal ou magia.",
        "vantagens": [
            "Imune (Abiótico, Doenças, Resiliente, Sem Mente)",
            "Bateria (precisa recarregar em vez de dormir)"
        ],
        "desvantagens": ["Sem Vida"]
    },

    "Dahllan": {
        "custo": 1,
        "descricao": "Híbridas de plantas, fadas e humanas.",
        "vantagens": [
            "Benção da Natureza (2PM: Ganho em Defesa até próximo turno)",
            "Empatia Selvagem (+1 em Animais)"
        ],
        "desvantagens": ["Código Dahllan"]
    },

    "Elfo": {
        "custo": 1,
        "descricao": "Belos, mágicos, elegantes e longevos.",
        "vantagens": [
            "Impecável (Ágil, Carismático ou Gênio)",
            "Natureza Mística (+1 em Mística)"
        ],
        "desvantagens": ["Frágil"]
    },

    "Fada": {
        "custo": 1,
        "descricao": "Seres mágicos ligados à natureza, pequenos ou delicados.",
        "vantagens": [
            "Magia das Fadas (Magia ou Ilusão com -1 PM, mínimo 1)"
        ],
        "desvantagens": ["Infame", "Delicada"]
    },

    "Fantasma": {
        "custo": 2,
        "descricao": "Espíritos imateriais presos ao mundo.",
        "vantagens": [
            "Espírito (imaterial; pode gastar PM para ficar sólido)",
            "Paralisia"
        ],
        "desvantagens": ["Devoto"]
    },

    "Goblin": {
        "custo": 1,
        "descricao": "Pequenos, hiperativos e engenhosos.",
        "vantagens": [
            "Espertalhão (+1 em Manha)",
            "Subterrâneo (Infravisão + Ganho contra doenças/venenos)"
        ],
        "desvantagens": ["Diferente"]
    },

    "Hynne": {
        "custo": 1,
        "descricao": "Pequeninos alegres, sorrateiros e sortudos.",
        "vantagens": [
            "Atirador (2PM para Ganho atacando Longe)",
            "Encantador (+1 em Influência)"
        ],
        "desvantagens": ["Diferente"]
    },

    "Kallyanach": {
        "custo": 2,
        "descricao": "Meios-dragões, poderosos e imponentes.",
        "vantagens": [
            "Baforada (Ataque Especial permanente com -1 PM)",
            "Poder Dracônico (Forte ou Carismático)"
        ],
        "desvantagens": ["Código dos Dragões"]
    },

    "Kemono": {
        "custo": 1,
        "descricao": "Seres antropomórficos com sentidos aguçados.",
        "vantagens": [
            "Percepção Apurada (+1 em Percepção)",
            "Talento (Ágil, Carismático, Forte, Gênio, Resoluto ou Vigoroso)"
        ],
        "desvantagens": ["Cacoete"]
    },

    "Medusa": {
        "custo": 1,
        "descricao": "Seres com cabelos de serpentes e olhar perigoso.",
        "vantagens": [
            "Carismático",
            "Olhar Atordoante (3PM: alvo não age por 1 rodada)"
        ],
        "desvantagens": ["Fracote"]
    },

    "Minotauro": {
        "custo": 1,
        "descricao": "Guerreiros fortes, orgulhosos e determinados.",
        "vantagens": [
            "Atlético (+1 em Esportes)",
            "Sentido Labiríntico (nunca se perde)"
        ],
        "desvantagens": ["Transtorno (Fobia de Altura)"]
    },

    "Ogro": {
        "custo": 1,
        "descricao": "Gigantes brutais e assustadores.",
        "vantagens": [
            "Destruidor (2PM para somar Poder adicional no crítico)",
            "Intimidador (Ganho em Influência para intimidar)"
        ],
        "desvantagens": ["Diferente"]
    },

    "Osteon": {
        "custo": 2,
        "descricao": "Esqueletos vivos com consciência.",
        "vantagens": [
            "Imune (Abiótico, Doenças, Resiliente)",
            "Memória Póstuma (+1 em uma perícia escolhida)"
        ],
        "desvantagens": ["Sem Vida"]
    },

    "Qareen": {
        "custo": 2,
        "descricao": "Meios-gênios mágicos e benevolentes.",
        "vantagens": [
            "Desejos (Magia com -2 PM quando cumpre pedido)",
            "Carismático"
        ],
        "desvantagens": ["Código da Gratidão"]
    },

    "Sauroide": {
        "custo": 2,
        "descricao": "Humanóides reptilianos rústicos e resistentes.",
        "vantagens": [
            "Cascudo (Resoluto + Vigoroso)",
            "Camuflagem (Ganho em Furtividade)"
        ],
        "desvantagens": ["Fraqueza (Frio)"]
    },

    "Vampiro": {
        "custo": 1,
        "descricao": "Sedutores, imortais e perigosos.",
        "vantagens": [
            "Talento (Ágil, Carismático, Forte, Gênio, Resoluto ou Vigoroso)",
            "Imortal"
        ],
        "desvantagens": ["Fraqueza (Luz do dia)"]
    },
}
# =============================== ROTAS ===============================

@app.route("/")
def index():
    return render_template("index.html")

# ETAPA 1 – ATRIBUTOS
@app.route("/criar_ficha/atributos", methods=["GET", "POST"])
def criar_ficha_atributos():
    if request.method == "POST":
        # converter valores para int de forma segura
        def to_int_safe(val, default=0):
            try:
                return int(val)
            except Exception:
                return default

        poder = to_int_safe(request.form.get("poder", 0))
        habilidade = to_int_safe(request.form.get("habilidade", 0))
        resistencia = to_int_safe(request.form.get("resistencia", 0))

        session["ficha"] = {
            "poder": poder,
            "habilidade": habilidade,
            "resistencia": resistencia
        }
        return redirect(url_for("criar_ficha_arquetipos"))

    return render_template("criar_ficha_atributos.html")

# ETAPA 2 – ARQUETIPOS
@app.route("/criar_ficha/arquetipos", methods=["GET", "POST"])
def criar_ficha_arquetipos():
    if "ficha" not in session:
        return redirect(url_for("criar_ficha_atributos"))

    if request.method == "POST":
        session["ficha"]["arquetipo"] = request.form.get("arquetipo", "")
        return redirect(url_for("criar_ficha_final"))

    return render_template("criar_ficha_arquetipos.html", arquetipos=arquetipos)

# ETAPA 3 – TOQUES FINAIS
@app.route("/criar_ficha/final", methods=["GET", "POST"])
def criar_ficha_final():
    if "ficha" not in session:
        return redirect(url_for("criar_ficha_atributos"))

    ficha = session["ficha"]

    if request.method == "POST":
        ficha_id = str(uuid.uuid4())

        # Campos
        ficha["id"] = ficha_id
        ficha["nome"] = request.form.get("nome", "").strip()
        ficha["idade"] = request.form.get("idade", "").strip()
        ficha["pericias"] = request.form.get("pericias", "").strip()
        ficha["vantagens"] = request.form.get("vantagens", "").strip()
        ficha["desvantagens"] = request.form.get("desvantagens", "").strip()
        ficha["historico"] = request.form.get("historico", "").strip()

        # Garante tipos numéricos
        ficha["poder"] = int(ficha.get("poder", 0))
        ficha["habilidade"] = int(ficha.get("habilidade", 0))
        ficha["resistencia"] = int(ficha.get("resistencia", 0))

        # Derivados
        ficha["pa"] = ficha["poder"]
        ficha["mana"] = ficha["habilidade"] * 5
        ficha["vida"] = ficha["resistencia"] * 5

        # Salvamento
        os.makedirs("data/fichas", exist_ok=True)
        caminho = f"data/fichas/{ficha_id}.json"

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(ficha, f, indent=4, ensure_ascii=False)

        session.pop("ficha", None)
        return redirect(url_for("fichas"))

    # GET
    return render_template("criar_ficha_final.html", ficha=ficha)

    # GET
    return render_template("criar_ficha_final.html", ficha=session.get("ficha", {}))

# =============================== ROTA DE EDIÇÃO ===============================
@app.route("/editar_ficha/<id>", methods=["GET", "POST"])
def editar_ficha(id):
    caminho = f"data/fichas/{id}.json"
    if not os.path.exists(caminho):
        return "Ficha não encontrada", 404

    with open(caminho, "r", encoding="utf-8") as f:
        ficha = json.load(f)

    if request.method == "POST":
        # atualizar campos que podem ter sido editados
        ficha["nome"] = request.form.get("nome","")
        ficha["idade"] = request.form.get("idade","")
        ficha["pericias"] = request.form.get("pericias","")
        ficha["vantagens"] = request.form.get("vantagens","")
        ficha["desvantagens"] = request.form.get("desvantagens","")
        ficha["historico"] = request.form.get("historico","")

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(ficha, f, indent=4, ensure_ascii=False)

        return redirect(url_for("ficha", id=id))

    # reusar template de criação em modo edição
    return render_template("criar_ficha_final.html", ficha=ficha, edit_mode=True)

# LISTAR FICHAS
@app.route("/fichas")
def fichas():
    lista = []
    for arquivo in os.listdir("data/fichas"):
        if arquivo.endswith(".json"):
            try:
                with open(f"data/fichas/{arquivo}", "r", encoding="utf-8") as f:
                    lista.append(json.load(f))
            except Exception:
                logger.exception("Falha ao ler ficha %s", arquivo)
    return render_template("fichas.html", fichas=lista)

# VER FICHA
@app.route("/ficha/<id>")
def ficha(id):
    caminho = f"data/fichas/{id}.json"
    if not os.path.exists(caminho):
        return "Ficha não encontrada", 404

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return render_template("ver_ficha.html", ficha=dados)

# =============================== ERROS ===============================
@app.errorhandler(500)
def internal_error(e):
    # mostra 500 simples para evitar TemplateNotFound quando algo dá errado
    return render_template("500.html", error=str(e)), 500

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", error=str(e)), 404

    # garantir chaves derivadas (caso ficha antiga não tenha)
    try:
        dados["poder"] = int(dados.get("poder", 0))
    except Exception:
        dados["poder"] = 0
    try:
        dados["habilidade"] = int(dados.get("habilidade", 0))
    except Exception:
        dados["habilidade"] = 0
    try:
        dados["resistencia"] = int(dados.get("resistencia", 0))
    except Exception:
        dados["resistencia"] = 0

    dados["pa"] = dados.get("pa", dados["poder"])
    dados["mana"] = dados.get("mana", dados["habilidade"] * 5)
    dados["vida"] = dados.get("vida", dados["resistencia"] * 5)

    return render_template("ver_ficha.html", ficha=dados)

# OUTRAS PÁGINAS
@app.route("/npc")
def npc():
    return render_template("npc.html")

@app.route("/campanha")
def campanha():
    return render_template("campanha.html")

@app.route("/homebrew_editor")
def homebrew_editor():
    return render_template("homebrew_editor.html")

# Handler 500 simples (útil para logs)
@app.errorhandler(500)
def internal_error(e):
    logger.exception("Internal server error: %s", e)
    return render_template("500.html", error=str(e)), 500

# RUN
if __name__ == "__main__":
    app.run(debug=True)
