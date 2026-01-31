import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 한글 및 특수문자 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] ★설정 확인★
BLOG_TITLE = "Capital Insight" 
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [📊 구글 트렌드 실시간 수집]
def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Market Liquidity", "Global Inflation"]
    except:
        return ["Economic Supercycle", "Asset Sovereignty"]

# [🖋️ 1,500자급 장문 리포트 엔진] - 요약형이 아닌 상세 분석형
def generate_deep_report(topic):
    return f"""
# [INTELLIGENCE] Strategic Market Analysis: The Impact of {topic}

## Executive Summary
The rapid emergence of **{topic}** has sent ripples through the global financial architecture. As we navigate the complexities of the 2026 fiscal supercycle, understanding the systemic shift triggered by {topic} is no longer optional—it is a requirement for institutional capital preservation. This report provides a deep-dive into the liquidity traps and sovereign opportunities presenting themselves in this current volatility window.

## 1. Macro-Data & The Liquidity Squeeze
The integration of {topic} into the global discourse follows a decade of unprecedented monetary expansion. However, as central banks pivot toward a 'higher-for-longer' interest rate environment, the hidden fragilities of the legacy banking system are being exposed.

Data from high-frequency trading nodes suggests that institutional 'smart money' is utilizing {topic} as a smokescreen for a massive exit from fiat-denominated liabilities. We are seeing a 14% increase in sub-millisecond front-running tactics specifically targeting retail liquidity pools. If you are not secured, you are the liquidity.

## 2. Structural Realignment: Decentralized Reservoirs
Our analysis indicates that {topic} is directly correlated with the accelerating outflow of capital from traditional commercial banks. Investors are increasingly seeking refuge in decentralized, non-custodial reservoirs. This is not merely a retail trend; sovereign wealth funds are quietly establishing infrastructure to bypass the legacy settlement layers that are now strained under the weight of {topic}.

The 'Alpha' in this market is found by identifying the divergence between public sentiment and actual institutional accumulation. While the media focuses on the surface-level noise of {topic}, the real movement is happening in off-exchange dark pools, where trillions are being repositioned into hardware-secured digital gold.

## 3. Preservation Protocol: Sovereignty Over Convenience
In an era of digital lockout and centralized freezes, the only defense against the systemic risks of {topic} is absolute self-custody. The convenience of centralized exchanges is the primary vulnerability. Historical data from previous market resets proves that those who wait for the official 'All Clear' signal are often the ones who find their accounts restricted.

The migration to cold storage is the most significant tactical move an investor can make in response to the {topic} surge. By removing your assets from the fractional reserve system, you effectively opt-out of the systemic fragility that is now being stress-tested by global market forces.

## Strategic Conclusion
The supercycle of 2026 is reaching its terminal phase. The volatility surrounding **{topic}** is a symptom of a larger structural reset. We recommend immediate action: reduce exposure to legacy debt, accumulate sovereign assets during these volatility spikes, and secure your private keys in physical, non-digital vaults. The time for preparation is closing; the time for sovereign execution is now.
"""

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --main-blue: #001f3f; --accent-gold: #c5a059; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; color: #1a1a1a; line-height: 1.8; margin: 0; }}
        header {{ background: var(--main-blue); color: #fff; padding: 25px 20px; text-align: center; border-bottom: 5px solid var(--accent-gold); position: relative; }}
        .brand {{ font-family: 'Oswald', sans-serif; font-size: 2rem; letter-spacing: 2px; text-transform: uppercase; }}
        .container {{ max-width: 1300px; margin: 30px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        main {{ background: #fff; padding: 45px; border-radius: 4px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border: 1px solid #eee; }}
        h1 {{ color: var(--main-blue); font-size: 2.5rem; line-height: 1.2; margin-top: 0; border-bottom: 2px solid #eee; padding-bottom: 15px; }}
        .content h2 {{ color: #d90429; font-family: 'Oswald'; margin-top: 40px; border-left: 5px solid var(--accent-gold); padding-left: 15px; }}
        img {{ width: 100%; height: auto; border-radius: 4px; margin-bottom: 30px; border: 1px solid #ddd; }}
        .side-card {{ background: #fff; padding: 25px; border-radius: 4px; margin-bottom: 25px; border-top: 5px solid var(--main-blue); box-shadow: 0 3px 10px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 15px; background: var(--main-blue); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 12px; border-radius: 4px; font-size: 1rem; transition: 0.2s; }}
        .btn-red {{ background: #d90429; }}
        footer {{ text-align: center; padding: 60px 20px; color: #999; border-top: 1px solid #eee; background: #fff; font-size: 0.85rem; }}
        .amazon-disclaimer {{ font-style: italic; margin-top: 10px; opacity: 0.8; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div></header>
    <div class="container">
        <main>
            <div style="color:#d90429; font-weight:bold; margin-bottom:10px;">[ STRATEGIC REPORT ]</div>
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
                <h3 style="margin-top:0; color:var(--main-blue); font-family:'Oswald';">LATEST SIGNALS</h3>
                <ul style="list-style:none; padding:0; line-height:2.2; font-size:0.9rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        &copy; 2026 {BLOG_TITLE}. Strategic Intel Protocols Applied.
        <div class="amazon-disclaimer">* As an Amazon Associate, this site earns from qualifying purchases. This supports our independent market research.</div>
    </footer></body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_deep_report(topic) 
    html_body = markdown.markdown(body_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional financial data analysis dark blue 8k')}?width=1200&height=600"
    
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
    log(f"✅ Full Strategic Update Complete: {topic}")

if __name__ == "__main__": main()
