# DoinBetter-Fractal-Whisper Requisite Skills

**Prototype context:** self-healing speech-to-text system and heyMicojava SVG pipeline.

## Skills recovered from repository material

### Speech-to-text system
- Speech capture and transcription system design.
- Audio input handling.
- Transcription pipeline integration.
- Recovery and resilience design for speech-to-text workflows.

**Evidence boundary:** the README identifies this prototype as a self-healing speech-to-text system. The implementation of the speech engine was not inspected in this pass.

### heyMicojava SVG pipeline
- SVG parsing.
- Embedded `<metadata>` extraction.
- JSON metadata parsing.
- Key/value metadata parsing.
- SVG width and height extraction.
- SHA-256 asset fingerprinting.
- Glyph ID and label construction.
- Tilesheet JSON generation.
- Render-intent registry integration.

**Source recovered:** `scripts/build_tilesheet.py` reads SVG files, extracts metadata and dimensions, hashes the original bytes, and writes a sorted tilesheet manifest.

### Related integration skills
- Asset manifest generation.
- Stable glyph identifiers.
- Metadata-preserving visual asset registration.
- SVG-to-render-intent mapping.

## Historical boundary

The README also references a Guardian ethics-lane trigger matrix. Preserve it as historical pipeline context. It is not part of the canonical coordinate traversal contract and must not introduce ranking, approval, denial, or evaluation stages into the coordinate resolver.

## Shared architecture

The shared coordinate runtime and cross-prototype skill atlas are owned by [systemsNxXD](https://github.com/git4emet/systemsNxXD). See the [conversation-recovered skill atlas](https://github.com/git4emet/systemsNxXD/blob/main/docs/skills/CONVERSATION_RECOVERED_SKILL_ATLAS.md).
