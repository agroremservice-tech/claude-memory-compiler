"""
SessionStart hook — injects KB context + daily briefing into every conversation.

On the first session of the day, fetches KeyCRM funnel data directly via REST API
(parallel requests, no MCP overhead) and injects a pre-formatted briefing block.
Subsequent sessions of the same day get KB + log only.
"""

import json
import re
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone, date
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent.parent
VAULT_ROOT    = ROOT.parent
KNOWLEDGE_DIR = ROOT / "knowledge"
DAILY_DIR     = ROOT / "daily"
SCRIPTS_DIR   = ROOT / "scripts"
INBOX_DIR     = VAULT_ROOT / "Inbox"
INDEX_FILE    = KNOWLEDGE_DIR / "index.md"

MAX_CONTEXT_CHARS = 12_000
MAX_LOG_LINES     = 15

# ── KeyCRM API ─────────────────────────────────────────────────────────────────
KEYCRM_API_KEY = "OGU4MWY1MzFlNDAzZjU4NGMyNzM2MWUyNjFiZWEyYTM0ZWU0MDM5OA"
KEYCRM_BASE    = "https://openapi.keycrm.app/v1"

STATUS_NAMES = {
    1: "Новий",         2: "Інбокс",   13: "Аванс",
    38: "Рахунок",      91: "Виробництво",    158: "Нараховано",
    189: "Критичний",   11: "КП підготовка",  37: "КП переговори",
    96: "КП фініш",     68: "Фото/ТЗ",        69: "Інфо Агрорем",
    70: "КП надіслано", 72: "КП пауза",       88: "Перестав відп.",
    148: "1 міс",       59: "Уточнення конт.", 67: "Зміна планів",
}

UA_DAYS = {
    "Monday": "Понеділок", "Tuesday": "Вівторок", "Wednesday": "Середа",
    "Thursday": "Четвер",  "Friday": "П'ятниця",  "Saturday": "Субота",
    "Sunday": "Неділя",
}


# ── KeyCRM helpers ─────────────────────────────────────────────────────────────

def _fetch_status(status_id: int) -> list:
    """Single HTTP request for one status_id, returns raw card list."""
    qs = (
        f"pipeline_id=1&filter[status_id]={status_id}"
        f"&include=contact,status,custom_fields&limit=50"
    )
    url = f"{KEYCRM_BASE}/pipelines/cards?{qs}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {KEYCRM_API_KEY}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            items = data.get("data", []) if isinstance(data, dict) else data
            return items if isinstance(items, list) else []
    except Exception:
        return []


def _get_cf(card: dict, field_id: str) -> str:
    for cf in card.get("custom_fields") or []:
        fid = str(cf.get("field_id") or cf.get("id") or "")
        if fid == field_id:
            v = cf.get("text_value") or cf.get("value") or ""
            return str(v).strip()
    return ""


def _parse_nc(dt_str: str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _fmt_date(d) -> str:
    return d.strftime("%d.%m") if d else "—"


# ── Briefing builder ───────────────────────────────────────────────────────────

def _fmt_amount(amount) -> str:
    if not amount:
        return "—"
    n = int(amount)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}М"
    if n >= 1000:
        return f"{n // 1000}к"
    return str(n)


