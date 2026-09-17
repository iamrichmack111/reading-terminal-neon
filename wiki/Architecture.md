# Architecture

Reading Terminal Neon is intentionally lightweight.

## Application

- Python 3
- ANSI / 256-color terminal output
- JSON progress persistence
- No browser required for normal use
- No GUI toolkit required

## Portfolio capture

The project uses a separate local media pipeline:

1. `ttyd` exposes the real terminal application locally.
2. Playwright opens the local terminal session in Chromium.
3. Playwright captures PNG screenshots and records WebM video.
4. FFmpeg converts the recording to an MP4 demo.

The browser is only used to document the terminal app; the learning application itself remains terminal based.
