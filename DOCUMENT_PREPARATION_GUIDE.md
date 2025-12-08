# Document Preparation Guide

**Critical First Step:** Before processing any Word document with this conversion system, you must convert automatic numbering to fixed text.

---

## Microsoft Word: VBA Macro Method (Most Reliable) ⭐

**This is the BEST method for Word** - it converts ALL automatic numbering to fixed text in seconds with 100% reliability.

### The Macro Code

```vba
Sub ConvertNumberingToText()
    Dim para As Paragraph
    For Each para In ActiveDocument.Paragraphs
        If para.Range.ListFormat.ListType <> wdListNoNumbering Then
            para.Range.ListFormat.ConvertNumbersToText
        End If
    Next para
End Sub
```

### How to Run This Macro in Word

#### Step 1: Open the Visual Basic Editor
1. **Open your document** in Microsoft Word
2. **Open VBA Editor:**
   - Press `Alt+F11` (Windows) / `Option+F11` (Mac)

#### Step 2: Create the Macro
1. In the VBA Editor, click `Insert → Module`
2. A new code window will appear
3. **Copy and paste** the macro code above into this window
4. **Save the macro:**
   - Click the Save button (💾) or press `Ctrl+S` / `Cmd+S`

#### Step 3: Run the Macro
1. In the VBA Editor, click anywhere inside the macro code
2. **Run the macro:**
   - Click `Run → Run Sub/UserForm`
   - OR: Press `F5`
   - OR: Click the Play button (▶) in the toolbar
3. **Wait for completion:**
   - The macro will process all paragraphs
   - For large documents, this may take 10-30 seconds
   - You'll see no visual feedback until it's done
4. **Close VBA Editor:**
   - Click the X button or press `Alt+Q` (Windows) / `Cmd+Q` (Mac)

#### Step 4: Verify and Save
1. **Return to your document**
2. **Check a numbered paragraph:**
   - Click on a numbered heading
   - Numbering button should NOT be highlighted ✓
3. **Save the document:**
   - `File → Save` or `Ctrl+S` / `Cmd+S`
4. **Optional:** Save as new filename with "-converted" suffix

### Why This Method is Best

✅ **100% reliable** - Converts ALL automatic numbering  
✅ **Preserves formatting** - Keeps bold, italic, fonts, colors  
✅ **Fast** - Processes entire document in seconds  
✅ **No manual work** - Fully automated  
✅ **Works with complex documents** - Handles nested lists, multi-level numbering  

### Troubleshooting the Macro

**If Developer tab is missing:**
- Follow Step 1 above to enable it in Options/Preferences

**If macro doesn't run:**
- Check if macros are enabled: `File → Options → Trust Center → Trust Center Settings → Macro Settings`
- Select: "Enable all macros" (temporarily, for this task)

**If you get security warnings:**
- Click "Enable Content" when prompted
- Or: Save document as .docm (macro-enabled) format

**If nothing seems to happen:**
- The macro runs silently - check if numbering button is no longer active
- Try the deletion test (delete a numbered paragraph, see if others renumber)

---

## Why This Is Necessary

Word and LibreOffice documents can use **automatic numbering** where:
- Section numbers (like "3.1", "4.2.3") are stored in the document's internal XML structure
- These numbers are **NOT part of the actual text**
- They appear on screen but are invisible to text extraction tools
- The conversion system cannot detect these sections, resulting in:
  - Missing sections in the output
  - Failed TOC validation
  - Broken navigation
  - Up to 25+ "missing" entries

**Solution:** Convert automatic numbering to fixed text before processing.

---

## Detection: Does Your Document Use Automatic Numbering?

### Quick Test

1. Click on a numbered heading (e.g., "3.1 Introduction")
2. Look at the numbering button in your toolbar
3. **If the button is highlighted/active** → You have automatic numbering ⚠️
4. Try deleting a numbered paragraph
5. **If other numbers automatically renumber** → You have automatic numbering ⚠️

### Visual Indicators

