# Markdown Generation Feature

## Overview

The build system now generates **both JSON and Markdown** output simultaneously from Word documents. The Markdown output mirrors the structure of the chapter-viewer and includes CSS styling that matches the web interface.

## Features

### Dual Output Format
- **JSON**: For the interactive chapter-viewer React app
- **Markdown**: Human-readable format for documentation, editing, and version control

### Markdown Capabilities
✅ **Formatting Preservation**
- Bold, italic, and combined formatting
- Inline code and code blocks
- Lists (bullet and numbered)

✅ **Structural Elements**
- Tables with markdown syntax
- Proper heading hierarchy (H1, H2, H3)
- Section headers in table cells

✅ **Navigation**
- Breadcrumb navigation at top
- Quick links at bottom
- Index page with full chapter listing
- Internal links between sections

✅ **Styling**
- CSS that matches chapter-viewer appearance
- Responsive design (mobile-friendly)
- Print-friendly formatting
- Professional typography

## Output Structure

```
markdown_chapters/
├── README.md                    # Main index with chapter links
├── style.css                    # Styling matching chapter-viewer
└── chapter_XX/
    ├── intro.md                 # Chapter introduction
    ├── section_XX.md            # Main sections
    └── section_XX_XX.md         # Subsections
```

## Sample Output

### Section File Example

```markdown
<link rel="stylesheet" href="../style.css">

[Home](../README.md) → [Chapter 1](intro.md) → Section 2 → Subsection 1

---

# 1.2.1

**1.2.1 Technical Scope**

The technical scope includes:

**Python** programming language for backend processing.

| Feature | Description |
| --- | --- |
| JSON Output | Structured data format |
| Markdown Output | Human-readable format |

---

<div class="nav-links">
<a href="../README.md">← Back to Index</a>
<a href="intro.md">Chapter 1 Home</a>
</div>
```

## Configuration

In `build_book.py`:

```python
ENABLE_MARKDOWN = True           # Enable/disable markdown generation
MARKDOWN_DIR = "markdown_chapters"
INPUT_DOCX = "original-book.docx"
```

## Usage

### Build Both Formats

```bash
make build
```

This generates:
- `chapter-viewer/book_content_json/` - JSON for web viewer
- `markdown_chapters/` - Markdown files

### View Markdown Output

```bash
# Open index
open markdown_chapters/README.md

# Or navigate to any section
open markdown_chapters/chapter_01/section_01.md
```

### Disable Markdown Generation

```python
# In build_book.py
ENABLE_MARKDOWN = False
```

## CSS Styling

The `style.css` file provides:

- **Colors**: Matching chapter-viewer theme
  - Primary: #2c3e50
  - Accent: #3498db
  - Background: #ffffff

- **Typography**: System fonts for native look
  - Headers: Bold with accent underlines
  - Body: 1.6 line height for readability
  - Code: Monospace with gray background

- **Layout**
  - Max width: 800px centered
  - Responsive breakpoints
  - Print stylesheet

- **Tables**
  - Striped rows
  - Border styling
  - Hover effects

## Testing

Tested with `sample-book.docx` containing:
- 2 chapters
- 5 sections (1.1, 1.2, 2.1, 2.2, 2.2.1)
- 3 subsections
- Mixed formatting (bold, italic)
- Tables
- Lists (bullet and numbered)

### Test Results
✅ All markdown files generated correctly  
✅ Navigation links functional  
✅ CSS applied properly  
✅ Tables formatted as markdown  
✅ Formatting preserved  
✅ Index created with all links  

## Benefits

### For Documentation
- Human-readable backup format
- Easy to search and grep
- Version control friendly (text-based)
- Can be edited with any text editor

### For Distribution
- No build process needed to read
- Works in any markdown viewer
- Can be converted to other formats (PDF, HTML)
- Lightweight and portable

### For Development
- Quick preview without running web server
- Easy to diff changes
- Can be included in git repositories
- Ideal for code review

## Comparison: JSON vs Markdown

| Feature | JSON | Markdown |
|---------|------|----------|
| Format | Structured data | Human-readable text |
| Use Case | Web viewer | Documentation, editing |
| Styling | Applied by React | CSS in markdown viewers |
| Editing | Requires parsing | Direct text editing |
| Size | Larger | Smaller |
| Searchable | Requires parsing | Native text search |
| Version Control | JSON diff | Clean text diff |

## Future Enhancements

Potential additions:
- [ ] Image embedding (base64 or file references)
- [ ] Footnote handling
- [ ] Cross-reference links between sections
- [ ] Export to PDF via markdown
- [ ] Syntax highlighting for code blocks
- [ ] Table of contents per chapter
- [ ] Search index generation

## Notes

- The markdown output structure mirrors the JSON structure exactly
- CSS links are included in each file for proper rendering
- Navigation uses relative paths for portability
- Tables require markdown-compatible viewers
- Best viewed in viewers that support inline HTML and CSS

---

**Part of the Document Conversion System**
