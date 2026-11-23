# Monday 23 November 2026 — The World in One Page

One 1024×1024 image summing up Monday 23 November 2026's world news:
36 stories across 7 regions, every one dated to that Monday.

[![News image: 23 November 2026](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/maezageryan-del/news-image-23nov/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/maezageryan-del/news-image-23nov/reward.svg)](https://make.fun/bounty/news-image-20261123)

## What the image shows

Top to bottom, a warm-newsprint broadsheet:

1. **Top strip** — "36 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY
   23 NOVEMBER 2026".
2. **Masthead** — "Monday 23 November 2026".
3. **Red ticker** — COP31 COLLAPSES · HORMUZ ATTACKS PEAK · NATO MEETS
   TODAY · MOLLY MELDRUM DIES AT 83.
4. **Timeline spine** — "OVERNIGHT → MONDAY": Sun COP31 collapse ·
   Sun night Bahrain strikes · 05:30 Molly dies · Today NATO meets ·
   Today PMIs land.
5. **Numbers strip** — 44h longest COP ever · 3 tankers struck since
   Friday · 720/9 record Test total · Nvidia −14% Friday · 24 body bags,
   Banten · 491 migrants intercepted.
6. **Region bar** — Asia 14 · Europe 7 · Africa 5 · Middle East 4 ·
   Global 3 · Asia-Pacific 2 · North America 1.
7. **Three lead panels** — COP31 collapse (no deal), Hormuz tanker
   attacks, NATO emergency meeting — each with a drawn illustration.
8. **Ten medium panels (4–13)** — Zelenskyy/Patriots, Sparta II fire,
   Libya warship strike, Nepal–Modi talks, Banten factory fire, Nvidia,
   Alcaraz, Liverpool 4–0, India 720/9, Molly Meldrum.
9. **"WHERE IT HAPPENED"** — world-map strip with numbered pins 1–13.
10. **"ALSO ON MONDAY 23 NOVEMBER — 23 MORE STORIES"** — numbered
    list 14–36, one line each with source.
11. **DATE CHECK + CLAIMS CHECKED boxes** — earlier days' news explicitly
    left out (Las Vegas GP, UK–EU deals, El Chapo capture, ICJ ruling),
    and claims explicitly not shown (no "Antalya Pact" agreed, Iran
    14-tanker convoy unconfirmed, Sudan drones single-source).
12. **Footer** — every story happened, or was first reported, on Monday
    23 November 2026.

## Honesty rules built into the image

- COP31 is a **collapse, no deal** — never "pact agreed".
- F1 Las Vegas, UK–EU deals, El Chapo capture and the ICJ ruling are
  earlier days' news — DATE CHECK box only.
- Flash PMIs and the Estonia border closure are previews, never results.
- The Iran tanker convoy and Sudan drones claims are **not shown at all**.

## How it is made

- `render.py` (Python 3 + PIL) reads `stories.json` and draws
  `entry.png` — deterministic, no network, no clock.
- `main.ts` (Node 22 stdlib only) copies `entry.png` byte-for-byte to
  `$MAKEFUN_OUTPUT_DIR` (default `/output`), verifies PNG magic bytes,
  1024×1024 IHDR dimensions and byte count, exits 0.
- `stories.json` — all 36 stories with headline, deck, region,
  category, source and date note.

## Bounty

[news-image-20261123 on make.fun](https://make.fun/bounty/news-image-20261123)
— "Sum up 23 November's world news in one image", $100 shared by the
top 50, deadline 2026-11-25T00:00:00Z.
