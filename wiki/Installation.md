# Installation

## Requirements

- Linux terminal
- Python 3

## Run the application

```bash
chmod +x reading_terminal_neon.py
READING_PARENT_PIN=4826 ./reading_terminal_neon.py
```

Progress is stored under the current user's home directory in `.reading_terminal/`.

## Build portfolio media

The included build script installs the local tools needed for screenshots and video, starts the terminal app through `ttyd`, then uses Playwright to capture the real terminal interface.

```bash
chmod +x build_reading_terminal_repo.sh
./build_reading_terminal_repo.sh
```
