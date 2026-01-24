# DoinBetter-Fractal-Whisper
Self-healing Speech-to-text system.

## Möbii³us HUD emoji render pipeline

This repo now scaffolds the SVG → tilesheet → intent registry flow for the
`heyMicojava_labels_svg_morning` glyph pack.

### Layout

```
assets/heyMicojava_labels_svg_morning/  # place SVG glyphs here
build/tilesheet.json                    # generated tile metadata
config/emoji_intents.json               # emoji intent registry
config/guardian_ethics_matrix.json      # ethics lane trigger matrix
scripts/build_tilesheet.py              # parses SVG <metadata>
scripts/pre_render.py                   # pre-render entrypoint
```

### SVG metadata

Add a `<metadata>` block to each SVG. JSON is preferred, but raw text is
captured if JSON parsing fails.

```xml
<metadata>{"lane":"north","palette":"morn","tile_size":64}</metadata>
```

### Pre-render step

```bash
python3 scripts/pre_render.py
```

This emits `build/tilesheet.json`, which is referenced by
`config/emoji_intents.json`.
