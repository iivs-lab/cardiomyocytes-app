# Build the application icon from stacked qtawesome glyphs

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

The old application's icon stacked two Font Awesome 5 glyphs through
qtawesome: `fa5s.heartbeat` in red under `fa5s.microscope` in white.
Its white microscope vanished on a white background, the stack was
blurry at small sizes, and it was not padded or placed with care. The
icon stands for the whole application, a suite of sub-apps, not for
one of them.

## Considered options

- Draw new artwork by hand as SVG.
- Other qtawesome stacks: a heart with a magnifier, a microscope with
  a heart badge, or the old stack with a third glyph as a corner badge
  (magnifier, chart, flask, and others).
- The old stack, kept as it is, with a border and careful fitting.

## Decision outcome

The old stack, built only from qtawesome glyphs by
`scripts/create_icon.py`, with no badge:

- Outside the glyphs the canvas is transparent.
- Every glyph gets a one-pixel black border, made by laying the glyph
  down in black at eight one-pixel offsets before drawing it on top.
- `icon.ico` holds 13 sizes, each drawn on its own: 16, 20, 24, 28,
  32, 40, 48, 56, 64, 80, and 96 px cover the 16 px and 32 px icons
  Windows asks for at display scales from 100 % to 300 %, and 128 and
  256 px cover Explorer.
- Each size is fitted to its canvas: its wider extent spans the canvas
  less one transparent pixel at each end, and nothing is drawn inside
  that pixel.
- Vertically, the heart's weight sits in its top lobes, so centering
  its top and bottom edges made it look high. The row put at the
  canvas center lies halfway from the middle of those edges to the
  center of mass.

## Consequences

- The icon's glyphs come from Font Awesome Free, whose icons are under
  CC BY 4.0; the application has to credit them when it lists the
  licenses it uses.
- Only the Windows format, ICO, is generated. macOS takes an `.icns`
  app-bundle icon up to 1024 px, and Linux an image installed for the
  desktop file rather than one inside the executable. Supporting them
  touches the script, `gui/assets/`, the icon loading, and the build's
  `icon` setting (`TODO.md`).
