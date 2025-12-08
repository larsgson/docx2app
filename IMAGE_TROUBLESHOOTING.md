# Image Troubleshooting Guide

This guide helps diagnose and fix image display issues in the chapter-viewer application.

## Quick Diagnostics

### Step 1: Run the Image Check Script

```bash
python3 check_images.py
```

This will:
- ✅ Verify all images referenced in JSON files exist on disk
- ✅ Check for format mismatches (WMF files with PNG extensions)
- ✅ Report statistics on image files

### Step 2: Clear Browser Cache

If images were recently fixed, your browser may have cached the old (broken) versions:

**Chrome/Edge:**
1. Open DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

**Firefox:**
1. Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)
2. Select "Cached Web Content"
3. Click "Clear Now"

**Or use Private/Incognito mode** to test without cache

### Step 3: Restart the Dev Server

```bash
cd chapter-viewer
npm run dev
```

Sometimes the Vite dev server needs to be restarted after file changes.

## Common Issues

### Issue 1: "Image load error" in Browser Console

**Symptoms:**
```
Image load error: {filename: 'image_160.png', attemptedPath: '/book_content_json/chapter_04/pictures/image_160.png'}
```

**Possible Causes:**

1. **Wrong chapter number in path** - The image might be in a different chapter
2. **File doesn't exist** - Image extraction failed during build
3. **Browser cache** - Old error cached from before fixes

**Solutions:**

```bash
# 1. Verify the image exists
ls chapter-viewer/public/book_content_json/chapter_04/pictures/image_160.png

# 2. Find which JSON references the image
grep -r "image_160" chapter-viewer/public/book_content_json/

# 3. Run diagnostics
python3 check_images.py

# 4. Clear browser cache and refresh
```

### Issue 2: Image Shows But Is Corrupted/Blank

**Symptoms:**
- Image loads but shows as blank or garbled

**Possible Causes:**
- WMF file with PNG extension (browser can't display WMF format)

**Solutions:**

```bash
# Check file format
file chapter-viewer/public/book_content_json/chapter_04/pictures/image_160.png

# If it shows "Windows metafile" instead of "PNG image data", convert it:
python3 fix_wmf_images.py
```

### Issue 3: Missing Images After Build

**Symptoms:**
- JSON references images that don't exist on disk

**Solutions:**

```bash
# Rebuild the book
python3 build_book.py

# Check for WMF conversion issues in the output
# You should see messages like:
#   ✓ chapter_01/pictures/image_001.png
#   ⚠️ WMF conversion failed: ...

# If WMF conversions fail, ensure tools are installed:
brew install imagemagick libreoffice
```

### Issue 4: All Images Missing

**Symptoms:**
- No images display at all

**Possible Causes:**
1. Vite dev server not serving the `public` directory correctly
2. Path configuration issue
3. Build hasn't been run

**Solutions:**

```bash
# 1. Verify images exist
ls chapter-viewer/public/book_content_json/chapter_01/pictures/

# 2. Check Vite is serving from public directory
# Images should be accessible at: http://localhost:3000/book_content_json/...

# 3. Restart Vite dev server
cd chapter-viewer
npm run dev
```

## Understanding Image Paths

### How Image Paths Work

**In JSON:**
```json
{
  "type": "image",
  "index": 160,
  "filename": "image_160.png",
  "path": "pictures/image_160.png"
}
```

**In React Component:**
```javascript
// If viewing chapter 3, section 5:
const imagePath = `/book_content_json/chapter_03/pictures/image_160.png`
```

**On Disk:**
```
chapter-viewer/
  public/
    book_content_json/
      chapter_03/
        pictures/
          image_160.png    ← Actual file
```

**In Browser:**
```
http://localhost:3000/book_content_json/chapter_03/pictures/image_160.png
```

### Path Construction Logic

The `ImageContent` component builds the path:

```javascript
const imagePath = item.path
  ? `/book_content_json/chapter_${chapterNum}//${item.path}`
  : `/book_content_json/chapter_${chapterNum}/pictures/${item.filename}`;
```

**Key Points:**
- `chapterNum` comes from the URL route parameter
- Images are chapter-specific (stored in each chapter's `pictures/` folder)
- Vite serves files from `public/` at the root URL

## Image Formats Supported

| Format | Browser Support | Notes |
|--------|-----------------|-------|
| PNG    | ✅ Full        | Preferred format |
| JPEG   | ✅ Full        | Used for photos |
| WMF    | ❌ None        | Must be converted to PNG |
| PDF    | ❌ None        | Must be converted to PNG |

## WMF Conversion Process

When WMF files are encountered during build:

```
WMF file → LibreOffice → PDF → ImageMagick → PNG
```

### Requirements

```bash
# macOS
brew install imagemagick libreoffice

# Ubuntu/Debian
sudo apt-get install imagemagick libreoffice

# Verify installation
which magick        # or 'which convert'
which libreoffice   # or 'which soffice'
```

### Manual Conversion

If automatic conversion fails:

```bash
# Convert a single WMF file
libreoffice --headless --convert-to pdf --outdir /tmp image.wmf
magick -density 300 /tmp/image.pdf -flatten png:image.png
```

## Error Messages Explained

### "Image not available" Fallback

After 2 retry attempts, the component shows a fallback:

```
⚠️
Image not available
image_160.png
```

This means:
1. Initial load failed
2. Retry 1 failed (after 500ms)
3. Retry 2 failed (after 1000ms)
4. Giving up and showing fallback

**Check browser console** for detailed error information.

### Console Error Details

```javascript
{
  filename: 'image_160.png',    // Image filename
  index: 160,                   // Sequential image number
  chapterNum: 4,                // Chapter being viewed
  attemptedPath: '/book_content_json/chapter_04/pictures/image_160.png',
  fullUrl: 'http://localhost:3000/book_content_json/chapter_04/pictures/image_160.png',
  retryCount: 0                 // Which retry attempt failed
}
```

Use this information to:
1. Verify the file exists at `attemptedPath`
2. Check if `chapterNum` is correct
3. Look for the image in other chapters

## Diagnostic Commands

```bash
# Count total images
find chapter-viewer/public/book_content_json -name "*.png" -o -name "*.jpg" | wc -l

# Find WMF files with wrong extensions
find chapter-viewer/public/book_content_json -name "*.png" -exec file {} \; | grep "Windows metafile"

# Search for a specific image
find chapter-viewer/public/book_content_json -name "image_160.png"

# Check which JSON references an image
grep -r "image_160" chapter-viewer/public/book_content_json/*.json

# Verify image format
file chapter-viewer/public/book_content_json/chapter_03/pictures/image_160.png

# List all images in a chapter
ls chapter-viewer/public/book_content_json/chapter_03/pictures/
```

## Preventive Measures

### Before Building

1. ✅ Ensure ImageMagick is installed
2. ✅ Ensure LibreOffice is installed
3. ✅ Check original DOCX file is present

### After Building

1. ✅ Run `python3 check_images.py`
2. ✅ Check build output for WMF conversion warnings
3. ✅ Verify sample images load in browser

### During Development

1. ✅ Use browser DevTools Network tab to see failed image requests
2. ✅ Check console for image load errors
3. ✅ Use "Disable cache" in DevTools while developing

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

3. **Gather browser info:**
   - Open DevTools Console
   - Copy any red error messages
   - Check Network tab for failed requests (red status codes)

4. **Provide information:**
   - Which chapter/section shows the error?
   - What does `image_report.txt` show?
   - Any errors in `build.log`?
   - Browser console errors?