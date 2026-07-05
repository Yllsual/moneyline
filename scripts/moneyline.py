#!/usr/bin/env python3
"""
Money Line backend — runs on GitHub Actions 4x daily.
Fetches crypto (Binance/CoinGecko) + stocks (Yahoo/TwelveData/AlphaVantage),
computes the Money Line (Supertrend hl2, Wilder ATR, len=10, mult=2.8) on
Weekly / Daily / 4H, writes docs/data.json for the dashboard, logs flips to
docs/flips.json, and sends Telegram alerts on confirmed trend flips.
"""

import json, os, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

# ── Config ───────────────────────────────────────────────────────────
ATR_LEN, MULT = 10, 2.8
TFS = {"1w": 604_800_000, "1d": 86_400_000, "4h": 14_400_000}
TF_LABEL = {"1w": "Weekly", "1d": "Daily", "4h": "4H"}
TOP_COINS = 100

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

TD_KEY  = os.environ.get("TWELVE_DATA_KEY", "")
AV_KEY  = os.environ.get("ALPHA_VANTAGE_KEY", "")
CMC_KEY = os.environ.get("CMC_KEY", "")
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TG_CHAT  = os.environ.get("TELEGRAM_CHAT_ID", "")

EXCLUDE = {"usdt","usdc","usds","usde","dai","fdusd","pyusd","tusd","usdp","usd1","susds","susde",
           "wbtc","weth","steth","wsteth","wbeth","weeth","reth","cbbtc","cbeth","rseth","ezeth",
           "meth","jitosol","msol","bnsol","lseth","tbtc","solvbtc","buidl","usdtb","usdf"}

STOCKS = [
 ("AAPL","Apple"),("MSFT","Microsoft"),("NVDA","NVIDIA"),("GOOGL","Alphabet"),("AMZN","Amazon"),
 ("META","Meta Platforms"),("AVGO","Broadcom"),("TSLA","Tesla"),("BRK.B","Berkshire Hathaway"),("LLY","Eli Lilly"),
 ("JPM","JPMorgan Chase"),("V","Visa"),("XOM","Exxon Mobil"),("UNH","UnitedHealth"),("MA","Mastercard"),
 ("ORCL","Oracle"),("COST","Costco"),("HD","Home Depot"),("PG","Procter & Gamble"),("NFLX","Netflix"),
 ("JNJ","Johnson & Johnson"),("BAC","Bank of America"),("CRM","Salesforce"),("ABBV","AbbVie"),("CVX","Chevron"),
 ("KO","Coca-Cola"),("AMD","AMD"),("MRK","Merck"),("PEP","PepsiCo"),("WMT","Walmart"),
 ("TMO","Thermo Fisher"),("ADBE","Adobe"),("CSCO","Cisco"),("ACN","Accenture"),("LIN","Linde"),
 ("MCD","McDonald's"),("ABT","Abbott Labs"),("INTU","Intuit"),("TXN","Texas Instruments"),("GE","GE Aerospace"),
 ("QCOM","Qualcomm"),("IBM","IBM"),("CAT","Caterpillar"),("DIS","Disney"),("VZ","Verizon"),
 ("PLTR","Palantir"),("AMGN","Amgen"),("PFE","Pfizer"),("ISRG","Intuitive Surgical"),("NOW","ServiceNow"),
 ("GS","Goldman Sachs"),("SPG","Simon Property"),("UBER","Uber"),("CMCSA","Comcast"),("MS","Morgan Stanley"),
 ("RTX","RTX Corp"),("UNP","Union Pacific"),("T","AT&T"),("AXP","American Express"),("BKNG","Booking Holdings"),
 ("HON","Honeywell"),("LOW","Lowe's"),("NEE","NextEra Energy"),("ELV","Elevance Health"),("BLK","BlackRock"),
 ("LMT","Lockheed Martin"),("SCHW","Charles Schwab"),("SBUX","Starbucks"),("BA","Boeing"),("MDT","Medtronic"),
 ("UPS","UPS"),("DE","Deere"),("GILD","Gilead"),("TMUS","T-Mobile"),("PYPL","PayPal"),
 ("C","Citigroup"),("CVS","CVS Health"),("MO","Altria"),("SO","Southern Company"),("DUK","Duke Energy"),
 ("MMM","3M"),("CL","Colgate-Palmolive"),("TGT","Target"),("BMY","Bristol-Myers"),("USB","US Bancorp"),
 ("FDX","FedEx"),("GM","General Motors"),("F","Ford"),("EMR","Emerson Electric"),("NKE","Nike"),
 ("GD","General Dynamics"),("COP","ConocoPhillips"),("WFC","Wells Fargo"),("MET","MetLife"),("COF","Capital One"),
 ("AIG","AIG"),("INTC","Intel"),("MU","Micron"),("MRVL","Marvell Technology"),("COIN","Coinbase"),
]

