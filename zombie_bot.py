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

# [1. 뉴스 주제]
def get_hot_topic():
    topics = [
        "Bitcoin Institutional Adoption 2026",
        "Gold vs. US Dollar Outlook",
        "AI Tech Sector Valuation Risks",
        "Global Supply Chain & Inflation",
        "Ethereum ETF Market Impact"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# [2. 악성 코드 & 광고 제거기 (핵심)]
def clean_content(text):
    text = text.strip()
    
    # (1) JSON 껍데기 벗기기
    if text.startswith("{") or "reasoning_content" in text:
        try:
            data = json.loads(text)
            if 'content' in data: text = data['content']
            elif 'choices' in data: text = data['choices'][0]['message']['content']
        except:
            match = re.search(r'"content":\s*"(.*?)"', text, re.DOTALL)
            if match: text = match.group(1).replace('\\n', '\n').replace('\\"', '"')

    # (2) 무료 AI 광고 문구 강제 삭제 (사용자님 스크린샷 대응)
    # "Powered by Pollinations.AI", "Support our mission", "Ad" 등의 문구를 다 지웁니다.
    patterns_to_remove = [
        r"Powered by Pollinations\.AI.*",
        r"Support our mission.*",
        r"🌸 Ad 🌸.*",
        r"pollinations\.ai",
        r"Running on free AI.*"
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # (3) 마크다운 헤더(#) 앞의 잡설 제거
    if '#' in text:
        text = text[text.find('#'):]

    return text.strip()

# [3. 글쓰기 엔진]
def generate_article_body(topic):
    log(f"🧠 주제: {topic}")
    prompt = f"""
    Act as a Senior Financial Analyst. Write a structured blog post about '{topic}'.
    - Structure: Introduction, Key Drivers, Market Outlook, Conclusion.
    - Style: Professional, Insightful, Concise.
    - Format: Pure Markdown only. Use ## for headings.
    - NO JSON. NO ADS. NO FOOTERS.
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
            clean = clean_content(resp.text) # 여기서 광고 삭제됨
            
            if len(clean) > 200: return clean
            
        except Exception as e:
            log(f"⚠️ 에러: {e}")
            time.sleep(2)

    return f"## Market Update: {topic}\n\nInstitutional flows indicate volatility. Please check back for full analysis."

# [4. 메인 실행 (바이비트 강제 삽입)]
def main():
    log("🏁 Empire Analyst (Ad-Block Ver) 가동")
    topic = get_hot_topic()
    
    # 1. 글 생성 및 정제
    raw_md = generate_article_body(topic)
    html_content = markdown.markdown(raw_md)
    
    # 2. 디자인 요소 준비
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ★ 3. 바이비트 섹션 (AI 글과 완전히 분리된 독립 구역)
    # 이 부분은 AI가 손댈 수 없습니다.
    ads_section = f"""
    <div style="margin-top: 50px; padding: 30px; background: #111; color: white; border-radius: 16px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h3 style="margin-top: 0; color: #f9aa33;">💰 Trader's Exclusive</h3>
        <p style="color: #aaa; margin-bottom: 25px;">Take advantage of market volatility.</p>
        
        <div style="display: flex; flex-direction: column; gap: 15px; max-width: 400px; margin: 0 auto;">
            <a href="{BYBIT_LINK}" target="_blank" style="display: block; padding: 18px; background: #f9aa33; color: black; text-decoration: none; border-radius: 8px; font-weight: 900; font-size: 1.2em; transition: 0.3s;">
                🎁 Claim $30,000 Bybit Bonus
            </a>
            
            <a href="https://www.amazon.com/s?k=ledger+nano&tag={AMAZON_TAG}" target="_blank" style="display: block; padding: 18px; background: #333; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; border: 1px solid #555;">
                🛡️ Secure Your Assets (Ledger)
            </a>
        </div>
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
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #222; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #fff; }}
            img {{ width: 100%; height: auto; border-radius: 12px; margin: 30px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 2.5rem; margin-bottom: 10px; border-bottom: 2px solid #f1f1f1; padding-bottom: 15px; letter-spacing: -1px; }}
            h2 {{ color: #2d3436; margin-top: 40px; border-left: 5px solid #000; padding-left: 15px; }}
            p {{ margin-bottom: 20px; font-size: 1.1em; color: #444; }}
            .badge {{ display: inline-block; background: #000; color: white; padding: 6px 12px; border-radius: 50px; font-size: 0.8rem; font-weight: bold; margin-bottom: 20px; }}
            .footer {{ margin-top: 80px; padding-top: 40px; border-top: 1px solid #eee; text-align: center; color: #888; font-size: 0.9rem; }}
            a {{ color: #0070f3; text-decoration: none; }}
        </style>
    </head>
    <body>
        <span class="badge">UPDATED: {current_time}</span>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Market Chart">
        
        <div class="content">
            {html_content}
        </div>
        
        {ads_section}
        
        <div class="footer">
            <p>Automated Analysis by <strong>Empire Analyst Systems</strong></p>
            <p><a href="{EMPIRE_URL}">Visit Official Headquarters →</a></p>
        </div>
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
            client.create_tweet(text=f"⚡ Market Alert: {topic}\n\nFull Analysis: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
