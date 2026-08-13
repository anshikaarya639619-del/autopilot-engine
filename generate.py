import os
from datetime import datetime

# मान लेते हैं कि तेरे सारे आर्टिकल 'public' फोल्डर में या रूट में सेव होते हैं
# यहाँ हम सभी जनरेटेड HTML फाइल्स को स्कैन करके index.html ऑटो-अपडेट करने का कोड सेट करते हैं:

def update_index_page():
    articles = []
    
    # फोल्डर से सभी एचटीएमएल फाइल्स ढूंढो (index, about, contact, privacy को छोड़कर)
    skip_files = ['index.html', 'about.html', 'contact.html', 'privacy.html']
    for file in os.listdir('.'):
        if file.endswith('.html') and file not in skip_files:
            # फाइल की मॉडिफिकेशन डेट या नाम से डेटा ले लो
            title = file.replace('.html', '').replace('-', ' ').title()
            articles.append({'title': title, 'url': file, 'date': 'Aug 13, 2026'})

    # अब नया index.html खुद जनरेट करो जिसमें सारे आर्टिकल्स की लिस्ट दिखे
    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autopilot Engine Pro</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>AUTOPILOT ENGINE PRO</h1>
        <p>AI द्वारा 100% ऑटोमैटिक जनरेट किए गए वायरल आर्टिकल्स</p>
    </header>
    <main class="container">
"""
    
    for art in articles:
        html_content += f"""
        <div class="article-card">
            <h3>{art['title']}</h3>
            <p>🔥 {art['date']}</p>
            <a href="{art['url']}" class="btn">⭐ Read Story →</a>
        </div>
        """

    html_content += """
    </main>
</body>
</html>
"""

    # index.html को ओवरराइट कर दो ताकि हमेशा ताज़ा लिस्ट दिखे
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# जब भी generate.py चले, यह फंक्शन कॉल हो जाना चाहिए
if __name__ == '__main__':
    update_index_page()
    print("🚀 Index.html successfully updated with all latest articles!")
              
