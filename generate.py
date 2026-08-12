import os
import json
import datetime
import urllib.request
import xml.etree.ElementTree as ET

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
BASE_URL = "https://anshikaarya639619-del.github.io/autopilot-engine"

def generate_article():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing in GitHub Secrets!")

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = """
    You are a viral content creator like MrBeast combined with Tech Genius Tony Stark.
    Write an insanely engaging, high-CTR, trending tech, AI, automobile, or future business article in Hindi (Hinglish friendly tone).
    
    Requirements for Content:
    - Start with a crazy hook in the first sentence.
    - Use bullet points, bold key insights, and strong subheadings (<h2>).
    - Add a "🔥 Key Takeaway / Quick Summary" box near the top using <blockquote>.
    
    Provide output STRICTLY in JSON format with two keys:
    1. "title": A MrBeast style extremely clickable title (Under 60 chars, e.g., "Don't Buy A Car Until You See This AI Tech!").
    2. "content": Complete article in rich HTML (<h2>, <p>, <ul>, <li>, <strong>, blockquote).
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

def update_sitemap(articles):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Home Page
    url_node = ET.SubElement(urlset, "url")
    ET.SubElement(url_node, "loc").text = f"{BASE_URL}/"
    ET.SubElement(url_node, "priority").text = "1.0"
    
    # Static Pages
    for p in ["privacy.html", "about.html"]:
        u = ET.SubElement(urlset, "url")
        ET.SubElement(u, "loc").text = f"{BASE_URL}/{p}"
        ET.SubElement(u, "priority").text = "0.5"

    # Articles
    for art in articles:
        u = ET.SubElement(urlset, "url")
        ET.SubElement(u, "loc").text = f"{BASE_URL}/public/articles/{art['file']}"
        ET.SubElement(u, "priority").text = "0.8"

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)

def update_index():
    articles_db_file = os.path.join("public", "articles.json")
    articles = []
    if os.path.exists(articles_db_file):
        try:
            with open(articles_db_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except:
            articles = []

    cards_html = ""
    for art in articles[:15]:
        cards_html += f"""
        <div class="card">
            <img src="{art['image']}" alt="Thumbnail" loading="lazy">
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
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600;800&family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', -apple-system, sans-serif; }}
        body {{ background-color: #030712; color: #f8fafc; min-height: 100vh; padding: 30px 15px; }}
        .container {{ max-width: 1050px; margin: 0 auto; text-align: center; }}
        .badge {{ background: linear-gradient(135deg, #FF0055, #7A00FF); padding: 8px 20px; border-radius: 30px; font-weight: 800; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; display: inline-block; box-shadow: 0 0 20px rgba(255,0,85,0.6); animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
        h1 {{ font-size: 3rem; font-weight: 800; margin: 20px 0 10px; background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; }}
        p.subtitle {{ font-size: 1.1rem; color: #94a3b8; margin-bottom: 35px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 20px; text-align: left; }}
        .card {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; overflow: hidden; transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); display: flex; flex-direction: column; }}
        .card:hover {{ transform: translateY(-8px) scale(1.02); border-color: #38bdf8; box-shadow: 0 20px 40px rgba(56, 189, 248, 0.2); }}
        .card img {{ width: 100%; height: 180px; object-fit: cover; }}
        .card-body {{ padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }}
        .card .date {{ font-size: 0.75rem; color: #f43f5e; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }}
        .card h3 {{ font-size: 1.2rem; color: #f8fafc; margin-bottom: 18px; line-height: 1.4; flex-grow: 1; font-weight: 600; }}
        .read-btn {{ display: block; text-align: center; background: linear-gradient(135deg, #22c55e, #16a34a); color: #fff; font-weight: 700; padding: 12px; border-radius: 12px; text-decoration: none; font-size: 0.95rem; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3); transition: all 0.2s ease; }}
        .read-btn:hover {{ background: linear-gradient(135deg, #16a34a, #15803d); box-shadow: 0 6px 20px rgba(34, 197, 94, 0.5); }}
        footer {{ margin-top: 60px; padding: 25px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem; color: #64748b; }}
        footer a {{ color: #38bdf8; text-decoration: none; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">🔥 Stark Enterprise Engine</span>
        <h1>AUTOPILOT ENGINE PRO</h1>
        <p class="subtitle">100% AI द्वारा ऑटोमैटिक जनरेट किए गए मिस्टर बीस्ट स्टाइल वायरल आर्टिकल्स</p>
        
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

    update_sitemap(articles)

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
        body {{ background-color: #030712; color: #e2e8f0; font-family: 'Poppins', -apple-system, sans-serif; padding: 20px; line-height: 1.8; max-width: 820px; margin: auto; }}
        h1 {{ font-size: 2.3rem; color: #38bdf8; margin-bottom: 20px; font-weight: 800; line-height: 1.3; }}
        img {{ width: 100%; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 12px 30px rgba(0,0,0,0.7); }}
        blockquote {{ background: rgba(30, 41, 59, 0.8); border-left: 4px solid #f43f5e; padding: 18px 24px; border-radius: 12px; margin: 25px 0; font-weight: 600; color: #fda4af; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }}
        .ad-slot {{ background: rgba(30, 41, 59, 0.5); border: 1px dashed #475569; padding: 18px; text-align: center; border-radius: 12px; margin: 30px 0; color: #94a3b8; font-size: 0.85rem; font-weight: 600; letter-spacing: 1px; }}
        a.back-btn {{ display: inline-block; margin-bottom: 25px; color: #38bdf8; text-decoration: none; font-weight: 700; background: #1e293b; padding: 10px 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); transition: 0.2s; }}
        a.back-btn:hover {{ background: #334155; }}
        h2 {{ color: #38bdf8; margin-top: 30px; margin-bottom: 12px; font-size: 1.5rem; font-weight: 700; }}
        ul {{ margin-left: 20px; margin-bottom: 20px; }}
        li {{ margin-bottom: 10px; }}
    </style>
</head>
<body>
    <a href="../../index.html" class="back-btn">← Back to Home</a>
    <h1>{title}</h1>
    <img src="{image_url}" alt="Article Banner">
    
    <div class="ad-slot">💰 [Google AdSense Monitized Slot]</div>
    
    <div class="article-body">
        {content}
    </div>
    
    <div class="ad-slot">🛒 [Sponsored Affiliate Monetization Slot]</div>
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

    update_index()
    print(f"Successfully generated article, sitemap & updated homepage: {filepath}")

if __name__ == "__main__":
    main()
  
