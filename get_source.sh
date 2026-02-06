#!/bin/bash
set -e

VERSION="3.3.3"
ARCHIVE="v${VERSION}.tar.gz"
EXTRACTED_DIR="openexr-${VERSION}"
DOWNLOAD_URL="https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/${ARCHIVE}"

mkdir -p source
cd source

# download archive
if [ ! -f "${ARCHIVE}" ]; then
    echo "📥 Downloading OpenEXR ${VERSION}..."
    curl -L -o "${ARCHIVE}" "${DOWNLOAD_URL}"
fi

# extract
if [ -d "${EXTRACTED_DIR}" ]; then
    echo "🧹 Removing previous extracted directory: ${EXTRACTED_DIR}"
    rm -rf "${EXTRACTED_DIR}"
fi

echo "📦 Extracting ${ARCHIVE}..."
tar -xzf "${ARCHIVE}"
echo "✅ OpenEXR ${VERSION} extracted."
