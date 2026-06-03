# NavTree v2 Format Specification

A hybrid data format for universal hierarchical navigation with multimedia content.
Designed to support unlimited depth, multiple media types (text, pictures, audio, video),
and both machine-generated and human-edited data.

## Design Principles

1. **Unlimited hierarchy depth** — no fixed "book/chapter/section" model
2. **Media-first** — every node can have pictures, audio, video, and text
3. **Folder-as-tree** — the directory hierarchy IS the navigation tree; no separate tree.json
4. **Hybrid format** — TOML for config and metadata, Markdown for content, JSON for generated indexes
5. **Source-agnostic** — the format is the same whether content comes from Obsidian, DOCX, or manual authoring
6. **Language-neutral paths** — folder names use numbers, not language-specific words
7. **Compatible with bibel-wiki conventions** — `index.toml` per folder, markdown content alongside, locale TOML files

## Content Identity and Deduplication

Each note has a stable `content_id` derived from its source filename slug
(e.g., `creation-care`). When the same content appears at multiple positions
in the tree, the first occurrence holds the content files and subsequent
occurrences use a `redirect_to` field in their `index.toml` pointing to
the primary location.

### How deduplication works

1. The build script assigns content to the first tree position it encounters.
2. At secondary positions, `index.toml` contains `redirect_to = "01/05/01"`
   pointing to the primary folder path.
3. The app reads the redirect and fetches content from the primary location.
4. `search-positions.json` lists all positions for each `content_id`,
   so search results can link to any occurrence.

### Communicating with AI agents

Two files coordinate between the build pipeline and AI agents:

- **`output/redirects.toml`** (build → agents): Lists all multi-position content.
  Agents fetch this before making structural changes to know which notes
  affect multiple tree positions.
- **`vault-changelog.toml`** (agents → build): Agents log structural changes
  here. The build script validates entries and archives them after a
  successful build.

