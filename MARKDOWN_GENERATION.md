# Markdown Generation Feature

## Overview

The build system generates **both JSON and Markdown** output simultaneously from Word documents. The Markdown output provides a human-readable format suitable for documentation, editing, and version control.

## Features

### Dual Output Format
- **JSON**: NavTree v2 format with `content.json` + `index.toml` per node
- **Markdown**: Human-readable format for documentation and editing

### Markdown Capabilities
- **Formatting Preservation** - Bold, italic, inline code
- **Tables** - Markdown table syntax
- **Headings** - Proper heading hierarchy
- **Navigation** - Breadcrumbs and quick links
- **Styling** - CSS included for consistent appearance

## Output Structure

```
export/                              # NavTree v2 JSON output
├── {lang}/
│   └── {book_id}/
│       ├── config.toml
│       ├── search-positions.json
│       └── 01/                      # Each node = folder
│           ├── index.toml
│           ├── content.json
│           └── 01/
│               ├── index.toml
│               └── content.json

export_md/                           # Markdown output
├── {lang}/
│   ├── README.md                    # Main index with chapter links
│   ├── style.css                    # Styling
│   └── 01/
│       ├── intro.md                 # Chapter introduction
│       ├── 01.md                    # Section 1.1
│       └── 01_01.md                 # Subsection 1.1.1
```

## Usage

```bash
# Build a language (generates both JSON and Markdown)
make build L=eng
```

This generates JSON in `export/` and Markdown in `export_md/`.

### View Markdown Output

```bash
open export_md/eng/README.md
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
