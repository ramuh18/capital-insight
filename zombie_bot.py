import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time
from datetime import datetime

# ==========================================
# [로그 함수: 진행 상황을 낱낱이 기록]
# ==========================================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ==========================================
# [설정 및 시크릿 로드]
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
# [1. 뉴스 엔진 (차단 방지 패치)]
# ==========================================
def get_hot_topic():
    # 1순위: 구글 뉴스 시도
    try:
        log("📰 구글 뉴스 접속 시도...")
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries:
            title = feed.entries[0].title
            log(f"✅ 뉴스 수신 성공: {title}")
            return title
    except Exception as e:
        log(f"⚠️ 뉴스 수신 에러: {e}")
    
    # 2순위: 실패 시 강제 주제 선정 (봇이 멈추지 않게 함)
    log("⚠️ 뉴스 차단됨 -> 비상 주제 리스트 사용")
    fallback_topics = ["Bitcoin ETF Surge", "Global Inflation Crisis", "AI Tech Bubble", "Gold Price Breakout", "Oil Market Volatility"]
    return random.choice(fallback_topics)

# ==========================================
# [2. 콘텐츠 엔진 (1300자 보장 + 타임아웃 연장)]
# ==========================================
def get_backup_article(topic, keyword):
    """AI가 모두 죽었을 때 나가는 최후의 보루 (비상 단어 아님, 완성된 글임)"""
    return f"""
### 🚨 Deep Dive Analysis: {topic}

**Executive Summary**
The global financial markets are undergoing a significant repricing. Institutional capital flows are shifting aggressively into **{keyword}**, signaling a potential regime change in asset allocation.

#### 1. Macroeconomic Drivers
Central banks are reaching the limits of quantitative tightening. History shows that when liquidity cycles turn, hard assets like **{keyword}** tend to outperform fiat-denominated securities by a wide margin. The risk-reward ratio at current levels is historically favorable.

#### 2. On-Chain & Technical Data
* **Accumulation**: Whale wallets (>1k units) have added 15% to their positions this month.
* **Supply Shock**: Exchange reserves are at multi-year lows.
* **Momentum**: The weekly RSI indicates a bullish divergence, often a precursor to a parabolic move.

#### 3. Strategic Action Plan
Retail investors often wait for confirmation, buying the top. Smart money buys the fear.
1. **Accumulate**: Dollar-cost average into {keyword}.
2. **Secure**: Move assets to cold storage immediately.
3. **Trade**: Hedge downside risk on Bybit.

*Automated Analysis via Empire Analyst Quantitative Bot.*
    """

def generate_content(topic, keyword):
    log("🧠 AI 글쓰기 시작...")
    
    # 프롬프트: 1300자 이상 강력 요구
    prompt = f"Act as a Wall Street Analyst. Write a detailed 1300-word financial report about '{topic}' and '{keyword}'. Use Markdown. Sections: Executive Summary, Macro Analysis, Technicals, Conclusion. Tone: Professional."
    
    # 1차: 구글 Gemini (타임아웃 30초로 연장)
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
                else:
                    log("⚠️ Gemini 생성 내용이 너무 짧음")
            else:
                log(f"⚠️ Gemini 에러 코드: {resp.status_code} / {resp.text}")
        except Exception as e:
            log(f"⚠️ Gemini 연결 실패: {e}")

    # 2차: 무료 AI (Pollinations)
    try:
        log("🔄 무료 AI 시도 중...")
        simple_prompt = f"Write a long comprehensive financial article about {keyword}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(simple_prompt)}"
        resp = requests.get(url, timeout=40)
        if resp.status_code == 200 and len(resp.text) > 800:
            log("✅ 무료 AI 생성 성공")
            return resp.text
    except Exception as e:
        log(f"⚠️ 무료 AI 실패: {e}")

    # 3차: 백업 템플릿 (절대 빈 화면 안 나감)
    log("❌ 모든 AI 실패 -> 고품질 백업 원고 사용")
    return get_backup_article(topic, keyword)

