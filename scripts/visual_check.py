"""End-to-end smoke test of the app in headless Chromium — WITHOUT touching
live Firestore.

Copies every git-tracked file into a temp directory, switches that copy's
storage.js to LocalStorageAdapter (and asserts the switch took), serves it on
a free localhost port, and drives it with Playwright at a 375x667 (iPhone SE)
viewport. Any request to Firestore is aborted and fails the run, as does any
uncaught page error or console error. The working tree is never modified.

Scenarios: full regular game -> results -> all three leaderboard modes; kill
(reload) mid-game and resume; the phone Back button mid-game opening the exit
sheet; "Start new" committing a leftover checkpoint; kill and resume a daily,
finish it, and open the daily review; the update-available toast.

Screenshots land in --out (default: a fresh temp dir, printed at the end).
LOOK at them (Read tool) — a clean exit code doesn't prove the layout is right.

Usage (from project root):
    python scripts/visual_check.py [--out DIR] [--headed]
Requires: pip install playwright && python -m playwright install chromium
"""
import argparse
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")  # labels can include ✓ etc.; Windows' cp1252 console can't encode them
ROOT = Path(__file__).resolve().parent.parent
FIREBASE_LINE = "const storage = new FirebaseAdapter();"
LOCAL_LINE = "const storage = new LocalStorageAdapter();"
SETTLE_MS = 450  # circle-wipe screen transition is 0.35s


