# Italiano offline

John's Italian flashcards as a home-screen app that works with no internet.

Open https://johnnutt22.github.io/italian-cards/ in Safari, tap Share, then Add to Home Screen.
Scores stay on the phone. Tap "Copy results for Claude" when back online and paste them in the Learning Italian chat.

## Updating the app (for Claude)

1. Read the live "My Italian words" page source (the claude.ai artifact) and save it as a file.
2. Save each database doc as `SEED/<collection>/<doc>.json` (progress/current, progress/sort, flash/stats, flash/focus, flash/later, flash/examples, time/stats, practice/stats, check/stats).
3. Run `python3 rebuild.py PAGE.html SEED` here. It keeps the offline parts from the current `index.html`, bumps the cache version and writes a fresh `data.json`.
4. Test offline, commit and push. The phone picks up the new version on its second open while online.
