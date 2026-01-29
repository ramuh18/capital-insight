import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_env(key):
    val = os.environ.get(key, "")
    if not val or "***" in val: return ""
    return val.strip()

AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
EMPIRE_URL = "https://empire-analyst.digital"

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
DEVTO_TOKEN = get_env("DEVTO_TOKEN")
X_API_KEY = get_env("X_API_KEY")
X_API_SECRET = get_env("X_API_SECRET")
X_ACCESS_TOKEN = get_env("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = get_env("X_ACCESS_TOKEN_SECRET")

# [1. 뉴스 엔진: 같은 뉴스 지겹다! 랜덤 섞기]
def get_hot_topic():
    # 가끔은 RSS 말고 강제로 다른 주제 선정 (다양성 확보)
    if random.random() < 0.3: 
        return random.choice([
            "Future of AI Trading Bots 2026", 
            "Bitcoin vs Gold: The Final Battle", 
            "Ethereum's Next Big Upgrade", 
            "Tesla Stock Analysis 2026",
            "Global Real Estate Market Crash?"
        ])
    
    try:
        log("📰 구글 뉴스 확인 중...")
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return "Market Volatility Update"

# [2. 외계어 적출 필터]
def clean_text(raw_text):
    raw_text = raw_text.strip()
    if raw_text.startswith('{'):
        try:
            data = json.loads(raw_text)
            if 'content' in data: return data['content']
            if 'choices' in data: return data['choices'][0]['message']['content']
        except: pass
    match = re.search(r'"content"\s*:\s*"(.*?)"', raw_text, re.DOTALL)
    if match: return match.group(1).replace('\\n', '\n').replace('\\"', '"').strip()
    if '#' in raw_text: return raw_text[raw_text.find('#'):]
    return raw_text

# [3. 콘텐츠 엔진]
def generate_content(topic):
    log(f"🧠 주제: {topic}")
    prompt = f"Write a new financial report about {topic}. Focus on future predictions. Markdown format. No JSON."
    
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if resp.status_code == 200:
                return clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
        except: pass

    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200: return clean_text(resp.text)
    except: pass
    
    return f"# Analysis: {topic}\n\nData is updating..."

# [4. 메인 실행]
def main():
    log("🏁 Zombie Bot (Visual Proof Version) 가동")
    topic = get_hot_topic()
    raw_md = generate_content(topic)
    
    if not raw_md or len(raw_md) < 50:
        raw_md = f"# {topic}\n\nAutomated analysis in progress."

    # ★ 핵심: 현재 시간을 아주 크게 박아넣음
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    keyword = "Finance"
    try:
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
        amz_link = f"https://www.amazon.com/s?k=investment&tag={AMAZON_TAG}"
        
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head><title>Empire Analyst</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Helvetica', sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #333; }}
            img {{ width: 100%; border-radius: 12px; margin: 30px 0; }}
            h1 {{ font-size: 2.2em; border-bottom: 2px solid #eee; padding-bottom: 15px; letter-spacing: -1px; }}
            .time-badge {{ background: #ffeaa7; color: #d35400; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 0.9em; }}
            .footer-card {{ background: #111; color: white; padding: 60px 20px; border-radius: 20px; text-align: center; margin-top: 80px; }}
            .btn {{ background: #fff; color: #000; padding: 12px 25px; text-decoration: none; border-radius: 30px; font-weight: bold; }}
            a {{ color: #0070f3; text-decoration: none; }}
        </style></head>
        <body>
            <div>
                <span class="time-badge">UPDATED: {current_time_str} UTC</span>
            </div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            {html_body}
            
            <div style="background:#f9f9f9; padding:20px; text-align:center; border-radius:10px; margin-top:40px;">
                 <h3>🛡️ Empire Selection</h3>
                 <a href="{amz_link}" style="background:#ff9900; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-weight:bold;">Check Prices</a>
            </div>

            <div class="footer-card">
                <h2>Empire Analyst</h2>
                <p>Automated Financial Intelligence</p>
                <a href="{EMPIRE_URL}" class="btn">OFFICIAL SITE →</a>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 업데이트 완료")
    except Exception as e: log(f"❌ HTML 저장 실패: {e}")

    # Dev.to & X 업로드
    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Update ({current_time_str}): {topic}\n\nLink: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
