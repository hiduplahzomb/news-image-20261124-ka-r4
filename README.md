# news-image-20261124-ka-r4

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r4/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r4/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world news of **Tuesday, 24 November 2026** —
a visual-first front page. Every story is anchored to 24 November
itself (all facts verified against live reporting on 25 November 2026):

- **Top story — Riyadh:** a Houthi projectile strikes the 80-storey
  PIF Tower in Riyadh's King Abdullah Financial District, injuring
  11 people (2 Saudis, 2 Indians, 3 Nepalis, 4 Egyptians) — the
  second strike on the tower in less than a week.
- **Gulf of Finland:** Zelensky confirms Ukrainian drones set the
  Russian cargo ship Sparta II ablaze on Saturday 21 November; all
  16 crew were evacuated, the ship reached St Petersburg on Monday
  23 November, and Zelensky confirmed the strike on 24 November.
- **United States:** a Brooklyn jury convicts Huawei on 10 of 12
  counts, including bank fraud and trade-secret theft, but acquits
  it of racketeering.
- **China:** China names the Shenzhou-24 crew — Tang Hongbo, Wu Yi
  and Pakistani pilot Muhammad Zeeshan Ali, the first foreign
  astronaut bound for Tiangong (launch 08:18 on 25 November).
- **Pacific:** the Solomon Islands scraps its 2022 China security
  pact and names Australia its primary security partner, with no
  foreign military base on its soil (reported 24 November; the
  Australia treaty was signed in Canberra on Wednesday 25 November
  local time).

Why the ICJ is no longer the lead: the Court's Rohingya genocide
ruling against Myanmar was handed down on **19 November**, five days
before this front page. Fourteen nations did affirm the ruling on
Monday 23 November, but that diplomatic follow-up is weaker as a
24 November lead than the PIF Tower strike, so the ICJ story was
dropped from the page.

## How it works

`draw_image.py` draws `entry.png` with Pillow (2x supersampling,
Lanczos downscale to 1024x1024, fully deterministic — no randomness,
no timestamps, no network). `main.py` (standard library only) copies
`entry.png` to the output directory and verifies the copy byte for byte.

```sh
python3 draw_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — entrypoint; copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (default `/output`) and verifies its SHA-256.
- `draw_image.py` — the Pillow renderer that draws `entry.png` from scratch.
- `entry.png` — the rendered 1024x1024 front page.
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