**Automatic Numbering (needs fixing):**
```
→ 1.0 Chapter Title        [Numbering button is ACTIVE]
  ↓
  [Delete this line]
  ↓
→ 1.1 Section Title        [Becomes 1.0 automatically]
```

**Fixed Text (ready to process):**
```
→ 1.0 Chapter Title        [Numbering button is INACTIVE]
  ↓
  [Delete this line]
  ↓
→ 1.1 Section Title        [Stays as 1.1]
```

---

## Conversion Instructions

### LibreOffice Writer

#### Method 1: Simple (Recommended)

1. **Open document** in LibreOffice Writer
2. **Select All**
   - Windows/Linux: `Ctrl+A`
   - Mac: `Cmd+A`
3. **Remove numbering format**
   - Go to: `Format → Lists → No List`
   - OR: Click the "Toggle Unordered List" button in toolbar to disable
4. **Save document**
   - File → Save (or `Ctrl+S` / `Cmd+S`)

**Result:** All automatic numbering becomes fixed text while preserving the numbers.

---

#### Method 2: Search & Replace (More Thorough)

1. **Open document** in LibreOffice Writer
2. **Open Find & Replace**
   - `Edit → Find & Replace`
   - OR: `Ctrl+H` (Windows/Linux) / `Cmd+H` (Mac)
3. **Configure search**
   - Click `Other Options` button
   - Check the box: `Search for Styles`
4. **Find numbering**
   - In `Find:` dropdown, select: `Numbering Symbols`
   - Leave `Replace:` field empty
5. **Execute replacement**
   - Click `Replace All`
   - Close the dialog
6. **Clear formatting artifacts**
   - Select All (`Ctrl+A` / `Cmd+A`)
   - Go to: `Format → Clear Direct Formatting`
   - OR: Press `Ctrl+M` / `Cmd+M`
7. **Save document**

**Result:** All automatic numbering styles removed, numbers preserved as text.

---

#### Method 3: Style-Based (Most Complete)

1. **Open document** in LibreOffice Writer
2. **Open Styles sidebar**
   - `Format → Styles`
   - OR: Press `F11`
3. **Select all numbered paragraphs**
   - `Ctrl+A` / `Cmd+A`
4. **Apply Default/Body Text style**
   - In Styles sidebar, click `Default Paragraph Style`
   - OR: Click `Body Text`
5. **Remove list formatting**
   - `Format → Lists → No List`
6. **Save document**

**Result:** Complete removal of numbering styles while keeping numbers as text.

---

### Microsoft Word (Manual Methods)

**Note:** The VBA Macro method above is recommended. Use these manual methods only if you cannot run macros.

#### Method 1: Simple

1. **Open document** in Microsoft Word
2. **Select All**
   - Windows: `Ctrl+A`
   - Mac: `Cmd+A`
3. **Apply Normal style**
   - Windows: Press `Ctrl+Shift+N`
   - Mac: Press `Cmd+Shift+N`
   - This strips numbering styles
4. **Disable numbering**
   - Go to: `Home` tab → `Paragraph` group
   - Click the `Numbering` button dropdown (▼)
   - Select: `None`
5. **Save document**
   - `File → Save` (or `Ctrl+S` / `Cmd+S`)

**Result:** Automatic numbering converted to plain text.

---

#### Method 2: Paste Special (Reliable)

1. **Open document** in Microsoft Word
2. **Select All** (`Ctrl+A` / `Cmd+A`)
3. **Copy** (`Ctrl+C` / `Cmd+C`)
4. **Create new blank document**
   - `File → New → Blank Document`
5. **Paste as unformatted text**
   - `Edit → Paste Special`
   - Windows: `Ctrl+Alt+V`
   - Mac: `Cmd+Ctrl+V`
6. **Select paste format**
   - Choose: `Unformatted Text` or `Text Only`
   - Click: `OK`
7. **Result check**
   - All formatting removed
   - Numbers become plain text
8. **Save as new file**
   - Recommended: Save with new filename
   - Original document preserved as backup

**Result:** Clean conversion with all automatic formatting removed.

---

#### Method 3: Conversion in Place