S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) MoneyLineScreener/1.0"

def get(url, tries=3, backoff=2.0, headers=None):
    last = None
    for a in range(1, tries + 1):
        try:
            r = S.get(url, timeout=30, headers=headers)
            if r.status_code in (418, 429):
                time.sleep(backoff * a); last = Exception("rate limited"); continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            if a < tries: time.sleep(backoff * a)
    raise last

# ── Engine: Wilder ATR + Supertrend(hl2) ─────────────────────────────
def supertrend(c):
    n = len(c)
    atr, prev = [0.0] * n, None
    for i in range(n):
        tr = (c[i]["h"] - c[i]["l"]) if i == 0 else max(
            c[i]["h"] - c[i]["l"], abs(c[i]["h"] - c[i-1]["c"]), abs(c[i]["l"] - c[i-1]["c"]))
        prev = tr if prev is None else (prev * (ATR_LEN - 1) + tr) / ATR_LEN
        atr[i] = prev
    line, dirn = [0.0] * n, [1] * n
    flo = fhi = None
    for i in range(n):
        src = (c[i]["h"] + c[i]["l"]) / 2
        lo, hi = src - MULT * atr[i], src + MULT * atr[i]
        if i == 0:
            flo, fhi = lo, hi; line[i] = fhi; continue
        flo = max(lo, flo) if c[i-1]["c"] > flo else lo
        fhi = min(hi, fhi) if c[i-1]["c"] < fhi else hi
        if dirn[i-1] == -1: dirn[i] = 1 if c[i]["c"] < flo else -1
        else:               dirn[i] = -1 if c[i]["c"] > fhi else 1
        line[i] = flo if dirn[i] == -1 else fhi
    return line, dirn

def drop_unclosed(cands, period_ms):
    now = time.time() * 1000
    out = list(cands)
    while out and out[-1]["t"] + period_ms > now:
        out.pop()
    return out

def analyse(cands, period_ms, live_price):
    closed = drop_unclosed(cands, period_ms)
    if len(closed) < ATR_LEN + 15:
        return None
    line, dirn = supertrend(closed)
    n = len(closed)
    flip_i = next((i for i in range(n - 1, 0, -1) if dirn[i] != dirn[i-1]), None)
    bull, lvl = dirn[-1] == -1, line[-1]
    price = live_price if live_price else closed[-1]["c"]
    fp = closed[flip_i]["c"] if flip_i else None
    return {
        "bull": bull,
        "price": round(price, 6),
        "flipLevel": round(lvl, 6),
        "flipPrice": round(fp, 6) if fp else None,
        "flipTime": closed[flip_i]["t"] if flip_i else None,
        "sinceFlip": round((price - fp) / fp * 100, 2) if fp else None,
        "dist": round(abs(price - lvl) / price * 100, 2),
    }

