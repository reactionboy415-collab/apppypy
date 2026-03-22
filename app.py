from flask import Flask, render_template_string, request, jsonify
import requests
import json
import random

app = Flask(__name__)

# --- ADVANCED SPOOFING CONFIG ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CineSage AI | Vercel Private Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root { --n: #00f2ff; --p: #7000ff; --bg: #050505; }
        body { margin: 0; background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; display: flex; justify-content: center; min-height: 100vh; }
        .container { width: 100%; max-width: 600px; padding: 50px 20px; text-align: center; }
        h1 { font-family: 'Syncopate', sans-serif; background: linear-gradient(90deg, var(--n), var(--p)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 5px; margin: 0; filter: drop-shadow(0 0 15px rgba(0,242,255,0.3)); }
        .box { background: rgba(255,255,255,0.05); padding: 30px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.1); margin-top: 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        textarea { width: 100%; height: 120px; background: rgba(0,0,0,0.5); border: 1px solid #333; border-radius: 12px; color: var(--n); padding: 15px; outline: none; font-size: 1rem; resize: none; box-sizing: border-box; }
        .btn { width: 100%; padding: 18px; margin-top: 15px; background: linear-gradient(45deg, var(--p), #ff00c8); border: none; border-radius: 12px; color: #fff; font-family: 'Syncopate', sans-serif; cursor: pointer; font-size: 0.8rem; letter-spacing: 2px; transition: 0.3s; }
        .btn:hover { transform: scale(1.02); filter: brightness(1.2); }
        #res { margin-top: 30px; text-align: left; }
        .m-card { background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; border-left: 4px solid var(--n); margin-bottom: 20px; animation: slideIn 0.5s ease; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; } }
    </style>
</head>
<body>
<div class="container">
    <h1>CINESAGE</h1>
    <div class="box">
        <textarea id="desc" placeholder="Describe the movie scene..."></textarea>
        <button class="btn" onclick="search()">EXECUTE SCAN</button>
    </div>
    <div id="loader" style="display:none; color:var(--n); margin-top:20px;">[ SYSTEM BYPASSING CLOUDFLARE... ]</div>
    <div id="res"></div>
</div>

<script>
async function search() {
    const desc = document.getElementById('desc').value;
    const resDiv = document.getElementById('res');
    const loader = document.getElementById('loader');
    if(!desc) return;

    resDiv.innerHTML = "";
    loader.style.display = "block";

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ description: desc })
        });
        const data = await response.json();
        loader.style.display = "none";

        if(data.error) { resDiv.innerHTML = "<p style='color:red;'>Error: " + data.error + "</p>"; return; }

        data.candidates.forEach(m => {
            resDiv.innerHTML += `
                <div class="m-card">
                    <h3 style="color:var(--n);margin:0;">${m.title} (${m.year})</h3>
                    <p style="color:#ccc; font-size:14px;">${m.plot_summary}</p>
                </div>`;
        });
    } catch(e) { loader.style.display = "none"; alert("System Overload!"); }
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    desc = data.get('description', '')
    
    # 🔥 ADVANCED FIRE BYPASS LOGIC 🔥
    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.aimoviefinder.com",
        "Referer": "https://www.aimoviefinder.com/",
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": fake_ip,
        "X-Real-IP": fake_ip
    }

    payload = {
        "provider": "openrouter",
        "model": "arcee-ai/trinity-large-preview:free",
        "messages": [{"role": "user", "content": f"Identify movie: {desc}. Return ONLY JSON with candidates list."}]
    }

    try:
        session = requests.Session()
        # Get cookies first
        session.get("https://www.aimoviefinder.com/", headers={"User-Agent": headers["User-Agent"]}, timeout=10)
        
        # Actual Attack
        r = session.post("https://www.aimoviefinder.com/api/demo/gen-text", json=payload, headers=headers, timeout=45)
        
        if r.status_code == 200:
            ai_data = r.json()
            # AI ke text field ko parse karke bhej rahe hain
            movie_json = json.loads(ai_data['data']['text'])
            return jsonify(movie_json)
        else:
            return jsonify({"error": f"Cloudflare Block ({r.status_code})"}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
