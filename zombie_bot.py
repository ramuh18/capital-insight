import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy
from datetime import datetime

# ==========================================
# [0. 설정값 로드]
# ==========================================
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://zombie-bot.vercel.app"
EMPIRE_URL = "https://empire-analyst.digital"

# 환경변수 가져오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET")

# ==========================================
# [1. 초대형 백업 엔진: AI 실패 시 나가는 1,300자+ 원고]
# ==========================================
def get_backup_article(topic, keyword):
    """AI가 응답하지 않을 때 사용하는 고품질 장문 분석글"""
    return f"""
### 🚨 Deep Dive Market Analysis: {topic}

**Executive Summary**
The global financial landscape is undergoing a seismic shift. While mainstream media focuses on short-term noise, on-chain data and institutional order flows suggest a completely different narrative. We are witnessing a historic accumulation phase for **{keyword}**, a trend that retail investors are largely ignoring at their peril. This report dives deep into the macroeconomic factors, technical indicators, and strategic imperatives driving this movement.

---

#### 1. The Macroeconomic Backdrop
To understand why **{keyword}** is poised for explosive growth, we must first look at the broader economic picture. Central banks around the world are grappling with persistent inflation and slowing growth. The traditional 60/40 portfolio is dead. In this environment, scarcity becomes the ultimate currency.

The liquidity cycle is turning. As global liquidity injections resume to prop up failing sovereign debt markets, assets with finite supply caps like **{keyword}** act as a sponge for this excess capital. We are not just seeing a price increase; we are seeing a repricing of fiat currency against hard assets.

#### 2. Institutional Money Flow: The "Smart Money" Move
While retail traders act on fear and greed, institutions act on data. Over the past quarter, OTC (Over-The-Counter) desks have reported a significant uptick in volume for **{keyword}**. This is "silent accumulation"—buying that doesn't immediately show up on the spot price but builds a massive floor of support.

* **Wallet Analysis**: Whale wallets (holding >1,000 units) have increased their exposure by 15% in the last 30 days.
* **Exchange Outflows**: Data shows a net outflow of **{keyword}** from exchanges to cold storage. This supply shock is the precursor to a supply squeeze.

#### 3. Technical Analysis & Key Levels
Looking at the weekly timeframe, **{keyword}** has printed a classic bullish divergence on the RSI. The price action is compressing within a multi-month wedge, signaling that volatility is about to return with a vengeance.

* **Support Zone**: The current levels represent a historical demand zone. Every time price visits this area, it is aggressively bought up by long-term holders.
* **The Breakout**: Once the overhead resistance is cleared, there is very little friction preventing a rapid retest of all-time highs.

#### 4. The Retail Trap
Why do most investors miss this move? Because they are waiting for "confirmation." They wait for the news headlines to tell them it's safe to buy. By the time CNN or Bloomberg is talking about **{keyword}** hitting new highs, the institutional phase is over, and the distribution phase begins.

The market is designed to transfer wealth from the impatient to the patient. Right now, the market is shaking out weak hands before the vertical move. Do not be the liquidity that institutions use to fill their buy orders.

#### 5. Strategic Action Plan
This is not financial advice, but a strategic framework for navigating the coming months.

1.  **Aggressive Accumulation**: Dollar-Cost Averaging (DCA) is the most effective strategy here. Ignore the daily candles and focus on increasing your stack size of **{keyword}**.
2.  **Custodial Security**: "Not your keys, not your coins" remains the golden rule. With exchange solvency risks always present, moving your **{keyword}** to a hardware wallet is non-negotiable.
3.  **Asymmetric Upside**: For those with a higher risk tolerance, using derivatives on platforms like Bybit can amplify gains. However, leverage should be used with extreme caution.

#### Conclusion
The window of opportunity to acquire **{keyword}** at these valuations is closing. The convergence of macro headwinds, institutional adoption, and favorable technicals creates a perfect storm for a parabolic run. The data is clear: the train is leaving the station. Are you on board?

*Analysis provided by the Empire Analyst Quantitative Team.*
    """

# ==========================================
# [2. AI 엔진 (구글 + 무료)]
# ==========================================
def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    models = ["gemini-1.5-flash", "gemini-pro"]
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, headers=headers, json=data, timeout=20)
            if resp.status_code == 200:
                text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                if len(text) > 1000: return text
        except: continue
    return None

def call_pollinations_text(prompt):
    try:
        simple_prompt = f"Write a very long 1500 word financial article about {prompt[:50]}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(simple_prompt)}"
        resp = requests.get(url, timeout=40)
        if resp.status_code == 200 and len(resp.text) > 800:
            return resp.text
    except: pass
    return None

def generate_content(topic, keyword):
    # 1300자 이상 강제 요청 프롬프트
    prompt = f"""
    Act as a senior Wall Street analyst. Write a comprehensive, deep-dive financial report on "{topic}", specifically focusing on "{keyword}".
    Requirements:
    1. Length: MUST be at least 1300 words. Do not write short summaries.
    2. Tone: Professional, urgent, institutional.
    3. Structure: Executive Summary, Macro Analysis, Technicals, On-Chain Data, Conclusion.
    4. Format: Markdown.
    """
    
    # 1차: 구글 Gemini
    content = call_gemini(prompt)
    if content: return content
    
    # 2차: 무료 AI
    content = call_pollinations_text(prompt)
    if content: return content
    
    # 3차: 백업 템플릿 (절대 실패 없음)
    print("⚠️ AI 응답 없음 -> 초대형 백업 엔진 가동")
    return get_backup_article(topic, keyword)

