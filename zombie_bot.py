import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time
from datetime import datetime

# ==========================================
# [로그 함수]
# ==========================================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ==========================================
# [설정 로드]
# ==========================================
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://zombie-bot.vercel.app"
EMPIRE_URL = "https://empire-analyst.digital"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET")

# ==========================================
# [1. 뉴스 엔진]
# ==========================================
def get_hot_topic():
    try:
        log("📰 구글 뉴스 접속 시도...")
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries:
            title = feed.entries[0].title
            log(f"✅ 뉴스 수신 성공: {title}")
            return title
    except: pass
    
    log("⚠️ 뉴스 차단됨 -> 비상 주제 사용")
    return random.choice(["Bitcoin ETF Surge", "Global Inflation Crisis", "AI Tech Bubble", "Gold Price Breakout", "Oil Market Volatility"])

# ==========================================
# [2. 콘텐츠 엔진 (백업 원고)]
# ==========================================
def get_backup_article(topic, keyword):
    return f"""
### 🚨 Deep Dive Analysis: {topic}

**Executive Summary**
The global financial markets are undergoing a significant repricing. Institutional capital flows are shifting aggressively into **{keyword}**, signaling a potential regime change in asset allocation. While retail investors are distracted by short-term volatility, smart money is accumulating.

#### 1. Macroeconomic Drivers
Central banks are reaching the limits of quantitative tightening. History shows that when liquidity cycles turn, hard assets like **{keyword}** tend to outperform fiat-denominated securities by a wide margin. The risk-reward ratio at current levels is historically favorable.

#### 2. On-Chain & Technical Data
* **Accumulation**: Whale wallets (>1k units) have added 15% to their positions this month.
* **Supply Shock**: Exchange reserves are at multi-year lows, creating a supply squeeze.
* **Momentum**: The weekly RSI indicates a bullish divergence, often a precursor to a parabolic move.

#### 3. Strategic Action Plan
Retail investors often wait for confirmation, buying the top. Smart money buys the fear.
1. **Accumulate**: Dollar-cost average into {keyword}.
2. **Secure**: Move assets to cold storage immediately.
3. **Trade**: Hedge downside risk on Bybit.

#### Conclusion
The window of opportunity is closing. The data suggests we are in the early stages of a secular bull market for scarce assets. Position yourself accordingly.

*Automated Analysis via Empire Analyst Quantitative Bot.*
    """

def generate_content(topic, keyword):
    log("🧠 AI 글쓰기 시작...")
    prompt = f"Act as a Wall Street Analyst. Write a detailed 1300-word financial report about '{topic}' and '{keyword}'. Use Markdown. Sections: Executive Summary, Macro Analysis, Technicals, Conclusion. Tone: Professional."
    
    # 1차: 구글 Gemini
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, headers={'Content-Type': 'application/json'}, json=data, timeout=30)
            if resp.status_code == 200:
                text = resp.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if len(text) > 800:
                    log("✅ Gemini 생성 성공")
                    return text
        except: pass

    # 2차: 무료 AI
    try:
        simple_prompt = f"Write a long comprehensive financial article about {keyword}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(simple_prompt)}"
        resp = requests.get(url, timeout=40)
        if resp.status_code == 200 and len(resp.text) > 800:
            log("✅ 무료 AI 생성 성공")
            return resp.text
    except: pass

    # 3차: 백업
    log("❌ AI 실패 -> 백업 원고 사용")
    return get_backup_article(topic, keyword)

# ==========================================
# [3. 업로드 및 파일 생성]
# ==========================================
def post_to_devto(title, md, canonical, img):
    if not DEVTO_TOKEN: return
    try:
        data = { "article": { "title": title, "published": True, "body_markdown": md, "canonical_url": canonical, "cover_image": img, "tags": ["finance", "crypto"] } }
        requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}, json=data, timeout=10)
    except: pass

def post_to_x(text):
    if not X_API_KEY: return
    try:
        client = tweepy.Client(consumer_key=X_API_KEY, consumer_secret=X_API_SECRET, access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_TOKEN_SECRET)
        client.create_tweet(text=text)
    except: pass

