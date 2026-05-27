#!/usr/bin/env python3
"""
Daily Crocs price checker for Hungarian webshops.
Target: Crocs sandals/slippers, size 45, ~12,000 HUF
"""

import re
import time
import logging
import smtplib
import os
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
from bs4 import BeautifulSoup

# ── Configuration ────────────────────────────────────────────────────────────
TARGET_PRICE    = 12_000   # HUF – "jó ár"
MAX_PRICE       = 20_000   # HUF – felső határár amig még riasztunk
SIZE            = "45"
NOTIFY_EMAIL    = "csatabalazs@gmail.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Data model ───────────────────────────────────────────────────────────────
@dataclass
class Deal:
    name:  str
    price: int
    url:   str
    store: str


# ── Helpers ──────────────────────────────────────────────────────────────────
def _get(url: str, **kwargs) -> Optional[requests.Response]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, **kwargs)
        r.raise_for_status()
        return r
    except Exception as e:
        log.warning(f"GET failed {url[:70]}… → {e}")
        return None


def _parse_price(text: str) -> Optional[int]:
    """'12 990 Ft' / '12.990,-' / '12990' → 12990"""
    text = text.replace("\xa0", "").replace(" ", "").replace(".", "").replace(",", "")
    m = re.search(r"(\d{4,6})", text)
    if m:
        val = int(m.group(1))
        if 1_000 <= val <= 150_000:
            return val
    return None


def _is_crocs(name: str) -> bool:
    return "crocs" in name.lower()


# ── Scrapers ─────────────────────────────────────────────────────────────────
def scrape_arukereso() -> list[Deal]:
    """árukereső.hu – Hungarian price comparison aggregator"""
    deals: list[Deal] = []
    queries = [
        "crocs+szandal+45",
        "crocs+papucs+45",
        "crocs+clog+45",
    ]
    for q in queries:
        r = _get(f"https://www.arukereso.hu/cipok-papucsok-c3231/?st={q}")
        if not r:
            continue
        soup = BeautifulSoup(r.text, "html.parser")

        for item in soup.select(".product-box, .offerBox, [class*='product-item']"):
            name_el  = item.select_one("[class*='name'], h3, h2, .title")
            price_el = item.select_one("[class*='price']")
            link_el  = item.select_one("a[href]")
            if not (name_el and price_el):
                continue
            name  = name_el.get_text(" ", strip=True)
            if not _is_crocs(name):
                continue
            price = _parse_price(price_el.get_text(strip=True))
            if not price:
                continue
            href = link_el["href"] if link_el else ""
            if href and not href.startswith("http"):
                href = "https://www.arukereso.hu" + href
            deals.append(Deal(name=name, price=price, url=href, store="árukereső.hu"))

        time.sleep(1)
    return deals


def scrape_deichmann() -> list[Deal]:
    """deichmann.com/hu"""
    deals: list[Deal] = []
    r = _get("https://www.deichmann.com/hu-hu/search?q=crocs&filter_size=45")
    if not r:
        return deals
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select("article, [data-testid='product-card'], [class*='ProductCard']"):
        name_el  = item.select_one("[class*='name'], [class*='title'], h3, h2")
        price_el = item.select_one("[class*='price'], [class*='Price']")
        link_el  = item.select_one("a[href]")
        if not (name_el and price_el):
            continue
        name = name_el.get_text(" ", strip=True)
        if not _is_crocs(name):
            continue
        price = _parse_price(price_el.get_text(strip=True))
        if not price:
            continue
        href = link_el["href"] if link_el else ""
        if href and not href.startswith("http"):
            href = "https://www.deichmann.com" + href
        deals.append(Deal(name=name, price=price, url=href, store="Deichmann"))

    return deals


