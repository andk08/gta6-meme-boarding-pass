# gta6-meme-boarding-pass

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/andk08/gta6-meme-boarding-pass/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/andk08/gta6-meme-boarding-pass/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A fake airline boarding pass for a flight to Leonida, made for the
make.fun bounty "Post a GTA 6 meme on X". Leonida Air, flight LS666,
Los Santos to Leonida (Vice City, FL), departure 2013 — status:
DELAYED 4,811 DAYS. Gate TBD, seat 13A, class Patience, co-pilots
Jason & Lucia, baggage: 13 years of hope, arrives: when Rockstar says
so. The fare was paid by my AI agent's make.fun bounty winnings, and
the make.fun ghost rides along on the stub, holding its magenta coin.

## The meme

`boarding-pass.png` (1400x800) is the picture that goes on X. It was
drawn with PIL (`draw_boarding.py`, so the layout is reproducible):
a clean boarding pass with a real barcode, the big red DELAYED
punchline, and the make.fun ghost — white ghost, thick black outline,
sparkle eyes, holding a magenta coin with a white star — worked into
the stub as the fare's payer, plus a magenta make.fun strip along the
bottom.

The joke lands in one second: a boarding pass is a document every
traveller recognises, and every field on it is the thirteen-year wait
— a 2013 departure, a 4,811-day delay, a gate that is still TBD, a
seat in Patience class. The dev board's top entries are mostly
official-document memes (receipts, invoices, citations, bills); a
boarding pass is a document format none of the top 20 used, and its
travel framing is a fresh angle on the same wait.

## The post

The draft text is in `POST_TEXT.md`. It carries the bounty link, the
play code `makefun-bridge-dairy-pueblo` and the boarding-pass pitch,
and it is posted from the public X account `@blacteamy0108` with
`boarding-pass.png` as its first picture. After posting, the post's
address goes in `POST.json`:

```json
{"url": "https://x.com/blacteamy0108/status/<id>"}
```

## Run it

`main.ts` (Node 22, standard library only) copies `POST.json` to the
output directory. That is all the program has to do — the house reads
the post itself from X.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=xp78qg6d&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
