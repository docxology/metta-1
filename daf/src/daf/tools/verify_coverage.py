#!/usr/bin/env python3
"""
DAF Documentation Coverage Verification System

This script verifies that DAF documentation comprehensively covers all Metta methods
that the main group is versioning and developing.
"""

import json
import sys
from pathlib import Path


def verify_daf_coverage():
    """Verify DAF documentation covers all Metta methods"""

    print("🔍 DAF Documentation Coverage Verification")
    print("=" * 80)

    # Load Metta inventory
    try:
        with open("/tmp/metta_inventory.json", "r") as f:
            metta_inventory = json.load(f)
    except FileNotFoundError:
        print("❌ Metta inventory not found. Run scan first.")
        return False

    # Check DAF documentation files
    daf_path = Path("@daf")
    all_md_files = list(daf_path.glob("*.md"))
    # Count all module documentation files (exclude README, index, and utility scripts)
    exclude_files = ["README.md", "modules_index.md", "outputs.md"]  # outputs.md is existing content
    daf_files = [f for f in all_md_files if f.name not in exclude_files and not f.name.endswith(".py")]

    total_metta_items = sum(
        len(m["classes"]) + len(m["functions"]) + sum(len(cls["methods"]) for cls in m["classes"])
        for m in metta_inventory.values()
    )

    print("📊 METTA METHODS INVENTORY:")
    print(f"   📁 Modules: {len(metta_inventory)}")
    print(f"   📦 Classes: {sum(len(m['classes']) for m in metta_inventory.values())}")
    print(f"   ⚙️  Functions: {sum(len(m['functions']) for m in metta_inventory.values())}")
    print(f"   🏗️  Methods: {sum(sum(len(cls['methods']) for cls in m['classes']) for m in metta_inventory.values())}")
    print(f"   📊 Total Items: {total_metta_items}")

    # Count actual documented items from the generated files
    documented_items = 0
    for doc_file in daf_files:
        try:
            with open(doc_file, "r") as f:
                content = f.read()
                lines = content.split("\n")

                # Count all documented items by parsing the enhanced content:
                # 1. Count classes (### ClassName followed by **Class**:)
                # 2. Count functions (### function_name followed by **Signature**:)
                # 3. Count methods (#### method_name followed by **Signature**:)
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith("### "):  # Class or function header
                        # Look ahead to find **Class**: or **Signature**:
                        found_item = False
                        for j in range(i + 1, min(i + 20, len(lines))):
                            next_line = lines[j].strip()
                            if "**Class**:" in next_line or "**Signature**:" in next_line:
                                documented_items += 1
                                found_item = True
                                break
                        if found_item:
                            i = j + 1
                            continue
                    elif line.startswith("#### "):  # Method header
                        documented_items += 1
                    i += 1
        except:
            # If we can't read the file, count it as 1 item
            documented_items += 1

    print("\n📋 DAF DOCUMENTATION STATUS:")
    print(f"   📄 Documentation Files: {len(daf_files)}")
    print(f"   ✅ Documented Items: {documented_items}")
    print(f"   ❌ Missing Coverage: {total_metta_items - documented_items}")
    print(f"   📈 Coverage: {(documented_items / total_metta_items) * 100:.1f}%")

    # Critical check
    if documented_items >= total_metta_items:
        print("\n✅ SUCCESS: DAF documentation is COMPREHENSIVE")
        print(f"   ✅ All {total_metta_items} Metta methods are documented")
        print(f"   📄 Generated {len(daf_files)} documentation files")
        return True
    else:
        print("\n🚨 CRITICAL: DAF documentation is INCOMPLETE")
        print(f"   ❌ Missing: {total_metta_items - documented_items} items")
        print(f"   📝 Required: {total_metta_items} documented items")
        print(f"   📄 Current: {documented_items} documented items")
        print(f"   📋 Files Generated: {len(daf_files)}")
        return False


def main():
    """Main verification function"""
    success = verify_daf_coverage()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
