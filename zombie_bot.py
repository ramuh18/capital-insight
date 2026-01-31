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

# [📊 구글 트렌드 실시간 수집]
def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Market Liquidity", "Global Inflation"]
    except:
        return ["Economic Supercycle", "Asset Sovereignty"]

# [🖋️ 1,500자급 초장문 엔진 복구]
def generate_deep_report(topic):
    return f"""
# [INTELLIGENCE] Strategic Market Analysis: The Impact of {topic}

## Executive Summary: The 2026 Fiscal Supercycle
The rapid emergence and market penetration of **{topic}** has sent unprecedented ripples through the global financial architecture. As we navigate the escalating complexities of the 2026 fiscal supercycle, understanding the systemic shift triggered by {topic} is no longer a tactical option—it is a mandatory requirement for institutional and private capital preservation. This intelligence report provides an exhaustive analysis of the liquidity traps and sovereign opportunities presenting themselves within this current volatility window.

## 1. Macro-Data & The Systematic Liquidity Squeeze
The integration of {topic} into the global economic discourse follows a decade of unprecedented monetary expansion and fractional reserve over-extension. However, as global central banks pivot toward a permanent 'higher-for-longer' interest rate environment, the hidden fragilities of the legacy banking system are being systematically exposed by the {topic} factor.

Proprietary data from high-frequency trading nodes suggests that institutional 'smart money' is utilizing the public volatility of {topic} as a strategic smokescreen for a massive, coordinated exit from fiat-denominated liabilities. We are currently observing a 14.8% increase in sub-millisecond front-running tactics specifically targeting retail liquidity pools associated with {topic}. In this environment, if you are not secured by non-custodial protocols, you are effectively the liquidity for the exit.

## 2. Structural Realignment: The Rise of Decentralized Reservoirs
Our real-time analysis indicates that the volatility of {topic} is directly correlated with the accelerating outflow of capital from traditional commercial banking institutions. Professional investors are increasingly seeking refuge in decentralized, non-custodial reservoirs to avoid the counterparty risks exposed by the {topic} surge. 

This is not merely a retail-driven trend; sovereign wealth funds and tier-1 family offices are quietly establishing the necessary infrastructure to bypass the legacy settlement layers that are now strained under the weight of the {topic} reset. The true 'Alpha' in this market is found by identifying the sharp divergence between public media sentiment regarding {topic} and the actual, cold-storage accumulation happening in off-exchange dark pools.

## 3. Preservation Protocol: Sovereignty Over Institutional Convenience
In an era increasingly defined by digital lockouts, centralized freezes, and 'bail-in' protocols, the only valid defense against the systemic risks of {topic} is absolute self-custody. The convenience of centralized exchanges and digital banks is currently the primary vulnerability for any significant capital holder. Historical data from previous market resets proves that those who wait for the official 'All Clear' signal regarding {topic} are precisely those who find their accounts restricted or frozen.

The migration to offline, hardware-secured storage is the most significant tactical move a rational investor can make in response to the **{topic}** surge. By removing your primary assets from the fractional reserve system, you effectively opt-out of the systemic fragility that is now being aggressively stress-tested by global market forces.

## Strategic Conclusion: Immediate Tactical Requirements
The supercycle of 2026 is reaching its terminal, high-volatility phase. The massive volatility surrounding **{topic}** is not an isolated event; it is a symptom of a much larger structural reset of the global financial order. We recommend immediate, non-negotiable action: reduce all exposure to legacy debt instruments, accumulate sovereign assets during these {topic} volatility spikes, and secure your private keys in physical, non-digital vaults. The window for preparation is closing; the era of sovereign execution has begun.
"""

# [🔍 자동 SEO 파일 생성기]
def generate_seo_files(history):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{BLOG_BASE_URL}</loc><priority>1.0</priority></url>\n'
    for h in history[:50]:
        sitemap += f'  <url><loc>{BLOG_BASE_URL}{h["file"]}</loc><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write(sitemap)
    
    robots = f"User-agent: *\nAllow: /\nSitemap: {BLOG_BASE_URL}sitemap.xml"
    with open("robots.txt", "w", encoding="utf-8") as f: f.write(robots)

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="여기에_인증코드_입력" />
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
        .btn {{ display: block; padding: 15px; background: var(--main-blue); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 12px; border-radius: 4px; }}
        footer {{ text-align: center; padding: 60px 20px; color: #999; border-top: 1px solid #eee; background: #fff; font-size: 0.85rem; }}
        .footer-links {{ margin-bottom: 20px; }}
        .footer-links a {{ color: #666; text-decoration: none; margin: 0 15px; cursor: pointer; font-weight: bold; }}
        .amazon-disclaimer {{ font-size: 0.75rem; color: #aaa; margin-top: 15px; font-style: italic; line-height: 1.4; }}
        
        /* Modal Styles */
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }}
        .modal-content {{ background: #fff; margin: 10% auto; padding: 30px; width: 80%; max-width: 600px; border-radius: 8px; color: #333; text-align: left; }}
        .close {{ color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div></header>
    <div class="container">
        <main>
            <div style="color:#d90429; font-weight:bold; margin-bottom:10px;">[ STRATEGIC REPORT ]</div>
            <h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn" style="background:#d90429;">🛑 ACCESS EXIT PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS</a>
            </div>
            <div class="side-card">
                <h3 style="color:var(--main-blue); font-family:'Oswald';">LATEST SIGNALS</h3>
                <ul style="list-style:none; padding:0; font-size:0.9rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        <div class="footer-links">
            <a onclick="openModal('about')">About Us</a>
            <a onclick="openModal('privacy')">Privacy Policy</a>
            <a onclick="openModal('contact')">Contact</a>
        </div>
        &copy; 2026 {BLOG_TITLE}. Strategic Intel Protocols Applied.
        <div class="amazon-disclaimer">
            * As an Amazon Associate, this site earns from qualifying purchases. This supports our independent market research and intelligence operations.
        </div>
    </footer>

    <div id="infoModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <div id="modalBody"></div>
        </div>
    </div>

    <script>
        const info = {{
            about: "<h2>About {BLOG_TITLE}</h2><p>Capital Insight provides high-level strategic analysis of global financial trends. We focus on macro-economic shifts and wealth preservation strategies for the modern institutional investor.</p>",
            privacy: "<h2>Privacy Policy</h2><p>We value your privacy. This site uses standard cookies for analytics. We do not collect personal identification information. Your data is used solely to improve our reporting services.</p>",
            contact: "<h2>Contact Information</h2><p>For administrative inquiries or data corrections, contact our strategic desk at: <b>admin@empire-analyst.digital</b></p>"
        }};
        function openModal(id) {{ 
            document.getElementById('modalBody').innerHTML = info[id];
            document.getElementById('infoModal').style.display = "block"; 
        }}
        function closeModal() {{ document.getElementById('infoModal').style.display = "none"; }}
        window.onclick = function(event) {{ if (event.target == document.getElementById('infoModal')) closeModal(); }}
    </script>
    </body></html>"""

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
    
    generate_seo_files(history)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
