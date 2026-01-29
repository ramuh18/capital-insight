import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_env(key):
    val = os.environ.get(key, "")
    if not val or "***" in val: return ""
    return val.strip()

# [설정]
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

# [1. 주제 선정]
def get_hot_topic():
    topics = [
        "Bitcoin 2026 Outlook: Institutional Flows",
        "Gold Prices: Technical Breakout Analysis",
        "AI Sector Valuation: Bubble or Growth?",
        "Federal Reserve Policy: 2026 Forecast",
        "Ethereum ETF: Market Impact Report"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# [2. 글 세척기 (외계어 앞부분 강제 절단)]
def clean_content(text):
    text = text.strip()
    
    # 1. JSON이면 파싱 시도 (운 좋으면 여기서 걸림)
    if text.startswith("{"):
        try:
            data = json.loads(text)
            if 'content' in data: text = data['content']
            elif 'choices' in data: text = data['choices'][0]['message']['content']
        except: pass

    # 2. ★ 핵심: 마크다운 제목(##)을 찾아서 그 앞(외계어/Reasoning)을 다 날려버림
    # 보통 본문은 "## Executive Summary" 등으로 시작함.
    # ##가 있으면 그 위치부터 끝까지만 살림.
    match = re.search(r'(##\s)', text)
    if match:
        text = text[match.start():]
    else:
        # ##가 없으면 첫 번째 #라도 찾음
        match_single = re.search(r'(#\s)', text)
        if match_single:
            text = text[match_single.start():]

    # 3. 광고 문구 제거
    patterns = [r"Powered by Pollinations.*", r"Running on free AI.*", r"🌸 Ad 🌸.*", r"Image:.*"]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    return text.strip()

# [3. 글쓰기 엔진 (AI에게 ## 쓰라고 강요)]
def generate_article_body(topic):
    log(f"🧠 주제: {topic}")
    prompt = f"""
    Act as a Senior Analyst. Write a financial report on '{topic}'.
    IMPORTANT: Start immediately with a Markdown heading (## Executive Summary).
    Structure:
    ## Executive Summary
    ## Market Drivers
    ## Institutional Analysis
    ## Conclusion
    Format: Markdown. NO JSON. NO INTRO.
    """
    
    for attempt in range(3):
        try:
            # Gemini
            if GEMINI_API_KEY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if resp.status_code == 200:
                    text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    clean = clean_content(text)
                    if len(clean) > 200: return clean

            # Pollinations
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            clean = clean_content(resp.text)
            if len(clean) > 200: return clean
            
        except: time.sleep(1)

    # 실패 시 수동 원고 (이것도 ## 로 시작하게 맞춤)
    return f"""
## Market Analysis: {topic}

**Executive Summary**
Institutional investors are currently hedging against macro volatility. Capital flow analysis suggests a shift towards defensive assets.

**Key Drivers**
* **Inflation:** Persistent CPI data is driving yield curves.
* **Geopolitics:** Uncertainty remains a key factor.

**Outlook**
We maintain a cautious stance. Gold and Bitcoin remain key accumulation targets.
"""

# [4. 메인 실행 (슬림 디자인)]
def main():
    log("🏁 Empire Analyst (Slim Header Ver) 가동")
    topic = get_hot_topic()
    raw_md = generate_article_body(topic)
    html_content = markdown.markdown(raw_md)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ★ 디자인 변경: 헤더 높이 대폭 축소 (padding 40px -> 20px, 폰트 축소)
    header_section = f"""
    <div style="background: #000; color: white; padding: 20px 15px; text-align: center; border-radius: 0 0 15px 15px; margin-bottom: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
        <div style="font-family: serif; font-size: 1.8rem; font-weight: 800; letter-spacing: 1px; line-height: 1;">EMPIRE ANALYST</div>
        <div style="font-size: 0.75rem; color: #f1c40f; margin-top: 5px; font-weight: bold; letter-spacing: 2px;">PREMIUM INTELLIGENCE</div>
    </div>
    """

    ads_section = f"""
    <div style="margin: 40px 0; padding: 25px; background: #f8f9fa; border: 1px solid #ddd; border-radius: 10px; text-align: center;">
        <h3 style="margin-top: 0; font-size: 1.2rem; color: #333;">⚡ Strategic Allocation</h3>
        <div style="display: flex; flex-direction: column; gap: 10px; max-width: 350px; margin: 15px auto 0;">
            <a href="{BYBIT_LINK}" target="_blank" style="background: #000; color: #f1c40f; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1rem;">🎁 Claim $30,000 Bonus</a>
            <a href="https://www.amazon.com/s?k=gold&tag={AMAZON_TAG}" target="_blank" style="background: #e67e22; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1rem;">🛡️ Check Gold Prices</a>
        </div>
    </div>
    """

    footer_section = f"""
    <div style="margin-top: 50px; padding: 30px 20px; background: #111; color: white; border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin: 0 0 15px 0; font-size: 1.2rem;">Empire Analyst HQ</h3>
        <a href="{EMPIRE_URL}" style="display: inline-block; background: white; color: black; padding: 8px 20px; border-radius: 20px; font-weight: bold; text-decoration: none; font-size: 0.9rem;">Official Site →</a>
    </div>
    """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: #333; max-width: 700px; margin: 0 auto; background-color: #fff; padding-bottom: 50px; }}
            img {{ width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }}
            h1 {{ font-size: 1.8rem; margin: 10px 0 10px 0; padding: 0 15px; line-height: 1.3; }}
            .meta {{ font-size: 0.75rem; color: #aaa; padding: 0 15px; font-weight: bold; }}
            .content {{ padding: 0 15px; font-size: 1rem; }}
            h2 {{ color: #2c3e50; font-size: 1.4rem; margin-top: 30px; border-bottom: 2px solid #f5f5f5; padding-bottom: 5px; }}
            li {{ margin-bottom: 8px; }}
            a {{ color: #2980b9; text-decoration: none; }}
        </style>
    </head>
    <body>
        {header_section}
        
        <div class="meta">UPDATED: {current_time}</div>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Chart">
        
        <div class="content">
            {html_content}
        </div>
        
        {ads_section}
        {footer_section}
    </body>
    </html>
    """

    try:
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 저장 완료")
    except Exception as e: log(f"❌ 저장 실패: {e}")

    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Analysis: {topic}\n\nLink: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
