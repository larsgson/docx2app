# Document Conversion System

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)

A comprehensive automated system to convert Microsoft Word documents into an interactive web-based reader with JSON content backend. This system can be adapted for any large document with chapter/section structure.

## 🎯 Standalone Chapter Viewer

The `chapter-viewer` directory is a **fully self-contained React application** that can be used independently:

- ✅ **Extract and use separately** - Copy the `chapter-viewer` folder to create your own book viewer
- ✅ **Reusable for any book** - Just provide your own JSON content
- ✅ **No dependencies on parent project** - All book data stored within the viewer directory
- ✅ **Ready to deploy** - Complete standalone web application
- ✅ **Easy to customize** - Modern React codebase with clear structure

### Using the Viewer Standalone

```bash
# Copy the viewer to create your own project
cp -r chapter-viewer my-book-viewer
cd my-book-viewer

# Add your book content to book_content_json/
# (Follow the JSON format described in chapter-viewer/README.md)

# Install and run
pnpm install
pnpm dev
```

The viewer becomes a **universal book reader** - perfect for documentation, handbooks, manuals, or any structured content!

See [chapter-viewer/README.md](chapter-viewer/README.md) for detailed standalone usage instructions.

### Distributing Your Book as a Standalone Viewer

After building your book, you can distribute the complete viewer:

```bash
# Build your book
make build

# The chapter-viewer directory is now self-contained!
# Package it for distribution:
tar -czf my-book-viewer.tar.gz chapter-viewer/

# Or just copy it anywhere:
cp -r chapter-viewer /path/to/my-book-viewer

# Recipients can use it immediately:
cd my-book-viewer
pnpm install
pnpm dev
```

The `chapter-viewer` directory contains:
- ✅ All book content in `book_content_json/`
- ✅ All images in `book_content_json/chapter_XX/pictures/`
- ✅ Complete React application
- ✅ Ready to run with no external dependencies

This makes it perfect for:
- 📦 Distributing documentation as a web app
- 🌐 Hosting on GitHub Pages, Netlify, Vercel
- 💿 Sharing as an offline viewer
- 📚 Creating multiple book viewers from one codebase

## Features

- 🚀 **One-command build** - Single `make build` converts entire document
- 📚 **Smart chapter detection** - Automatically identifies chapters and sections
- 🖼️ **Image extraction** - Extracts all images including WMF conversion
- 📊 **Table processing** - Preserves complex table structures including headers in cells
- 🎨 **Format preservation** - Maintains bold, italic, fonts, alignment
- ✅ **TOC validation** - Automatically extracts and validates table of contents
- 📝 **Dual output format** - Generates both JSON and Markdown simultaneously
- 🔍 **Verification tools** - Built-in integrity checking
- 📱 **React web viewer** - Responsive mobile-friendly interface

## ⚠️ Document Preparation (CRITICAL FIRST STEP!)

**You MUST convert automatic numbering to fixed text before processing.**

Automatic numbering in Word/LibreOffice stores section numbers (like "3.1", "4.2.3") invisibly in the document's internal structure. This causes missing sections and failed TOC validation.

**Quick Fix:**
- **LibreOffice:** Select All → Format → Lists → No List → Save
- **Word:** Select All → Ctrl+Shift+N → Numbering → None → Save

**📖 See [DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md) for detailed instructions, verification steps, and troubleshooting.**

---

## Quick Start

```bash
# 1. Install dependencies
make install-deps

# 2. Build the book
make build

# 3. Start the web viewer
make viewer
```

Open your browser to `http://localhost:3000` to view the book.

## System Requirements

### Required Dependencies

- **Python 3.8+** with python-docx
- **ImageMagick 7+** - Image processing
- **Ghostscript** - PDF to PNG conversion
- **LibreOffice** - WMF to PDF conversion
- **Node.js 16+** - Web viewer

### Installation

**macOS:**
```bash
brew install imagemagick ghostscript
brew install --cask libreoffice
make install-deps
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install imagemagick ghostscript libreoffice python3-pip nodejs npm
make install-deps
```

**macOS LibreOffice Setup:**

If LibreOffice was installed via DMG (not Homebrew), run:
```bash
make setup-libreoffice
```

This creates a symlink so ImageMagick can access LibreOffice.

