# Table Math

Banquet table seating arithmetic. A round table 150 across has a rim of 471.2, so at 60 per guest it seats 7 and leaves 51.2 of rim unused.

## What it computes

All sizes are whole numbers (1 to 10000) in one unit of your choice.

- **The round table** - the rim (pi times the diameter, to one decimal), how many guests fit at your space per guest, and the rim left over.
- **The rectangular table** - guests along the two long sides, plus the ends you choose to seat (0, 1 or 2), each at the same space per guest.
- **The guest list** - tables of a given size needed for a guest list plus the spare seats you ask for, with the seat and empty-seat counts.

## Boundary

Arithmetic only. It counts guest spaces from the owner's own sizes. It does not know any venue's, fire marshal's or caterer's limits, aisle or chair rules and gives no verdict on whether a layout is comfortable or allowed.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (pi as a 50-digit integer, BigInt floors).
- `oracle.py` - the Python mirror (pi from Machin's formula, counts guest by guest) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (178 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/tablemath/
Repo: https://github.com/iLanis-agent/tablemath
