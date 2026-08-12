import os
import json
import datetime
import urllib.request
from groq import Groq

# Init Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_article():
    prompt = """
    Write a viral, high-CTR, trending tech/business/AI news article in Hindi (hinglish friendly).
    Provide output STRICTLY in JSON format with two keys:
    1. "title": A MrBeast style catchy title (Under 60 chars).
    2. "content": Complete article in well-formatted HTML with <h2>, <p>, and <ul> tags.
    Do not add markdown codeblocks inside JSON value. Return raw JSON.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
        response_format={"type": "json_object"}
    )
    
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["content"]

def main():
    title, content = generate_article()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"article_{timestamp}.html"
    filepath = os.path.join("public", "articles", filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Random High-Quality Thumbnail
    image_url = f"https://picsum.photos/800/400?random={timestamp}"
    
    # Apple/Stark Pro HTML Template
    full_html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #0b0f19; color: #e2e8f0; font-family: 'Poppins', sans-serif; padding: 20px; line-height: 1.8; max-width: 800px; margin: auto; }}
        h1 {{ font-size: 2rem; color: #38bdf8; margin-bottom: 20px; }}
        img {{ width: 100%; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}
        .ad-slot {{ background: #1e293b; border: 1px dashed #475569; padding: 15px; text-align: center; border-radius: 8px; margin: 20px 0; color: #94a3b8; font-size: 0.8rem; }}
        a.back-btn {{ display: inline-block; margin-bottom: 20px; color: #38bdf8; text-decoration: none; font-weight: 600; }}
    </style>
</head>
<body>
    <a href="../../index.html" class="back-btn">← Back to Home</a>
    <h1>{title}</h1>
    <img src="{image_url}" alt="Article Banner">
    
    <div class="ad-slot">-- Google AdSense Monitized Slot --</div>
    
    <div class="article-body">
        {content}
    </div>
    
    <div class="ad-slot">-- Sponsored Affiliate Deals Slot --</div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Successfully generated: {filepath}")

if __name__ == "__main__":
    main()
  