def build_briefing() -> str:
    today  = datetime.now(timezone.utc).astimezone().date()
    cutoff = today - timedelta(days=14)

    MONEY_SIDS   = [13, 38, 91]           # Нараховано (158) не включати
    WATCH_SIDS   = [70, 37, 96]           # КП надіслано / переговори / фініш
    CRITICAL_SID = 189
    CALL_SIDS    = [1, 2, 11, 70, 37, 96, 68, 69, 72, 88, 148, 59, 67]
    FETCH_IDS    = list(dict.fromkeys(MONEY_SIDS + WATCH_SIDS + [CRITICAL_SID] + CALL_SIDS))

    cards_by_status: dict[int, list] = {}
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(_fetch_status, sid): sid for sid in FETCH_IDS}
        for fut in as_completed(futs, timeout=13):
            sid = futs[fut]
            try:
                cards_by_status[sid] = fut.result()
            except Exception:
                cards_by_status[sid] = []

    out = []

    # ── 1. Гроші в роботі (Аванс / Рахунок / Виробництво) ────────────────
    money_rows = []
    for sid in MONEY_SIDS:
        for c in cards_by_status.get(sid, []):
            amount  = int(c.get("products_total") or 0)
            abc     = _get_cf(c, "LD_1036")
            contact = c.get("contact") or {}
            name    = contact.get("full_name") or c.get("title") or f"#{c['id']}"
            money_rows.append((amount, STATUS_NAMES.get(sid, ""), name, abc))
    money_rows.sort(key=lambda x: -x[0])

    out.append("### 💰 ГРОШІ В РОБОТІ\n")
    if money_rows:
        for amount, status_nm, name, abc in money_rows:
            out.append(f"{name} | {status_nm} | {_fmt_amount(amount)} | {abc or '—'}")
        out.append(f"РАЗОМ: {_fmt_amount(sum(r[0] for r in money_rows))}\n")
    else:
        out.append("Немає\n")

    # ── 2. Топ воронки (A+B, КП надіслано / переговори / фініш) ──────────
    watch_rows = []
    seen_watch: set = set()
    for sid in WATCH_SIDS:
        for c in cards_by_status.get(sid, []):
            cid = c.get("id")
            if cid in seen_watch:
                continue
            abc = _get_cf(c, "LD_1036") or ""
            if abc not in ("A", "B"):
                continue
            seen_watch.add(cid)
            amount  = int(c.get("products_total") or 0)
            contact = c.get("contact") or {}
            name    = contact.get("full_name") or c.get("title") or f"#{cid}"
            nc_date = _parse_nc(c.get("communicate_at", ""))
            watch_rows.append((-amount, name, STATUS_NAMES.get(sid, ""), amount, abc, nc_date))
    watch_rows.sort()

    out.append("### 🎯 ТОП ВОРОНКИ (A+B)\n")
    if not watch_rows:
        out.append("Немає\n")
    else:
        for _, name, status_nm, amount, abc, nc_date in watch_rows[:10]:
            out.append(f"{name} | {_fmt_amount(amount)} | {status_nm} | {abc} | НК: {_fmt_date(nc_date)}")
        out.append("")

    # ── 3. Дзвонити сьогодні (НК <= сьогодні, >= cutoff) ─────────────────
    call_rows = []
    seen_ids: set = set()
    for sid in CALL_SIDS:
        for c in cards_by_status.get(sid, []):
            cid = c.get("id")
            if cid in seen_ids:
                continue
            nc_date = _parse_nc(c.get("communicate_at", ""))
            if nc_date and cutoff <= nc_date <= today:
                seen_ids.add(cid)
                amount    = int(c.get("products_total") or 0)
                abc       = _get_cf(c, "LD_1036") or ""
                abc_order = {"A": 0, "B": 1, "C": 2}.get(abc, 3)
                contact   = c.get("contact") or {}
                name      = contact.get("full_name") or c.get("title") or f"#{cid}"
                status_nm = STATUS_NAMES.get(sid, "")
                pfx       = "⚠️ " if nc_date < today else ""
                call_rows.append((abc_order, -amount, nc_date, pfx, name, amount, status_nm, abc))
    call_rows.sort(key=lambda x: (x[0], x[1], x[2]))

    a_rows  = [r for r in call_rows if r[0] == 0][:10]
    bc_rows = [r for r in call_rows if r[0] != 0][:10]

    out.append("### 📞 ДЗВОНИТИ СЬОГОДНІ\n")
    if not call_rows:
        out.append("НК немає ✅\n")
    else:
        if a_rows:
            out.append("A:")
            for _, neg_amt, nc_date, pfx, name, amount, status_nm, abc in a_rows:
                out.append(f"{pfx}{name} | {_fmt_amount(amount)} | {status_nm} | {_fmt_date(nc_date)}")
            out.append("")
        if bc_rows:
            out.append("B/C:")
            for _, neg_amt, nc_date, pfx, name, amount, status_nm, abc in bc_rows:
                out.append(f"{pfx}{name} | {_fmt_amount(amount)} | {status_nm} | {abc or '—'} | {_fmt_date(nc_date)}")
        out.append("")

    # ── 4. Критичні ───────────────────────────────────────────────────────
    critical = cards_by_status.get(CRITICAL_SID, [])
    out.append("### 🔥 КРИТИЧНІ\n")
    if not critical:
        out.append("Немає ✅\n")
    else:
        for c in critical:
            contact = c.get("contact") or {}
            name    = contact.get("full_name") or c.get("title") or f"#{c['id']}"
            amount  = int(c.get("products_total") or 0)
            nc_date = _parse_nc(c.get("communicate_at", ""))
            abc     = _get_cf(c, "LD_1036")
            out.append(f"{name} | {_fmt_amount(amount)} | НК: {_fmt_date(nc_date)} | {abc or '—'}")
        out.append("")

    return "\n".join(out)


