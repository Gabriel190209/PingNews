from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
import sqlite3
import threading
import time

resumidor = pipeline("summarization", model="facebook/bart-large-cnn")

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

news_sites = {
    "G1": "https://g1.globo.com",
    "CNN Brasil": "https://www.cnnbrasil.com.br",
    "UOL": "https://noticias.uol.com.br",
    "Globo": "https://globo.com"
}

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS noticias (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fonte TEXT,
                        titulo TEXT,
                        resumo TEXT
                    )''')
    conn.commit()
    conn.close()

# Função para salvar uma notícia no banco de dados
def salvar_noticia(fonte, titulo, resumo):
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO noticias (fonte, titulo, resumo) VALUES (?, ?, ?)",
                       (fonte, titulo, resumo))
        conn.commit()
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    finally:
        conn.close()

# Função para carregar as notícias do banco de dados
def carregar_noticias():
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fonte, titulo, resumo FROM noticias ORDER BY id DESC")
    resultados = [{"fonte": f, "titulo": t, "resumo": r} for f, t, r in cursor.fetchall()]
    conn.close()
    return resultados

# Função para buscar links das notícias
def buscar_links(site_url, max_links=3):
    try:
        response = requests.get(site_url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links_validos = [
            link for link in links
            if link.startswith("http")
            and site_url.split("//")[1] in link
            and "utm_" not in link
            and "#" not in link
            and len(link.split("/")) > 4
        ]
        return list(dict.fromkeys(links_validos))[:max_links]
    except Exception as e:
        print(f"Erro ao buscar links: {e}")
        return []

# Função para extrair título e texto de uma notícia
def extrair_titulo_e_texto(link):
    try:
        response = requests.get(link, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        titulo = soup.title.string.strip() if soup.title and soup.title.string else "Sem título"
        paragrafos = soup.find_all('p')
        texto = " ".join(p.get_text() for p in paragrafos)
        return titulo, texto.strip()[:1024]
    except Exception as e:
        print(f"Erro ao extrair conteúdo de {link}: {e}")
        return "Sem título", None

# Função para resumir o texto com o modelo
def resumir_com_modelo(texto):
    try:
        print("🔍 Resumindo com modelo local...")
        resumo_raw = resumidor(texto, max_length=130, min_length=30, do_sample=False)
        resumo = resumo_raw[0]['summary_text']
        print("✅ Resumo:", resumo[:200])
        return resumo
    except Exception as e:
        print("❌ Erro ao resumir:", e)
        return "Resumo indisponível."

# Função para processar as notícias e enviar via SocketIO
def processar_noticias():
    while True:
        for nome_site, url in news_sites.items():
            links = buscar_links(url)
            for link in links:
                titulo, texto = extrair_titulo_e_texto(link)
                if texto and len(texto) > 200:
                    resumo = resumir_com_modelo(texto)
                    salvar_noticia(nome_site, titulo, resumo)
                    socketio.emit('nova_noticia', {"fonte": nome_site, "titulo": titulo, "resumo": resumo})
        print("⏳ Aguardando 5 minutos para nova verificação...")
        time.sleep(300)

@app.route("/noticias")
def get_noticias():
    noticias = carregar_noticias()

    vistas = set()
    unicas = []
    for noticia in noticias:
        chave = f"{noticia['titulo']}-{noticia['resumo']}"
        if chave in vistas:
            continue
        vistas.add(chave)
        unicas.append(noticia)

    return jsonify(unicas)

@app.route("/index")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado.")

@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado.")

if __name__ == "__main__":
    init_db()  # Inicia o banco de dados
    threading.Thread(target=processar_noticias, daemon=True).start()
    socketio.run(app, debug=True, port=5001)

