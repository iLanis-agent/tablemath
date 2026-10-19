// Table Math engine: how many guests fit around round and rectangular tables, and how many tables a guest list needs.
// Pi is held as a 50-digit integer so floors and tenths are exact. Sizes are in whatever unit you use, as whole numbers.
var PI50 = 314159265358979323846264338327950288419716939937510n; // pi x 10^50
var E50 = 100000000000000000000000000000000000000000000000000n;
var SIZE_ERR = "the table sizes and the space per guest must be whole numbers from 1 to 10000";
var ENDS_ERR = "the seated ends must be 0, 1 or 2";
var GUEST_ERR = "the guests must be a whole number from 1 to 100000";
var PER_ERR = "the seats per table must be a whole number from 1 to 1000";
var SPARE_ERR = "the spare seats must be a whole number from 0 to 1000";

function _int(t, re, lo, hi, err) {
  t = typeof t === "string" ? t.trim() : "";
  if (!re.test(t)) throw new Error(err);
  var n = parseInt(t, 10);
  if (n < lo || n > hi) throw new Error(err);
  return n;
}
function _size(t) { return _int(t, /^[0-9]{1,5}$/, 1, 10000, SIZE_ERR); }
function _plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
// tenths of x given as a scaled integer v / E50, rounded half up, shown with one decimal
function _tenths(v) {
  var t = (v * 10n * 2n + E50) / (E50 * 2n); // round half up of v*10/E50
  var neg = t < 0n; if (neg) t = -t;
  return (neg ? "-" : "") + (t / 10n) + "." + (t % 10n);
}

function roundTruth(diameter, space) {
  var d = BigInt(_size(diameter)), s = BigInt(_size(space));
  var rim = d * PI50; // x 10^50
  var n = rim / (s * E50);
  var left = rim - n * s * E50;
  var out = "A round table " + d + " across has a rim of " + _tenths(rim) + " around. At " + s + " per guest it seats " + n + ", leaving " + _tenths(left) + " of rim unused.";
  return out;
}
function rectTruth(length, width, space, ends) {
  var l = _size(length), w = _size(width), s = _size(space);
  var e = _int(ends, /^[0-9]$/, 0, 2, ENDS_ERR);
  var side = Math.floor(l / s), end = Math.floor(w / s);
  var sides = 2 * side, endSeats = e * end;
  var endTxt = e === 0 ? "no seated ends" : _plural(endSeats, "guest", "guests") + " at the " + _plural(e, "seated end", "seated ends");
  return "A table " + l + " by " + w + " at " + s + " per guest: " + _plural(sides, "guest", "guests") + " along the two long sides and " + endTxt + ", " + _plural(sides + endSeats, "guest", "guests") + " in all.";
}
function fillTruth(guests, perTable, spare) {
  var g = _int(guests, /^[0-9]{1,6}$/, 1, 100000, GUEST_ERR);
  var p = _int(perTable, /^[0-9]{1,4}$/, 1, 1000, PER_ERR);
  var x = _int(spare, /^[0-9]{1,4}$/, 0, 1000, SPARE_ERR);
  var t = Math.floor((g + x + p - 1) / p);
  var seats = t * p;
  return _plural(g, "guest", "guests") + " with at least " + _plural(x, "spare seat", "spare seats") + " at tables of " + p + ": " + _plural(t, "table", "tables") + ", " + _plural(seats, "seat", "seats") + ", " + _plural(seats - g, "empty seat", "empty seats") + ".";
}