# ── Briefing cache ─────────────────────────────────────────────────────────────

def _cache_path(d: date) -> Path:
    return SCRIPTS_DIR / f"briefing-{d.isoformat()}.txt"


def get_briefing_with_cache() -> str:
    """Return today's briefing from cache if available, otherwise fetch and cache it."""
    today     = datetime.now(timezone.utc).astimezone().date()
    cache     = _cache_path(today)
    yesterday = _cache_path(today - timedelta(days=1))

    # Clean up yesterday's cache file to avoid clutter
    if yesterday.exists():
        try:
            yesterday.unlink()
        except Exception:
            pass

    if cache.exists():
        return cache.read_text(encoding="utf-8")

    briefing = build_briefing()
    try:
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text(briefing, encoding="utf-8")
    except Exception:
        pass
    return briefing


# ── KB helpers ─────────────────────────────────────────────────────────────────

def slim_kb_index(content: str) -> str:
    """Reduce KB index table to 2 columns (Article + Summary) to save tokens."""
    lines  = content.splitlines()
    result = []
    in_table = False
    for line in lines:
        s = line.strip()
        if s.startswith("| Article") and "Summary" in s:
            result.append("| Article | Summary |")
            in_table = True
            continue
        if in_table and s.startswith("|---"):
            result.append("|---------|---------|")
            continue
        if in_table and s.startswith("|") and s.endswith("|"):
            cols = [c.strip() for c in s.split("|")[1:-1]]
            if len(cols) >= 2:
                result.append(f"| {cols[0]} | {cols[1]} |")
            continue
        if in_table and not s.startswith("|"):
            in_table = False
        result.append(line)
    return "\n".join(result)


def get_recent_log() -> str:
    """Read the most recent daily log (today or yesterday)."""
    today = datetime.now(timezone.utc).astimezone()
    for offset in range(2):
        d        = today - timedelta(days=offset)
        log_path = DAILY_DIR / f"{d.strftime('%Y-%m-%d')}.md"
        if log_path.exists():
            lines  = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            recent = lines[-MAX_LOG_LINES:] if len(lines) > MAX_LOG_LINES else lines
            return "\n".join(recent)
    return "(no recent daily log)"


# ── Daily note auto-creation ───────────────────────────────────────────────────

def _is_real_task(line: str) -> bool:
    s = line.strip()
    return s.startswith("- [ ]") and bool(s[5:].strip())


def _parse_prev_note(content: str) -> dict:
    """Extract unchecked tasks from previous day's note, grouped by section."""
    buckets: dict = {
        "велик": [], "крит": [], "нк": [],
        "надіслати": [], "перев": [],
        "внутр": [], "кп_doc": [], "фінанси": [],
        "на_завтра": [], "на_потім": [],
    }
    section = sub = None

    for raw in content.splitlines():
        line = raw.rstrip()
        s    = line.strip()

        if s.startswith("## "):
            h = s[3:]
            if   "ДЗВІНКИ"      in h: section, sub = "dzv", None
            elif "ПОВІДОМЛЕННЯ"  in h: section, sub = "msg", None
            elif "ЗАДАЧІ"        in h: section, sub = "tsk", None
            elif "НА ЗАВТРА"     in h: section, sub = "zav", None
            elif "НА ПОТІМ"      in h: section, sub = "pot", None
            else:                      section, sub = None, None
            continue

        if s.startswith("### ") and section:
            h = s[4:]
            if section == "dzv":
                if   "💰" in h:            sub = "велик"
                elif "🚨" in h:            sub = "крит"
                elif "🔔" in h:            sub = "нк"
            elif section == "msg":
                if   "Надіслати"  in h:    sub = "надіслати"
                elif "Перевірити" in h:    sub = "перев"
            elif section == "tsk":
                if   "Внутрішні"  in h:    sub = "внутр"
                elif "КП"         in h:    sub = "кп_doc"
                elif "Фінанси"    in h:    sub = "фінанси"
            continue

        if not _is_real_task(line):
            continue

        if   section == "zav":                          buckets["на_завтра"].append(line)
        elif section == "pot":                          buckets["на_потім"].append(line)
        elif section in ("dzv", "msg", "tsk") and sub: buckets[sub].append(line)

    return buckets


def _is_today_potim(task: str, today_ddmm: str) -> bool:
    m = re.search(r"- \[ \]\s+(\d{2}\.\d{2})", task)
    return bool(m) and m.group(1) == today_ddmm


