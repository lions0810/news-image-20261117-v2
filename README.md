# One Day in the World — 17 November 2026 (V2: the broadside)

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/lions0810/news-image-20261117-v2/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/lions0810/news-image-20261117-v2/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

An entry for the make.fun bounty
[news-image-20261117](https://make.fun/bounty/news-image-20261117): one
1024×1024 image summing up the world news of Tuesday, 17 November 2026.

V1 of this entry carried six stories and ranked mid-field; the leaders
carry dozens. V2 is a dense broadsheet front page with **26 stories**: the
same four illustrated leads (Crimea bridge barrage, Iran–Bahrain/Hormuz,
the Xi–Trump–Putin Shenzhen summit, the failed Vulcan launch), 18 text
briefs spanning markets, migration, climate, health, technology and four
continents, and a four-item ticker (the U.S. losing measles-free status,
the Pope's rosary forgiveness in Peru, Robert Pattinson named as the new
James Bond, and Jay Shah re-elected ICC chairman).

## How it works

- `compose.py` renders the page with PIL: the four illustration panels
  (text-free AI illustrations, in `panels/`) are centre-cropped into the
  lead row, and every word on the page — masthead, captions, briefs,
  ticker — is drawn by PIL in DejaVu Sans, so no text is garbled.
- `entry.png` holds JPEG bytes (allowed by the bounty: the file is told
  apart by its first bytes) and is under the 1 MiB cap.
- `main.py` is the submitted program: it copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Standard library
  only, no network, byte-identical on every run.

## Run it

```sh
python3 compose.py          # rebuild entry.png from panels + copy
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
