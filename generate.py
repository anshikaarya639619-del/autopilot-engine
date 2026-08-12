import urllib.parse

def get_smart_image(title):
    # टाइटल के हिसाब से स्मार्ट कीवर्ड सेट करना
    keyword = "technology" # डिफॉल्ट
    
    if any(word in title.lower() for word in ['car', 'खाए', 'इलेक्ट्रिक', 'vehicle', 'ड्राइव']):
        keyword = "sports-car,electric-car"
    elif any(word in title.lower() for word in ['startup', 'डॉलर्स', 'पैसा', 'money', 'business']):
        keyword = "startup,office,success"
    elif any(word in title.lower() for word in ['AI', 'टेक', 'tech', 'future']):
        keyword = "artificial-intelligence,futuristic"
        
    # Unsplash Source या Picsum का बेहतर इस्तेमाल (या Unsplash random keyword API)
    return f"https://source.unsplash.com/800x450/?{keyword}"
  
