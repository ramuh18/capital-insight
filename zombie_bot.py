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
        "Bitcoin Supercycle: 2026 Price Targets",
        "Global Recession & Gold: The Ultimate Hedge",
        "AI Tech Bubble: Institutional Exit Strategy",
        "Ethereum ETF: On-Chain Data Analysis",
        "Federal Reserve Pivot: Market Impact Study"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# [2. 글 세척기]
def clean_chunk(text):
    text = text.strip()
    if text.startswith("{"):
        try:
            data = json.loads(text)
            if 'content' in data: text = data['content']
            elif 'choices' in data: text = data['choices'][0]['message']['content']
        except: pass
    
    # 잡설 제거
    patterns = [r"Powered by Pollinations.*", r"Running on free AI.*", r"Here is the.*", r"Sure, I can.*"]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)
    
    # 마크다운 헤더 정리 (제목 중복 방지용)
    if text.startswith("# "): 
        text = text[text.find("\n"):] # 첫 줄(큰 제목)은 제거하고 본문만 씀
        
    return text.strip()

# [3. 파트별 생성 함수 (핵심)]
def generate_part(topic, section_prompt):
    full_prompt = f"""
    Act as a Senior Financial Analyst. Write a DETAILED section for a report on '{topic}'.
    Focus specifically on: {section_prompt}
    Length: Write at least 400 words.
    Format: Markdown (use ## for subheadings).
    NO JSON. NO INTROS.
    """
    
    for attempt in range(2):
        try:
            # Gemini
            if GEMINI_API_KEY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": full_prompt}]}]}, timeout=45)
                if resp.status_code == 200:
                    return clean_chunk(resp.json()['candidates'][0]['content']['parts'][0]['text'])

            # Pollinations
            url = f"https://text.pollinations.ai/{urllib.parse.quote(full_prompt)}"
            resp = requests.get(url, timeout=60)
            return clean_chunk(resp.text)
        except: time.sleep(1)
    
    return f"## Analysis Update\nData for {section_prompt} is currently processing."

# [4. 3단 합체 생성기]
def generate_full_report(topic):
    log(f"🧠 주제: {topic} (3단 합체 시작)")
    
    # 파트 1: 서론 & 거시경제
    log("✍️ Part 1: Macro Analysis 작성 중...")
    part1 = generate_part(topic, "Executive Summary, Macroeconomic Backdrop, and Interest Rate Outlook.")
    
    # 파트 2: 기관 동향 & 기술적 분석
    log("✍️ Part 2: Institutional & Technical 작성 중...")
    part2 = generate_part(topic, "Institutional Capital Flows, ETF Data, and Technical Analysis (Support/Resistance).")
    
    # 파트 3: 리스크 & 전략
    log("✍️ Part 3: Strategy & Conclusion 작성 중...")
    part3 = generate_part(topic, "Geopolitical Risks, Regulatory Environment, and Final Investment Strategy.")
    
    # 합체
    full_text = f"{part1}\n\n{part2}\n\n{part3}"
    log(f"✅ 전체 리포트 완성 (길이: {len(full_text)}자)")
    return full_text

# [5. 메인 실행]
def main():
    log("🏁 Empire Analyst (Mega-Long Ver) 가동")
    topic = get_hot_topic()
    raw_md = generate_full_report(topic)
    html_content = markdown.markdown(raw_md)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 디자인 요소들
    header_section = f"""
    <div style="background: #000; color: white; padding: 20px 15px; text-align: center; border-radius: 0 0 15px 15px; margin-bottom: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
        <div style="font-family: serif; font-size: 1.8rem; font-weight: 800; letter-spacing: 1px; line-height: 1;">EMPIRE ANALYST</div>
        <div style="font-size: 0.75rem; color: #f1c40f; margin-top: 5px; font-weight: bold; letter-spacing: 2px;">DEEP DIVE REPORT</div>
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
            .content {{ padding: 0 15px; font-size: 1rem; text-align: justify; }}
            h2 {{ color: #2c3e50; font-size: 1.4rem; margin-top: 40px; border-bottom: 2px solid #f5f5f5; padding-bottom: 5px; }}
            li {{ margin-bottom: 8px; }}
            a {{ color: #2980b9; text-decoration: none; }}
        </style>
    </head>
    <body>
        {header_section}
        <div class="meta">UPDATED: {current_time}</div>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Chart">
        <div class="content">{html_content}</div>
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
            client.create_tweet(text=f"⚡ Report: {topic}\n\nLink: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