## What It Does

### Build Pipeline

```
Word Document
    ↓
1. Extract TOC automatically
2. Extract chapters & sections with TOC validation
3. Parse text with formatting
4. Extract images (WMF → PNG)
5. Process tables (including headers in cells)
6. Build navigation index
    ↓
Interactive Web Viewer
```

### Detailed Steps

1. **TOC Extraction** - Automatically extracts Table of Contents from document
2. **Chapter Detection** - Identifies chapters by N.0 headings (e.g., "1.0 Introduction")
3. **Section Parsing** - Subdivides chapters into N.X sections (e.g., "1.1", "1.2")
4. **Content Extraction** - Preserves formatting, images, tables, footnotes
5. **Table Cell Headers** - Detects and processes section headers inside table cells
6. **WMF Conversion** - Converts Windows Metafiles to PNG via LibreOffice → PDF → PNG
7. **Index Building** - Creates navigation structure with statistics

## Usage

### Build Commands

```bash
make build           # Build complete book content
make rebuild-all     # Clean and rebuild from scratch
make clean           # Remove generated files
```

### Development Commands

```bash
make dev             # Build and start viewer in one command
make viewer          # Start chapter-viewer dev server
make status          # Show current project status
make stats           # Display content statistics
```

### Verification Commands

```bash
make check-deps      # Verify all dependencies installed
make verify          # Check image integrity and content
```

## Project Structure

```
project-root/
├── build_book.py                    # Main build system (JSON output)
├── verify_images.py                 # Image verification tool
├── Makefile                         # Build automation
├── setup_libreoffice.sh             # LibreOffice configuration helper
├── requirements.txt                 # Python dependencies
├── LICENSE                          # GPL-3.0 license
│
├── original-book.docx               # Source document (not in repo)
│
├── markdown_chapters/               # Markdown export (optional, not in repo)
│   ├── README.md                    # Navigation index
│   └── chapter_XX/                  # Chapter directories
│       ├── section_X_X.md           # Section content
│       └── pictures/                # Extracted images
│
└── chapter-viewer/                  # STANDALONE React web application
    ├── book_content_json/           # Book data (self-contained!)
    │   ├── index.json               # Navigation index
    │   ├── toc_structure.json       # Table of contents
    │   └── chapter_XX/              # Chapter directories
    │       ├── chapter.json         # Chapter metadata
    │       ├── section_XX.json      # Section content
    │       └── pictures/            # Chapter images
    ├── src/                         # React source code
    ├── public/
    │   └── book_content_json/       # Symlink to ../book_content_json/
    ├── package.json
    └── README.md                    # Standalone usage guide
```

## Output Format

### JSON Structure

Each section file contains:
```json
{
  "chapter_number": 1,
  "chapter_title": "1.0 FIRST CHAPTER",
  "content": [
    {
      "type": "paragraph",
      "index": 0,
      "text": "Full paragraph text",
      "runs": [
        {"text": "Bold text", "bold": true, "font_size": 12.0}
      ],
      "alignment": "LEFT (0)"
    },
    {
      "type": "table",
      "rows": 3,
      "cols": 2,
      "cells": [...]
    }
  ],
  "statistics": {
    "paragraphs": 78,
    "tables": 1,
    "images": 10
  }
}
```

## Key Features

### Smart Chapter Detection

Handles both standard chapters (N.0 format) and appendix-style chapters (starting with N.1):

- **Regular chapters:** Start with N.0 heading (e.g., "1.0 Introduction")
- **Appendix chapters:** Start with N.1 section (e.g., "24.1 First Section")

### TOC Validation System

- Extracts entire Table of Contents 
- Excludes TOC paragraphs from actual content
- Cross-validates TOC against actual content
- Generates detailed discrepancy report
- Uses actual content titles as source of truth

### WMF Image Conversion

Automatically converts Windows Metafile images using the conversion chain:

```
WMF → LibreOffice → PDF → Ghostscript → PNG
```

This ensures all images are properly displayed in modern web browsers.

### Table Cell Header Support

The system detects and processes section headers that appear inside table cells, maintaining proper chapter/section hierarchy even when headers are embedded in complex table layouts.

## Configuration

Edit `build_book.py` to customize:

