import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration]
BLOG_TITLE = "Alpha Intelligence" 
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Dividend Growth", "Compound Interest"]
    except:
        return ["Alpha Accumulation", "Quantitative Security"]

# [🖋️ 1,500자급 초장문 엔진 복구]
def generate_alpha_report(topic):
    return f"""
# [ALPHA INTEL] Quantitative Analysis: The Structural Shift in {topic}

## Executive Summary: The Era of Volatile Accumulation
The financial landscape of 2026 is being radically redefined by the rapid evolution and market penetration of **{topic}**. For the long-term compounder and dividend seeker, understanding the hidden interplay between surface market volatility and the underlying structural trends of {topic} is no longer just an advantage—it is a critical requirement for survival. This report provides an exhaustive, data-driven deep dive into how {topic} is influencing global asset accumulation and why robust security protocols are mandatory during this transition.

## 1. Algorithmic Dominance & The {topic} Factor
Recent data surrounding {topic} suggests a massive, 200% increase in algorithmic intervention within public markets over the last fiscal quarter. Our proprietary monitoring nodes have successfully identified a recurring pattern of 'liquidity hunting' specifically tied to {topic} news cycles. These institutional front-running tactics often create artificial price floors that retail investors mistakenly identify as organic support.

To achieve true Alpha in the 2026 supercycle, an investor must look far beyond the noisy surface volatility of {topic}. The real value lies in analyzing net-settlement flows and identifying where institutional 'smart money' is actually parking capital. We are currently witnessing a historic migration of capital away from inflationary, legacy assets toward the very nodes of value that {topic} is presently stress-testing in real-time.

## 2. Compounding Under Systemic Pressure: The Security Dividend
While {topic} continues to dominate the global headlines, the silent, more dangerous threat remains the inherent vulnerability of centralized custodial systems. The true 'dividend' of the 2026 era is not just financial gain—it is the absolute security of your principal. As {topic} disrupts traditional valuation models, the risk of a 'systemic freeze' or digital lockout grows exponentially each day.

Our strategic recommendation is to treat digital and physical security as a primary asset class in itself. The accumulation of wealth through {topic} trends is rendered meaningless if the access points to that wealth are controlled by a third party with their own agenda. We observe that the most successful sovereign investors are utilizing this period of {topic} volatility to move their core holdings into hardware-secured, non-custodial vaults. This is the only proven method to ensure that the compounding process remains uninterrupted by the geopolitical realignment currently underway.

## 3. Tactical Preservation: Opting Out of Fractional Fragility
The systemic fragility exposed by the rise of {topic} is not a bug; it is a fundamental feature of the current legacy financial architecture. By opting out of fractional reserve systems, you effectively insulate your entire portfolio from the inevitable fallout of the {topic} volatility cycle. This requires a fundamental, psychological shift in mindset: prioritizing sovereignty and control over mere convenience and speed.

We must emphasize that the migration to cold storage is not an optional suggestion—it is a mandatory tactical requirement for 2026. The current volatility of {topic} is being strategically used by institutional players to flush out leveraged participants and retail holders. Maintaining a neutral position in terms of security is the only viable path to achieving the 'Alpha Intelligence' necessary for long-term capital integrity and generational wealth.

## Strategic Conclusion: The Time for Sovereign Execution
The era of passive, 'set-it-and-forget-it' accumulation has officially ended. The complex dynamics of **{topic}** demand an active, security-first approach to all compounding strategies. We recommend an immediate, comprehensive audit of your asset custody protocols. Minimize your exposure to centralized exchange platforms, secure your private keys in physical, non-digital vaults, and focus exclusively on the quantitative signals that truly drive value. The reset is accelerating, and only the sovereign will prevail.
"""

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
    <meta name="google-site-verification" content="여기에_2호기_인증태그_입력" />
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --alpha-navy: #101820; --alpha-silver: #adb5bd; --alpha-blue: #0047ab; }}
        body {{ font-family: 'Inter', sans-serif; background: #e9ecef; color: #212529; line-height: 1.8; margin: 0; }}
        header {{ background: var(--alpha-navy); color: #fff; padding: 30px 20px; text-align: center; border-bottom: 5px solid var(--alpha-silver); }}
        .brand {{ font-family: 'Montserrat', sans-serif; font-size: 1.8rem; letter-spacing: 1px; text-transform: uppercase; color: var(--alpha-silver); }}
        .container {{ max-width: 1300px; margin: 40px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        main {{ background: #fff; padding: 45px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
        h1 {{ color: var(--alpha-navy); font-size: 2.5rem; line-height: 1.2; margin-top: 0; }}
        .content h2 {{ color: var(--alpha-blue); border-bottom: 2px solid var(--alpha-silver); padding-bottom: 10px; margin-top: 50px; font-family: 'Montserrat'; }}
        img {{ width: 100%; height: auto; border-radius: 6px; margin-bottom: 30px; border: 1px solid #dee2e6; }}
        .side-card {{ background: #fff; padding: 25px; border-radius: 8px; margin-bottom: 25px; border-left: 6px solid var(--alpha-blue); box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 15px; background: var(--alpha-navy); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 12px; border-radius: 4px; transition: 0.2s; }}
        footer {{ text-align: center; padding: 60px 20px; color: #6c757d; border-top: 1px solid #dee2e6; background: #f8f9fa; font-size: 0.85rem; }}
        .footer-links {{ margin-bottom: 20px; }}
        .footer-links a {{ color: #444; text-decoration: none; margin: 0 15px; cursor: pointer; font-weight: bold; }}
        .amazon-disclaimer {{ font-size: 0.75rem; color: #888; margin-top: 15px; font-style: italic; line-height: 1.4; }}
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }}
        .modal-content {{ background: #fff; margin: 10% auto; padding: 30px; width: 80%; max-width: 600px; border-radius: 8px; color: #333; text-align: left; }}
        .close {{ color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }}
    </style></head>
    <body>
    <header><div class="brand">ALPHA_INTELLIGENCE</div></header>
    <div class="container">
        <main>
            <div style="color:var(--alpha-blue); font-weight:bold; margin-bottom:10px;">[ QUANTITATIVE REPORT ]</div>
            <h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn" style="background:#c8102e;">🛑 ACCESS ALPHA PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS</a>
            </div>
            <div class="side-card">
                <h3 style="color:var(--alpha-navy); font-family:'Montserrat';">LATEST ALPHA</h3>
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
        &copy; 2026 {BLOG_TITLE}. Quantitative Accumulation Protocols.
        <div class="amazon-disclaimer">
            * As an Amazon Associate, this site earns from qualifying purchases. This supports our independent market research.
        </div>
    </footer>
    <div id="infoModal" class="modal"><div class="modal-content"><span class="close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div></div>
    <script>
        const info = {{
            about: "<h2>About {BLOG_TITLE}</h2><p>Alpha Intelligence focuses on quantitative strategies for capital growth and compounding. We analyze systemic risks to ensure portfolio integrity.</p>",
            privacy: "<h2>Privacy Policy</h2><p>We do not collect personal data. Cookies are used for analytics only. Your privacy is paramount in our sovereign network.</p>",
            contact: "<h2>Contact</h2><p>For data inquiries: <b>intel@alpha-intelligence.net</b></p>"
        }};
        function openModal(id) {{ document.getElementById('modalBody').innerHTML = info[id]; document.getElementById('infoModal').style.display = "block"; }}
        function closeModal() {{ document.getElementById('infoModal').style.display = "none"; }}
    </script>
    </body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_alpha_report(topic) 
    html_body = markdown.markdown(body_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional clean financial workspace silver blue accent 8k')}?width=1200&height=600"
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li><b style='color:var(--alpha-blue);'>▶</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    generate_seo_files(history)
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
