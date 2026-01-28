import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정 로드 - 비밀번호 공백 제거 및 안전장치]
def get_env(key):
    val = os.environ.get(key, "")
    if not val or val.startswith("***"): return "" # 가려진 값이나 빈 값 처리
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

# [1. 뉴스 엔진]
def get_hot_topic():
    try:
        log("📰 최신 금융 뉴스 분석 중...")
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(["AI Tech Bubble & Gold Tug-of-War", "Bitcoin ETF Institutional Inflow", "Global Inflation & Hard Assets"])

# [2. 슈퍼 세척 필터 (사용자님 화면의 reasoning_content 대응)]
def clean_text(raw_text):
    """상자 속에 숨은 '고민 내용'까지 강제로 뜯어내는 함수"""
    raw_text = raw_text.strip()
    
    # 1. JSON 형태라면 모든 구멍을 다 뒤져서 글을 찾아냄
    if raw_text.startswith('{'):
        try:
            data = json.loads(raw_text)
            # 진짜 본문이 있으면 1순위
            if 'content' in data and data['content']: return data['content']
            # OpenAI 스타일이면 2순위
            if 'choices' in data: return data['choices'][0]['message']['content']
            # ★ 사용자님 화면에 뜬 '고민 내용(reasoning)'을 본문으로 변환 (3순위)
            if 'reasoning_content' in data and data['reasoning_content']: 
                return data['reasoning_content']
        except:
            # 파싱 실패 시 강제로 문구 추출
            for key in ['"content":', '"reasoning_content":']:
                if key in raw_text:
                    extracted = raw_text.split(key)[1].split('","')[0].split('"}')[0]
                    return extracted.replace('\\n', '\n').replace('\\"', '"').strip('"')

    # 2. 마크다운 코드 블록(```)이 있으면 그 안의 내용만 추출
    if '```' in raw_text:
        blocks = re.findall(r'```(?:markdown)?(.*?)```', raw_text, re.DOTALL)
        if blocks: return blocks[-1].strip()

    # 3. 마지막 수단: 제목(#)부터 끝까지 가져오기
    if '#' in raw_text:
        return raw_text[raw_text.find('#'):].strip()
        
    return raw_text

# [3. 콘텐츠 엔진 (페르소나 + 1000자 유지)]
def generate_content(topic):
    log(f"🧠 월가 분석가 페르소나 가동: {topic}")
    prompt = f"Act as a Senior Analyst at Bloomberg. Write a detailed 1000-word financial report about {topic}. Use professional tone. Markdown only. No JSON."
    
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
    return f"# Market Insight: {topic}\n\nThe detailed report is being processed."

# [4. 메인 실행]
def main():
    log("🏁 Empire Analyst Quantitative Bot 가동")
    topic = get_hot_topic()
    raw_md = generate_content(topic)
    keyword = "Gold" if "Gold" in topic else "AI"

    try:
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' finance chart 8k')}"
        amz_link = f"https://www.amazon.com/s?k={keyword}&tag={AMAZON_TAG}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head><title>Empire Analyst | {topic}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Inter', sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #2d3436; }}
            img {{ width: 100%; border-radius: 16px; margin: 30px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 2.5em; letter-spacing: -1px; }}
            .promo-card {{ background: #f8f9fa; border-radius: 16px; padding: 30px; margin: 50px 0; border: 1px solid #eee; }}
            .btn {{ display: block; padding: 18px; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; margin: 15px 0; }}
            .footer-card {{ background: #000; color: white; padding: 60px 30px; border-radius: 24px; text-align: center; margin-top: 100px; }}
            .footer-card a {{ display: inline-block; background: white; color: black; padding: 12px 30px; border-radius: 30px; font-weight: bold; text-decoration: none; margin-top: 20px; }}
        </style></head>
        <body>
            <span style="color:#d63031; font-weight:bold;">STRATEGIC REPORT • {timestamp}</span>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{html_body}</div>
            
            <div class="promo-card">
                <h3>🛡️ Featured Asset: {keyword}</h3>
                <a href="{amz_link}" class="btn" style="background:#ff9900;color:white;">🛒 Check {keyword} Market Prices</a>
                <a href="{BYBIT_LINK}" class="btn" style="background:#1a1a1a;color:#f9aa33;">🎁 Claim $30,000 Trading Bonus</a>
            </div>

            <div class="footer-card">
                <div style="font-size:3.5em;">🏛️</div>
                <h2 style="color:white; margin:10px 0;">Empire Analyst</h2>
                <p style="color:#888;">Quantitative Intelligence for Sovereign Investors</p>
                <a href="{EMPIRE_URL}">VISIT HEADQUARTERS →</a>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ 리포트 생성 및 디자인 완료")
    except Exception as e: log(f"❌ 실패: {e}")

    # Dev.to 업로드 (에러 방지 강화)
    if DEVTO_TOKEN and len(DEVTO_TOKEN) > 10:
        try:
            requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}, 
                          json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass

    # X(트위터) 업로드 (에러 방지 강화)
    if X_API_KEY and len(X_API_KEY) > 10:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ {topic}\n\nDeep-dive analysis via Empire Analyst 👇\n{BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
