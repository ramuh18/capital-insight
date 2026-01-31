import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration]
BLOG_TITLE = "Capital Insight" 
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Market Reset", "Global Inflation"]
    except:
        return ["Economic Supercycle", "Asset Sovereignty"]

def generate_fixed_report(topic):
    templates = [
        f"""## Analysis: {topic} and Strategic Capital Flow
The 2026 financial markets are adjusting to the emergence of **{topic}**. This intelligence report examines the systemic implications and institutional responses to this trend.

## 1. Macro-Indicators
The integration of {topic} into the broader economic discourse follows a period of extreme monetary expansion. As liquidity tightens, {topic} has become a focal point for risk assessment.

## 2. Strategic Preservation
The primary risk associated with {topic} is systemic lockout. We recommend non-custodial storage solutions to maintain sovereignty over your capital.

## 3. Final Conclusion
Monitoring {topic} is mandatory for the 2026 fiscal cycle. Secure your assets in hardware-based vaults immediately."""
    ]
    return random.choice(templates)

def create_final_html(topic, img_url, body_html, sidebar_html):
    # [수정포인트] header의 position: sticky 제거 및 로고 크기 축소
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --main-blue: #001f3f; --accent-gold: #c5a059; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; color: #1a1a1a; line-height: 1.8; margin: 0; }}
        
        /* 로고 크기 축소 및 화면 고정 해제 */
        header {{ background: var(--main-blue); color: #fff; padding: 25px 20px; text-align: center; border-bottom: 5px solid var(--accent-gold); position: relative; z-index:10; }}
        .brand {{ font-family: 'Oswald', sans-serif; font-size: 2rem; letter-spacing: 2px; text-transform: uppercase; text-shadow: 2px 2px 0px var(--accent-gold); }}
        .tagline {{ font-size: 0.75rem; letter-spacing: 1.5px; color: var(--accent-gold); margin-top: 5px; font-weight: bold; opacity: 0.9; }}

        .container {{ max-width: 1300px; margin: 30px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        
        main {{ background: #fff; padding: 35px; border-radius: 4px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border: 1px solid #eee; }}
        h1 {{ color: var(--main-blue); font-size: 2.5rem; line-height: 1.2; margin-top: 0; }}
        img {{ width: 100%; height: auto; border-radius: 4px; margin-bottom: 30px; border: 1px solid #ddd; }}
        
        .side-card {{ background: #fff; padding: 25px; border-radius: 4px; margin-bottom: 25px; border-top: 5px solid var(--main-blue); box-shadow: 0 3px 10px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 15px; background: var(--main-blue); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 12px; border-radius: 4px; font-size: 1rem; transition: 0.2s; }}
        .btn-red {{ background: #d90429; }}
        .btn:hover {{ opacity: 0.8; transform: translateY(-2px); }}
        
        .amazon-notice {{ font-size: 0.75rem; color: #999; line-height: 1.5; margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px; font-style: italic; }}
        footer {{ text-align: center; padding: 60px 20px; color: #888; border-top: 1px solid #eee; }}
    </style></head>
    <body>
    <header>
        <div class="brand">{BLOG_TITLE}</div>
        <div class="tagline">STRATEGIC FINANCIAL INTELLIGENCE</div>
    </header>
    <div class="container">
        <main>
            <div style="color:#d90429; font-weight:bold; margin-bottom:10px; font-size:0.9rem;">[ TREND REPORT ]</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn btn-red">🛑 ACCESS EXIT PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS</a>
            </div>
            <div class="side-card">
                <h3 style="margin-top:0; color:var(--main-blue); font-family:'Oswald'; border-bottom:2px solid var(--accent-gold); padding-bottom:5px; font-size:1.1rem;">LATEST SIGNALS</h3>
                <ul style="list-style:none; padding:0; line-height:2.2; font-size:0.9rem;">{sidebar_html}</ul>
            </div>
            <div class="amazon-notice">
                * As an Amazon Associate, this site earns from qualifying purchases.
            </div>
        </aside>
    </div>
    <footer>&copy; 2026 {BLOG_TITLE}. Strategic Intel Protocols Applied.</footer></body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_fixed_report(topic)
    html_body = markdown.markdown(body_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('financial chart blue gold 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><b style='color:var(--accent-gold);'>▶</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
