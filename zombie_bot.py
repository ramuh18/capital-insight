import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy
from datetime import datetime

# ==========================================
# [설정 구역]
# ==========================================
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://zombie-bot.vercel.app"
EMPIRE_URL = "https://empire-analyst.digital"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")

# ==========================================
# [엔진 1: 구글 Gemini (주력)]
# ==========================================
def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    # 3가지 모델을 순서대로 두드려봅니다.
    models = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, headers=headers, json=data, timeout=20)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except: continue
    return None

# ==========================================
# [엔진 2: Pollinations AI (비상용)]
# ==========================================
def call_pollinations_text(prompt):
    print("⚠️ 구글 엔진 실패 -> 비상용 무료 엔진 가동")
    try:
        # 무료 텍스트 생성 API (No Key Required)
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=40)
        if resp.status_code == 200: return resp.text
    except: pass
    return None

# [통합 생성기]
def generate_content(prompt):
    # 1차 시도
    content = call_gemini(prompt)
    if content: return content
    # 2차 시도
    content = call_pollinations_text(prompt)
    if content: return content
    # 3차 시도 (최후의 안전장치)
    return "Market volatility detected. Secure your assets in hardware wallets immediately."

# ==========================================
# [기능 함수]
# ==========================================
def get_hot_topic():
    try:
        # 구글 뉴스 (경제 섹션) RSS
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return random.choice(feed.entries[:5]).title
    except: pass
    return "Global Financial Shift"

def post_to_devto(title, md, canonical, img):
    if not DEVTO_TOKEN: return
    try:
        data = {"article": {"title": title, "published": True, "body_markdown": md, "canonical_url": canonical, "cover_image": img, "tags": ["finance", "crypto"]}}
        requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}, json=data)
    except: pass

def post_x_thread(contents):
    try:
        client = tweepy.Client(
            consumer_key=os.environ.get("X_API_KEY"),
            consumer_secret=os.environ.get("X_API_SECRET"),
            access_token=os.environ.get("X_ACCESS_TOKEN"),
            access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET")
        )
        client.create_tweet(text=contents[0])
    except: pass

# ==========================================
# [메인 실행]
# ==========================================
def main():
    print("🚀 좀비 봇(Hybrid) 가동 시작")
    
    # 1. 주제 선정
    hot_topic = get_hot_topic()
    print(f"📝 주제: {hot_topic}")
    
    # 2. 키워드 추출
    keyword_prompt = f"Extract ONE main physical object from headline '{hot_topic}' (e.g. Gold, Bitcoin, Oil). Output ONLY the word."
    product_keyword = generate_content(keyword_prompt).strip().replace('"', '').split('\n')[0]
    if len(product_keyword) > 20: product_keyword = "Wealth Strategy"
    
    # 3. 본문 작성 (월스트리트 톤)
    main_prompt = f"""
    Act as a Wall Street Analyst. Write a short, punchy market update on "{hot_topic}".
    Focus on why smart money is moving into "{product_keyword}".
    Tone: Professional, Direct, Urgent. No robotic intros.
    Length: 800 words. Markdown format.
    """
    raw_markdown = generate_content(main_prompt)

    # 4. 이미지 및 링크
    image_prompt = urllib.parse.quote_plus(f"{hot_topic} {product_keyword} cinematic hyper-realistic 8k")
    header_image = f"https://image.pollinations.ai/prompt/{image_prompt}"
    
    safe_keyword = urllib.parse.quote_plus(product_keyword)
    amazon_link = f"https://www.amazon.com/s?k={safe_keyword}&tag={AMAZON_TAG}"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 5. HTML 조립
    disclaimer = f"\n\n---\n<small><i>Updated: {timestamp} | Affiliate links included.</i></small>"
    
    promo_md = f"""
    \n\n---
    ### 🏛️ Premium Research
    **[Read full analysis at Empire Analyst ->]({EMPIRE_URL})**
    
    ### 🛡️ Recommended Asset: {product_keyword}
    Check prices: **[Amazon Best Deals]({amazon_link})**
    \n
    ### 💰 Trade the News
    Get **$30,000 Bonus** on Bybit (`DOVWK5A`): **[Claim Bonus]({BYBIT_LINK})**
    """
    
    final_content = f"![Header]({header_image})\n\n" + raw_markdown + promo_md + disclaimer
    
    html_body = markdown.markdown(final_content)
    
    # [중요] 기존 vercel.json을 건드리지 않고 index.html만 덮어씁니다.
    full_html = f"""
    <!DOCTYPE html>
    <html><head>
        <title>{hot_topic}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Helvetica', sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; color: #333; }}
            img {{ max-width: 100%; border-radius: 8px; margin: 20px 0; }}
            a {{ color: #d93025; font-weight: bold; text-decoration: none; }}
            h1 {{ font-size: 2.2em; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .btn {{ display: block; background: #000; color: #fff !important; text-align: center; padding: 15px; margin: 40px 0; border-radius: 5px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <p style="color:#666; font-size:0.8em;">DAILY BRIEFING • {timestamp}</p>
        <h1>{hot_topic}</h1>
        {html_body}
        <a href="{EMPIRE_URL}" class="btn">🚀 Visit Official Empire Analyst Site</a>
    </body></html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    print("✅ index.html 업데이트 완료")

    # 6. 확산 (Dev.to & X)
    post_to_devto(hot_topic, final_content, BLOG_BASE_URL, header_image)
    post_x_thread([f"⚡ {hot_topic}\n\nFocus: {product_keyword}\nRead: {BLOG_BASE_URL}", f"Details 🔗 {BLOG_BASE_URL}"])

if __name__ == "__main__": main()
