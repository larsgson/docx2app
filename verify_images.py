#!/usr/bin/env python3
"""
Verify that all image references in JSON files have corresponding image files.
This script checks the integrity of the book content structure.
"""

import json
from collections import defaultdict
from pathlib import Path


def verify_images():
    """Check all JSON files for image references and verify files exist."""

    export_path = Path("export")

    if not export_path.exists():
        print(f"❌ Export path not found: {export_path}")
        return False

    issues = []
    stats = defaultdict(int)

    # Find all language/book directories
    for lang_dir in sorted(export_path.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name == "pictures":
            continue

        for book_dir in sorted(lang_dir.iterdir()):
            if not book_dir.is_dir():
                continue

            print(f"\n📚 Checking: {lang_dir.name}/{book_dir.name}")

            # Iterate through all chapter directories (XX_chapter_name format)
            for chapter_dir in sorted(book_dir.iterdir()):
                if not chapter_dir.is_dir():
                    continue
                # Skip non-chapter directories
                if not chapter_dir.name[0].isdigit():
                    continue

                # Get all JSON files in the chapter
                for json_file in sorted(chapter_dir.glob("*.json")):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        # Check all content items
                        content = data.get("content", [])
                        for item in content:
                            if item.get("type") == "image":
                                stats["total_images"] += 1

                                path = item.get("path")

                                if not path:
                                    issues.append(
                                        f"⚠️  {json_file.name}: Image missing path"
                                    )
                                    stats["missing_path"] += 1
                                    continue

                                # Image path format: pictures/{section_path}/{filename}
                                # Actual file location: export/pictures/{lang}/{book_id}/{section_path}/{filename}
                                if path.startswith("pictures/"):
                                    rel_path = path[9:]  # Remove "pictures/" prefix
                                    image_file = (
                                        export_path
                                        / "pictures"
                                        / lang_dir.name
                                        / book_dir.name
                                        / rel_path
                                    )
                                else:
                                    image_file = chapter_dir / path

                                if not image_file.exists():
                                    issues.append(
                                        f"❌ {chapter_dir.name}/{json_file.name}: "
                                        f"Missing image file: {path}"
                                    )
                                    stats["missing_files"] += 1
                                else:
                                    stats["valid_images"] += 1

                    except json.JSONDecodeError as e:
                        issues.append(f"❌ Error parsing {json_file}: {e}")
                        stats["json_errors"] += 1
                    except Exception as e:
                        issues.append(f"❌ Error processing {json_file}: {e}")
                        stats["other_errors"] += 1

    # Print results
    print("\n" + "=" * 70)
    print("Image Verification Report")
    print("=" * 70)

    print(f"\n📊 Statistics:")
    print(f"   Total images referenced:  {stats['total_images']}")
    print(f"   Valid images found:       {stats['valid_images']}")
    print(f"   Missing image files:      {stats['missing_files']}")
    print(f"   Missing path field:       {stats['missing_path']}")
    print(f"   JSON parsing errors:      {stats['json_errors']}")
    print(f"   Other errors:             {stats['other_errors']}")

    if issues:
        print(f"\n⚠️  Found {len(issues)} issue(s):\n")
        for issue in issues[:20]:  # Show first 20 issues
            print(f"   {issue}")

        if len(issues) > 20:
            print(f"\n   ... and {len(issues) - 20} more issues")

        print("\n❌ Verification FAILED")
        return False
    else:
        print("\n✅ All image references verified successfully!")
        return True


def list_orphaned_images():
    """Find image files that are not referenced in any JSON."""

    export_path = Path("export")
    pictures_path = export_path / "pictures"

    if not pictures_path.exists():
        return

    print("\n" + "=" * 70)
    print("Orphaned Images Report")
    print("=" * 70)

    total_orphaned = 0

    # Build set of all referenced images
    referenced = set()

    for lang_dir in sorted(export_path.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name == "pictures":
            continue

        for book_dir in sorted(lang_dir.iterdir()):
            if not book_dir.is_dir():
                continue

            for chapter_dir in sorted(book_dir.iterdir()):
                if not chapter_dir.is_dir() or not chapter_dir.name[0].isdigit():
                    continue

                for json_file in chapter_dir.glob("*.json"):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        for item in data.get("content", []):
                            if item.get("type") == "image":
                                path = item.get("path", "")
                                if path.startswith("pictures/"):
                                    # Store full relative path from pictures root
                                    full_path = (
                                        f"{lang_dir.name}/{book_dir.name}/{path[9:]}"
                                    )
                                    referenced.add(full_path)
                    except:
                        continue

    # Check for orphaned files in pictures directory
    for img_file in sorted(pictures_path.rglob("*")):
        if img_file.is_file():
            rel_path = str(img_file.relative_to(pictures_path))
            # Skip backup files and manifest
            if img_file.name.endswith(".backup") or img_file.name == "manifest.json":
                continue
            if rel_path not in referenced:
                print(f"   🔸 {rel_path}")
                total_orphaned += 1

    if total_orphaned == 0:
        print("\n✅ No orphaned images found!")
    else:
        print(f"\n📊 Total orphaned images: {total_orphaned}")
        print("   (These images exist but are not referenced in any JSON file)")


if __name__ == "__main__":
    print("\n🔍 Starting image verification...\n")

    success = verify_images()
    list_orphaned_images()

    print("\n" + "=" * 70 + "\n")

    exit(0 if success else 1)