# ==========================================
# [3. 확산 엔진 (Dev.to & X)]
# ==========================================
def post_to_devto(title, md, canonical, img):
    if not DEVTO_TOKEN:
        print("⚠️ DEVTO_TOKEN 없음. 업로드 패스.")
        return

    print(f"🚀 Dev.to 업로드 시도: {title}")
    try:
        data = {
            "article": {
                "title": title,
                "published": True,
                "body_markdown": md,
                "canonical_url": canonical,
                "cover_image": img,
                "tags": ["finance", "crypto", "investing", "economy"]
            }
        }
        headers = {"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}
        resp = requests.post("https://dev.to/api/articles", headers=headers, json=data, timeout=15)
        
        if resp.status_code == 201:
            print(f"✅ Dev.to 성공: {resp.json()['url']}")
        else:
            print(f"❌ Dev.to 실패 ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"❌ Dev.to 에러: {e}")

def post_x_thread(contents):
    if not (X_API_KEY and X_API_SECRET and X_ACCESS_TOKEN and X_ACCESS_TOKEN_SECRET):
        print("⚠️ X(트위터) 키 없음. 업로드 패스.")
        return

    print("🚀 X(트위터) 포스팅 시도...")
    try:
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET
        )
        # 첫 번째 트윗 게시
        response = client.create_tweet(text=contents[0])
        tweet_id = response.data['id']
        print(f"✅ 트윗 작성 성공 (ID: {tweet_id})")
        
        # 스레드(답글)가 있다면 이어달기
        if len(contents) > 1:
            for reply in contents[1:]:
                response = client.create_tweet(text=reply, in_reply_to_tweet_id=tweet_id)
                tweet_id = response.data['id']
    except Exception as e:
        print(f"❌ 트위터 에러: {e}")

# ==========================================
# [4. 메인 실행 로직]
# ==========================================
def main():
    print("🚀 좀비 봇 풀가동 (All-In-One Version)")
    
    # 1. 주제 및 키워드 추출
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        hot_topic = random.choice(feed.entries[:5]).title if feed.entries else "Global Wealth Shift"
    except: hot_topic = "Global Financial Shift"
    
    product_keyword = "Bitcoin" if "Crypto" in hot_topic else "Gold"
    if "Oil" in hot_topic: product_keyword = "Oil"
    
    print(f"📝 주제: {hot_topic} / 키워드: {product_keyword}")

    # 2. 본문 생성 (1300자 이상)
    raw_markdown = generate_content(hot_topic, product_keyword)

    # 3. 이미지 및 링크 생성
    image_prompt = urllib.parse.quote_plus(f"{hot_topic} {product_keyword} cinematic hyper-realistic 8k")
    header_image = f"https://image.pollinations.ai/prompt/{image_prompt}"
    amazon_link = f"https://www.amazon.com/s?k={urllib.parse.quote(product_keyword)}&tag={AMAZON_TAG}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 4. 콘텐츠 조립
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
    
    final_content = f"![Header]({header_image})\n\n" + raw_markdown + promo_md + f"\n\n<small>Updated: {timestamp}</small>"
    
    # 5. index.html 파일 생성 (Vercel용)
    html_body = markdown.markdown(final_content)
    full_html = f"""
    <!DOCTYPE html>
    <html><head>
        <title>{hot_topic}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.8; max-width: 800px; margin: auto; padding: 20px; color: #1a1a1a; background-color: #f9f9f9; }}
            img {{ max-width: 100%; border-radius: 12px; margin: 30px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            a {{ color: #0070f3; font-weight: bold; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            h1 {{ font-size: 2.5em; margin-bottom: 10px; color: #111; letter-spacing: -1px; }}
            h2 {{ margin-top: 40px; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }}
            h3 {{ margin-top: 30px; color: #444; }}
            p {{ font-size: 1.1em; color: #333; }}
            .btn {{ display: block; background: #000; color: #fff !important; text-align: center; padding: 18px; margin: 50px 0; border-radius: 8px; font-size: 1.2em; transition: transform 0.2s; }}
            .btn:hover {{ transform: scale(1.02); }}
            code {{ background: #eee; padding: 2px 5px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <p style="color:#666; font-size:0.9em; font-weight:bold;">DAILY BRIEFING • {timestamp}</p>
        <h1>{hot_topic}</h1>
        {html_body}
        <a href="{EMPIRE_URL}" class="btn">🚀 Visit Official Empire Analyst Site</a>
    </body></html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    print("✅ index.html 생성 완료")
    
    # 6. 외부 플랫폼 업로드
    # Dev.to
    post_to_devto(hot_topic, final_content, BLOG_BASE_URL, header_image)
    
    # Twitter (X)
    tweet_text = f"⚡ Market Alert: {hot_topic}\n\nInstitutional money is moving into {product_keyword}. Are you prepared?\n\nRead full report 👇\n{BLOG_BASE_URL}\n\n#Crypto #Investing #{product_keyword}"
    post_x_thread([tweet_text])

if __name__ == "__main__": main()
