# Development

## Validate Python

```bash
python3 -m py_compile reading_terminal_neon.py
```

## Regenerate Playwright media

The normal build script starts an isolated demo session so screenshots do not overwrite or depend on the child's real progress data.

```bash
./build_reading_terminal_repo.sh
```

## Repository automation

The build script can:

- generate screenshots
- generate the Playwright demo video
- create/update the README badges
- push the repository
- add GitHub topics
- create a Git tag / release
- enable the GitHub Wiki
- publish the included wiki pages once the GitHub Wiki has been initialized
