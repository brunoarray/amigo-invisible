# amigo_invisible_web.py
# Web privada de Amigo Invisible – segura, sin auto-asignaciones

from flask import Flask, abort
import random
import secrets
import datetime

print("🔥 VERSION CON /admin-links CARGADA 🔥")

app = Flask(__name__)

# ================= CONFIGURACIÓN =================
PERSONAS = [
    "BRUNO",
    "LUANA",
    "SABRINA",
    "KATY",
    "VALERIA",
    "JESSICA",
]

# Fecha límite (opcional)
FECHA_LIMITE = datetime.date(2025, 12, 24)

# ================================================

def sorteo_seguro(personas):
    if len(personas) < 2:
        raise ValueError("Se necesitan al menos 2 personas")
    while True:
        mezclados = personas[:]
        random.shuffle(mezclados)
        if all(p != m for p, m in zip(personas, mezclados)):
            return dict(zip(personas, mezclados))

resultado = sorteo_seguro(PERSONAS)

# Token -> amigo invisible (persistente)
tokens = {}

for persona, amigo in resultado.items():
    token = secrets.token_urlsafe(8)
    tokens[token] = amigo

@app.route("/")
def inicio():
    return "<h2>Amigo Invisible 🎁</h2><p>Usá el link que te enviaron.</p>"

@app.route("/<token>")
def ver_resultado(token):
    hoy = datetime.date.today()
    if FECHA_LIMITE and hoy > FECHA_LIMITE:
        return "<h2>⏰ El sorteo ya expiró</h2>"

    if token not in tokens:
        abort(404)

    amigo = tokens[token]  # ✅ NO se borra

    return f"""
    <html>
    <body style='font-family: Arial; text-align:center; margin-top:50px;'>
        <h1>🎁 Tu amigo invisible es:</h1>
        <h2 style='color:green'>{amigo}</h2>
        <p>Guardá este resultado 😉</p>
    </body>
    </html>
    """

@app.route("/admin-links")
def admin_links():
    html = "<h2>Links del Amigo Invisible</h2><ul>"
    for token in tokens.keys():
        html += f"<li>https://amigo-invisible-k2e0.onrender.com/{token}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