def scrape_pepita() -> list[Deal]:
    """pepita.hu"""
    deals: list[Deal] = []
    r = _get("https://www.pepita.hu/kereses?q=crocs+szandal+45&orderby=price_asc")
    if not r:
        return deals
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select(".product, [class*='product-item'], [class*='ProductItem']"):
        name_el  = item.select_one("[class*='name'], [class*='title'], h3, h2")
        price_el = item.select_one("[class*='price']")
        link_el  = item.select_one("a[href]")
        if not (name_el and price_el):
            continue
        name = name_el.get_text(" ", strip=True)
        if not _is_crocs(name):
            continue
        price = _parse_price(price_el.get_text(strip=True))
        if not price:
            continue
        href = link_el["href"] if link_el else ""
        if href and not href.startswith("http"):
            href = "https://www.pepita.hu" + href
        deals.append(Deal(name=name, price=price, url=href, store="Pepita"))

    return deals


def scrape_zalando() -> list[Deal]:
    """zalando.hu – tries embedded __NEXT_DATA__ JSON first, falls back to HTML"""
    deals: list[Deal] = []
    urls = [
        "https://www.zalando.hu/kereses/?q=crocs+szandal&size=EU+45",
        "https://www.zalando.hu/kereses/?q=crocs+papucs&size=EU+45",
    ]
    for url in urls:
        r = _get(url)
        if not r:
            continue
        soup = BeautifulSoup(r.text, "html.parser")

        # Next.js sites embed initial data here
        next_data_tag = soup.find("script", id="__NEXT_DATA__")
        if next_data_tag:
            try:
                import json
                data = json.loads(next_data_tag.string)
                # Walk the nested structure to find articles
                articles = (
                    data.get("props", {})
                       .get("pageProps", {})
                       .get("ssrData", {})
                       .get("search", {})
                       .get("articles", {})
                       .get("items", [])
                )
                for item in articles:
                    name  = item.get("name", "") or item.get("brandName", "")
                    if not _is_crocs(name):
                        name = (item.get("brandName", "") + " " + item.get("name", "")).strip()
                    if not _is_crocs(name):
                        continue
                    price_raw = (
                        item.get("price", {}).get("promotional")
                        or item.get("price", {}).get("original")
                        or {}
                    )
                    price = _parse_price(str(price_raw.get("value", "") or price_raw.get("amount", "")))
                    if not price:
                        continue
                    slug = item.get("urlKey", "") or item.get("slug", "")
                    href = f"https://www.zalando.hu/{slug}.html" if slug else url
                    deals.append(Deal(name=name, price=price, url=href, store="Zalando"))
            except Exception as e:
                log.debug(f"Zalando JSON parse error: {e}")

        # HTML fallback for when Next.js data structure changes
        for item in soup.select(
            "[data-testid='product-card'], article[class*='Card'], "
            "[class*='productCard'], [class*='ProductCard']"
        ):
            name_el  = item.select_one("[class*='name'], [class*='Name'], h3, h2")
            price_el = item.select_one("[class*='price'], [class*='Price']")
            link_el  = item.select_one("a[href]")
            if not (name_el and price_el):
                continue
            name = name_el.get_text(" ", strip=True)
            if not _is_crocs(name):
                continue
            price = _parse_price(price_el.get_text(strip=True))
            if not price:
                continue
            href = link_el["href"] if link_el else url
            if href and not href.startswith("http"):
                href = "https://www.zalando.hu" + href
            deals.append(Deal(name=name, price=price, url=href, store="Zalando"))

        time.sleep(2)
    return deals


