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

# [1. 뉴스 주제 선정 (더 자극적이고 전문적인 주제)]
def get_hot_topic():
    topics = [
        "Bitcoin vs Gold: The Ultimate Safe Haven 2026",
        "AI Bubble Burst? Tech Sector Risk Analysis",
        "Global Recession Signals & Investment Strategy",
        "Ethereum ETF: Institutional Money Flow",
        "Oil Prices & Geopolitical Volatility Impact"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# [2. 글 세척기 (무료 AI 광고 삭제 + 퀄리티 보존)]
def clean_content(text):
    text = text.strip()
    
    # (1) JSON 제거
    if text.startswith("{") or "reasoning_content" in text:
        try:
            data = json.loads(text)
            if 'content' in data: text = data['content']
            elif 'choices' in data: text = data['choices'][0]['message']['content']
        except:
            match = re.search(r'"content":\s*"(.*?)"', text, re.DOTALL)
            if match: text = match.group(1).replace('\\n', '\n').replace('\\"', '"')

    # (2) 무료 AI 생색내기 문구 삭제 (중요)
    patterns = [
        r"Powered by Pollinations\.AI.*", r"Support our mission.*", 
        r"🌸 Ad 🌸.*", r"Running on free AI.*", r"Image:.*"
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    # (3) 마크다운 정제
    if '#' in text: text = text[text.find('#'):]

    return text.strip()

# [3. 글쓰기 엔진 (고퀄리티 명령 탑재)]
def generate_article_body(topic):
    log(f"🧠 주제: {topic}")
    # ★ 프롬프트 강화: 단순 요약 금지, 전문적 분석 요구
    prompt = f"""
    Act as a Wall Street Senior Analyst. Write a high-quality, deep-dive financial report about '{topic}'.
    
    Requirements:
    1. Tone: Professional, Authoritative, Insightful.
    2. Structure: 
       - Executive Summary
       - Key Market Drivers
       - Institutional Flow Analysis
       - Strategic Outlook
    3. Length: Detailed (approx 800 words).
    4. Format: Pure Markdown. Use ## for headers.
    5. STRICTLY FORBIDDEN: JSON, Ads, "Here is the report" phrases.
    """
    
    for attempt in range(3):
        try:
            # Gemini (1순위)
            if GEMINI_API_KEY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if resp.status_code == 200:
                    text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    clean = clean_content(text)
                    if len(clean) > 300: return clean

            # Pollinations (2순위)
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            clean = clean_content(resp.text)
            
            if len(clean) > 300: return clean
            
        except: time.sleep(2)

    return f"## Market Update: {topic}\n\nInstitutional flows indicate volatility. Full analysis updating..."

# [4. 메인 실행 (디자인 총집합)]
def main():
    log("🏁 Empire Analyst (The Complete Ver) 가동")
    topic = get_hot_topic()
    
    # 1. 글 생성
    raw_md = generate_article_body(topic)
    html_content = markdown.markdown(raw_md)
    
    # 2. 디자인 요소
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' luxury finance chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ★ 섹션 1: 헤더 (브랜드 강조)
    header_section = f"""
    <div style="text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #eaeaea;">
        <div style="font-size: 0.9rem; font-weight: bold; color: #d63031; letter-spacing: 1px; margin-bottom: 5px;">PREMIUM INTELLIGENCE</div>
        <div style="font-family: serif; font-size: 2.5rem; font-weight: 900; color: #2d3436;">EMPIRE ANALYST</div>
        <div style="font-size: 0.8rem; color: #636e72;">QUANTITATIVE MARKET INSIGHTS • EST. 2026</div>
    </div>
    """

    # ★ 섹션 2: 광고 (바이비트/아마존 고정)
    ads_section = f"""
    <div style="margin: 50px 0; padding: 30px; background: linear-gradient(135deg, #1e1e1e 0%, #2d3436 100%); border-radius: 12px; text-align: center; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15);">
        <h3 style="margin-top: 0; color: #f1c40f;">⚡ Exclusive Trader Access</h3>
        <p style="color: #b2bec3; margin-bottom: 25px;">Institutional-grade tools for serious investors.</p>
        <div style="display: flex; flex-direction: column; gap: 15px; max-width: 400px; margin: 0 auto;">
            <a href="{BYBIT_LINK}" target="_blank" style="background: #f39c12; color: #fff; padding: 15px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1.1rem; transition: 0.3s;">🎁 Claim $30,000 Bonus</a>
            <a href="https://www.amazon.com/s?k=gold+bar&tag={AMAZON_TAG}" target="_blank" style="background: rgba(255,255,255,0.1); color: #fff; padding: 15px; border-radius: 6px; text-decoration: none; font-weight: bold; border: 1px solid rgba(255,255,255,0.2);">🛡️ Physical Asset Hedge</a>
        </div>
    </div>
    """

    # ★ 섹션 3: 푸터 (본진 홍보 - 블랙 카드 디자인 복구)
    footer_section = f"""
    <div style="margin-top: 60px; padding: 40px 20px; background: #000; color: white; border-radius: 16px; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🏛️</div>
        <h2 style="color: white; margin: 0 0 10px 0;">Empire Analyst HQ</h2>
        <p style="color: #636e72; margin-bottom: 30px;">Access full archive and premium signals.</p>
        <a href="{EMPIRE_URL}" style="display: inline-block; background: white; color: black; padding: 12px 30px; border-radius: 30px; font-weight: bold; text-decoration: none; transition: 0.3s;">VISIT OFFICIAL SITE →</a>
        <p style="margin-top: 30px; font-size: 0.7rem; color: #444;">© 2026 Empire Analyst Systems. All rights reserved.</p>
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
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto; padding: 40px 20px; background-color: #fff; }}
            img {{ width: 100%; height: auto; border-radius: 8px; margin: 30px 0; }}
            h1 {{ font-size: 2.2rem; margin-bottom: 10px; line-height: 1.2; }}
            h2 {{ color: #2c3e50; margin-top: 40px; border-bottom: 2px solid #f1f1f1; padding-bottom: 10px; }}
            p {{ margin-bottom: 20px; font-size: 1.05rem; }}
            a {{ color: #2980b9; text-decoration: none; }}
            .meta {{ font-size: 0.8rem; color: #999; margin-bottom: 30px; text-transform: uppercase; }}
        </style>
    </head>
    <body>
        {header_section}
        
        <div class="meta">UPDATED: {current_time}</div>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Market Analysis">
        
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

    # 배포
    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Analysis: {topic}\n\nRead Report: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
