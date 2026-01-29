import os, json, random, requests, markdown, urllib.parse, feedparser, time, re
from datetime import datetime

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정 로드]
def get_env(key):
    val = os.environ.get(key, "")
    if not val: return ""
    return val.strip().replace("\n", "").replace("\r", "")

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
DEVTO_TOKEN = get_env("DEVTO_TOKEN")

# [기본 설정]
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
AMAZON_TAG = "empireanalyst-20"
EMPIRE_URL = "https://empire-analyst.digital"

# ==========================================
# [1. 제목 선정: 자연스러운 어그로]
# ==========================================
def get_hot_topic():
    # 실시간 뉴스 수집
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "Market Crash Warning"
    except: raw_news = "Global Financial Crisis"

    # AI에게 제목 변환 요청 (8단어 이하, 로봇 말투 금지)
    prompt = f"""
    Rewrite this news headline into a short, viral blog title (UNDER 8 WORDS).
    Original: "{raw_news}"
    Rules:
    1. NO "BREAKING:", "ALERT:", "WARNING:". No robot words.
    2. Make it sound like a smart financial insider whispering a secret.
    3. STRICTLY under 8 words.
    """
    
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                if resp.status_code == 200:
                    return clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=30)
            return clean_text(resp.text)
        except: time.sleep(1)
    return "Why The Market Is Collapsing"

def clean_text(text):
    text = text.strip()
    patterns = [r"Title:", r"\"", r"\*", r"BREAKING:", r"ALERT:", r"Here is.*"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [2. 본문 생성]
# ==========================================
def generate_part(topic, focus):
    prompt = f"Act as a cynical wall street trader. Write a section on '{topic}'. Focus: {focus}. Length: 400+ words. Markdown. NO JSON."
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
                if resp.status_code == 200: return clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            return clean_text(resp.text)
        except: time.sleep(1)
    return f"Analysis pending for {focus}..."

# ==========================================
# [3. 메인 실행 및 Dev.to 업로드]
# ==========================================
def main():
    log("🏁 Empire Analyst (Dev.to Only Ver) 가동")
    topic = get_hot_topic()
    log(f"🔥 제목: {topic}")
    
    # 본문 생성
    p1 = generate_part(topic, "The Ugly Truth")
    p2 = generate_part(topic, "Technical Signals")
    p3 = generate_part(topic, "Prediction")
    raw_md = clean_text(f"{p1}\n\n{p2}\n\n{p3}")
    html_body = markdown.markdown(raw_md)
    
    # 파일 저장 (내 블로그용)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_filename = f"post_{file_timestamp}.html"
    
    # HTML 템플릿 (내부 링크 포함)
    full_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{topic}</title>
    <link rel="canonical" href="{BLOG_BASE_URL}{archive_filename}" />
    <style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.7;color:#333;max-width:700px;margin:0 auto;padding-bottom:50px}}img{{width:100%;border-radius:8px;margin:20px 0}}h1{{font-size:2rem;color:#c0392b;font-weight:900}}a{{color:#2980b9;text-decoration:none}}.header{{background:#000;color:#fff;padding:20px;text-align:center;border-radius:0 0 15px 15px}}</style></head><body>
    <div class="header"><h1>EMPIRE ANALYST</h1></div>
    <h1>{topic}</h1><img src="{img_url}">{html_body}
    <div style="margin-top:50px;padding:20px;background:#f8f9fa;text-align:center;"><h3>🚀 Strategic Allocation</h3><a href="{BYBIT_LINK}" style="background:#000;color:#f1c40f;padding:10px 20px;border-radius:5px;font-weight:bold;">🎁 Get $30,000 Bonus</a></div>
    </body></html>"""
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ 블로그 저장 완료: {archive_filename}")

    # ★ Dev.to 업로드 (상세 에러 출력 기능 포함)
    if DEVTO_TOKEN:
        log("🚀 Dev.to 업로드 시도 중...")
        try:
            # Dev.to용 마크다운 (이미지, 링크 포함)
            final_md = f"# {topic}\n\n![Chart]({img_url})\n\n{raw_md}\n\n## 🔗 Check Original Report\nRead the full analysis here: [{BLOG_BASE_URL}{archive_filename}]({BLOG_BASE_URL}{archive_filename})"
            
            payload = {
                "article": {
                    "title": topic,
                    "published": True,
                    "body_markdown": final_md,
                    "canonical_url": f"{BLOG_BASE_URL}{archive_filename}",
                    "tags": ["finance", "crypto", "investing", "bitcoin"]
                }
            }
            resp = requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json=payload, timeout=15)
            
            if resp.status_code in [200, 201]:
                log(f"✅ Dev.to 업로드 성공! 주소: {resp.json().get('url')}")
            else:
                log(f"❌ Dev.to 실패 (코드: {resp.status_code})")
                log(f"❌ 에러 메시지: {resp.text}") 
        except Exception as e:
            log(f"⚠️ Dev.to 연결 에러: {e}")
    else:
        log("⚠️ Dev.to 토큰이 없습니다. (GitHub Secrets를 확인하세요)")

if __name__ == "__main__": main()