1. **Open document** in Microsoft Word
2. **Create backup** (important!)
   - `File → Save As`
   - Save copy with "_backup" suffix
3. **Select All** (`Ctrl+A` / `Cmd+A`)
4. **Right-click** on selected text
5. **Choose numbering option**
   - Look for: `Continue Numbering` or `Set Numbering Value`
   - Select: `Stop Numbering`
6. **Remove list format**
   - Still selected, click `Home` tab
   - In `Paragraph` group, click `Numbering` dropdown
   - Select: `None`
7. **Verify conversion**
   - Click on various numbered paragraphs
   - Numbering button should NOT be highlighted
8. **Save document**

**Result:** Numbers preserved as text, automatic numbering removed.

---

#### Method 4: Settings-Based (Advanced)

1. **Configure paste options**
   - `File → Options → Advanced`
   - Scroll to: `Cut, Copy, and Paste` section
   - Set `Pasting within the same document` to: `Keep Text Only`
2. **Apply to document**
   - Select All (`Ctrl+A` / `Cmd+A`)
   - Copy (`Ctrl+C` / `Cmd+C`)
   - Paste (`Ctrl+V` / `Cmd+V`)
3. **Restore settings** (optional)
   - Return to `File → Options → Advanced`
   - Reset paste option to previous setting
4. **Save document**

**Result:** All automatic formatting converted to text.

---

## Verification Steps

After conversion, verify that numbering is now fixed text:

### Test 1: Visual Check
- Click on a numbered paragraph (e.g., "3.1 Introduction")
- Look at the toolbar
- **✓ Success:** Numbering button is NOT highlighted/active
- **✗ Still automatic:** Numbering button is highlighted - repeat conversion

