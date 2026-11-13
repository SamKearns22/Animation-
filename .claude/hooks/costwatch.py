#!/usr/bin/env python3
"""Cost watch: warns Claude (and Sam) when a chat gets expensive. Rulebook rule 85.

MAP
  prices/limits ..... PRICE, WEEK_USD, CTX_AMBER/RED, CHAT_AMBER/RED, GAP_MIN
  read_usage() ...... sums this chat's cost from the transcript (cached by byte offset), and its helpers'
                      (helper_files: the records beside the chat's own); Fable has its own price row
  level() ........... green / amber / red from history size and chat cost
  main() ............ hook entry (UserPromptSubmit, PostToolUse); --report for handovers

Runs as a Claude Code hook. Every step re-reads the whole chat, so cost per step grows
with the chat's history; after an hour idle the whole history is loaded again at the
dearer write price. Prices are list $ per million tokens, fitted to this account's
own chat records (Nov 2026); WEEK_USD is a week's allowance at list price, set on 13 Nov (Job O) so Blessed's recorded dollars (about
$137: $101 from the app, $36 estimated for 11 Nov chats the app cannot show) read 80% of a week, as Sam saw it (was 290). Both are estimates: good to about +-20%.
"""
import glob, json, os, sys, time
from datetime import datetime

PRICE = {  # read, write(1h cache), input, output
    "fable":  (0.18, 16.0, 10.0, 50.0),  # list price: twice Opus, the same to re-read (11 Nov)
    "opus":   (0.18, 8.0, 5.0, 25.0),
    "sonnet": (0.10, 4.0, 3.0, 15.0),
    "haiku":  (0.03, 1.3, 1.0, 5.0),
}
WEEK_USD = 171.0
FRESH = 90_000           # tokens a fresh chat starts with (rules, notes, tools)
CTX_AMBER, CTX_RED = 200_000, 300_000
CHAT_AMBER, CHAT_RED = 3.0, 5.0   # % of the week spent by this one chat
GAP_MIN = 55             # cache lasts an hour; after that the history reloads
LEVELS = ["green", "amber", "red"]
STATE_DIR = os.path.expanduser("~/.claude/costwatch")


def fam(model):
    m = (model or "").lower()
    return ("sonnet" if "sonnet" in m else "haiku" if "haiku" in m else
            "fable" if "fable" in m or "mythos" in m else "opus")


def helper_files(path):
    """A chat's helpers (critique and other agents) keep their own records beside it; rule 85 counts them."""
    return sorted(glob.glob(os.path.join(os.path.splitext(path)[0], "**", "*.jsonl"), recursive=True))


def read_usage(path, helper_of=None):
    """Running totals for the transcript, re-reading only the new bytes. A chat's total takes in its helpers'
    (st["helpers_usd"]); a helper's own state is saved here, the chat's by main()."""
    os.makedirs(STATE_DIR, exist_ok=True)
    name = (os.path.basename(helper_of)[:8] + "-" if helper_of else "") + os.path.basename(path)
    sp = os.path.join(STATE_DIR, name + ".json")
    st = {"offset": 0, "usd": 0.0, "ctx": 0, "last_ts": None, "seen": [], "said": "green",
          "model": ""}
    try:
        st.update(json.load(open(sp)))
    except Exception:
        pass
    seen = set(st["seen"])
    with open(path, "rb") as f:
        f.seek(st["offset"])
        for raw in f:
            if not raw.endswith(b"\n"):
                break  # half-written line: read it next time
            st["offset"] += len(raw)
            try:
                d = json.loads(raw)
            except Exception:
                continue
            m = d.get("message")
            if d.get("type") != "assistant" or not isinstance(m, dict) or not m.get("usage"):
                continue
            mid = m.get("id")
            if mid in seen:
                continue  # one reply is written as several lines with the same usage
            seen.add(mid)
            u = m["usage"]
            r, w, i, o = PRICE[fam(m.get("model"))]
            rd, wr = u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0)
            st["usd"] += (rd * r + wr * w + u.get("input_tokens", 0) * i
                          + u.get("output_tokens", 0) * o) / 1e6
            if not d.get("isSidechain"):
                st["ctx"] = rd + wr + u.get("input_tokens", 0)
                st["last_ts"] = d.get("timestamp")
                st["model"] = m.get("model", "")
    st["seen"] = list(seen)[-3000:]
    if helper_of:
        json.dump(st, open(sp, "w"))
    else:
        st["helpers_usd"] = 0.0
        for h in helper_files(path):
            try:
                st["helpers_usd"] += read_usage(h, helper_of=path)[0]["usd"]
            except Exception:
                pass  # a helper record that cannot be read never breaks the chat
    return st, sp


