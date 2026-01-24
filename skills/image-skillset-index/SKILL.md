---
name: image-skillset-index
description: "Create, update, or validate a skillsset image index for user-supplied images (screenshots, diagrams, UI mockups, or artwork). Use when images need to be cataloged with captions, OCR text, hashes, and metadata, or when turning a set of image files into a JSON index for later retrieval."
---

# Image Skillset Index

## Overview

Build and maintain a JSON index of image assets with optional captions and OCR text so future tasks can find and reuse them quickly.

## Quick start

1. Gather images in a directory.
2. Run the indexer script.
3. Review/update captions or OCR text as needed.

```bash
python skills/image-skillset-index/scripts/index_images.py ./path/to/images --output skillsset_index.json
```

## Tasks

### 1) Create or refresh a local index

- Use `scripts/index_images.py` for a deterministic JSON index.
- Provide a captions JSON file when you have curated descriptions.

```bash
python skills/image-skillset-index/scripts/index_images.py ./images \
  --output skillsset_index.json \
  --captions captions.json
```

`captions.json` is a mapping of filename to caption:

```json
{
  "dashboard.png": "Analytics dashboard with performance charts and small multiples",
  "network.png": "Starburst network of nodes on dark background"
}
```

### 2) Add entries for images that only exist in chat context

When images are only shared in chat (not on disk), append manual entries to the index:

- Use `path: "chat://<sequence>"`.
- Add a descriptive `caption` and any visible text in `ocr_text`.
- Set `bytes`, `sha256`, and `size` to `null` if unavailable.

Example entry:

```json
{
  "path": "chat://image-01",
  "filename": "user-upload-01",
  "sha256": null,
  "bytes": null,
  "mime": "image/png",
  "indexed_at": "2025-01-01T00:00:00Z",
  "size": null,
  "caption": "Screenshot of Grok project UI with a chat composer and share URL",
  "ocr_text": "https://grok.com/share/..."
}
```

### 3) Validate the index structure

- Ensure `generated_at`, `count`, and `entries` are present.
- Validate fields against the schema in `references/index-schema.md`.

## Resources

### scripts/

- `index_images.py`: Builds a JSON index from local image files with hashes, sizes, and optional OCR text.

### references/

- `index-schema.md`: Schema and field definitions for the index output.
