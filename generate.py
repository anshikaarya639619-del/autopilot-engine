def get_mrbeast_thumbnail(title):
    title_lower = title.lower()
    
    # टाइटल के हिसाब से 100% सटीक कीवर्ड्स
    if any(word in title_lower for word in ['car', 'इलेक्ट्रिक', 'vehicle', 'ड्राइव', 'KM', 'लाख कार']):
        keyword = "electric-car, supercar"
    elif any(word in title_lower for word in ['startup', 'डॉलर्स', 'पैसा', 'money', 'business', 'बिल्ियन']):
        keyword = "startup, office, wealth"
    elif any(word in title_lower for word in ['ai', 'tech', 'технологии', 'डेटा']):
        keyword = "artificial-intelligence, technology"
    else:
        keyword = "futuristic, innovation"
        
    # Unsplash Direct Keyword Image URL
    return f"https://source.unsplash.com/800x450/?{keyword}"
  