See [AI Agent Prompt](#ai-agent-prompt) for the recommended agent instructions.

## Directory Structure

```
output/
├── config.toml                    # Global settings: media sources, defaults
├── search-positions.json          # Generated: content_id → tree positions map
├── 01/                            # Root node (numbered)
│   ├── index.toml                 # Node metadata, children are subfolders
│   ├── content.md                 # Text content — .md and/or .json per node
│   ├── locales/                   # Optional: translations
│   │   ├── eng.toml
│   │   └── swe.toml
│   ├── 01/                        # Child node
│   │   ├── index.toml
│   │   ├── content.md             # Markdown only (e.g., from Obsidian)
│   │   └── 01/                    # Grandchild — unlimited depth
│   │       ├── index.toml
│   │       ├── content.md
│   │       └── content.json       # Both formats (e.g., DOCX pipeline)
│   └── 02/
│       ├── index.toml
│       └── content.json           # JSON only (e.g., from docx2navTree)
├── 02/                            # Second root — may be a redirect
│   └── index.toml                 # redirect_to = "01/01/01" (no content)
└── 03/
    ├── index.toml
    └── content.md
```

The folder hierarchy is the tree. Numbered folders at each level correspond
to navigation nodes. This is the same convention used by bibel-wiki
(`templates/{name}/{category}/{story}`), generalized to unlimited depth
with numeric folder names.

## File Formats

### config.toml — Global Configuration

```toml
format_version = "2.0"
project_name = "My Knowledge Base"

default_language = "eng"
languages = ["eng", "swe", "fra"]

[pictures]
base_url = "https://cdn.example.com/images"
path_pattern = "{content_id}/{filename}"
thumbs_pattern = "{content_id}/thumbs/{filename}"
medium_pattern = "{content_id}/medium/{filename}"
local_dir = "media/pictures"

[audio]
base_url = "https://cdn.example.com/audio"
path_pattern = "{content_id}/{lang}/{filename}"
local_dir = "media/audio"
formats = ["mp3", "ogg"]

[video]
base_url = "https://cdn.example.com/video"
path_pattern = "{content_id}/{lang}/{filename}"
local_dir = "media/video"
formats = ["mp4", "webm"]
```

### index.toml — Node Metadata

Every node folder has an `index.toml`. This replaces both the old `node.toml`
(per-content metadata) and `tree.json` (navigation structure).

**Primary node (has content):**

```toml
content_id = "hermeneutics"
title = "Hermeneutics"
description = "The science and art of biblical interpretation"
thumbnail = "hermeneutics-cover.jpg"

# Pictures attached to this node
[[pictures]]
filename = "hermeneutics-overview.jpg"
caption = "Overview of interpretive methods"
alt = "Diagram showing hermeneutic approaches"

# Audio attached to this node
[[audio]]
filename = "hermeneutics-intro.mp3"
language = "eng"
duration_seconds = 342
timing_file = "hermeneutics-intro-timing.json"

# Localized titles (for multilingual navigation labels)
[locales.eng]
title = "Hermeneutics"
description = "The science and art of biblical interpretation"

[locales.swe]
title = "Hermeneutik"
description = "Konsten att tolka Bibeln"
```

**Redirect node (content lives elsewhere):**

```toml
content_id = "hermeneutics"
title = "Hermeneutics"
redirect_to = "01/03/02"
```

When an app encounters `redirect_to`, it fetches `index.toml` and content
from the target folder path instead. No content files exist at the redirect location.

#### Media Config Overrides

An `index.toml` can include `[pictures_config]`, `[audio_config]`, or
`[video_config]` sections that override the global `config.toml` media
settings for this node and all its descendants. Child nodes inherit from
the nearest ancestor that defines an override; `config.toml` is the
final fallback.

```toml
content_id = "the-good-story"
title = "The Good Story"

[pictures_config]
base_url = "https://cdn.example.com/tgs"
path_pattern = "{content_id}/{filename}"
thumbs_pattern = "{content_id}/thumbs/{filename}"
medium_pattern = "{content_id}/medium/{filename}"
```

The `_config` suffix distinguishes the override from the `[[pictures]]`
array-of-tables that lists attached media files.

#### App-Specific Metadata

`index.toml` is extensible — apps can add custom fields that the format
passes through without interpretation. For example, bibel-wiki uses
`canon` to indicate Old/New Testament:

```toml
content_id = "gods-creation"
title = "God's Creation"
canon = "nt"
```

### Node Content — `content.md` and/or `content.json`

A node's content can be provided as `content.md`, `content.json`, or both.
**Any single format is sufficient for V2 compliance.** Each pipeline writes
whichever format is natural to its source:

- Obsidian pipeline → `content.md` (source is markdown)
- DOCX pipeline (docx2navTree) → `content.json` (source is structured blocks)
- Either can optionally write both, but doesn't have to

Conversion scripts (`md_to_json.py`, `json_to_md.py`) are available to
generate one format from the other when an app needs it.

#### content.md — Markdown Content

The v2 format is **transparent to content syntax** — it preserves whatever
is in the markdown file without interpretation:

- Obsidian `[[wikilinks]]` pass through
- App-specific syntax like `[[t:locale.key]]` or `[[ref:BOOK C:V]]` passes through
- Standard markdown images, headings, lists, tables all work

**Obsidian source example:**
```markdown
See also [[Literary Genres]] and [[Historical Context]].
```

**Bibel-wiki source example:**
```markdown
### [[t:02.01.1_1.p_hd]]
![Image](43_Jn_01_02_RG.jpg)
[[ref:JHN 1:1-2]]
```

#### content.json — Structured Content Blocks

A JSON file containing a `ContentBlock[]` array, the same format used by
navtree-app's `ContentRenderer`. Apps that already consume this format
need no changes.

```json
{
  "content": [
    {
      "type": "paragraph",
      "text": "Some introductory text..."
    },
    {
      "type": "image",
      "path": "pictures/01/01/001.png",
      "alt": "Description",
      "caption": ""
    },
    {
      "type": "table",
      "rows": [
        {
          "cells": [
            {"text": "Animal"},
            {"text": "Temperature"}
          ]
        },
        {
          "cells": [
            {"text": "Cattle"},
            {"text": "38.5°C"}
          ]
        }
      ]
    },
    {
      "type": "heading",
      "text": "Section Title"
    }
  ]
}
```

**ContentBlock types:**

| Type | Fields | Description |
|------|--------|-------------|
| `paragraph` | `text` | Plain text (may contain inline formatting) |
| `heading` | `text` | Section heading |
| `image` | `path`, `alt`, `caption` | Image reference |
| `table` | `rows[].cells[].text` | Data table |

#### When both formats exist

When both `content.md` and `content.json` are present, they represent the
same content in different serializations. Neither is "the source of truth" —
both are derived from whatever produced them (vault, DOCX, etc.). If
hand-editing is needed, edit the `.md` and re-run the conversion script.

### search-positions.json — Search Result Linking

Maps each `content_id` to all tree positions where it appears, with
breadcrumbs for display.

```json
{
  "creation-care": [
    {
      "tree_id": "01/05/01",
      "breadcrumb": ["Five Marks of Mission", "Stewarding Creation", "Creation Care"]
    },
    {
      "tree_id": "02",
      "breadcrumb": ["Creation Care"]
    }
  ]
}
```

### Locale Files (Optional)

For nodes needing section-level or verse-level translations, place
locale TOML files alongside the node:

```
01/03/02/
├── index.toml
├── content.md              # and/or content.json
└── locales/
    ├── eng.toml
    └── swe.toml
```

Locale files use hierarchical keys scoped to the node's content sections:

```toml
title = "In the beginning"
description = "God creates the heavens and the earth"

[1_1]
p_hd = "God creates the heavens and the earth"

[1_3]
p_hd = "God separates light from darkness"
```

**When to use locale files vs. index.toml `[locales]`:**

| Need | Use |
|------|-----|
| Translated title + description only | `[locales.lang]` in `index.toml` |
| Section-level or verse-level translations | `locales/{lang}.toml` files |
| Both | Both — `index.toml` for nav labels, locale files for content |

### Audio Timing Files (Optional)

**Generic section timing:**

```json
{
  "audio_file": "hermeneutics-intro.mp3",
  "entries": [
    {
      "id": "intro",
      "label": "Introduction",
      "start_time": 0.0,
      "end_time": 45.2,
      "section_index": 0
    }
  ]
}
```

**Verse-based timing (for Bible content):**

```json
{
  "audio_file": "john-01-eng.mp3",
  "entries": [
    {
      "verse_start": 1,
      "verse_end": 2,
      "start_time": 0.5,
      "end_time": 2.3,
      "book_code": "JHN",
      "chapter": 1,
      "section_index": 0
    }
  ]
}
```

### redirects.toml — Multi-Position Content Log (in output)

Generated by the build script into the output folder.
Lists notes that appear at multiple tree positions:

```toml
# Auto-generated by build_navtree.py — do not edit manually.

[[multi_position]]
content = "Creation Care / Stewardship"
content_id = "creation-care"
positions = ["01/05/01", "02"]
primary = "01/05/01"
```

AI agents fetch this from the output (via raw GitHub URL after CI commits)
to know which notes are multi-position before making structural changes.

### vault-changelog.toml — Agent Change Log (in source vault)

Written by AI agents in the vault root whenever they make structural changes
to multi-position content. The build script validates entries against the
current vault state and archives them to `vault-changelog.archive.toml`
after a successful build.

```toml
[[change]]
date = "2026-06-02"
agent = "wiki-curator"
type = "rename"
note = "Creation Care"
new_name = "Creation Stewardship"
reason = "Aligning with updated terminology"
affected_positions = ["01/05/01", "02"]
```

**Change types:** `rename`, `restructure`, `split`, `delete`.

Notes not in `redirects.toml` can be changed freely without logging.

## Schema Summary

| File | Format | Generated or Manual | Purpose |
|------|--------|-------------------|---------|
| `config.toml` | TOML | Manual | Global settings, media CDN config |
| `{num}/index.toml` | TOML | Generated (then hand-editable) | Per-node metadata, media refs, optional media config overrides |
| `{num}/content.md` | Markdown | Manual (from Obsidian or other source) | Text content (syntax is transparent) |
| `{num}/content.json` | JSON | Generated (from DOCX or other source) | Structured ContentBlock[] array |
| `{num}/locales/{lang}.toml` | TOML | Manual | Translations (nav labels and/or deep content) |
| `search-positions.json` | JSON | Generated | `content_id` → tree positions map for search linking |
| `*-timing.json` | JSON | Generated (from audio tooling) | Audio-to-content sync (generic or verse-based) |
| `redirects.toml` | TOML | Generated (in output) | Multi-position content log for AI agents |
| `vault-changelog.toml` | TOML | Written by AI agents (in vault) | Structural change log, validated and archived by build |

## Comparison with v1 and bibel-wiki

| Aspect | navtree-app v1 | bibel-wiki | NavTree v2 |
|--------|---------------|------------|------------|
| Hierarchy depth | 3 levels (fixed) | 3 levels (fixed) | Unlimited |
| Tree structure | Folder scanning | TOML folder scanning | Folder hierarchy (same convention) |
| Content format | Embedded in JSON | Markdown per story | Markdown per node |
| Metadata | `_book.toml` | `index.toml` per level | `index.toml` per folder |
| Deduplication | None | None | `redirect_to` in `index.toml` |
| Images | Local, in content blocks | CDN with URL patterns | Both local and CDN |
| Audio | Not supported | External APIs + timing | Local or CDN + timing |
| Video | Not supported | Not supported | Local or CDN |
| Languages | Folder-per-language | Locale TOML files | Locale TOML files |
| Content syntax | JSON content blocks | `[[t:]]` `[[ref:]]` | Transparent — any syntax |
| Search index | Not supported | Not supported | `search-positions.json` |

## Build Pipeline

```
Source (Obsidian, DOCX, manual)
        ↓
  Source-specific parser
  (build_navtree.py, docx2navtree.py, etc.)
        ↓
  Writes: numbered folder hierarchy with index.toml + content.md and/or content.json
  Writes: search-positions.json
  Writes: config.toml (if not already present)
  Writes: redirects.toml in source vault (for AI agents)
        ↓
  Media enrichment modules (independent, optional)
  ├── add_pictures.py  — attaches images, updates index.toml
  ├── add_audio.py     — attaches audio + timing, updates index.toml
  └── add_video.py     — attaches video, updates index.toml
        ↓
  Web app (reads folder hierarchy + config.toml)
  └── Walks folders to build navigation
  └── Follows redirect_to for deduplicated content
  └── Resolves locale-specific titles from index.toml or locale files
  └── Renders URLs using numeric paths (language-neutral)
```

## AI Agent Prompt

When AI agents maintain the Obsidian vault that feeds the build pipeline,
include this instruction in their prompt. See the
[README](../README.md#recommended-agent-prompt) for the full prompt text
covering all change types, the changelog format, and the rules for when
logging is required vs. optional.