def scrape_aboutyou() -> list[Deal]:
    """aboutyou.hu – tries embedded JSON first, falls back to HTML"""
    deals: list[Deal] = []
    urls = [
        "https://www.aboutyou.hu/kereses?query=crocs+szandal&size=45",
        "https://www.aboutyou.hu/kereses?query=crocs+papucs&size=45",
    ]
    for url in urls:
        r = _get(url)
        if not r:
            continue
        soup = BeautifulSoup(r.text, "html.parser")

        # About You (Scayle platform) also uses Next.js / embedded state
        next_data_tag = soup.find("script", id="__NEXT_DATA__")
        if next_data_tag:
            try:
                import json
                data = json.loads(next_data_tag.string)
                products = (
                    data.get("props", {})
                       .get("pageProps", {})
                       .get("initialData", {})
                       .get("products", {})
                       .get("entities", [])
                )
                for item in products:
                    brand = (item.get("brandName") or item.get("brand", {}).get("name") or "")
                    name  = brand + " " + (item.get("name") or "")
                    name  = name.strip()
                    if not _is_crocs(name):
                        continue
                    variants = item.get("variants", []) or [item]
                    for v in variants:
                        price_cents = (
                            v.get("price", {}).get("withTax")
                            or v.get("lowestPrice", {}).get("withTax")
                            or item.get("priceRange", {}).get("min", {}).get("withTax")
                        )
                        if price_cents:
                            # About You stores prices in cents (e.g. 1299000 = 12990 HUF)
                            price = price_cents // 100
                            if not (1_000 <= price <= 150_000):
                                price = _parse_price(str(price_cents))
                            if not price:
                                continue
                            slug = item.get("slug", "") or str(item.get("id", ""))
                            href = f"https://www.aboutyou.hu/p/{slug}" if slug else url
                            deals.append(Deal(name=name, price=price, url=href, store="About You"))
                            break
            except Exception as e:
                log.debug(f"About You JSON parse error: {e}")

        # HTML fallback
        for item in soup.select(
            "[data-testid='product-card'], [class*='ProductCard'], "
            "[class*='productCard'], [class*='product-tile']"
        ):
            name_el  = item.select_one("[class*='name'], [class*='Name'], h3, h2, p")
            price_el = item.select_one("[class*='price'], [class*='Price']")
            link_el  = item.select_one("a[href]")
            if not (name_el and price_el):
                continue
            name = name_el.get_text(" ", strip=True)
            if not _is_crocs(name):
                continue
            price = _parse_price(price_el.get_text(strip=True))
            if not price:
                continue
            href = link_el["href"] if link_el else url
            if href and not href.startswith("http"):
                href = "https://www.aboutyou.hu" + href
            deals.append(Deal(name=name, price=price, url=href, store="About You"))

        time.sleep(2)
    return deals


def scrape_argep() -> list[Deal]:
    """árgép.hu – another price comparison site"""
    deals: list[Deal] = []
    r = _get("https://www.argep.hu/search.php?q=crocs+szandal+45&orderby=price")
    if not r:
        return deals
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select(".product, .offer, [class*='ProductCard']"):
        name_el  = item.select_one("[class*='name'], [class*='title'], h3")
        price_el = item.select_one("[class*='price']")
        link_el  = item.select_one("a[href]")
        if not (name_el and price_el):
            continue
        name = name_el.get_text(" ", strip=True)
        if not _is_crocs(name):
            continue
        price = _parse_price(price_el.get_text(strip=True))
        if not price:
            continue
        href = link_el["href"] if link_el else ""
        if href and not href.startswith("http"):
            href = "https://www.argep.hu" + href
        deals.append(Deal(name=name, price=price, url=href, store="árgép.hu"))

    return deals


