import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

NICHES = [
    "AI Tools for Financial Planning 2026",
    "Best Tax Saving Software USA",
    "Automated Investment Dashboard Tools"
]

def generate_article(topic):
    prompt = f"Write a comprehensive, SEO-optimized guide in English targeted at US users about: '{topic}'. Format in clean HTML with <h1>, <h2>, <p>, and <ul> tags."
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content

def save_output(content, topic):
    os.makedirs("public/articles", exist_ok=True)
    filename = topic.lower().replace(" ", "-") + ".html"
    filepath = os.path.join("public/articles", filename)
    
    html_template = f"<!DOCTYPE html><html><head><title>{topic}</title></head><body>{content}</body></html>"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    for niche in NICHES:
        article_html = generate_article(niche)
        save_output(article_html, niche)
  