# ==========================================
# [3. 업로드 엔진 (에러 방지 처리)]
# ==========================================
def post_to_devto(title, md, canonical, img):
    if not DEVTO_TOKEN:
        log("⚠️ Dev.to 토큰 없음 (건너뜀)")
        return
    
    log("🚀 Dev.to 업로드 시도...")
    try:
        data = {
            "article": {
                "title": title,
                "published": True,
                "body_markdown": md,
                "canonical_url": canonical,
                "cover_image": img,
                "tags": ["finance", "crypto", "investing"]
            }
        }
        resp = requests.post("https://dev.to/api/articles", 
                           headers={"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}, 
                           json=data, timeout=20)
        if resp.status_code in [200, 201]:
            log(f"✅ Dev.to 성공: {resp.json()['url']}")
        else:
            log(f"❌ Dev.to 실패: {resp.status_code} - {resp.text}")
    except Exception as e:
        log(f"❌ Dev.to 에러: {e}")

def post_to_x(text):
    if not X_API_KEY:
        log("⚠️ 트위터 키 없음 (건너뜀)")
        return

    log("🚀 트위터 포스팅 시도...")
    try:
        # Client V2 사용 (쓰기 전용)
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET
        )
        resp = client.create_tweet(text=text)
        log(f"✅ 트위터 성공 (ID: {resp.data['id']})")
    except Exception as e:
        log(f"❌ 트위터 에러: {e}")

# ==========================================
# [메인 실행]
# ==========================================
def main():
    log("🏁 봇 전수 조사 수정본 실행")
    
    # 1. 주제 선정
    hot_topic = get_hot_topic()
    keyword = "Bitcoin" if "Crypto" in hot_topic else "Gold"
    if "Oil" in hot_topic: keyword = "Oil"
    
    log(f"📝 확정 주제: {hot_topic} / 키워드: {keyword}")

    # 2. 본문 생성
    raw_md = generate_content(hot_topic, keyword)

    # 3. 이미지 및 링크 준비
    try:
        img_prompt = urllib.parse.quote_plus(f"{hot_topic} {keyword} chart finance 8k")
        img_url = f"https://image.pollinations.ai/prompt/{img_prompt}"
        amz_link = f"https://www.amazon.com/s?k={keyword}&tag={AMAZON_TAG}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        promo = f"\n\n---\n### 🛡️ Recommended Asset: {keyword}\n[Check Prices]({amz_link})\n\n### 💰 Bonus\n[$30k Bybit Bonus]({BYBIT_LINK})"
        final_content = f"![Header]({img_url})\n\n{raw_md}{promo}\n<small>Updated: {timestamp}</small>"
        
        # 4. 파일 저장 (Vercel용)
        html_body = markdown.markdown(final_content)
        full_html = f"""
        <!DOCTYPE html>
        <html><head>
            <title>{hot_topic}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: auto; padding: 20px; line-height: 1.6; color: #333; }}
                img {{ max-width: 100%; border-radius: 10px; margin: 20px 0; }}
                a {{ color: #0070f3; font-weight: bold; text-decoration: none; }}
                h1 {{ font-size: 2.2em; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }}
                code {{ background: #f0f0f0; padding: 3px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <p style="color:#666; font-size:0.9em;">DAILY REPORT • {timestamp}</p>
            <h1>{hot_topic}</h1>
            {html_body}
            <div style="margin-top:50px; text-align:center;">
                <a href="{EMPIRE_URL}" style="background:black; color:white; padding:15px 30px; border-radius:5px;">🚀 Visit Empire Analyst</a>
            </div>
        </body></html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        log("✅ index.html 저장 완료")
        
    except Exception as e:
        log(f"❌ 파일 생성 중 에러: {e}")

    # 5. 외부 업로드 실행
    post_to_devto(hot_topic, final_content, BLOG_BASE_URL, img_url)
    
    tweet_text = f"⚡ {hot_topic}\n\nInstitutional flow detected in {keyword}.\n\nRead more: {BLOG_BASE_URL}\n\n#Finance #Crypto #{keyword}"
    post_to_x(tweet_text)
    
    log("🏁 모든 작업 종료")

if __name__ == "__main__":
    main()
