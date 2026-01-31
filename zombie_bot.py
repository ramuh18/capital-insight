import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BLOG_TITLE = "Capital Insight"
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# [🛡️ 비상용 원고 - 중복 방지를 위한 5종 리포트]
FALLBACK_REPORTS = [
    {"title": "Global Market Forecast: 2026 Trends", "content": "The global financial landscape is shifting. Interest rates remain a primary concern for institutional investors..."},
    {"title": "Institutional Crypto Adoption Analysis", "content": "Institutional entry into the digital asset space has reached a tipping point. Cold storage is now mandatory..."},
    {"title": "The Future of Reserve Currencies", "content": "Analyzing the structural decline of legacy fiat systems and the rise of decentralized alternatives..."},
    {"title": "Supply Chain Resilience and Inflation", "content": "Inflationary pressures are being reshaped by geopolitical shifts. Logistics costs are the new indicator..."},
    {"title": "Venture Capital Flows in the AI Era", "content": "Capital is concentrating in automated intelligence sectors. Understanding the new equity supercycle..."}
]

def generate_report(topic):
    # [1,500자 정량화 프롬프트] 너무 길지 않게, 하지만 전문적으로
    prompt = f"""
    Write a professional 1500-word financial analysis report on '{topic}'. 
    
    Guidelines:
    1. Structure: Introduction, 3 Core Market Data points, and 1 Final Investment Strategy.
    2. Tone: Trustworthy, Institutional, Logical.
    3. Length: Strictly aim for around 1500 words. Do not exceed 2000 words.
    4. Language: English Only. Use Markdown headers.
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        # Max output tokens를 1500~1800 단어 수준으로 조절
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.6, "maxOutputTokens": 1800}}, timeout=60)
        return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except:
        fallback = random.choice(FALLBACK_REPORTS)
        log(f"⚠️ API Limit: Using Fallback '{fallback['title']}'")
        return f"## {fallback['title']}\n\n{fallback['content']}"

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f4f7f9; color: #333; line-height: 1.7; margin: 0; }}
        header {{ background: #003366; color: white; padding: 25px; text-align: center; border-bottom: 4px solid #00509d; }}
        .container {{ max-width: 1200px; margin: 40px auto; display: grid; grid-template-columns: 1fr 320px; gap: 40px; padding: 0 20px; }}
        
        /* [모바일 가독성 개선] 사이드바 겹침 방지 */
        @media(max-width: 1000px) {{ 
            .container {{ grid-template-columns: 1fr; }} 
            .sidebar {{ position: static !important; border-top: 4px solid #003366; margin-top: 20px; }}
        }}
        
        main {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #003366; font-size: 2.5rem; line-height: 1.2; }}
        .content {{ font-size: 1.1rem; }}
        img {{ width: 100%; height: 450px; object-fit: cover; border-radius: 8px; margin-bottom: 30px; }}
        .sidebar {{ background: #fff; padding: 25px; border-radius: 8px; height: fit-content; border-top: 4px solid #003366; }}
        .btn {{ display: block; padding: 15px; background: #003366; color: white; text-decoration: none; text-align: center; font-weight: bold; margin-top: 20px; }}
        footer {{ text-align: center; padding: 60px; color: #888; font-size: 0.9rem; }}
    </style></head>
    <body>
    <header><h1>{BLOG_TITLE}</h1></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <h3 style="margin-top:0;">LATEST INSIGHTS</h3>
            <ul style="list-style:none; padding:0; line-height:2;">{sidebar_html}</ul>
            <a href="{EMPIRE_URL}" class="btn">UNLOCK FULL DATA</a>
        </aside>
    </div>
    <footer>&copy; 2026 Capital Insight | Strategic Intelligence Unit</footer></body></html>"""

def main():
    log("⚡ Unit 1 (Capital) Executing - 1500 Words Target...")
    # 비상 원고 제목 리스트에서 하나를 골라 API 주제로 사용 (다양성 확보)
    sample_topics = ["Global Liquidity Cycle", "Bond Market Volatility", "Emerging Market Reset", "Institutional Gold Demand"]
    topic = random.choice(sample_topics)
    
    full_text = generate_report(topic)
    html_body = markdown.markdown(full_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional financial workstation blue stock charts 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#003366; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Unit 1 1500-word Update Complete.")

if __name__ == "__main__": main()
