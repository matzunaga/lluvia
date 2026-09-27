# Lluvia: handoff notes

Built in a claude.ai session, September 2026. Single file, no build step.

## Where the skyline comes from
POLY in index.html is San Diego traced from a photo taken across the bay
(PW = photo width 682, BASE = base row 286). The reference photos were stock
images, used only to measure the shape. Nothing else from them is in the piece.
Retracing from Matzunaga's own photos would make it fully clean.
tools/trace_skyline.py reproduces the trace for any city.

Known gaps: Emerald Plaza's hexagonal crowns are hidden behind other towers
in the source photo, so they are missing. The tallest crown is approximate.

## Performance rules (the first version ran at about 2 fps; these fixed it)
- Everything static is drawn once in build() into offscreen canvases:
  sky, parallax districts, city, steady neon, reflection, streaks, overlays.
- No shadowBlur inside the frame loop. Glow is baked; failing neon is a
  prebuilt sprite whose alpha stutters.
- Never draw the main canvas onto itself. The reflection is a prebuilt
  canvas drawn in 6-pixel bands with a sideways ripple.
- Rain is batched: three depth layers, one stroke call each.

## Not done yet
- Sound: rain bed and thunder, sourced and license-checked
- The Maya mark: ha'al, rain, drawn only from an attested form
- Live weather from Open-Meteo (plan not decided)
- More cities, one at a time
