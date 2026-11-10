#!/usr/bin/env python3
"""Check Unicode block art: allowed glyphs, tabs, control characters, row widths.

Exit 1 on any error. Lines starting with ``` are skipped, so a fenced block can be checked as-is.
"""
import argparse
import sys
import unicodedata

PALETTE = (
    "▀▁▂▃▄▅▆▇█"
    "▉▊▋▌▍▎▏▐"
    "░▒▓"
    "▔▕"
    "▖▗▘▙▚▛▜▝▞▟"
    "■□▪▫▣▤▥▦▧▨▩◧◨◩◪◫◰◱◲◳"
    "◆◇◈◊"
    "▲△▼▽◀◁▶▷◢◣◤◥◸◹◺◿"
    "●○◉◎◌◍◐◑◒◓◔◕◖◗◴◵◶◷◠◡"
)
ALLOWED = set(PALETTE) | {" "} | {chr(c) for c in range(0x2800, 0x2900)}


def width(ch, ambiguous):
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("W", "F"):
        return 2
    if eaw == "A":
        return ambiguous
    return 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", nargs="?", help="UTF-8 art file (default: stdin)")
    p.add_argument("--require-equal-width", action="store_true", help="treat ragged rows as errors")
    p.add_argument("--ambiguous-width", type=int, choices=(1, 2), default=1,
                   help="columns for ambiguous-width glyphs (2 = CJK terminal)")
    args = p.parse_args()

    raw = open(args.file, "rb").read() if args.file else sys.stdin.buffer.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"error: not valid UTF-8: {e}")
        return 1
    text = text.lstrip("﻿")

    errors, warnings, widths = [], [], []
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            continue
        for col, ch in enumerate(line, 1):
            if ch == "\t":
                errors.append(f"line {n} col {col}: tab, use spaces")
            elif ch not in ALLOWED:
                name = unicodedata.name(ch, "UNNAMED")
                errors.append(f"line {n} col {col}: U+{ord(ch):04X} {name} is not in the palette")
        if line != line.rstrip(" "):
            warnings.append(f"line {n}: trailing spaces")
        widths.append((n, sum(width(ch, args.ambiguous_width) for ch in line)))

    drawn = [w for _, w in widths if w]
    if drawn and len(set(drawn)) > 1:
        detail = ", ".join(f"{n}:{w}" for n, w in widths if w)
        msg = f"row widths differ (line:columns) {detail}"
        (errors if args.require_equal_width else warnings).append(msg)

    for m in errors:
        print(f"error: {m}")
    for m in warnings:
        print(f"warning: {m}")
    rows = len(widths)
    cols = max(drawn, default=0)
    print(f"{'FAIL' if errors else 'OK'}: {rows} rows, {cols} columns max")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
