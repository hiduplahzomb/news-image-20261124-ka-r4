# news-image-20261124-ka-r4

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r4/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r4/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world news of **Tuesday, 24 November 2026** —
a visual-first front page:

- **Top story — The Hague:** the International Court of Justice rules
  Myanmar committed genocide against the Rohingya; 14 states backed
  The Gambia's case.
- **China:** Shenzhou-24 crew launches to the Tiangong space station.
- **Ukraine / Gulf of Finland:** the war at sea puts Gulf shipping lanes
  under a closer watch.
- **United Nations:** Secretary-General Antonio Guterres urges global
  rules to govern AI.
- **Pacific:** the Solomon Islands deepens its ties with Australia.

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
- `entry.png` — the rendered 1024x1024 front page (273,406 bytes).
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
