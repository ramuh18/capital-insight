import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
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
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
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
    return random.choice(["Bitcoin ETF Surge", "Global Inflation Crisis", "AI Tech Bubble", "Gold Price Breakout", "Oil Market Volatility"])

# ==========================================
# [2. 콘텐츠 엔진 (강력 세척 모드)]
# ==========================================
def clean_text(raw_text):
    """외계어(JSON)를 강제로 찢고 알맹이만 꺼내는 함수"""
    # 1. 만약 순수 텍스트라면 그냥 반환
    if not raw_text.strip().startswith("{"):
        return raw_text
        
    # 2. JSON 파싱 시도 (가장 깔끔한 방법)
    try:
        data = json.loads(raw_text)
        # 'content' 키가 있으면 그게 진짜다
        if isinstance(data, dict):
            if 'choices' in data: return data['choices'][0]['message']['content']
            if 'content' in data: return data['content']
            if 'message' in data: return data['message']['content']
    except: pass

    # 3. 파싱 실패 시: "content":" 뒤에 있는 글자들을 강제로 긁어옴 (무식하지만 확실함)
    try:
        if '"content":"' in raw_text:
            # "content":" 뒤쪽을 다 자르고, 끝에 있는 "}' 같은 찌꺼기 제거
            extracted = raw_text.split('"content":"')[1]
            extracted = extracted.split('"}')[0]
            extracted = extracted.replace('\\n', '\n').replace('\\"', '"') # 깨진 문자 복구
            return extracted
    except: pass
    
    # 4. 정 안되면: '#'으로 시작하는 부분(제목)부터 끝까지 싹 긁음
    match = re.search(r'(#\s.*)', raw_text, re.DOTALL)
    if match:
        return match.group(1)

    # 5. 최후의 수단: 그냥 원본 (근데 여기까지 올 일 거의 없음)
    return raw_text

def generate_content(topic, keyword):
    log(f"🧠 글쓰기 시작: {topic}")
    
    # 1차: 구글 Gemini
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            data = {"contents": [{"parts": [{"text": f"Act as a Wall Street Analyst. Write a detailed 1000-word financial report about '{topic}' and '{keyword}'. Use Markdown. Tone: Professional."}]}]}
            resp = requests.post(url, headers={'Content-Type': 'application/json'}, json=data, timeout=30)
            if resp.status_code == 200:
                text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                return text
        except: pass

    # 2차: 무료 AI (Pollinations)
    try:
        prompt = f"Write a professional financial news article about {topic} and {keyword}. Markdown format. Do not use JSON."
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=60)
        
        if resp.status_code == 200:
            # ★ 여기서 강력 세척기 돌림
            final_text = clean_text(resp.text)
            if len(final_text) > 300:
                log("✅ 무료 AI 생성 성공 (세척 완료)")
                return final_text
    except Exception as e: log(f"Error: {e}")

    # 3차: 비상용 원고
    return f"### 🚨 Market Update: {topic}\n\nInstitutional volume is rising in **{keyword}**. Smart money is accumulating."

# ==========================================
# [3. 업로드 및 디자인]
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
    log("🏁 강력 세척 버전 가동")
    
    hot_topic = get_hot_topic()
    keyword = "Bitcoin" if "Crypto" in hot_topic else "Gold"
    
    # 본문 생성 (세척 포함)
    raw_md = generate_content(hot_topic, keyword)

    try:
        img_prompt = urllib.parse.quote_plus(f"{hot_topic} {keyword} chart finance 8k")
        img_url = f"https://image.pollinations.ai/prompt/{img_prompt}"
        amz_link = f"https://www.amazon.com/s?k={keyword}&tag={AMAZON_TAG}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        promo_html = f"""
        <div style="margin-top: 50px; padding: 25px; background: #f8f9fa; border-radius: 12px; border: 1px solid #e9ecef;">
            <h3 style="margin-top: 0; color: #2d3436;">🛡️ Recommended: <span style="color: #d63031;">{keyword}</span></h3>
            <a href="{amz_link}" style="display: block; background: #ff9900; color: white; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                🛒 Check {keyword} Prices on Amazon
            </a>
            <h3 style="margin-top: 0; color: #2d3436;">💰 Trader's Bonus</h3>
            <a href="{BYBIT_LINK}" style="display: block; background: #1a1a1a; color: #f9aa33; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                🎁 Claim $30,000 Bybit Bonus
            </a>
        </div>
        """

        footer_html = f"""
        <div style="margin-top: 80px; background: #111; padding: 40px 20px; border-radius: 16px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
            <div style="font-size: 3em; margin-bottom: 10px;">🏛️</div>
            <h2 style="color: white; border: none; margin: 0; font-size: 1.8em;">Empire Analyst</h2>
            <p style="color: #888; margin: 10px 0 30px 0; font-size: 0.9em;">Premium Financial Intelligence & Automated Insights</p>
            <a href="{EMPIRE_URL}" style="display: inline-block; background: white; color: black; padding: 15px 35px; border-radius: 30px; font-weight: bold; text-decoration: none; font-size: 1em; transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(255,255,255,0.2);">
                🚀 Visit Official Headquarters
            </a>
            <p style="margin-top: 30px; font-size: 0.7em; color: #444;">
                © 2026 Empire Analyst Systems. All rights reserved.
            </p>
        </div>
        """

        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head>
            <title>{hot_topic}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: auto; padding: 20px; line-height: 1.7; color: #333; }}
                img {{ max-width: 100%; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                h1 {{ font-size: 2.2em; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; margin-top: 10px; }}
                a {{ color: #0070f3; text-decoration: none; }}
                .tag {{ display: inline-block; background: #eee; padding: 5px 12px; border-radius: 20px; font-size: 0.85em; color: #666; font-weight: 600; }}
            </style>
        </head>
        <body>
            <span class="tag">DAILY INSIGHT • {timestamp}</span>
            <h1>{hot_topic}</h1>
            <img src="{img_url}" alt="Header">
            {html_body}
            {promo_html}
            {footer_html}
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        
    except Exception as e: log(f"❌ 에러: {e}")

    post_to_devto(hot_topic, raw_md, BLOG_BASE_URL, img_url)
    tweet_txt = f"⚡ {hot_topic}\n\nSmart money is moving.\n\nRead full report 👇\n{BLOG_BASE_URL}\n\n#{keyword} #Finance"
    post_to_x(tweet_txt)

if __name__ == "__main__":
    main()
