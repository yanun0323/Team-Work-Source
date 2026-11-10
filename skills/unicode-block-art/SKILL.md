---
name: unicode-block-art
description: Terminal art drawn with Unicode block, geometric, and Braille glyphs. Use for CLI banners, splash screens, logos, mascots, icons, requests for block art, Braille art, or "ASCII art" in a terminal, or gaps showing between rows of block art.
---

Draw copy-pasteable text art from the glyph palette below: filled silhouettes, not slash/underscore line art or box-drawing outlines. Users call it "ASCII art", but every glyph here except the space is Unicode.

## Steps

1. **Brief.** Pin down the subject, where it will show (splash, logo, avatar, …), the column and row budget, and whether ANSI color is allowed. Fill gaps with defaults instead of asking: at most 24 columns, monochrome, compact. Keep any shape the user supplies, including its distinctive features. Done when every one of these has a value.
2. **Mode.** Pick one, and mix only where it helps legibility:
   - **solid** (default): full and partial blocks, quadrants.
   - **shaded**: `░▒▓` for depth.
   - **geometric**: triangles, circles, squares.
   - **Braille**: 2×4 dots per cell, for fine detail.
3. **Silhouette first.** Block out the main shape as solid areas, then add detail. Aim for balanced proportions, a flat baseline where the subject sits on one, and deliberate empty space. Done when the subject is recognisable as a squint-level silhouette with no detail glyphs.
4. **Validate.** Save the art to a file and run `scripts/check_art.py` on it. Fix every error (disallowed glyph, tab, control character). A width warning can be intentional for ragged art; judge it by eye. Done when the checker exits 0 and the art still reads at real terminal width.
5. **Deliver.** Art first, inside a ```` ```text ```` fence, flush left. Explanations go outside the fence. When the user asks for several options, make the silhouettes clearly different, not small tweaks of one. Add a sentence on width or color only when it matters.

For a project's splash screen, edit the source file and run the program to see the real output instead of pasting art into chat.

## Palette

The ASCII space and newlines are for layout. Draw only with:

- **Upper/lower fills:** `▀ ▁ ▂ ▃ ▄ ▅ ▆ ▇ █`
- **Left/right fills:** `▉ ▊ ▋ ▌ ▍ ▎ ▏ ▐`
- **Shades:** `░ ▒ ▓`
- **Thin edges:** `▔ ▕`
- **Quadrants:** `▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟`
- **Squares:** `■ □ ▪ ▫ ▣ ▤ ▥ ▦ ▧ ▨ ▩ ◧ ◨ ◩ ◪ ◫ ◰ ◱ ◲ ◳`
- **Diamonds:** `◆ ◇ ◈ ◊`
- **Triangles:** `▲ △ ▼ ▽ ◀ ◁ ▶ ▷ ◢ ◣ ◤ ◥ ◸ ◹ ◺ ◿`
- **Circles/arcs:** `● ○ ◉ ◎ ◌ ◍ ◐ ◑ ◒ ◓ ◔ ◕ ◖ ◗ ◴ ◵ ◶ ◷ ◠ ◡`
- **Braille:** the whole `U+2800–U+28FF` block (256 patterns, `⠀` to `⣿`), in Braille mode.

`scripts/check_art.py` enforces this exact set.

## Terminal geometry

- A terminal cell is about twice as tall as it is wide. A circle drawn with `█` needs roughly twice as many columns as rows. For square pixels, treat each cell as two stacked pixels and draw with `▀ ▄ █` and space.
- Most of the palette, `█ ▀ ▄` included, has ambiguous East Asian width: a CJK terminal set to "ambiguous = wide" draws each one two columns wide. Braille, the quadrants `▖▗▘▙▚▛▜▝▞▟`, `▐ ░`, and the small squares are always one column. Most terminals draw blocks one column wide by default, so mixing in geometric shapes (`■ ▲ ●`) is the bigger risk in aligned grids. Run `--ambiguous-width 2` when the target terminal may be CJK.
- Pad with the ASCII space only. Braille blank `⠀` is a drawn cell: use it only inside Braille art, where it keeps the cell width steady.
- Plain text by default. Add ANSI color only when the user asks for it or the renderer is known to support it. Escape codes take zero columns.
- Alignment depends on the font. Say so, and preview in the target terminal when it matters.

## Row gaps

`fill_gaps.py` treats a leading `<org>` as original ink/hole colours and `<inv>` as swapped colours. Untagged lines default to swapped colours. The prefix is removed, affects only that line, and both modes retain background-fill conversion. For example, `<org>mho-cli` keeps text in `--ink` on `--hole`; `<inv>mho-cli` uses `--hole` on `--ink`. JSON exports the resulting colour roles too.

Some terminals draw block glyphs from the font instead of filling the cell, so a strip shows between rows: macOS Terminal.app always, and any terminal with line spacing above 1. A background colour paints the whole cell, strip included. Use this for coloured art a program renders; plain-text output keeps the glyph version.

- **Fill rule:** each cell's background takes its majority colour; only the minority quadrants are drawn as a glyph in the other colour. Full cells become coloured spaces. Ties go to the transparent colour if there is one, otherwise the hole. Text beside the art (letters, `-`, CJK) keeps its glyph in the ink colour on the hole colour. `scripts/fill_gaps.py` applies it.
- **Transparent colour:** pass `default` for one of the two colours to leave it on the terminal's own background. Cells where it is the majority stay truly transparent; where it is the minority, the glyph is drawn with reverse video (glyph colour = the other colour, background = default, then reversed; in tcell `Foreground(c).Background(tcell.ColorDefault).Reverse(true)`). Reverse video paints the background colour solid, so on a translucent or image window background those quadrants show as patches: pick a real colour there.
- **Seams survive at single-quadrant details** whose minority quadrant touches a row edge: ear tips, corner steps, a half-cell outer border. Keep large areas that cross a row boundary as full cells, and accept or redesign the details.
- **Render the filled version everywhere colour is on.** Terminals that fill block glyphs show it identically. Fall back to the glyph version when colour is off (`NO_COLOR`, output piped to a file). Claude Code switches only for `TERM_PROGRAM=Apple_Terminal`.

## Scripts

Paths are relative to this skill's folder.

```bash
python3 scripts/check_art.py art.txt                         # palette, tabs, controls, row widths
python3 scripts/check_art.py art.txt --require-equal-width   # ragged rows become errors
python3 scripts/check_art.py art.txt --ambiguous-width 2     # measure as a CJK terminal would
python3 scripts/pixels_to_braille.py mask.txt                # '#' = dot, '.' or space = empty
python3 scripts/pixels_to_braille.py mask.txt --space        # empty cells as ASCII spaces
python3 scripts/fill_gaps.py art.txt                         # ANSI preview with background fills (cyan on black)
python3 scripts/fill_gaps.py art.txt --ink '#d77757' --hole 30
python3 scripts/fill_gaps.py art.txt --hole default          # transparent holes
python3 scripts/fill_gaps.py art.txt --json                  # per-cell glyph/fg/bg, for porting into code
```

Both read stdin when no file is given. For Braille detail, draw a `#`/`.` pixel mask and convert it with the script rather than picking dot patterns by hand.