def copy_site(dest: Path) -> None:
    files = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    for rel in filter(None, files.decode("utf-8").split("\0")):
        src = ROOT / rel
        if not src.is_file():
            continue  # deleted in the working tree but not yet committed
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest / rel)
    # Pick up new, not-yet-committed files too (e.g. a new script the page loads).
    untracked = subprocess.run(["git", "ls-files", "-z", "--others", "--exclude-standard"],
                               cwd=ROOT, capture_output=True, check=True).stdout
    for rel in filter(None, untracked.decode("utf-8").split("\0")):
        if (ROOT / rel).is_file():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest / rel)
    storage = dest / "storage.js"
    text = storage.read_text(encoding="utf-8")
    text = text.replace(FIREBASE_LINE, LOCAL_LINE)
    if FIREBASE_LINE in text or "new FirebaseAdapter()" in text or LOCAL_LINE not in text:
        sys.exit("ABORT: could not switch the test copy of storage.js to LocalStorageAdapter")
    storage.write_text(text, encoding="utf-8")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Check:
    def __init__(self, page, out: Path):
        self.page, self.out, self.failures, self.n = page, out, [], 0

    def ok(self, cond, label):
        print(("  PASS  " if cond else "  FAIL  ") + label)
        if not cond:
            self.failures.append(label)

    def shot(self, name):
        self.page.wait_for_timeout(SETTLE_MS)
        self.n += 1
        self.page.screenshot(path=str(self.out / f"{self.n:02d}-{name}.png"))

    def visible(self, sel):
        return self.page.is_visible(sel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    site = Path(tempfile.mkdtemp(prefix="disney-visual-site-"))
    out = args.out or Path(tempfile.mkdtemp(prefix="disney-visual-out-"))
    out.mkdir(parents=True, exist_ok=True)
    copy_site(site)
    port = free_port()
    base = f"http://127.0.0.1:{port}/index.html"
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                              cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    firestore_hits, errors = [], []
    try:
        time.sleep(1.0)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not args.headed)
            ctx = browser.new_context(viewport={"width": 375, "height": 667})

            def guard(route):
                firestore_hits.append(route.request.url)
                route.abort()
            ctx.route("**/firestore.googleapis.com/**", guard)
            page = ctx.new_page()
            page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
            page.on("console", lambda m: m.type == "error" and "fonts.g" not in (m.location or {}).get("url", "")
                    and errors.append(f"console: {m.text}"))
            c = Check(page, out)

            def boot():
                page.wait_for_selector("#screen-home:not(.hidden) .user-card", timeout=20000)
                page.wait_for_timeout(SETTLE_MS)

            def pick_player(name):
                page.locator(".user-card", has_text=name).first.click()
                page.wait_for_selector("#screen-settings:not(.hidden)")

            def answer(n):
                for _ in range(n):
                    page.click("#answers-grid .answer-btn >> nth=0")
                    page.click("#btn-next")

            def progress_text():
                return page.inner_text("#game-progress")

            def answered(user):  # LocalStorageAdapter's committed totalAnswered
                return page.evaluate(f"JSON.parse(localStorage.getItem('disney_trivia_v1')).users.{user}.totalAnswered || 0")

            def checkpoint(user):
                return page.evaluate(f"localStorage.getItem('disney_game_progress_{user}')")

            print("Regular game")
            page.goto(base)
            boot()
            c.shot("home")
            pick_player("Kristen")
            c.ok(not c.visible("#confirm-overlay"), "no resume prompt with no checkpoint")
            c.shot("settings")
            page.click("#btn-start-game")
            page.wait_for_selector("#screen-game:not(.hidden)")
            c.shot("game")
            page.click("#answers-grid .answer-btn >> nth=0")
            c.shot("game-answered")
            page.click("#btn-next")
            answer(9)
            page.wait_for_selector("#screen-results:not(.hidden)")
            c.ok(True, "finished a 10-question game")
            c.shot("results")
            c.ok(checkpoint("kristen") is None, "checkpoint cleared after a saved game")
            c.ok(answered("kristen") == 10, "finished game committed exactly 10 answers")

            print("Leaderboard")
            page.click("#btn-results-leaderboard")
            page.wait_for_selector("#screen-leaderboard:not(.hidden)")
            for mode in ["lifetime", "month", "lastmonth"]:
                page.click(f'#lb-mode-group .pill[data-mode="{mode}"]')
                page.wait_for_timeout(200)
                c.ok(page.locator("#leaderboard-list > *").count() > 0 or c.visible("#leaderboard-empty"),
                     f"leaderboard renders ({mode})")
                c.shot(f"leaderboard-{mode}")
            page.go_back()
            page.wait_for_selector("#screen-home:not(.hidden)")
            c.ok(True, "Back from leaderboard returns home")

            print("Kill mid-game and resume")
            pick_player("Kristen")
            page.click("#btn-start-game")
            page.wait_for_selector("#screen-game:not(.hidden)")
            answer(2)
            c.ok(progress_text().startswith("Q 3 "), "on Q3 before reload")
            score_before = page.inner_text("#game-score-display")
            page.reload()
            boot()
            page.wait_for_timeout(300)
            c.ok(page.evaluate("(history.state && history.state.depth) || 0") == 0,
                 "reload from a depth-1 screen collapses history back to home")
            pick_player("Kristen")
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            c.ok("2 of 10" in page.inner_text("#confirm-message"), "resume prompt shows 2 of 10")
            c.shot("resume-prompt")
            page.click("#confirm-ok")
            page.wait_for_selector("#screen-game:not(.hidden)")
            c.ok(progress_text().startswith("Q 3 "), "resumed at Q3")
            c.ok(page.inner_text("#game-score-display") == score_before, f"score restored ({score_before})")

            print("Back button mid-game")
            page.go_back()
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            c.ok("Leave this game" in page.inner_text("#confirm-title"), "Back mid-game opens the exit sheet")
            c.shot("exit-sheet")
            page.click("#confirm-cancel")
            page.wait_for_timeout(200)
            c.ok(c.visible("#screen-game") and not c.visible("#confirm-overlay"), "Keep playing stays in the game")
            page.go_back()
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
            c.ok(c.visible("#screen-game"), "Escape dismisses the exit sheet")
            before = answered("kristen")
            page.click("#btn-exit-game")
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            page.click("#confirm-ok")
            page.wait_for_selector("#screen-home:not(.hidden)")
            c.ok(checkpoint("kristen") is None, "Exit commits and clears the checkpoint")
            c.ok(answered("kristen") == before + 2, "Exit after 2 answers commits exactly 2")

            print("Start new with a leftover checkpoint")
            pick_player("Kristen")
            page.click("#btn-start-game")
            page.wait_for_selector("#screen-game:not(.hidden)")
            answer(1)
            page.reload()
            boot()
            pick_player("Kristen")
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            page.click("#confirm-cancel")  # "Not now"
            page.wait_for_timeout(200)
            c.ok(checkpoint("kristen") is not None, "'Not now' keeps the checkpoint")
            before = answered("kristen")
            page.click("#btn-start-game")
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            c.ok(page.inner_text("#confirm-cancel") == "Start new", "starting a game offers 'Start new'")
            page.click("#confirm-cancel")
            page.wait_for_selector("#screen-game:not(.hidden)")
            c.ok(progress_text().startswith("Q 1 "), "'Start new' starts a fresh game")
            c.ok(answered("kristen") == before + 1, "'Start new' commits the 1 leftover answer exactly once")
            page.click("#btn-exit-game")
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            page.click("#confirm-ok")
            page.wait_for_selector("#screen-home:not(.hidden)")
            c.ok(answered("kristen") == before + 1, "exiting with 0 answers commits nothing")

            print("Failed save is kept and offered again")
            pick_player("Kristen")
            page.click("#btn-start-game")
            page.wait_for_selector("#screen-game:not(.hidden)")
            answer(9)
            before = answered("kristen")
            page.evaluate("() => { storage.updateStats = () => Promise.reject(new Error('offline')); }")
            answer(1)
            page.wait_for_selector("#screen-results:not(.hidden)")
            c.ok(c.visible("#save-warning"), "results show the save warning")
            c.shot("results-save-failed")
            c.ok(checkpoint("kristen") is not None, "failed save keeps the checkpoint")
            c.ok(answered("kristen") == before, "failed save committed nothing")
            page.reload()  # restores the real updateStats
            boot()
            pick_player("Kristen")
            page.wait_for_selector("#confirm-overlay:not(.hidden)")
            c.ok(page.inner_text("#confirm-title") == "Unsaved game", "player is offered the unsaved game")
            c.shot("unsaved-game-prompt")
            page.click("#confirm-ok")
            page.wait_for_selector("#screen-results:not(.hidden)")
            c.ok(not c.visible("#save-warning"), "'Save it' saves without a warning")
            c.ok(answered("kristen") == before + 10, "'Save it' commits exactly 10")
            c.ok(checkpoint("kristen") is None, "checkpoint cleared after 'Save it'")
            page.click("#btn-results-home")
            page.wait_for_selector("#screen-home:not(.hidden)")

            print("Daily: kill, resume, finish, review")
            pick_player("Cara")
            page.click("#btn-daily-challenge")
            page.wait_for_selector("#screen-game:not(.hidden)")
            answer(3)
            page.reload()
            boot()
            pick_player("Cara")
            c.ok("3/10" in page.inner_text("#btn-daily-challenge"), "settings shows Resume Daily (3/10)")
            c.shot("daily-resume-button")
            page.click("#btn-daily-challenge")
            page.wait_for_selector("#screen-game:not(.hidden)")
            c.ok(progress_text().startswith("Q 4 of 10"), "daily resumed at Q4")
            answer(6)
            # The post-save refresh failing (flaky wifi) must not report a failed
            # save, and must not leave the finished daily replayable.
            page.evaluate("() => { window._realGetUsers = storage.getUsers; storage.getUsers = () => Promise.reject(new Error('timeout')); }")
            answer(1)
            page.wait_for_selector("#screen-results:not(.hidden)")
            c.ok(not c.visible("#save-warning"), "refresh timeout after a landed save shows no warning")
            c.ok(answered("cara") == 10, "daily committed exactly 10")
            c.shot("daily-results")
            page.click("#btn-play-again")
            page.wait_for_selector("#screen-settings:not(.hidden)")
            c.ok("Review" in page.inner_text("#btn-daily-challenge"), "finished daily is replay-blocked despite the refresh timeout")
            page.evaluate("() => { storage.getUsers = window._realGetUsers; }")
            page.click("#btn-daily-challenge")
            page.wait_for_selector("#screen-daily-review:not(.hidden)")
            page.wait_for_timeout(500)
            c.ok(page.locator("#daily-review-list > *").count() >= 10, "daily review lists the 10 questions")
            c.shot("daily-review")
            page.go_back()
            page.wait_for_selector("#screen-settings:not(.hidden)")
            c.ok(True, "Back from daily review returns to settings")

            print("Update toast")
            page.click("#btn-settings-back")
            page.wait_for_selector("#screen-home:not(.hidden)")
            idx = site / "index.html"
            orig = idx.read_text(encoding="utf-8")
            try:
                idx.write_text(orig.replace("app.js?v=", "app.js?v=999-"), encoding="utf-8")
                page.evaluate("_lastUpdateCheck = 0; checkForUpdate()")
                page.wait_for_selector("#update-toast:not(.hidden)", timeout=5000)
                c.ok(True, "update toast appears for a new build")
                c.shot("update-toast")
            finally:
                idx.write_text(orig, encoding="utf-8")

            browser.close()
    finally:
        server.terminate()
        shutil.rmtree(site, ignore_errors=True)

    print()
    c.ok(not firestore_hits, f"no Firestore requests ({len(firestore_hits)} blocked)")
    c.ok(not errors, "no page/console errors" + ("".join("\n        " + e for e in errors[:10]) if errors else ""))
    print(f"\nScreenshots: {out}")
    if c.failures:
        print(f"{len(c.failures)} check(s) FAILED")
        return 1
    print("All checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
