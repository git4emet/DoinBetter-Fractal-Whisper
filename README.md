# DoinBetter-Fractal-Whisper
Self-healing Speech-to-text system.

## heyMicojava SVG pipeline

This repository now includes a minimal pipeline for registering heyMicojava SVGs as emoji render intents,
building a tilesheet JSON, and wiring Guardian ethics lane triggers.

### Directory layout

- `assets/heyMicojava_labels_svg_morning/` — place SVG glyphs here (each file may include `<metadata>`).
- `assets/tilesheet.json` — generated tilesheet manifest for the emoji engine.
- `config/emoji/intent_registry.json` — registry entry that points the engine at the tilesheet.
- `config/guardian/ethics_lane_trigger_matrix.json` — Guardian lane/trigger mapping.

### Build the tilesheet

```bash
python3 scripts/build_tilesheet.py \
  --source assets/heyMicojava_labels_svg_morning \
  --output assets/tilesheet.json
```

The script reads embedded `<metadata>` blocks in each SVG, along with width/height attributes, and emits
a tilesheet manifest containing glyph IDs, hashes, and metadata payloads.