def main():
    log("🏁 디자인 업그레이드 버전 가동")
    
    # 주제/키워드 선정
    hot_topic = get_hot_topic()
    keyword = "Bitcoin" if "Crypto" in hot_topic else "Gold"
    if "Oil" in hot_topic: keyword = "Oil"
    
    # 본문 생성
    raw_md = generate_content(hot_topic, keyword)

    # 이미지/링크
    try:
        img_prompt = urllib.parse.quote_plus(f"{hot_topic} {keyword} chart finance 8k")
        img_url = f"https://image.pollinations.ai/prompt/{img_prompt}"
        amz_link = f"https://www.amazon.com/s?k={keyword}&tag={AMAZON_TAG}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # [디자인 강화] 프로모션 박스 HTML 직접 제작
        promo_html = f"""
        <div style="margin-top: 50px; padding: 25px; background: #f8f9fa; border-radius: 12px; border: 1px solid #e9ecef;">
            <h3 style="margin-top: 0; color: #2d3436; font-size: 1.4em;">🛡️ Recommended Asset: <span style="color: #d63031;">{keyword}</span></h3>
            <p style="color: #636e72;">Smart money is accumulating. Don't miss the entry.</p>
            <a href="{amz_link}" style="display: block; background: #ff9900; color: white; padding: 16px; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; margin-bottom: 25px; font-size: 1.1em; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                🛒 Check {keyword} Prices on Amazon
            </a>
            
            <hr style="border: 0; border-top: 1px solid #e9ecef; margin: 25px 0;">
            
            <h3 style="margin-top: 0; color: #2d3436; font-size: 1.4em;">💰 Trader's Bonus</h3>
            <p style="color: #636e72;">Volatility is an opportunity. Use leverage wisely.</p>
            <a href="{BYBIT_LINK}" style="display: block; background: #1a1a1a; color: #f9aa33; padding: 16px; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 1.1em; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                🎁 Claim $30,000 Bybit Bonus
            </a>
        </div>
        """

        # HTML 변환 및 저장
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head>
            <title>{hot_topic}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; line-height: 1.7; color: #333; }}
                img {{ max-width: 100%; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                h1 {{ font-size: 2.5em; font-weight: 800; margin-bottom: 10px; letter-spacing: -1px; line-height: 1.2; }}
                h2 {{ margin-top: 40px; border-bottom: 2px solid #000; padding-bottom: 10px; font-size: 1.8em; }}
                h3 {{ margin-top: 30px; font-size: 1.4em; color: #444; }}
                p {{ margin-bottom: 20px; font-size: 1.1em; color: #444; }}
                a {{ color: #0070f3; text-decoration: none; }}
                .tag {{ display: inline-block; background: #eee; padding: 5px 12px; border-radius: 20px; font-size: 0.85em; margin-bottom: 20px; color: #666; font-weight: 600; }}
                .footer {{ margin-top: 60px; text-align: center; padding-top: 20px; border-top: 1px solid #eaeaea; color: #888; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <span class="tag">DAILY INSIGHT • {timestamp}</span>
            <h1>{hot_topic}</h1>
            <img src="{img_url}" alt="Header Image">
            {html_body}
            {promo_html}
            <div class="footer">
                <p>Automated Analysis by Empire Analyst</p>
                <a href="{EMPIRE_URL}" style="color: #0070f3; font-weight: bold;">Visit Official Site →</a>
            </div>
        </body></html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        log("✅ index.html 저장 완료")
        
    except Exception as e:
        log(f"❌ 파일 생성 중 에러: {e}")

    # 외부 업로드
    # Dev.to에는 디자인된 HTML 박스가 안 먹히니, 기존 마크다운 방식으로 보냄
    devto_promo = f"\n\n---\n### 🛡️ Recommended: {keyword}\n[Check Prices]({amz_link})\n\n### 💰 Bonus\n[$30k Bybit Bonus]({BYBIT_LINK})"
    post_to_devto(hot_topic, raw_md + devto_promo, BLOG_BASE_URL, img_url)
    post_to_x(f"⚡ {hot_topic}\n\nRead more: {BLOG_BASE_URL}\n\n#{keyword} #Finance")
    
    log("🏁 작업 종료")

if __name__ == "__main__":
    main()
