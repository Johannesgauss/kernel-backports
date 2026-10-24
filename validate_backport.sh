#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KERNEL_DIR="${KERNEL_DIR:~$HOME/linux}"
PATCH_DIR="$SCRIPT_DIR/patches"

if [ ! -d "$KERNEL_DIR" ]; then
    echo "[!] Error: Kernel folder $KERNEL_DIR not found."
    exit 1
fi

for patch in "$PATCH_DIR"/*.patch; do
    
    "$KERNEL_DIR/scripts/checkpatch.pl" --no-tree --terse "$patch" || true

    grep -E "^(From:|Subject:|Date:|Signed-off-by:|Fixes:|CVE-)" "$patch" | head -n 8
done
