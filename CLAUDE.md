# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the bot

```bash
pip install -r requirements.txt
python main.py
```

Before running, set real credentials in `main.py` (currently placeholder tokens):
- AiLab API key (line ~20)
- YooKassa account ID and secret key (lines ~23-24)
- Telegram bot token (line ~173)

## Architecture

This is a single-process Telegram bot built with `aiogram 3.x` (async). All bot logic lives in `main.py`.

**State machine:** Users progress through 4 FSM states (`wait_photo` → `choose_haircut`/`choose_color` → `generating_photo`), managed by aiogram's built-in FSM. All per-user state (photo URL, selections, credit count) is stored in memory via FSM state — there is no database.

**Key flow:**
1. User sends photo → bot saves Telegram file URL to FSM state
2. User picks hairstyle (and optionally color) via paginated inline keyboards
3. Bot POSTs to AiLab API (`ailabapi.com/api/portrait/effects/hairstyle-editor-pro`) and polls every 3 seconds for result
4. Users get 2 free generations; further results are blurred (`blur_image()` with Gaussian radius 40) until they pay 50 RUB via YooKassa

**File responsibilities:**
- `main.py` — all bot handlers, API calls, payment logic, FSM transitions
- `keyboard.py` — `KeyboardFactory` builds paginated `InlineKeyboardMarkup`; callback data uses patterns like `haircut_page_2`, `haircut_view_BuzzCut`, `haircut_choose`
- `options.py` — hairstyle/color lists and Russian display names; `callback_options` dict maps callback prefixes to `Options` instances
- `logger.py` — `EventLogger` writes timestamped log files; uses `UserIdFilter` context for per-user logging
- `APIKeyManager.py` — key rotation helper (defined but not yet wired into `main.py`, which hardcodes a single key)

**Static assets:**
- `haircut_photos/` — reference images shown during style selection (named by hairstyle identifier, e.g. `BuzzCut.png`)
- `generated_images/` — runtime output folder; files named `DATETIME_USERID.png`