# ── Aggregation helpers ──────────────────────────────────────────────
def agg(cands, ms):
    out = {}
    for c in cands:
        k = (c["t"] // ms) * ms
        w = out.get(k)
        if not w: out[k] = dict(t=k, o=c["o"], h=c["h"], l=c["l"], c=c["c"])
        else: w["h"] = max(w["h"], c["h"]); w["l"] = min(w["l"], c["l"]); w["c"] = c["c"]
    return [out[k] for k in sorted(out)]

def weekly_from_daily(daily):
    out = {}
    for c in daily:
        dt = datetime.fromtimestamp(c["t"] / 1000, tz=timezone.utc)
        mon = dt - timedelta(days=dt.weekday())
        k = int(datetime(mon.year, mon.month, mon.day, tzinfo=timezone.utc).timestamp() * 1000)
        w = out.get(k)
        if not w: out[k] = dict(t=k, o=c["o"], h=c["h"], l=c["l"], c=c["c"])
        else: w["h"] = max(w["h"], c["h"]); w["l"] = min(w["l"], c["l"]); w["c"] = c["c"]
    return [out[k] for k in sorted(out)]

# ── Crypto sources ───────────────────────────────────────────────────
def crypto_universe():
    coins = []
    if CMC_KEY:
        try:
            j = get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=170&convert=USD",
                    headers={"X-CMC_PRO_API_KEY": CMC_KEY})
            coins = [(c["symbol"].upper(), c["name"]) for c in j["data"]]
            print(f"universe via CoinMarketCap: {len(coins)} candidates")
        except Exception as e:
            print("CMC universe failed:", e)
    if not coins:
        j = get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=170&page=1", backoff=4)
        coins = [((m["symbol"] or "").upper(), m["name"]) for m in j]
        print(f"universe via CoinGecko: {len(coins)} candidates")
    import re as _re
    seen, out = set(), []
    for sym, name in coins:
        if not _re.fullmatch(r"[A-Z0-9]{1,10}", sym): continue   # junk / non-latin tickers
        if sym.lower() in EXCLUDE or sym in seen: continue
        seen.add(sym); out.append((sym, name))
        if len(out) >= TOP_COINS: break
    return out

# data-api.binance.vision = Binance's official public-data mirror (not geo-blocked,
# unlike api.binance.com which returns 451 from US-hosted GitHub runners)
BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]

def binance_get(path):
    last = None
    for base in BINANCE_BASES:
        try:
            return get(base + path, tries=2)
        except Exception as e:
            last = e
    raise last

def binance_symbols():
    try:
        return {t["symbol"] for t in binance_get("/api/v3/ticker/price")}
    except Exception as e:
        print("Binance symbol list failed:", e); return set()

def binance_klines(sym, iv, limit):
    j = binance_get(f"/api/v3/klines?symbol={sym}&interval={iv}&limit={limit}")
    return [dict(t=k[0], o=float(k[1]), h=float(k[2]), l=float(k[3]), c=float(k[4])) for k in j]

def gecko_id_map(symbols):
    """Map ticker symbols → coingecko ids for the non-Binance stragglers."""
    try:
        j = get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1", backoff=4)
        m = {}
        for c in j:
            s = (c["symbol"] or "").upper()
            if s in symbols and s not in m: m[s] = c["id"]
        return m
    except Exception:
        return {}

