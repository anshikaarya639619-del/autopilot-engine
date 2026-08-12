import os
import json
import datetime
import urllib.request

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_article():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing in GitHub Secrets!")

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # MrBeast Style Viral Prompt
    prompt = """
    You are a viral content creator like MrBeast combined with Tech Genius Tony Stark.
    Write an insanely engaging, high-CTR, trending tech, AI, automobile, or future business article in Hindi (Hinglish tone).
    
    Requirements for Content:
    - Start with a crazy hook in the first sentence.
    - Use bullet points, bold key insights, and strong subheadings (<h2>).
    - Add a "🔥 Key Takeaway / Quick Summary" box near the top.
    
    Provide output STRICTLY in JSON format with two keys:
    1. "title": A MrBeast style extremely clickable title (Under 60 chars, e.g., "Don't Buy A Car Until You See This AI Tech!").
    2. "content": Complete article in rich HTML (<h2>, <p>, <ul>, <li>, <strong>, <blockquote>).
    Return raw JSON only.
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        content_str = res_data["choices"][0]["message"]["content"]
        data = json.loads(content_str)
        return data.get("title", "🔥 Mind-Blowing Tech Update!"), data.get("content", "<p>Content generated successfully.</p>")

def update_index_and_sitemap():
    articles_db_file = os.path.join("public", "articles.json")
    articles = []
    if os.path.exists(articles_db_file):
        try:
            with open(articles_db_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except:
            articles = []

    cards_html = ""
    for art in articles[:12]:
        cards_html += f"""
        <div class="card">
            <img src="{art['image']}" alt="Thumbnail">
            <div class="card-body">
                <span class="date">🔥 {art['date']}</span>
                <h3>{art['title']}</h3>
                <a href="./public/articles/{art['file']}" class="read-btn">⚡ Read Story →</a>
            </div>
        </div>
        """

    index_html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AUTOPILOT ENGINE | Stark Viral Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }}
        body {{ background-color: #0b0f19; color: #f8fafc; min-height: 100vh; padding: 30px 15px; }}
        .container {{ max-width: 1000px; margin: 0 auto; text-align: center; }}
        .badge {{ background: linear-gradient(135deg, #FF0055, #7A00FF); padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; display: inline-block; box-shadow: 0 0 15px rgba(255,0,85,0.5); }}
        h1 {{ font-size: 2.8rem; font-weight: 800; margin: 15px 0; background: linear-gradient(to right, #00f2fe, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        p.subtitle {{ font-size: 1.1rem; color: #94a3b8; margin-bottom: 30px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; text-align: left; }}
        .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 16px; overflow: hidden; transition: all 0.3s ease; display: flex; flex-direction: column; }}
        .card:hover {{ transform: translateY(-7px) scale(1.02); border-color: #38bdf8; box-shadow: 0 15px 30px rgba(56, 189, 248, 0.25); }}
        .card img {{ width: 100%; height: 170px; object-fit: cover; }}
        .card-body {{ padding: 18px; display: flex; flex-direction: column; flex-grow: 1; }}
        .card .date {{ font-size: 0.75rem; color: #f43f5e; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }}
        .card h3 {{ font-size: 1.15rem; color: #fff; margin-bottom: 15px; line-height: 1.4; flex-grow: 1; font-weight: 600; }}
        .read-btn {{ display: block; text-align: center; background: linear-gradient(135deg, #FF0055, #7A00FF); color: #fff; font-weight: 700; padding: 12px; border-radius: 10px; text-decoration: none; font-size: 0.95rem; box-shadow: 0 5px 15px rgba(255,0,85,0.3); }}
        footer {{ margin-top: 50px; padding: 20px; border-top: 1px solid #334155; font-size: 0.85rem; color: #94a3b8; }}
        footer a {{ color: #38bdf8; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">🔥 Stark Enterprise Engine</span>
        <h1>AUTOPILOT ENGINE PRO</h1>
        <p class="subtitle">AI द्वारा ऑटोमैटिक जनरेट किए गए वायरल ट्रेंडिंग आर्टिकल्स</p>
        
        <div class="grid">
            {cards_html if cards_html else '<p style="text-align:center; grid-column: 1/-1;">ताज़ा वायरल आर्टिकल लोड हो रहे हैं...</p>'}
        </div>

        <footer>
            <p>© 2026 Autopilot Engine. All Rights Reserved.</p>
            <p><a href="privacy.html">Privacy Policy</a> | <a href="about.html">About Us</a></p>
        </footer>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

def main():
    title, content = generate_article()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.datetime.now().strftime("%b %d, %Y")
    filename = f"article_{timestamp}.html"
    filepath = os.path.join("public", "articles", filename)
    image_url = f"https://picsum.photos/800/400?random={timestamp}"
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    full_html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #0b0f19; color: #e2e8f0; font-family: 'Poppins', sans-serif; padding: 20px; line-height: 1.8; max-width: 800px; margin: auto; }}
        h1 {{ font-size: 2.2rem; color: #38bdf8; margin-bottom: 20px; font-weight: 800; line-height: 1.3; }}
        img {{ width: 100%; border-radius: 14px; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); }}
        blockquote {{ background: #1e293b; border-left: 4px solid #FF0055; padding: 15px 20px; border-radius: 8px; margin: 20px 0; font-weight: 600; color: #fb7185; }}
        .ad-slot {{ background: #1e293b; border: 1px dashed #475569; padding: 15px; text-align: center; border-radius: 10px; margin: 25px 0; color: #94a3b8; font-size: 0.85rem; font-weight: 600; }}
        a.back-btn {{ display: inline-block; margin-bottom: 20px; color: #38bdf8; text-decoration: none; font-weight: 700; background: #1e293b; padding: 8px 16px; border-radius: 8px; border: 1px solid #334155; }}
        h2 {{ color: #38bdf8; margin-top: 25px; margin-bottom: 10px; font-size: 1.4rem; }}
        ul {{ margin-left: 20px; margin-bottom: 20px; }}
        li {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <a href="../../index.html" class="back-btn">← Back to Home</a>
    <h1>{title}</h1>
    <img src="{image_url}" alt="Article Banner">
    
    <div class="ad-slot">💰 [Google AdSense Banner Slot]</div>
    
    <div class="article-body">
        {content}
    </div>
    
    <div class="ad-slot">🛒 [Amazon / Affiliate Monetization Slot]</div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_html)

    articles_db_file = os.path.join("public", "articles.json")
    articles = []
    if os.path.exists(articles_db_file):
        try:
            with open(articles_db_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except:
            articles = []

    articles.insert(0, {
        "title": title,
        "file": filename,
        "image": image_url,
        "date": date_str
    })

    with open(articles_db_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    update_index_and_sitemap()
    print(f"Successfully generated MrBeast-Style article & updated homepage: {filepath}")

if __name__ == "__main__":
    main()
  
