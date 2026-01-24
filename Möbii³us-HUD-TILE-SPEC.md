# Möbii³us HUD Tile Integration Spec

## Purpose
This document defines the production contract between the Emoji Tile Canvas pipeline and the Möbii³us substrate, including routing via LaneSpace16, TOFAR logging, and HUD composition. It is intended to be copied into deployable modules so that the rendering layer and Möbii³us substrate can evolve independently without breaking the interface.

## System Overview

### 1) Emoji Rendering Pipeline
The rendering pipeline turns SVG or raster inputs into a cached N×M emoji grid.

| Stage | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| Edge Mask + Intent Extraction | Detects regions and classifies them as `Text`, `Icon`, or `Decorative` via vector parsing or raster filters (e.g., Canny) with optional ML augmentation. | SVG, raster, or pre-labeled metadata | Region intents + region masks |
| Emoji Mapping | Maps region intent to emoji from curated palette using a stable content hash. | Region intents + palette | Emoji selection map |
| Tiling & Caching | Renders emoji into N×M tiles with LRU cache. | Emoji map + grid size | Emoji grid + cache key |
| TOFAR Logging | Emits a TOFAR event for every render with trust/ethics annotations. | Render metadata | TOFAR render event |

#### Render Event (TOFAR) Schema
| Field | Type | Description |
| --- | --- | --- |
| `event_id` | string | UUID for the render event. |
| `event_type` | string | `emoji_render`. |
| `timestamp` | string | ISO-8601 time. |
| `lane` | number | LaneSpace16 lane ID (0–15). |
| `source_hash` | string | Content hash for render determinism. |
| `grid` | object | `{ rows: number, cols: number }`. |
| `intent_counts` | object | Counts of `text`, `icon`, `decorative`. |
| `trust` | object | `{ score: number, threshold: number, verdict: "pass"|"warn"|"fail" }`. |
| `ethics` | object | `{ annotations: string[], gate: string }`. |
| `cache` | object | `{ hit: boolean, key: string }`. |

### 2) LaneSpace16 Overlay
LaneSpace16 is the routing and policy overlay for all HUD events.

| Field | Type | Description |
| --- | --- | --- |
| `lane` | number | Lane ID, 0–15. |
| `basis_vector` | string | Sedenionic basis vector label (e.g., `e7`). |
| `namespace` | string | Logical namespace (e.g., `sandbox/notes`). |
| `policy` | object | Policy rules (trust floors, allowlists). |
| `pressure` | object | `{ temperature: number, pressure: number }`. |

#### Example Lane Map (Default)
| Lane | Namespace | Example Use |
| --- | --- | --- |
| 3 | `sandbox/files_local` | File-handling overlays |
| 7 | `sandbox/clipboard` | Clipboard overlays |
| 11 | `kernel/ethics` | Ethics threshold enforcement |
| 12 | `kernel/forecast` | Forecast auto-trust rules |

### 3) Möbii³us Substrate + TOFAR
All user interactions log glyph stamps and propagate to TOFAR.

#### Glyph Stamp Schema
| Field | Type | Description |
| --- | --- | --- |
| `glyph_id` | string | UUID for the glyph stamp. |
| `kind` | string | E.g., `defect`, `note`, `route`. |
| `x` | number | Normalized X coordinate in viewport. |
| `y` | number | Normalized Y coordinate in viewport. |
| `strength` | number | 0–1 stamp intensity. |
| `label` | string | E.g., `viewport_tap`. |
| `lane` | number | LaneSpace16 lane ID. |
| `timestamp` | string | ISO-8601 time. |

#### Tap Event (TOFAR) Schema
| Field | Type | Description |
| --- | --- | --- |
| `event_id` | string | UUID for the tap event. |
| `event_type` | string | `viewport_tap`. |
| `timestamp` | string | ISO-8601 time. |
| `lane` | number | LaneSpace16 lane ID. |
| `glyph` | object | Glyph stamp record. |
| `trust` | object | `{ score: number, threshold: number, verdict: "pass"|"warn"|"fail" }`. |
| `ethics` | object | `{ annotations: string[], gate: string }`. |

## HUD Composition
| Layer | Role | Notes |
| --- | --- | --- |
| Emoji Canvas | Center grid visualization | N×M emoji tiles, subtle edge animation. |
| Lane Ring | 16-lane sedenionic overlay | Pressure/temperature indicators. |
| Config Ring | Mode toggle | Collapses UI if missing (one-page rule). |
| Glyph Layer | Background pulse marks | Fades over time with glow. |
| Metrics Panel | Coherence, queue depth, trust | Gate verdicts included. |

## API Contract
| Route | Method | Description |
| --- | --- | --- |
| `/api/emoji/render` | POST | Render emoji grid from SVG/raster. |
| `/api/viewport/tap` | POST | Register glyph stamp + TOFAR tap. |
| `/api/lanes` | GET | LaneSpace16 map. |
| `/api/metrics` | GET | HUD metrics payload. |

### Render Request (POST `/api/emoji/render`)
```json
{
  "source": {
    "type": "svg",
    "payload": "<svg>...</svg>"
  },
  "lane": 7,
  "grid": { "rows": 18, "cols": 30 },
  "palette": "default",
  "metadata": {
    "intent_mode": "metadata-preferred",
    "trust_floor": 0.74
  }
}
```

### Render Response
```json
{
  "grid": ["😀", "✨", "📎"],
  "rows": 18,
  "cols": 30,
  "cache": { "hit": false, "key": "render:2b1a..." },
  "tofar": { "event_id": "..." }
}
```

### Tap Request (POST `/api/viewport/tap`)
```json
{
  "x": 0.42,
  "y": 0.68,
  "lane": 11,
  "kind": "defect",
  "strength": 0.73,
  "label": "viewport_tap"
}
```

## SVG Metadata Contract
To reduce runtime parsing costs, embed intent and lane hints inside SVG `<metadata>` blocks.

### Required Metadata Keys
| Key | Description | Example |
| --- | --- | --- |
| `intent` | `Text`, `Icon`, or `Decorative` | `Text` |
| `lane` | LaneSpace16 lane ID | `7` |
| `emoji_hint` | Preferred emoji (optional) | `📎` |
| `palette` | Preferred palette (optional) | `default` |
| `edge_id` | Stable ID for region | `edge-clipboard-01` |

### Metadata JSON Shape
```json
{
  "edge_id": "edge-clipboard-01",
  "intent": "Icon",
  "lane": 7,
  "emoji_hint": "📎",
  "palette": "default"
}
```

## Guardrails
- Lane 11 (`kernel/ethics`) must enforce trust floor 0.74 for render and tap events.
- All render and tap events must emit TOFAR records.
- Cache keys must be derived from content hash + grid configuration + palette.

## Deployment Notes
- Server entrypoints should be split into emoji-render and substrate modules.
- FastAPI wiring should be minimal; handler modules must be importable without side effects.
- Telemetry should include lane pressure and ethics gate verdicts for HUD metrics.