def level(st):
    pct = 100 * (st["usd"] + st.get("helpers_usd", 0.0)) / WEEK_USD
    lv = 0
    if st["ctx"] >= CTX_AMBER or pct >= CHAT_AMBER:
        lv = 1
    if st["ctx"] >= CTX_RED or pct >= CHAT_RED:
        lv = 2
    return lv, pct


def describe(st, pct):
    words = int(st["ctx"] * 0.75)
    times = max(1.0, st["ctx"] / FRESH)
    extra = ""
    if st.get("helpers_usd"):
        extra = f" ({100 * st['helpers_usd'] / WEEK_USD:.1f} of it its helpers)"
    return (f"this chat has cost about {pct:.1f}% of the week{extra}; its history is about "
            f"{words // 1000}k words, so every step costs about {times:.1f}x a fresh chat's")


def main():
    if "--report" in sys.argv:
        path = sys.argv[sys.argv.index("--report") + 1] if len(sys.argv) > 2 else None
        if not path:
            d = os.path.expanduser("~/.claude/projects")
            files = [os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs if f.endswith(".jsonl")]
            path = max(files, key=os.path.getmtime)
        st, _ = read_usage(path)
        lv, pct = level(st)
        print(f"{LEVELS[lv].upper()}: {describe(st, pct)}.")
        return
    try:
        inp = json.load(sys.stdin)
        path = inp["transcript_path"]
        event = inp.get("hook_event_name", "")
        st, sp = read_usage(path)
    except Exception:
        return  # never break a chat over the cost watch
    lv, pct = level(st)
    said = LEVELS.index(st.get("said", "green"))
    msgs = []

    if event == "UserPromptSubmit":
        prompt = (inp.get("prompt") or "").strip().lower()
        gap = None
        if st["last_ts"]:
            t = datetime.fromisoformat(st["last_ts"].replace("Z", "+00:00")).timestamp()
            gap = (time.time() - t) / 60
        if gap and gap >= GAP_MIN and st["ctx"] >= 120_000:
            r, w, _, _ = PRICE[fam(st["model"])]
            reload_pct = 100 * st["ctx"] * w / 1e6 / WEEK_USD
            msgs.append(f"COST WATCH: Sam came back after {gap / 60:.1f} h, so this reply reloads the "
                        f"whole chat: about {reload_pct:.1f}% of the week before any work. Tell Sam in "
                        "the first line, and say that after a gap of over an hour a new chat from the "
                        "handover is cheaper.")
        if lv == 2 and not prompt.startswith("override"):
            msgs.append(f"COST WATCH RED: {describe(st, pct)}. Do not start new work. Write the handover "
                        "now (CLAUDE.md, Models and chats) and give Sam the 3 lines. The first line of "
                        "your reply: 'Cost: red. New chat needed.' Sam can type 'override' to go on.")
        elif lv == 2:
            msgs.append(f"COST WATCH RED (Sam said override): {describe(st, pct)}. Do only what Sam asked, "
                        "then hand over.")
        elif lv == 1:
            msgs.append(f"COST WATCH AMBER: {describe(st, pct)}. Finish the step in hand, then hand over; "
                        "start no new round of notes or new build here. Put a 'Cost: amber' line in your reply.")
    elif lv > said:  # PostToolUse: speak only when the level goes up
        if lv == 2:
            msgs.append(f"COST WATCH RED: {describe(st, pct)}. Finish the command in hand, save, then write "
                        "the handover and stop; tell Sam 'Cost: red. New chat needed.'")
        else:
            msgs.append(f"COST WATCH AMBER: {describe(st, pct)}. Finish the step in hand, then hand over.")

    st["said"] = LEVELS[max(lv, said if event != "UserPromptSubmit" else lv)]
    json.dump(st, open(sp, "w"))
    if msgs:
        text = " ".join(msgs)
        print(json.dumps({"systemMessage": text,
                          "hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))


if __name__ == "__main__":
    main()