def _blk(tasks: list, fallback: str = "- [ ] ") -> str:
    return "\n".join(tasks) if tasks else fallback


def create_daily_note_if_needed(briefing: str) -> None:
    """Auto-create today's Inbox daily note with carry-over tasks + briefing."""
    now       = datetime.now(timezone.utc).astimezone()
    today     = now.date()
    note_path = INBOX_DIR / f"{today.isoformat()}.md"

    if note_path.exists():
        return

    today_str  = today.strftime("%d.%m.%Y")
    day_name   = UA_DAYS.get(now.strftime("%A"), now.strftime("%A"))
    today_ddmm = today.strftime("%d.%m")

    buckets: dict = {}
    for offset in range(1, 5):
        prev = INBOX_DIR / f"{(today - timedelta(days=offset)).isoformat()}.md"
        if prev.exists():
            buckets = _parse_prev_note(prev.read_text(encoding="utf-8", errors="replace"))
            break

    na_zavtra_extra = [t for t in buckets.get("на_потім", []) if     _is_today_potim(t, today_ddmm)]
    na_potim_rest   = [t for t in buckets.get("на_потім", []) if not _is_today_potim(t, today_ddmm)]
    na_zavtra       = buckets.get("на_завтра", []) + na_zavtra_extra

    lines = [
        f"# 📅 {today_str} — {day_name}", "",
        "---", "",
        "## 🔥 Топ-5 на сьогодні", "",
        "1. 🚨 ", "2. 🚨 ", "3. ", "4. ", "5. ", "",
        "---", "",
        "## 📞 ДЗВІНКИ", "",
        "### 💰 Великий чек + критична готовність",
        _blk(buckets.get("велик",     [])), "",
        "### 🚨 Критичні (рішення зріле)",
        _blk(buckets.get("крит",      [])), "",
        "### 🔔 НК на сьогодні",
        _blk(buckets.get("нк",        [])), "",
        "---", "",
        "## 💬 ПОВІДОМЛЕННЯ (Вайбер)", "",
        "### 📤 Надіслати",
        _blk(buckets.get("надіслати", [])), "",
        "### 🔁 Перевірити відповідь",
        _blk(buckets.get("перев",     [])), "",
        "---", "",
        "## 📋 ЗАДАЧІ", "",
        "### 🔧 Внутрішні / підрядники",
        _blk(buckets.get("внутр",     [])), "",
        "### 📄 КП / договори / документи",
        _blk(buckets.get("кп_doc",    [])), "",
        "### 💰 Фінанси / Адмін",
        _blk(buckets.get("фінанси",   [])), "",
        "---", "",
        "## 🔄 НА ЗАВТРА", "",
        _blk(na_zavtra, "- [ ] \n- [ ] \n- [ ] "), "",
        "---", "",
        "## 📅 НА ПОТІМ (з датою)", "",
        _blk(na_potim_rest), "",
        "---", "",
        "## 📝 Нотатки за день", "",
        "---", "",
        "## 📊 Бриф воронки", "",
        briefing,
    ]

    try:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        note_path.write_text("\n".join(lines), encoding="utf-8")
    except Exception:
        pass


# ── Main context builder ───────────────────────────────────────────────────────

def build_context() -> str:
    parts = []

    # Today's date
    today = datetime.now(timezone.utc).astimezone()
    parts.append(f"## Today\n{today.strftime('%A, %B %d, %Y')}")

    # Daily briefing first — most time-sensitive, must not be truncated
    try:
        briefing = get_briefing_with_cache()
        if briefing:
            parts.append(f"## 📊 Бриф воронки\n\n{briefing}")
    except Exception:
        pass  # network down or API error — skip silently

    # Recent daily log
    parts.append(f"## Recent Daily Log\n\n{get_recent_log()}")

    # Knowledge base index (slim — 2 columns, lowest priority)
    if INDEX_FILE.exists():
        index_content = INDEX_FILE.read_text(encoding="utf-8", errors="replace")
        index_content = slim_kb_index(index_content)
        parts.append(f"## Knowledge Base Index\n\n{index_content}")
    else:
        parts.append("## Knowledge Base Index\n\n(empty - no articles compiled yet)")

    context = "\n\n---\n\n".join(parts)
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n\n...(truncated)"
    return context


def main():
    briefing = get_briefing_with_cache()
    create_daily_note_if_needed(briefing)
    context  = build_context()
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
