#!/bin/bash
echo "=== Fixing README Image Paths ==="

# 1. Check current image references
echo "Current image references in README.md:"
grep -o 'https://images/[^)]*' README.md 2>/dev/null || echo "No https://images/ references found"

# 2. Fix all image paths
echo "Fixing paths from https://images/ to README/images/..."
sed -i 's|https://images/|README/images/|g' README.md
sed -i 's|https://images/|README/images/|g' README/README.md

# 3. Verify images exist
echo ""
echo "=== Verifying images exist ==="
for img in $(grep -o 'README/images/[^)]*\.png' README.md); do
    if [ -f "$img" ]; then
        echo "✅ $img"
    else
        echo "❌ $img - MISSING!"
    fi
done

# 4. Show before/after example
echo ""
echo "=== Before/After Example ==="
echo "BEFORE: https://images/django_installed_successfully.png"
echo "AFTER:  README/images/django_installed_successfully.png"
