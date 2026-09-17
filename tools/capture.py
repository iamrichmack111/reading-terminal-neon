from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "media" / "screenshots"
VIDEOS = ROOT / "media" / "video"
URL = os.environ.get("READING_DEMO_URL", "http://127.0.0.1:7681")

SHOTS.mkdir(parents=True, exist_ok=True)
VIDEOS.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir=str(VIDEOS),
        record_video_size={"width": 1280, "height": 800},
    )

    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    page.screenshot(path=str(SHOTS / "01-main-menu.png"))

    # Choose Reading.
    page.keyboard.type("2")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    page.screenshot(path=str(SHOTS / "02-reading.png"))

    # Reading-only screens advance with Enter.
    page.keyboard.press("Enter")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "03-activity.png"))

    page.keyboard.press("Enter")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "04-next-step.png"))

    page.wait_for_timeout(3500)
    video = page.video
    ctx.close()
    video_path = Path(video.path())
    browser.close()

print(video_path)
