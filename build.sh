#!/usr/bin/env bash
set -euo pipefail

PLUGINS=(marketing sales customer-support product-management legal finance cowork-plugin-management)
BUILD_DIR="build"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

for plugin in "${PLUGINS[@]}"; do
  if [ -d "$plugin" ]; then
    zip -r "$BUILD_DIR/${plugin}.zip" "$plugin" -x "*.DS_Store"
    echo "Built: $BUILD_DIR/${plugin}.zip"
  else
    echo "Warning: plugin directory '$plugin' not found, skipping"
  fi
done

echo ""
echo "Build complete. $(ls "$BUILD_DIR"/*.zip 2>/dev/null | wc -l | tr -d ' ') plugins packaged in $BUILD_DIR/"
