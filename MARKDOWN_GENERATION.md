# Markdown Generation Feature

## Overview

The build system generates **both JSON and Markdown** output simultaneously from Word documents. The Markdown output provides a human-readable format suitable for documentation, editing, and version control.

## Features

### Dual Output Format
- **JSON**: Structured md2rag-compatible format for applications
- **Markdown**: Human-readable format for documentation and editing

### Markdown Capabilities
- **Formatting Preservation** - Bold, italic, inline code
- **Tables** - Markdown table syntax
- **Headings** - Proper heading hierarchy
- **Navigation** - Breadcrumbs and quick links
- **Styling** - CSS included for consistent appearance

## Output Structure

```
export/                              # JSON output
├── {lang}/
│   └── {book_id}/
│       ├── _book.toml
│       └── XX_chapter_name/
│           └── ...
└── pictures/
    └── {lang}/
        └── {book_id}/
            └── ...

export_md/                           # Markdown output
├── README.md                        # Main index with chapter links
├── style.css                        # Styling
└── chapter_XX/
    ├── intro.md                     # Chapter introduction
    ├── section_XX.md                # Main sections
    └── section_XX_XX.md             # Subsections
```

## Configuration

In `build_book.py`:

```python
ENABLE_MARKDOWN = True       # Enable/disable markdown generation
MARKDOWN_DIR = "export_md"   # Output directory
```

## Usage

### Build Both Formats

```bash
make build
```

This generates JSON in `export/` and Markdown in `export_md/`.

### Disable Markdown Generation

```python
# In build_book.py
ENABLE_MARKDOWN = False
```

### View Markdown Output

```bash
# Open index
open export_md/README.md

# Or navigate to any section
open export_md/chapter_01/section_01.md
```

## Sample Output

### Section File Example

```markdown
<link rel="stylesheet" href="../style.css">

[Home](../README.md) → [Chapter 1](intro.md) → Section 2

---

# 1.2 Section Title

Content paragraph here...

| Feature | Description |
| --- | --- |
| JSON Output | Structured data format |
| Markdown Output | Human-readable format |

---

<div class="nav-links">
<a href="../README.md">← Back to Index</a>
<a href="intro.md">Chapter Home</a>
</div>
```

## CSS Styling

The `style.css` file provides:

- **Colors**: Professional theme
- **Typography**: System fonts, readable line height
- **Layout**: Centered, max-width container
- **Tables**: Striped rows, borders
- **Print**: Print-friendly stylesheet

## Benefits

| Use Case | Benefit |
|----------|---------|
| Documentation | Human-readable backup format |
| Version Control | Text-based, easy to diff |
| Editing | Works with any text editor |
| Distribution | No build process needed to read |
| Conversion | Can convert to PDF, HTML, etc. |

## Comparison: JSON vs Markdown

| Feature | JSON | Markdown |
|---------|------|----------|
| Format | Structured data | Human-readable text |
| Use Case | Applications, RAG | Documentation, editing |
| Editing | Requires parsing | Direct text editing |
| Size | Larger | Smaller |
| Searchable | Requires parsing | Native text search |

## Notes

- Markdown structure mirrors the chapter structure
- CSS links included in each file for rendering
- Navigation uses relative paths for portability
- Best viewed in markdown viewers that support inline HTML/CSS
