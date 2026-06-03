# docx2navTree - Document to Structured JSON Converter

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Convert Microsoft Word documents into structured JSON content suitable for web applications, content management systems, or RAG (Retrieval-Augmented Generation) pipelines.

## Features

- **Multi-language support** - Process books in multiple languages from a single repo
- **Automatic TOC extraction** - Identifies chapters and sections from Table of Contents
- **NavTree v2 output** - Structured JSON with per-node metadata (index.toml)
- **Image extraction** - Extracts all images including WMF to PNG conversion
- **Table processing** - Preserves complex table structures
- **Markdown export** - Optional parallel Markdown output

## How This Repo Works

This is a **template repository**. It contains the build tools but no content.

To use it with your own documents, **fork it** to a private repository and add your content there. The `.gitignore` is structured so you can easily enable content tracking in your fork.

### Quick Start (Template)

Use the included sample document to verify the toolchain works:

```bash
make install-deps
make build
```

### Setting Up Your Fork

1. **Fork** this repo to your own (private) GitHub account
2. **Edit `.gitignore`** — remove the first section labeled "Content files — TEMPLATE ONLY"
3. **Add your content** to `lang-store/<lang>/` (see below)
4. **Commit** your content files — they are now tracked in your private fork

### .gitignore Structure

The `.gitignore` has three clearly marked sections:

| Section | Template repo | Your fork |
|---------|--------------|-----------|
| **Content files — TEMPLATE ONLY** | Ignored | **Remove this section** to track content |
| **Generated output** | Ignored | Keep ignored |
| **Standard ignores** | Ignored | Keep ignored |

## Content Organization

All source content lives under `lang-store/`, organized by language:

```
lang-store/
├── eng/
│   ├── book_config.toml       # Book metadata and settings
│   ├── original-book.docx     # Source Word document
│   └── exceptions.eng.conf    # TOC numbering fixes (optional)
├── fra/
│   ├── book_config.toml
│   ├── source-document.docx
│   └── cover.png
└── rus/
    ├── book_config.toml
    ├── source-document.docx
    └── exceptions.rus.conf
```

The build system auto-discovers files in each language directory.

### Book Configuration

Each language needs a `book_config.toml`. Copy from `book_config.toml.example`:

```toml
canonical_id = "my-book-title"
language = "eng"
title = "My Book Title"
is_original = true
pictures_location = "root"
```

If `title` is left empty, it will be extracted from the DOCX metadata or first paragraph.

## Building

```bash
# Build a specific language (default: eng)
make build L=eng
make build L=fra

# Build with images
make all L=eng

# See available languages
make help
```

## Output Structure (NavTree v2)

Generated output goes to `export/` (JSON) and `export_md/` (Markdown) — both are gitignored.

The folder hierarchy IS the navigation tree. Each section gets its own folder
with `index.toml` (metadata) and `content.json` (content blocks).

```
export/
├── {lang}/
│   └── {book_id}/
│       ├── config.toml                 # Global settings
│       ├── search-positions.json       # content_id → tree positions
│       ├── 01/                         # Chapter 1
│       │   ├── index.toml              # Chapter metadata
│       │   ├── content.json            # Chapter intro content
│       │   ├── 01/                     # Section 1.1
│       │   │   ├── index.toml
│       │   │   ├── content.json
│       │   │   └── 01/                 # Subsection 1.1.1
│       │   │       ├── index.toml
│       │   │       └── content.json
│       │   └── 02/                     # Section 1.2
│       │       ├── index.toml
│       │       └── content.json
│       └── 02/                         # Chapter 2
└── pictures/
    └── {lang}/
        └── {book_id}/
            └── 01/
                └── 01/
                    └── 001.png

export_md/                              # Parallel Markdown export
└── {lang}/
    ├── README.md
    ├── style.css
    └── 01/
        ├── intro.md
        └── 01.md
```

See [docs/navtree-v2-format.md](docs/navtree-v2-format.md) for the full format specification.

## Make Commands

```bash
make build           # Build JSON/Markdown for one language
make all             # Build JSON/Markdown + extract images
make rebuild-all     # Clean and rebuild from scratch
make clean           # Remove generated files
make check-deps      # Verify dependencies installed
make verify          # Check image integrity
make status          # Show project status
make stats           # Display content statistics
```

Use `L=<lang>` to select language: `make build L=fra`

## System Requirements

- **Python 3.8+** with python-docx
- **ImageMagick 7+** - Image processing
- **Ghostscript** - PDF to PNG conversion
- **LibreOffice** - WMF to PDF conversion (optional, for Windows Metafile images)

### Installation

**macOS:**
```bash
brew install imagemagick ghostscript
brew install --cask libreoffice
make install-deps
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install imagemagick ghostscript libreoffice python3-pip
make install-deps
```

## Document Preparation

**Important:** Convert automatic numbering to fixed text before processing.

Word/LibreOffice automatic numbering stores section numbers invisibly, causing missing sections in the output.

**Quick Fix:**
- **LibreOffice:** Select All → Format → Lists → No List → Save
- **Word:** Use the VBA macro in [DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md)

## Exception Handling

If your document has known numbering inconsistencies, create an exceptions file in your language directory (e.g., `lang-store/eng/exceptions.eng.conf`):

```
# Format: wrong_number = correct_number
10.7.7 = 10.7.5
21.4.3 = 21.2.3
```

## Documentation

- [docs/navtree-v2-format.md](docs/navtree-v2-format.md) - Output format specification
- [DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md) - Preparing Word documents
- [WMF_CONVERSION_GUIDE.md](WMF_CONVERSION_GUIDE.md) - WMF image conversion
- [MARKDOWN_GENERATION.md](MARKDOWN_GENERATION.md) - Markdown output details
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing to the template

## License

GNU General Public License v3.0 (GPL-3.0) - See [LICENSE](LICENSE) file.