def gecko_candles(cid):
    """Returns (daily_candles_365d, hourly_candles_42d) — close-derived."""
    def pts_to_cands(pts):
        out = []
        for i in range(1, len(pts)):
            p0, p1 = pts[i-1][1], pts[i][1]
            out.append(dict(t=pts[i][0], o=p0, h=max(p0, p1), l=min(p0, p1), c=p1))
        return out
    d = get(f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=365&interval=daily", backoff=4)
    time.sleep(2.5)
    hqs = get(f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=42", backoff=4)
    return pts_to_cands(d["prices"]), pts_to_cands(hqs["prices"])

# ── Stock sources ────────────────────────────────────────────────────
def yahoo(sym, iv, rng):
    j = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym.replace('.', '-')}?interval={iv}&range={rng}")
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(res["timestamp"]):
        if q["close"][i] is None: continue
        out.append(dict(t=ts * 1000, o=q["open"][i], h=q["high"][i], l=q["low"][i], c=q["close"][i]))
    return out

def twelve(sym, iv):
    j = get(f"https://api.twelvedata.com/time_series?symbol={sym}&interval={iv}&outputsize=300&apikey={TD_KEY}", tries=2, backoff=4)
    if j.get("status") == "error" or "values" not in j:
        raise Exception(j.get("message", "TwelveData error"))
    out = [dict(t=int(datetime.fromisoformat(v["datetime"]).replace(tzinfo=timezone.utc).timestamp() * 1000),
                o=float(v["open"]), h=float(v["high"]), l=float(v["low"]), c=float(v["close"])) for v in j["values"]]
    return sorted(out, key=lambda x: x["t"])

def alpha(sym, weekly):
    fn = "TIME_SERIES_WEEKLY" if weekly else "TIME_SERIES_DAILY"
    key = "Weekly Time Series" if weekly else "Time Series (Daily)"
    j = get(f"https://www.alphavantage.co/query?function={fn}&symbol={sym}&apikey={AV_KEY}", tries=1)
    ts = j.get(key)
    if not ts: raise Exception(j.get("Note") or j.get("Information") or "AlphaVantage: no data")
    out = [dict(t=int(datetime.fromisoformat(d).replace(tzinfo=timezone.utc).timestamp() * 1000),
                o=float(v["1. open"]), h=float(v["2. high"]), l=float(v["3. low"]), c=float(v["4. close"]))
           for d, v in ts.items()]
    return sorted(out, key=lambda x: x["t"])[-300:]

# ── Telegram ─────────────────────────────────────────────────────────
def tg_chat_id():
    global TG_CHAT
    if TG_CHAT or not TG_TOKEN: return TG_CHAT
    try:
        j = get(f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates", tries=1)
        for u in reversed(j.get("result", [])):
            m = u.get("message") or u.get("channel_post")
            if m: TG_CHAT = str(m["chat"]["id"]); break
        if TG_CHAT:
            print(f">>> Telegram chat id auto-discovered: {TG_CHAT} — add it as the TELEGRAM_CHAT_ID secret to make this permanent")
    except Exception as e:
        print("Telegram chat discovery failed:", e)
    return TG_CHAT

def tg_send(text):
    if not (TG_TOKEN and tg_chat_id()): return
    try:
        S.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
               json={"chat_id": TG_CHAT, "text": text, "parse_mode": "HTML"}, timeout=20)
    except Exception as e:
        print("Telegram send failed:", e)

# ── Main ─────────────────────────────────────────────────────────────
def main():
    started = time.time()
    prev_assets = {}
    first_run = True
    data_path = DOCS / "data.json"
    if data_path.exists():
        try:
            old = json.loads(data_path.read_text())
            prev_assets = {(a["kind"], a["sym"]): a for a in old.get("assets", [])}
            first_run = not prev_assets
        except Exception:
            pass

    assets = []

    # ── crypto ──
    universe = crypto_universe()
    bsyms = binance_symbols()
    non_bin = [s for s, _ in universe if s + "USDT" not in bsyms]
    gmap = gecko_id_map(set(non_bin)) if non_bin else {}
    print(f"crypto: {len(universe)} coins ({len(universe)-len(non_bin)} on Binance)")

    gecko_fails = 0
    for sym, name in universe:
        entry = dict(kind="crypto", sym=sym, name=name, tf={})
        try:
            if sym + "USDT" in bsyms:
                for tf, iv, lim in (("1w", "1w", 300), ("1d", "1d", 400), ("4h", "4h", 400)):
                    cands = binance_klines(sym + "USDT", iv, lim)
                    live = cands[-1]["c"] if cands else None
                    r = analyse(cands, TFS[tf], live)
                    if r: entry["tf"][tf] = r
                    time.sleep(0.15)
                entry["src"] = "binance"
            elif sym in gmap:
                if gecko_fails >= 6:
                    raise Exception("skipped — CoinGecko persistently rate limited this run")
                daily, hourly = gecko_candles(gmap[sym])
                live = daily[-1]["c"] if daily else None
                for tf, cands in (("1w", weekly_from_daily(daily)), ("1d", daily), ("4h", agg(hourly, TFS["4h"]))):
                    r = analyse(cands, TFS[tf], live)
                    if r: entry["tf"][tf] = r
                entry["src"] = "coingecko"
                time.sleep(2.5)
            else:
                entry["err"] = "no data source"
        except Exception as e:
            entry["err"] = str(e)[:120]
            if "rate limited" in entry["err"]: gecko_fails += 1
        if entry["tf"]:
            assets.append(entry)
            if entry.get("src") == "coingecko": gecko_fails = 0
        elif entry.get("err"): print(f"  crypto {sym}: {entry['err']}")

    # ── stocks ──
    for sym, name in STOCKS:
        entry = dict(kind="stocks", sym=sym, name=name, tf={})
        try:
            daily = yahoo(sym, "1d", "2y"); time.sleep(0.35)
            hourly = yahoo(sym, "1h", "6mo"); time.sleep(0.35)
            live = daily[-1]["c"] if daily else None
            for tf, cands in (("1w", weekly_from_daily(daily)), ("1d", daily), ("4h", agg(hourly, TFS["4h"]))):
                r = analyse(cands, TFS[tf], live)
                if r: entry["tf"][tf] = r
            entry["src"] = "yahoo"
        except Exception:
            try:
                if not TD_KEY: raise Exception("no TD key")
                for tf, iv in (("1w", "1week"), ("1d", "1day"), ("4h", "4h")):
                    cands = twelve(sym, iv)
                    r = analyse(cands, TFS[tf], cands[-1]["c"] if cands else None)
                    if r: entry["tf"][tf] = r
                    time.sleep(8.2)
                entry["src"] = "twelvedata"
            except Exception:
                try:
                    daily = alpha(sym, weekly=False)
                    live = daily[-1]["c"] if daily else None
                    for tf, cands in (("1w", weekly_from_daily(daily)), ("1d", daily)):
                        r = analyse(cands, TFS[tf], live)
                        if r: entry["tf"][tf] = r
                    entry["src"] = "alphavantage"
                    time.sleep(1)
                except Exception as e3:
                    entry["err"] = str(e3)[:120]
        if entry["tf"]: assets.append(entry)
        else: print(f"  stock {sym}: {entry.get('err','no data')}")

    # ── flips vs previous run ──
    flips = []
    for a in assets:
        pa = prev_assets.get((a["kind"], a["sym"]))
        if not pa: continue
        for tf, cur in a["tf"].items():
            po = (pa.get("tf") or {}).get(tf)
            if po and po.get("bull") is not None and po["bull"] != cur["bull"]:
                flips.append(dict(sym=a["sym"], name=a["name"], kind=a["kind"], tf=tf,
                                  bull=cur["bull"], price=cur["price"], t=int(time.time() * 1000)))

    # write flip log (rolling, newest first, capped)
    flog_path = DOCS / "flips.json"
    flog = []
    if flog_path.exists():
        try:
            flog = json.loads(flog_path.read_text())
            if not isinstance(flog, list): flog = []
        except Exception:
            flog = []
    flog = (flips[::-1] + flog)[:500]
    flog_path.write_text(json.dumps(flog))

    # ── write data.json ──
    bulls = sum(1 for a in assets if a["tf"].get("1w", {}).get("bull"))
    out = dict(
        updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        params=dict(atrLen=ATR_LEN, mult=MULT),
        stats=dict(total=len(assets), bull_1w=bulls, bear_1w=len(assets) - bulls),
        assets=assets,
    )
    data_path.write_text(json.dumps(out))
    print(f"wrote {len(assets)} assets in {time.time()-started:.0f}s | {len(flips)} flips")

    # ── Telegram ──
    if first_run:
        tg_send("✅ <b>Money Line backend is live.</b> You'll get a message here whenever an asset flips trend.")
    if flips:
        lines = [f"<b>Money Line — {len(flips)} flip{'s' if len(flips)>1 else ''}</b>"]
        for f in flips[:25]:
            e = "🟢 BULLISH" if f["bull"] else "🔴 BEARISH"
            lines.append(f"{e} — <b>{f['sym']}</b> ({TF_LABEL[f['tf']]}) at ${f['price']:,}")
        if len(flips) > 25: lines.append(f"…and {len(flips)-25} more")
        tg_send("\n".join(lines))

if __name__ == "__main__":
    main()
