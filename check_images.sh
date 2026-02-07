#!/bin/bash
echo "=== COMPLETE IMAGE CHECK ==="

# Check README.md
echo "1. Checking README.md:"
echo "   Properly formatted: $(grep -c '!\[.*\](README/images/.*\.png)' README.md)"
echo "   Naked paths: $(grep -c '^README/images/.*\.png$' README.md)"

# List all images
echo ""
echo "2. All image references in README.md:"
while IFS= read -r line; do
    if [[ "$line" =~ !\[.*\]\(README/images/.*\.png\) ]]; then
        echo "   ✅ $line"
    elif [[ "$line" =~ ^README/images/.*\.png$ ]]; then
        echo "   ❌ Naked: $line"
    fi
done < README.md | head -20

# Check README/README.md
echo ""
echo "3. Checking README/README.md:"
echo "   Properly formatted: $(grep -c '!\[.*\](README/images/.*\.png)' README/README.md)"
echo "   Naked paths: $(grep -c '^README/images/.*\.png$' README/README.md)"

# Verify files exist
echo ""
echo "4. Verifying image files exist:"
count=0
for img in $(grep -o 'README/images/[^)]*\.png' README.md); do
    if [ -f "$img" ]; then
        count=$((count+1))
    fi
done
echo "   Found $count referenced images on disk"