# ── Notification ─────────────────────────────────────────────────────────────
def _build_html(deals: list[Deal]) -> str:
    rows = ""
    for d in sorted(deals, key=lambda x: x.price):
        if d.price <= TARGET_PRICE:
            bg, badge = "#d4edda", "🔥 JÓ ÁR"
        elif d.price <= TARGET_PRICE * 1.25:
            bg, badge = "#fff3cd", "💰 Kedvező"
        else:
            bg, badge = "#ffffff", ""

        rows += (
            f'<tr style="background:{bg}">'
            f'<td style="padding:8px 12px">{badge}</td>'
            f'<td style="padding:8px 12px">{d.name}</td>'
            f'<td style="padding:8px 12px;text-align:right"><strong>{d.price:,}&nbsp;Ft</strong></td>'
            f'<td style="padding:8px 12px">{d.store}</td>'
            f'<td style="padding:8px 12px"><a href="{d.url}">Megnyit</a></td>'
            f"</tr>\n"
        )

    return f"""<!DOCTYPE html>
<html lang="hu"><body style="font-family:Arial,sans-serif;max-width:900px;margin:auto;padding:16px">
<h2 style="color:#1565c0">Crocs szandál/papucs akciók – 45-ös méret</h2>
<p>Célár: <strong>{TARGET_PRICE:,} Ft</strong> &nbsp;|&nbsp; Dátum: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
<table border="1" cellspacing="0"
       style="border-collapse:collapse;width:100%;font-size:14px">
  <tr style="background:#1565c0;color:#fff">
    <th style="padding:8px 12px">Státusz</th>
    <th style="padding:8px 12px">Termék</th>
    <th style="padding:8px 12px">Ár</th>
    <th style="padding:8px 12px">Bolt</th>
    <th style="padding:8px 12px">Link</th>
  </tr>
  {rows}
</table>
<p style="color:#888;font-size:11px">Automatikus értesítő – crocs-monitor</p>
</body></html>"""


def notify(deals: list[Deal]):
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD")

    best = min(deals, key=lambda d: d.price)
    subject = (
        f"🔥 Crocs akció! Legjobb ár: {best.price:,} Ft – {len(deals)} találat"
        if best.price <= TARGET_PRICE
        else f"Crocs árak – legjobb: {best.price:,} Ft ({len(deals)} találat)"
    )

    # Always print to stdout (visible in GitHub Actions log)
    print(f"\n{'='*60}")
    print(subject)
    print('='*60)
    for d in sorted(deals, key=lambda x: x.price):
        flag = "🔥" if d.price <= TARGET_PRICE else "  "
        print(f"{flag} {d.price:>8,} Ft  {d.store:<20}  {d.name[:50]}")
        print(f"      {d.url}")
    print('='*60 + "\n")

    if not (gmail_user and gmail_pass):
        log.warning("GMAIL_USER / GMAIL_APP_PASSWORD nincs beállítva – email kihagyva")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = gmail_user
    msg["To"]      = NOTIFY_EMAIL

    plain = "\n".join(
        f"{'[JO AR] ' if d.price <= TARGET_PRICE else ''}"
        f"{d.price:,} Ft  {d.store}  {d.name}\n  {d.url}"
        for d in sorted(deals, key=lambda x: x.price)
    )
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(_build_html(deals), "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_pass)
        smtp.sendmail(gmail_user, NOTIFY_EMAIL, msg.as_string())
    log.info(f"Email elküldve → {NOTIFY_EMAIL}")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    log.info(f"Crocs ár-figyelő indul – méret: {SIZE}, célár: {TARGET_PRICE:,} Ft")

    scrapers = [
        scrape_arukereso,
        scrape_argep,
        scrape_deichmann,
        scrape_pepita,
        scrape_zalando,
        scrape_aboutyou,
    ]

    all_deals: list[Deal] = []
    for fn in scrapers:
        try:
            found = fn()
            log.info(f"{fn.__name__:25s} → {len(found)} találat")
            all_deals.extend(found)
        except Exception as e:
            log.error(f"{fn.__name__} hiba: {e}")
        time.sleep(2)

    # Deduplicate by URL
    seen: set[str] = set()
    unique: list[Deal] = []
    for d in all_deals:
        if d.url not in seen:
            seen.add(d.url)
            unique.append(d)

    good = [d for d in unique if d.price <= MAX_PRICE]
    log.info(f"Összesen {len(unique)} egyedi találat, {len(good)} db MAX_PRICE ({MAX_PRICE:,} Ft) alatt")

    if good:
        notify(good)
    else:
        log.info("Ma nincs megfelelő árú termék – értesítés kihagyva.")


if __name__ == "__main__":
    main()
