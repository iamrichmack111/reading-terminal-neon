# Reading Terminal Neon

[![CI](https://github.com/iamrichmack111/reading-terminal-neon/actions/workflows/ci.yml/badge.svg)](https://github.com/iamrichmack111/reading-terminal-neon/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Terminal](https://img.shields.io/badge/UI-Terminal-111827?logo=gnometerminal&logoColor=white)
![Playwright](https://img.shields.io/badge/Demo-Playwright-2EAD33?logo=playwright&logoColor=white)
![Linux](https://img.shields.io/badge/Platform-Linux-FCC624?logo=linux&logoColor=111)
[![Release](https://img.shields.io/github/v/release/iamrichmack111/reading-terminal-neon)](https://github.com/iamrichmack111/reading-terminal-neon/releases)
[![Last Commit](https://img.shields.io/github/last-commit/iamrichmack111/reading-terminal-neon)](https://github.com/iamrichmack111/reading-terminal-neon/commits/main)
[![Wiki](https://img.shields.io/badge/docs-wiki-7C3AED)](https://github.com/iamrichmack111/reading-terminal-neon/wiki)

A colorful terminal-based reading and typing practice app designed for young readers.

## Highlights

- Simple terminal-first interface
- Read-only activities advance with **Enter**
- Easy sentences for early readers
- Child typing does not require punctuation or capitalization where appropriate
- Multiple lesson choices
- Resume unfinished sessions
- Stars, skill mastery, and progress tracking
- End-of-session report card
- Parent controls
- Playwright screenshots and demo video
- GitHub Wiki source included

## Screenshots

### Main Menu
![Main Menu](media/screenshots/01-main-menu.png)

### Progress Dashboard
![Progress](media/screenshots/02-progress.png)

### Reading Plan
![Reading Plan](media/screenshots/03-reading-plan.png)

### Sight Word
![Sight Word](media/screenshots/04-sight-word.png)

### Read a Sentence
![Read Sentence](media/screenshots/05-read-sentence.png)

## Demo Video

▶️ [Watch the Playwright-recorded demo](media/reading-terminal-demo.mp4)

## Run

```bash
chmod +x reading_terminal_neon.py
READING_PARENT_PIN=4826 ./reading_terminal_neon.py
```

## Regenerate screenshots + demo

```bash
./build_reading_terminal_repo.sh
```

## Documentation

The repository includes full Wiki source under [`wiki/`](wiki/). After the GitHub Wiki is initialized, the build script publishes those pages to the repository Wiki.
