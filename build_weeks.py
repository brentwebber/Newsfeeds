import re
import feedparser
from urllib.parse import quote_plus
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(".")
DAYS = 7
MAX_ITEMS = 7

WEEKS = {
    1: ("Unethical Behaviors in Organizations",
        ['fraud OR bribery OR corruption OR whistleblower OR misconduct OR "ethics scandal"']),
    2: ("Historical Perspective on Ethics",
        ['"landmark case" ethics OR "years after" scandal OR "history of" business ethics']),
    3: ("Hiring Ethical People & Code of Conduct",
        ['hiring discrimination OR "code of conduct" company OR HR ethics lawsuit']),
    4: ("Ethical Decision Making & Training",
        ['"ethics training" OR compliance training OR "culture of compliance"']),
    5: ("Diversity and Ethics Reporting Systems",
        ['DEI OR discrimination OR harassment AND (hotline OR reporting OR retaliation)']),
    6: ("Managers as Ethical Leaders & Empowering Ethical Employees",
        ['ethical leadership OR servant leadership OR toxic leadership OR empowerment']),
    7: ("Community Outreach and Respect",
        ['CSR OR "community outreach" OR corporate philanthropy OR stakeholder engagement']),
    8: ("Final Reflections on Management Ethics",
        ['business ethics trust OR corporate governance integrity OR ethical leadership lessons'])
}

def rss(query):
    q = quote_plus(f"{query} when:{DAYS}d")
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"

def norm(t):
    t = t.lower()
    t = re.sub(r'[^a-z0-9 ]+', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def build_week(week, title, queries):
    seen = set()
    items = []

    for q in queries:
        feed = feedparser.parse(rss(q))
        for e in feed.entries:
            t = e.get("title", "")
            l = e.get("link", "")
            if not t or not l:
                continue
            key = norm(t)
            if key in seen:
                continue
            seen.add(key)
            items.append((t, l))
            if len(items) >= MAX_ITEMS:
                break
        if len(items) >= MAX_ITEMS:
            break

    date = datetime.now().strftime("%B %d, %Y")
    html = [
        f"<h2>Week {week}: {title}</h2>",
        f"<p><em>Updated automatically – {date}</em></p>",
        "<ul>"
    ]
    for t, l in items:
        html.append(f'<li><a href="{l}" target="_blank" rel="noopener">{t}</a></li>')
    html.append("</ul>")
    html.append(
        "<p><strong>Discussion prompt:</strong> "
        "Select one article and analyze it using an ethical framework "
        "(utilitarianism, deontology, virtue ethics, or justice).</p>"
    )

    (OUTPUT_DIR / f"week{week}.html").write_text("\n".join(html), encoding="utf-8")

def main():
    for wk, (title, queries) in WEEKS.items():
        build_week(wk, title, queries)
    print("All week pages generated.")

if __name__ == "__main__":
    main()
