# Money Line — always-live trend-flip screener

Supertrend-style ATR trailing stop (Wilder ATR, hl2, **len 10 / mult 2.8**) computed
server-side 4x daily on ~100 large-cap cryptos + 100 large-cap stocks, across
Weekly / Daily / 4H. GitHub Actions does the fetching; GitHub Pages serves the
dashboard; Telegram pings you when anything flips.

**Dashboard URL after setup:** `https://yllsual.github.io/moneyline/`

## Setup (one time, ~10 minutes, all in the browser)

1. **Create the repo.** On github.com → "+" → *New repository* → name it `moneyline`
   → **Public** → Create.

2. **Upload these files.** In the new repo → *uploading an existing file* link (or
   Add file → Upload files) → drag in ALL contents of this bundle **keeping the folder
   structure** (`.github/workflows/refresh.yml`, `scripts/moneyline.py`, `docs/…`,
   `README.md`) → Commit.
   *If the drag-drop flattens folders: create files manually via Add file → Create
   new file and type the path (e.g. `.github/workflows/refresh.yml`) as the filename.*

3. **Add your API keys as encrypted secrets.** Repo → Settings → Secrets and
   variables → Actions → *New repository secret*, one at a time:
   | Name | Value |
   |---|---|
   | `TWELVE_DATA_KEY` | your Twelve Data key |
   | `ALPHA_VANTAGE_KEY` | your Alpha Vantage key |
   | `CMC_KEY` | your CoinMarketCap key |
   | `TELEGRAM_TOKEN` | your bot token from @BotFather |
   | `TELEGRAM_CHAT_ID` | *(optional — see step 5)* |

4. **Turn on the dashboard.** Repo → Settings → Pages → Source: *Deploy from a
   branch* → Branch: `main`, folder: `/docs` → Save. Your dashboard appears at
   the URL above within a minute or two.

5. **Telegram.** Open Telegram, find your bot, send it any message (e.g. "hi").
   On its first run the script auto-discovers your chat id, prints it in the
   Action log, and sends you a "backend is live" confirmation. For permanence,
   copy that chat id from the log into a `TELEGRAM_CHAT_ID` secret.

6. **First run.** Repo → Actions tab → *Money Line refresh* → *Run workflow*.
   Takes ~5–8 minutes. When it finishes, refresh the dashboard — full board.
   After this it runs itself at 00:05, 08:05, 14:45 and 21:15 UTC daily.

## Notes
- API usage at this cadence is a fraction of every free tier (~800 Yahoo/day,
  ~20% of CoinGecko monthly, ~1% of CMC, TD/AV only as retries).
- Flips are computed on **closed candles only** — no intrabar fake-flips.
- `docs/flips.json` keeps a rolling log of the last 500 flips (shown on the page).
- Tune universe/params by editing the constants at the top of `scripts/moneyline.py`.
- GitHub cron can drift 5–15 min at busy times; normal, not a failure.