```python
INPUT_DOCX = "original-book.docx"
JSON_DIR = "chapter-viewer/book_content_json"
EXCEPTIONS_FILE = "conf/exceptions.conf"
```

## Build Process

The build system provides real-time feedback showing:

- Number of TOC entries extracted
- Chapters and sections detected
- Paragraphs and tables processed
- Images extracted and converted
- Build completion time

## Troubleshooting

### WMF Images Not Converting

```bash
# Check if LibreOffice is accessible
libreoffice --version

# If not found, configure it
make setup-libreoffice

# Rebuild
make rebuild-all
```

### Images Not Loading in Viewer

```bash
# Check image integrity
make verify

# If issues found, rebuild
make rebuild-all
```

### Build Fails with Missing Dependencies

```bash
# Check what's missing
make check-deps

# Install dependencies
make install-deps
```

### Content Not Updating

```bash
# Clean and rebuild
make clean
make build

# Force browser refresh
# Chrome/Firefox: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)
```

## Advanced Usage

### TOC Extraction

The system automatically extracts the Table of Contents directly from the document during the build process:

```bash
# TOC is automatically extracted during build
make build
# TOC structure is extracted internally and used for validation
```

**Features:**
- ✅ Automatically extracts all TOC entries from document
- ✅ Handles extra spaces in numbering (e.g., "3. 1", "21. 2")
- ✅ Supports Unicode smart quotes in titles
- ✅ Filters out false positives (dosages, measurements)
- ✅ Validates section headers against TOC during parsing
- ✅ Handles headers inside table cells

### Custom Document Processing

To process your own Word document:

1. **Prepare your document** - Convert automatic numbering to fixed text (see [DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md))
2. Place your `.docx` file in the project root
3. Name the book "original-book.docx" or else update `INPUT_DOCX` in `build_book.py`
4. Create `conf/exceptions.conf` if you have known numbering errors
5. Run `make rebuild-all`

### Exception Handling

If your document has known numbering inconsistencies, create `conf/exceptions.conf`:

```
# Format: wrong_number = correct_number
10.7.7 = 10.7.5
10.7.8 = 10.7.6
21.4.3 = 21.2.3
```

The system will automatically correct these during parsing.

### Accessing Build Reports

After build, check:
- Console output shows TOC extraction and validation statistics
- Build process reports number of TOC entries extracted and numbered entries found

## Documentation

- **[DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md)** - ⚠️ **START HERE** - Document preparation (convert automatic numbering)
- **[WMF_CONVERSION_GUIDE.md](WMF_CONVERSION_GUIDE.md)** - Image conversion guide
- **[MARKDOWN_GENERATION.md](MARKDOWN_GENERATION.md)** - Markdown output feature guide
- **[chapter-viewer/README.md](chapter-viewer/README.md)** - Web viewer documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

### Main Scripts

- **[build_book.py](build_book.py)** - Main build system with integrated TOC extraction
- **[verify_images.py](verify_images.py)** - Image verification tool

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make verify` to check integrity
5. Submit a pull request

## License

This project is licensed under the **GNU General Public License v3.0** (GPL-3.0).

This means you can:
- ✅ Use commercially
- ✅ Modify the code
- ✅ Distribute
- ✅ Use privately

Under the conditions:
- 📋 Disclose source
- 📋 License and copyright notice
- 📋 Same license for derivatives
- 📋 State changes made

See [LICENSE](LICENSE) file for full details.


## Acknowledgments

- **python-docx** - Word document parsing
- **ImageMagick** - Image processing
- **LibreOffice** - Document conversion
- **React** - Web viewer interface
- **Vite** - Build tooling

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section above
2. Review existing issues on GitHub
3. Create a new issue with:
   - System information (OS, Python version, etc.)
   - Output of `make check-deps`
   - Error messages or unexpected behavior
   - Steps to reproduce

## Roadmap

Potential future enhancements:
- [ ] Support for more document formats (PDF, EPUB input)
- [ ] Full-text search in viewer
- [ ] Export to EPUB/PDF from JSON
- [ ] Image optimization options
- [ ] Multi-language support
- [ ] Cloud deployment guides
- [ ] Docker containerization

---

**Note:** This repository does not include source Word documents or generated content. You'll need to provide your own document to process.
