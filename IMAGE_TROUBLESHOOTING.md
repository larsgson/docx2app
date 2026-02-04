# Image Troubleshooting Guide

This guide helps diagnose and fix image extraction and conversion issues.

## Quick Diagnostics

### Step 1: Run the Image Check Script

```bash
python3 check_images.py
```

This will:
- Verify all images referenced in JSON files exist on disk
- Check for format mismatches (WMF files with PNG extensions)
- Report statistics on image files

### Step 2: Check Build Output

Review the build output for image-related warnings:

```bash
python3 build_book.py 2>&1 | grep -i "image\|wmf\|png"
```

## Common Issues

### Issue 1: WMF Images Not Converting

**Symptoms:**
- Build shows WMF conversion warnings
- Image files exist but are actually WMF format with .png extension

**Solutions:**

```bash
# Check file format
file export/pictures/eng/*/chapter_name/section_name/image_001.png

# If it shows "Windows metafile" instead of "PNG image data":

# 1. Ensure conversion tools are installed
brew install imagemagick libreoffice  # macOS
# or
sudo apt-get install imagemagick libreoffice  # Ubuntu

# 2. Verify LibreOffice is accessible
libreoffice --version

# 3. On macOS, run setup if needed
make setup-libreoffice

# 4. Rebuild
make rebuild-all
```

### Issue 2: Missing Images After Build

**Symptoms:**
- JSON references images that don't exist on disk

**Solutions:**

```bash
# Check for extraction issues
python3 check_images.py

# Rebuild the book
make rebuild-all

# Check output for errors
python3 build_book.py 2>&1 | tee build.log
```

### Issue 3: Image Shows Corrupted/Blank

**Symptoms:**
- Image file exists but shows as blank or garbled

**Possible Causes:**
- WMF file with PNG extension (needs conversion)
- Corrupted during extraction

**Solutions:**

```bash
# Check actual file format
file export/pictures/eng/*/chapter_name/section_name/image_001.png

# Run WMF fixer if needed
python3 fix_wmf_images.py

# Or rebuild
make rebuild-all
```

## Image Formats

| Format | Support | Notes |
|--------|---------|-------|
| PNG    | Full    | Preferred output format |
| JPEG   | Full    | Used for photos |
| WMF    | Convert | Automatically converted to PNG |
| GIF    | Full    | Preserved as-is |

## WMF Conversion Process

When WMF files are encountered during build:

```
WMF → LibreOffice → PDF → ImageMagick/Ghostscript → PNG
```

### Requirements

```bash
# macOS
brew install imagemagick ghostscript
brew install --cask libreoffice

# Ubuntu/Debian
sudo apt-get install imagemagick ghostscript libreoffice

# Verify installation
which magick        # or 'which convert'
which libreoffice
which gs            # Ghostscript
```

### Manual Conversion

If automatic conversion fails:

```bash
# Convert a single WMF file
libreoffice --headless --convert-to pdf --outdir /tmp image.wmf
magick -density 300 /tmp/image.pdf -flatten image.png
```

## Diagnostic Commands

```bash
# Count total images
find export/pictures -name "*.png" -o -name "*.jpg" | wc -l

# Find WMF files with wrong extensions
find export/pictures -name "*.png" -exec file {} \; | grep -i "metafile"

# Search for a specific image
find export/pictures -name "image_001.png"

# Check which JSON references an image
grep -r "image_001" export/eng/

# List all images for a book
find export/pictures/eng/book_id -type f -name "*.png" | head -20
```

## Output Structure

Images are stored at the root level in a hierarchical structure:

```
export/
└── pictures/
    └── {lang}/
        └── {book_id}/
            ├── chapter_name/
            │   └── section_name/
            │       ├── image_001.png
            │       └── image_002.png
            └── manifest.json     # Image metadata
```

The `manifest.json` contains alt text and captions for each image.

## Preventive Measures

### Before Building

1. Ensure ImageMagick is installed
2. Ensure Ghostscript is installed
3. Ensure LibreOffice is installed and accessible
4. Check original DOCX file is present

### After Building

1. Run `python3 check_images.py`
2. Check build output for WMF conversion warnings
3. Verify sample images are valid PNG/JPEG files

## Getting Help

If you're still experiencing issues:

1. **Run diagnostics:**
   ```bash
   python3 check_images.py > image_report.txt
   ```

2. **Check build logs:**
   ```bash
   python3 build_book.py 2>&1 | tee build.log
   ```

3. **Provide information:**
   - Output of `make check-deps`
   - Contents of `image_report.txt`
   - Any errors in `build.log`
