#!/usr/bin/env python3
"""
Diagnostic script to check image references and files.

This script:
1. Scans all JSON files for image references
2. Verifies that referenced images exist on disk
3. Checks for WMF files with wrong extensions
4. Reports statistics and issues
"""

import json
from pathlib import Path


def check_file_format(file_path):
    """Check if a file is actually the format its extension claims."""
    try:
        with open(file_path, "rb") as f:
            magic = f.read(8)

            # PNG: 89 50 4E 47 0D 0A 1A 0A
            if magic[:4] == b"\x89PNG":
                return "PNG"
            # JPEG: FF D8 FF
            elif magic[:3] == b"\xff\xd8\xff":
                return "JPEG"
            # WMF: D7 CD C6 9A or 01 00 09 00
            elif magic[:4] == b"\xd7\xcd\xc6\x9a" or magic[:4] == b"\x01\x00\x09\x00":
                return "WMF"
            # PDF: 25 50 44 46
            elif magic[:4] == b"%PDF":
                return "PDF"
            else:
                return "UNKNOWN"
    except Exception as e:
        return f"ERROR: {e}"


def check_images(export_dir="export"):
    """Check all image references and files."""
    print("=" * 80)
    print("IMAGE DIAGNOSTIC CHECK")
    print("=" * 80)
    print()

    export_path = Path(export_dir)
    pictures_path = export_path / "pictures"

    # Statistics
    stats = {
        "total_json_files": 0,
        "total_image_refs": 0,
        "missing_images": [],
        "format_mismatches": [],
        "wmf_files": [],
        "images_on_disk": set(),
    }

    # Find all language/book directories
    for lang_dir in sorted(export_path.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name == "pictures":
            continue

        for book_dir in sorted(lang_dir.iterdir()):
            if not book_dir.is_dir():
                continue

            print(f"Scanning {lang_dir.name}/{book_dir.name}...")

            # Scan JSON files for image references
            for json_file in book_dir.rglob("*.json"):
                if json_file.name in ["index.json", "manifest.json"]:
                    continue

                stats["total_json_files"] += 1

                try:
                    with open(json_file) as f:
                        data = json.load(f)

                    if "content" not in data:
                        continue

                    for item in data["content"]:
                        if item.get("type") != "image":
                            continue

                        stats["total_image_refs"] += 1

                        # Get image path
                        img_path_rel = item.get("path", "")

                        if not img_path_rel:
                            stats["missing_images"].append(
                                {
                                    "json": str(json_file.relative_to(export_path)),
                                    "filename": "unknown",
                                    "expected_path": "missing path field",
                                }
                            )
                            continue

                        # Construct full path
                        # Path format: pictures/{section_path}/{filename}
                        # Actual location: export/pictures/{lang}/{book_id}/{section_path}/{filename}
                        if img_path_rel.startswith("pictures/"):
                            rel_path = img_path_rel[9:]  # Remove "pictures/" prefix
                            img_path = (
                                pictures_path / lang_dir.name / book_dir.name / rel_path
                            )
                        else:
                            img_path = json_file.parent / img_path_rel

                        # Check if image exists
                        if not img_path.exists():
                            stats["missing_images"].append(
                                {
                                    "json": str(json_file.relative_to(export_path)),
                                    "filename": img_path.name,
                                    "expected_path": str(
                                        img_path.relative_to(export_path)
                                    ),
                                }
                            )
                        else:
                            # Check file format
                            actual_format = check_file_format(img_path)
                            expected_ext = img_path.suffix.upper()[
                                1:
                            ]  # Remove dot, uppercase

                            if expected_ext == "JPG":
                                expected_ext = "JPEG"

                            if actual_format != expected_ext and actual_format not in [
                                "ERROR",
                                "UNKNOWN",
                            ]:
                                stats["format_mismatches"].append(
                                    {
                                        "file": str(img_path.relative_to(export_path)),
                                        "expected": expected_ext,
                                        "actual": actual_format,
                                    }
                                )

                            if actual_format == "WMF":
                                stats["wmf_files"].append(
                                    str(img_path.relative_to(export_path))
                                )

                except Exception as e:
                    print(f"  ⚠️  Error reading {json_file.name}: {e}")

    print(f"✓ Scanned {stats['total_json_files']} JSON files")
    print(f"✓ Found {stats['total_image_refs']} image references")
    print()

    # Scan actual image files on disk
    print("Scanning image files on disk...")
    if pictures_path.exists():
        for img_file in pictures_path.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in [
                ".png",
                ".jpg",
                ".jpeg",
            ]:
                stats["images_on_disk"].add(str(img_file.relative_to(export_path)))

    print(f"✓ Found {len(stats['images_on_disk'])} image files on disk")
    print()

    # Report issues
    print("=" * 80)
    print("REPORT")
    print("=" * 80)
    print()

    if stats["missing_images"]:
        print(f"❌ MISSING IMAGES: {len(stats['missing_images'])}")
        print()
        for item in stats["missing_images"][:20]:
            print(f"  File: {item['filename']}")
            print(f"  Referenced in: {item['json']}")
            print(f"  Expected at: {item['expected_path']}")
            print()
        if len(stats["missing_images"]) > 20:
            print(f"  ... and {len(stats['missing_images']) - 20} more")
            print()
    else:
        print("✅ All referenced images exist on disk")
        print()

    if stats["format_mismatches"]:
        print(f"⚠️  FORMAT MISMATCHES: {len(stats['format_mismatches'])}")
        print()
        for item in stats["format_mismatches"][:10]:
            print(f"  {item['file']}")
            print(f"    Expected: {item['expected']}, Actual: {item['actual']}")
        if len(stats["format_mismatches"]) > 10:
            print(f"  ... and {len(stats['format_mismatches']) - 10} more")
        print()
    else:
        print("✅ All image files match their extensions")
        print()

    if stats["wmf_files"]:
        print(f"❌ WMF FILES WITH PNG/JPG EXTENSIONS: {len(stats['wmf_files'])}")
        print()
        print("  These files need to be converted. Run:")
        print("    python3 fix_wmf_images.py")
        print()
        for wmf in stats["wmf_files"][:10]:
            print(f"  {wmf}")
        if len(stats["wmf_files"]) > 10:
            print(f"  ... and {len(stats['wmf_files']) - 10} more")
        print()
    else:
        print("✅ No WMF files with wrong extensions")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"JSON files: {stats['total_json_files']}")
    print(f"Image references: {stats['total_image_refs']}")
    print(f"Images on disk: {len(stats['images_on_disk'])}")
    print(f"Missing images: {len(stats['missing_images'])}")
    print(f"Format mismatches: {len(stats['format_mismatches'])}")
    print(f"WMF files: {len(stats['wmf_files'])}")
    print()

    if (
        not stats["missing_images"]
        and not stats["format_mismatches"]
        and not stats["wmf_files"]
    ):
        print("✅ All checks passed! Images are in good shape.")
    else:
        print("⚠️  Issues found. Please review the report above.")

    print("=" * 80)

    return stats


if __name__ == "__main__":
    check_images()
