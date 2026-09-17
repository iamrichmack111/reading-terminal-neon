# Media and Demo

The project includes automated portfolio capture with Playwright.

## Generated screenshots

- Main menu
- Progress dashboard
- Reading lesson plan
- Sight-word activity
- Sentence-reading activity

## Demo video

`tools/capture.py` records the actual terminal UI through `ttyd`. The build script converts the Playwright WebM recording to:

```text
media/reading-terminal-demo.mp4
```

To regenerate the media, run:

```bash
./build_reading_terminal_repo.sh
```
