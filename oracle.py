#!/usr/bin/env python3
# Table Math oracle - mirrors engine.js. Pi comes from Machin's formula in Python integers, not from a stored constant.
import json, re, random
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_FLOOR

getcontext().prec = 80

def arctan_inv(x, digits):
    scale = 10 ** (digits + 10)
    total = term = scale // x
    x2 = x * x; n = 1; sign = -1
    while term:
        term //= x2; n += 2
        total += sign * (term // n); sign = -sign
    return total
def pi_decimal(digits=60):
    p = 4 * (4 * arctan_inv(5, digits) - arctan_inv(239, digits))
    return Decimal(p) / Decimal(10 ** (digits + 10))
PI = pi_decimal()

SIZE_ERR = "the table sizes and the space per guest must be whole numbers from 1 to 10000"
ENDS_ERR = "the seated ends must be 0, 1 or 2"
GUEST_ERR = "the guests must be a whole number from 1 to 100000"
PER_ERR = "the seats per table must be a whole number from 1 to 1000"
SPARE_ERR = "the spare seats must be a whole number from 0 to 1000"

def pint(t, pat, lo, hi, err):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(pat, t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def size(t): return pint(t, r"[0-9]{1,5}", 1, 10000, SIZE_ERR)
def plural(n, one, many): return f"{n} {one if n == 1 else many}"
def tenth(x): return str(x.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

def round_truth(d, s):
    d, s = size(d), size(s)
    rim = Decimal(d) * PI
    n = int((rim / s).to_integral_value(rounding=ROUND_FLOOR))
    left = rim - n * s
    return f"A round table {d} across has a rim of {tenth(rim)} around. At {s} per guest it seats {n}, leaving {tenth(left)} of rim unused."

def rect_truth(l, w, s, e):
    l, w, s = size(l), size(w), size(s)
    e = pint(e, r"[0-9]", 0, 2, ENDS_ERR)
    sides = 0
    for edge in (l, l):  # count seats edge by edge, one guest space at a time
        k = 0
        while (k + 1) * s <= edge: k += 1
        sides += k
    k = 0
    while (k + 1) * s <= w: k += 1
    end = e * k
    et = "no seated ends" if e == 0 else f"{plural(end,'guest','guests')} at the {plural(e,'seated end','seated ends')}"
    return f"A table {l} by {w} at {s} per guest: {plural(sides,'guest','guests')} along the two long sides and {et}, {plural(sides+end,'guest','guests')} in all."

def fill_truth(g, p, x):
    g = pint(g, r"[0-9]{1,6}", 1, 100000, GUEST_ERR)
    p = pint(p, r"[0-9]{1,4}", 1, 1000, PER_ERR)
    x = pint(x, r"[0-9]{1,4}", 0, 1000, SPARE_ERR)
    t = 0
    while t * p < g + x: t += 1
    seats = t * p
    return f"{plural(g,'guest','guests')} with at least {plural(x,'spare seat','spare seats')} at tables of {p}: {plural(t,'table','tables')}, {plural(seats,'seat','seats')}, {plural(seats-g,'empty seat','empty seats')}."

FNS = {"roundTruth": round_truth, "rectTruth": rect_truth, "fillTruth": fill_truth}

def cases():
    c = []
    rnd = random.Random(694)
    for d, s in [("150","60"),("1","1"),("10000","1"),("10000","10000"),("7","22"),("7","21"),("113","100"),("100","314"),("100","315"),
                 ("0","5"),("5","0"),("10001","5"),("5","10001"),("abc","5"),("","5"),(" 150 "," 60 "),("1.5","5"),("-5","5"),("00150","60"),("7","7"),("1","4")]:
        c.append(("roundTruth", [d, s]))
    for _ in range(40):
        c.append(("roundTruth", [str(rnd.randint(1, 10000)), str(rnd.randint(1, 500))]))
    for a in [["240","90","60","2"],["240","90","60","0"],["240","90","60","1"],["60","60","60","2"],["59","59","60","2"],["1","1","1","1"],
              ["10000","10000","1","2"],["10000","1","10000","2"],["100","100","30","2"],["120","30","60","1"],["240","90","60","3"],["240","90","60","x"],["0","90","60","2"],["240","0","60","2"],["240","90","0","2"],["240","90","60",""],[" 240 "," 90 "," 60 "," 2 "]]:
        c.append(("rectTruth", a))
    for _ in range(40):
        c.append(("rectTruth", [str(rnd.randint(1, 400)), str(rnd.randint(1, 200)), str(rnd.randint(1, 100)), str(rnd.randint(0, 2))]))
    for a in [["62","8","3"],["1","1","0"],["1","1","1"],["8","8","0"],["9","8","0"],["100000","1000","1000"],["100000","1","0"],["64","8","0"],["64","8","1"],
              ["0","8","3"],["100001","8","3"],["62","0","3"],["62","1001","3"],["62","8","1001"],["62","8","-1"],["a","8","3"],["62","8",""],[" 62 "," 8 "," 3 "],["1","8","0"],["7","8","1"]]:
        c.append(("fillTruth", a))
    for _ in range(40):
        c.append(("fillTruth", [str(rnd.randint(1, 2000)), str(rnd.randint(1, 30)), str(rnd.randint(0, 40))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