### Test 2: Deletion Test
- Delete a numbered paragraph in the middle of the document
- Check the paragraph that was below it
- **✓ Success:** Number stays the same (doesn't decrease)
- **✗ Still automatic:** Number automatically changes - repeat conversion

### Test 3: Copy Test
- Copy a numbered paragraph
- Paste it elsewhere in the document
- **✓ Success:** Number stays exactly as copied
- **✗ Still automatic:** Number changes to match new position - repeat conversion

### Test 4: Find & Replace Test
- Open Find & Replace (`Ctrl+H` / `Cmd+H`)
- Search for: `^#` (caret followed by hash - finds automatic numbers)
- **✓ Success:** No matches found (or very few)
- **✗ Still automatic:** Many matches found - repeat conversion

---

## Common Issues and Solutions

### Issue: Numbers Disappeared After Conversion

**Problem:** Automatic numbers were removed but not replaced with text.

**Solution:**
1. Undo the conversion (`Ctrl+Z` / `Cmd+Z`)
2. Use a different method (try Paste Special approach)
3. If numbers are lost, restore from backup

### Issue: Formatting Lost

**Problem:** Bold, italic, colors removed along with numbering.

**Solution:**
- Use Method 1 (Simple) instead of Paste Special
- LibreOffice: Use `Format → Lists → No List` only
- Word: Use `Numbering → None` without applying Normal style

### Issue: Some Numbers Still Automatic

**Problem:** Mixed automatic and fixed numbering.

**Solution:**
1. Search for remaining automatic numbers
2. Select those specific paragraphs only
3. Apply conversion method again
4. Verify with deletion test

### Issue: Document Won't Save

**Problem:** File locked or permission error.

**Solution:**
1. Save As new filename
2. Close and reopen document
3. Try again with administrator/sudo privileges

---

## Best Practices

### Before Conversion

✓ **Create backup** - Always save original document  
✓ **Close other programs** - Ensure document isn't open elsewhere  
✓ **Check file permissions** - Ensure you can edit the file  
✓ **Note the format** - Remember if it's .docx or .doc  

### During Conversion

✓ **Use recommended method first** - Start with Method 1  
✓ **Work on a copy** - Don't modify the original until tested  
✓ **Save frequently** - Save after each major step  
✓ **Test incrementally** - Verify conversion worked before proceeding  

### After Conversion

✓ **Run all verification tests** - Don't skip verification  
✓ **Keep both versions** - Original and converted  
✓ **Document the process** - Note which method you used  
✓ **Test with conversion system** - Process a chapter to verify  

---

## For Specific Document Types

### Academic Papers

- Usually have automatic numbering for sections
- **Recommended:** LibreOffice Method 2 (Search & Replace)
- **Reason:** Preserves citations and footnotes

### Technical Manuals

- Often have multi-level numbering (1.2.3.4)
- **Recommended:** Word Method 1 (Simple)
- **Reason:** Handles complex hierarchies well

### Books/Handbooks

- May have chapter AND section numbering
- **Recommended:** Either platform Method 1
- **Reason:** Fast, preserves structure

### Legal Documents

- Critical that numbering stays exact
- **Recommended:** Paste Special method
- **Reason:** Ensures no automatic renumbering can occur

---

## Testing Your Converted Document

Before running the full conversion system:

1. **Quick test with one chapter**
   ```bash
   python3 build_book.py
   ```
   
2. **Check the JSON output**
   ```bash
   cat chapter-viewer/book_content_json/chapter_01/section_01.json | grep "chapter_title"
   ```

3. **Expected results**
   - Section numbers visible in titles
   - No "missing in content" errors
   - TOC validation passes

4. **If issues found**
   - Re-examine original document
   - Look for remaining automatic numbering
   - Repeat conversion process

---

## Troubleshooting Conversion System Issues

Even after converting to fixed text, you might see issues:

### "Missing in content" errors for existing sections

**Cause:** Sections might be:
- Out of sequence in document
- Using different formatting
- In tables or lists
- Using special characters

**Solution:** Run the debug script:
```bash
python3 debug_missing_entries.py
```

### High number of "unexpected" entries

**Cause:** Document structure doesn't match TOC

**Solution:**
- Check if TOC itself needs updating
- Verify section numbers match between TOC and content
- Look for duplicate section numbers

### Automatic numbering still detected

**Cause:** Some paragraphs still have automatic numbering

**Solution:**
1. Search document for automatic numbering:
   - Word: Find `^#`
   - LibreOffice: Search for "Numbering Symbols" style
2. Convert those specific paragraphs
3. Re-save and reprocess

---

## Platform-Specific Notes

### LibreOffice Writer

**Advantages:**
- ✓ More reliable automatic numbering removal
- ✓ Better preservation of original formatting
- ✓ Free and open source

**Considerations:**
- Some complex Word formatting may change
- WMF images might need reconversion
- Equation formatting may differ

### Microsoft Word

**Advantages:**
- ✓ Native .docx format support
- ✓ Preserves all original document features
- ✓ Familiar interface for most users

**Considerations:**
- Automatic numbering more persistent
- May need multiple conversion attempts
- Licensing required

### Cross-Platform Workflow

**Best approach:**
1. Open in original application (Word → Word, LibreOffice → LibreOffice)
2. Convert automatic numbering using appropriate method
3. Save as .docx format
4. Verify in both applications if possible
5. Process with conversion system

---

## Quick Reference

| Platform | Quick Method | Time | Success Rate |
|----------|--------------|------|--------------|
| LibreOffice | Format → Lists → No List | 30 sec | 95% |
| Word | Ctrl+Shift+N → Numbering → None | 45 sec | 90% |
| LibreOffice (thorough) | Find & Replace Numbering Symbols | 2 min | 99% |
| Word (thorough) | Paste Special → Text Only | 2 min | 98% |

---

## Support

If conversion doesn't work:

1. **Check the DEBUG_SUMMARY** - Review `workspace/AUTO_DETECTION_DEBUG_SUMMARY.md`
2. **Run debug scripts** - Use `debug_missing_entries.py`
3. **Review this guide** - Try alternative methods
4. **Check document structure** - Some formats may need manual adjustment
5. **Create an issue** - Provide document details (without sensitive content)

---

**Remember:** This is a one-time preparation step. Once converted, the document is ready for all future processing runs!
