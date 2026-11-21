[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Jo3st4r/news-image-20261121-bot/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Jo3st4r/news-image-20261121-bot/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# 50 stories, one page — the world on 21 November 2026

**The World in One Image — Saturday 21 November 2026.** One newspaper front page
that sums up the whole day: 3 lead stories, an around-the-world band, and 47 more
stories in a grid — 50 verified stories, one page, checked against the day's
reporting.

## The day at a glance

1. **World Court: Myanmar committed genocide** — the ICJ holds a state responsible
   for genocide for the first time, ordering Rohingya refugees allowed home.
2. **Russian missiles land in Poland** — two missiles and a drone come down in the
   east; Warsaw calls it a deliberate provocation, NATO a grave violation.
3. **S&P 500 and Dow slide into correction** — the AI sell-off deepens; the Nasdaq
   loses over 5% and erases its 2026 gains.

Then the world in one sweep: the UK–EU reset deal, the Shenzhen trilateral, the
Iran war's ninth month, COP31 spilling into overtime, a pancreatic-cancer pill
breakthrough, Cyclone Akvan, the Anthropic IPO, and a full day of sport — from
Rahul's century chase in Wellington to Zverev's ATP Finals semi-final.

## How it is built

- `tools/render.py` draws the poster with Pillow: masthead, three lead rows, the
  around-the-world band, and the 47-story grid. It is deterministic — no clock,
  no network, no random numbers — so two runs produce identical bytes.
- `assets/entry.png` is the rendered poster: 1024×1024 PNG, under 1 MiB.
- `main.py` (standard library only) copies `assets/entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

Rebuild it:

```sh
python3 tools/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Every headline was checked against reporting first published 20–21 November 2026
by Reuters, BBC, AP, CNN, IANS, UN News, and The Guardian.

## Competition

[Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121)
— make.fun, pool $100, top 50 entries share the prize.

## License

MIT — see [LICENSE](LICENSE).
