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
- Windows are steady. The only lights that change are about 170 single
  points in the distant districts, each fading on and off on its own random
  schedule (TWINKLE_ON, TWINKLE_OFF, TWINKLE_FADE at the top of the script).

## Sound
rain.mp3 is "Rain" by alex36917, https://freesound.org/people/alex36917/sounds/524605/ ,
licensed CC BY (as listed in the Blanket app's SOUNDS_LICENSING.md; the exact
version could not be checked from the build machine, so confirm it on that page).
Changes: edited by Porrumentzio for Blanket, then raised 4 dB and saved as a
112 kbps MP3 here. It loops through a four-second equal-power crossfade.
The sound starts only from the Sound button, since browsers need a tap.
CC BY asks for credit where the piece is seen; if an i card is added, put the
credit line there too.

## Not done yet
- Thunder, sourced and license-checked
- The Maya mark: ha'al, rain, drawn only from an attested form
- Live weather from Open-Meteo (plan not decided)
- More cities, one at a time
