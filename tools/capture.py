#!/usr/bin/env python3
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "media" / "screenshots"
VIDEOS = ROOT / "media" / "video"
URL = os.environ.get("READING_DEMO_URL", "http://127.0.0.1:7681")
SHOTS.mkdir(parents=True, exist_ok=True)
VIDEOS.mkdir(parents=True, exist_ok=True)


def snap(page, name):
    page.wait_for_timeout(600)
    page.screenshot(path=str(SHOTS / name), full_page=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir=str(VIDEOS),
        record_video_size={"width": 1280, "height": 800},
    )
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2600)
    snap(page, "01-main-menu.png")

    # Progress dashboard -> back to menu.
    page.keyboard.type("7")
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    snap(page, "02-progress.png")
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)

    # Reading lesson overview.
    page.keyboard.type("2")
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    snap(page, "03-reading-plan.png")

    # Start lesson, capture the first sight-word screen.
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    snap(page, "04-sight-word.png")

    # Read five sight words.
    for _ in range(5):
        page.keyboard.press("Enter")
        page.wait_for_timeout(450)

    # Move to next activity and capture sentence-reading screen.
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    snap(page, "05-read-sentence.png")

    # Let the recording linger on the actual terminal UI.
    page.wait_for_timeout(3200)
    video = page.video
    ctx.close()
    video_path = Path(video.path())
    browser.close()

print(video_path)
