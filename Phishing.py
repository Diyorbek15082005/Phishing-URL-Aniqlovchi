import re
import tkinter as tk
from tkinter import messagebox
import socket
import requests

# Ma'lum phishing domenlari
phishing_domains = [
    "example-phishing.com",
    "paypal-secure.tk",
    "free-bonus.win",
    "login-secure-account-check.com",
]

# URL phishing xavfini tekshirish funksiyasi
def check_phishing_url(url):
    result = []
    # 1. HTTPS ulanishini tekshirish
    if not url.startswith("https://"):
        result.append("⚠️ HTTPS mavjud emas.")
    
    # 2. Soxta domen belgilarini tekshirish
    suspicious_patterns = [
        r"https?:\/\/.*?@.*",
        r"https?:\/\/.*?([0-9]{1,3}\.){3}[0-9]{1,3}.*",
        r"https?:\/\/.*?-.*?-.*",
        r"https?:\/\/.*?\.(tk|ml|ga|cf|gq)",
        r"https?:\/\/.*?(free|bonus|win|gift).*",
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, url):
            result.append("❌ URL shubhali belgilarga mos keladi.")

    # 3. Domenni phishing ro‘yxat bilan solishtirish
    try:
        domain = url.split("/")[2]
        if domain in phishing_domains:
            result.append("❌ Domen phishing ro‘yxatida bor.")
    except IndexError:
        result.append("❌ URL noto‘g‘ri formatda.")
    
    # 4. DNS domenni tekshirish
    try:
        socket.gethostbyname(domain)
    except Exception:
        result.append("❌ Domenni DNS orqali topib bo‘lmadi.")
    
    return result if result else ["✅ URL xavfsiz ko‘rinadi."]

# URL-ni tahlil qilish va natijani ko‘rsatish
def analyze_url():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Ogohlantirish", "Iltimos, URL ni kiriting!")
        return

    result = check_phishing_url(url)
    result_text = "\n".join(result)
    result_label.config(text=result_text, fg="red" if "❌" in result_text else "green")

# Dasturning grafik interfeysi
app = tk.Tk()
app.title("Phishing URL Aniqlovchi")
app.geometry("500x400")

# Sarlavha
title_label = tk.Label(app, text="Phishing URL Aniqlovchi", font=("Arial", 16))
title_label.pack(pady=10)

# URL kiritish uchun maydon
url_label = tk.Label(app, text="URL-ni kiriting:")
url_label.pack(pady=5)
url_entry = tk.Entry(app, width=60)
url_entry.pack(pady=5)

# Tekshirish tugmasi
check_button = tk.Button(app, text="Tekshirish", command=analyze_url, bg="blue", fg="white")
check_button.pack(pady=10)

# Natijalarni ko‘rsatish uchun label
result_label = tk.Label(app, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=20)

# Dasturni ishga tushirish
app.mainloop() 