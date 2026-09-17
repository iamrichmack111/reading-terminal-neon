#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="${HOME}/Downloads/reading-terminal-neon"
SELF_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="reading-terminal-neon"
PARENT_PIN="${READING_PARENT_PIN:-4826}"
RELEASE_TAG="${READING_RELEASE_TAG:-v1.0.0}"

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
warn() { printf '\n\033[1;33mWARNING: %s\033[0m\n' "$*" >&2; }
fail() { printf '\n\033[1;31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

cleanup() {
  if [[ -n "${TTYD_PID:-}" ]]; then
    kill "$TTYD_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# If this script was launched from an extracted bundle with a different folder
# name, copy that bundle into the canonical project folder first.
if [[ "$SELF_DIR" != "$REPO_DIR" ]]; then
  say "Preparing $REPO_DIR"
  mkdir -p "$REPO_DIR"
  cp -a "$SELF_DIR"/. "$REPO_DIR"/
fi

cd "$REPO_DIR"
APP_FILE="$REPO_DIR/reading_terminal_neon.py"
[[ -f "$APP_FILE" ]] || fail "Missing $APP_FILE"
[[ -f tools/capture.py ]] || fail "Missing tools/capture.py"
[[ -f wiki/Home.md ]] || fail "Missing wiki pages"

command -v python3 >/dev/null 2>&1 || fail "python3 is not installed"
command -v git >/dev/null 2>&1 || fail "git is not installed"
command -v gh >/dev/null 2>&1 || fail "GitHub CLI (gh) is not installed"
gh auth status >/dev/null 2>&1 || fail "Run: gh auth login"

say "Installing local media dependencies"
sudo apt-get update
sudo apt-get install -y python3-venv ffmpeg ttyd

chmod +x reading_terminal_neon.py tools/capture.py
python3 -m py_compile reading_terminal_neon.py

say "Installing Playwright"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install -q --upgrade pip
python -m pip install -q playwright
python -m playwright install chromium

say "Preparing isolated demo profile"
rm -rf .demo-home media/video
mkdir -p .demo-home media/screenshots media/video

# Avoid stale local ttyd servers from earlier attempts.
pkill -x ttyd 2>/dev/null || true
sleep 1

PORT=""
for p in $(seq 7681 7699); do
  if ! ss -ltn 2>/dev/null | awk '{print $4}' | grep -Eq ":${p}$"; then
    PORT="$p"
    break
  fi
done
[[ -n "$PORT" ]] || fail "No free demo port found"

say "Starting the real terminal app on local demo port $PORT"
HOME="$REPO_DIR/.demo-home" ttyd -p "$PORT" bash -lc \
  "HOME='$REPO_DIR/.demo-home' READING_PARENT_PIN='$PARENT_PIN' python3 '$APP_FILE'" \
  >/tmp/reading-terminal-ttyd.log 2>&1 &
TTYD_PID=$!
sleep 4
if ! kill -0 "$TTYD_PID" 2>/dev/null; then
  cat /tmp/reading-terminal-ttyd.log || true
  fail "ttyd failed to start"
fi

say "Capturing screenshots and Playwright demo video"
export READING_DEMO_URL="http://127.0.0.1:${PORT}"
RAW_VIDEO="$(python tools/capture.py | tail -n 1)"
[[ -f "$RAW_VIDEO" ]] || fail "Playwright did not create a video"

ffmpeg -y -loglevel error \
  -i "$RAW_VIDEO" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  media/reading-terminal-demo.mp4
[[ -s media/reading-terminal-demo.mp4 ]] || fail "Demo MP4 was not created"

kill "$TTYD_PID" 2>/dev/null || true
TTYD_PID=""

GH_USER="$(gh api user -q .login)"
REPO_SLUG="${GH_USER}/${REPO_NAME}"

say "Writing badge-rich README"
cat > README.md <<EOF
# Reading Terminal Neon

[![CI](https://github.com/${REPO_SLUG}/actions/workflows/ci.yml/badge.svg)](https://github.com/${REPO_SLUG}/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Terminal](https://img.shields.io/badge/UI-Terminal-111827?logo=gnometerminal&logoColor=white)
![Playwright](https://img.shields.io/badge/Demo-Playwright-2EAD33?logo=playwright&logoColor=white)
![Linux](https://img.shields.io/badge/Platform-Linux-FCC624?logo=linux&logoColor=111)
[![Release](https://img.shields.io/github/v/release/${REPO_SLUG})](https://github.com/${REPO_SLUG}/releases)
[![Last Commit](https://img.shields.io/github/last-commit/${REPO_SLUG})](https://github.com/${REPO_SLUG}/commits/main)
[![Wiki](https://img.shields.io/badge/docs-wiki-7C3AED)](https://github.com/${REPO_SLUG}/wiki)

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

\`\`\`bash
chmod +x reading_terminal_neon.py
READING_PARENT_PIN=4826 ./reading_terminal_neon.py
\`\`\`

## Regenerate screenshots + demo

\`\`\`bash
./build_reading_terminal_repo.sh
\`\`\`

## Documentation

The repository includes full Wiki source under [\`wiki/\`](wiki/). After the GitHub Wiki is initialized, the build script publishes those pages to the repository Wiki.
EOF

say "Preparing Git repository"
if [[ ! -d .git ]]; then git init; fi
git branch -M main
git config user.name >/dev/null 2>&1 || git config user.name "$GH_USER"
git config user.email >/dev/null 2>&1 || git config user.email "${GH_USER}@users.noreply.github.com"

git add reading_terminal_neon.py README.md .gitignore tools wiki .github media/screenshots media/reading-terminal-demo.mp4 build_reading_terminal_repo.sh
git commit -m "feat: portfolio release with badges wiki and Playwright demo" || true

say "Creating or updating GitHub repository"
if gh repo view "$REPO_SLUG" >/dev/null 2>&1; then
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "git@github.com:${REPO_SLUG}.git"
  else
    git remote add origin "git@github.com:${REPO_SLUG}.git"
  fi
  git push -u origin main
else
  gh repo create "$REPO_NAME" \
    --public \
    --source=. \
    --remote=origin \
    --description "Colorful terminal reading practice for young readers" \
    --push
fi

say "Adding GitHub topics"
gh repo edit "$REPO_SLUG" \
  --add-topic python \
  --add-topic terminal \
  --add-topic education \
  --add-topic reading \
  --add-topic kids \
  --add-topic homeschool \
  --add-topic playwright \
  --add-topic learning-app \
  --enable-wiki

say "Creating Git tag and release"
if ! git rev-parse "$RELEASE_TAG" >/dev/null 2>&1; then
  git tag -a "$RELEASE_TAG" -m "Reading Terminal Neon $RELEASE_TAG"
fi
if ! git ls-remote --tags origin "refs/tags/$RELEASE_TAG" | grep -q .; then
  git push origin "$RELEASE_TAG"
fi
if ! gh release view "$RELEASE_TAG" --repo "$REPO_SLUG" >/dev/null 2>&1; then
  gh release create "$RELEASE_TAG" \
    --repo "$REPO_SLUG" \
    --title "Reading Terminal Neon $RELEASE_TAG" \
    --notes "Terminal reading practice release with Playwright screenshots, demo video, badges, CI, progress tracking, and Wiki documentation." \
    media/reading-terminal-demo.mp4
fi

say "Publishing Wiki pages"
rm -rf .wiki-publish
mkdir .wiki-publish
cp wiki/*.md .wiki-publish/
(
  cd .wiki-publish
  git init -b master >/dev/null
  git config user.name "$GH_USER"
  git config user.email "${GH_USER}@users.noreply.github.com"
  git add .
  git commit -m "docs: publish Reading Terminal Neon wiki" >/dev/null
  git remote add origin "git@github.com:${REPO_SLUG}.wiki.git"
  if git push -u origin master --force; then
    echo "Wiki published: https://github.com/${REPO_SLUG}/wiki"
  else
    echo
    echo "Wiki source is ready in $REPO_DIR/wiki"
    echo "GitHub may require the first Wiki page to be created once in the Wiki tab."
    echo "After creating that first page, rerun this script and all Wiki pages will publish automatically."
  fi
)
rm -rf .wiki-publish

say "DONE"
echo "Repo:    https://github.com/${REPO_SLUG}"
echo "Wiki:    https://github.com/${REPO_SLUG}/wiki"
echo "Release: https://github.com/${REPO_SLUG}/releases/tag/${RELEASE_TAG}"
echo "Demo:    $REPO_DIR/media/reading-terminal-demo.mp4"
echo "Shots:   $REPO_DIR/media/screenshots"
