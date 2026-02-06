# openexr 3.3.3 (Major v3)

VFX Platform 2025 compatible build package for openexr.

## Package Information

- **Package Name**: openexr
- **Version**: 3.3.3
- **Major Version**: 3
- **Repository**: vfxplatform-2025/openexr-3
- **Description**: OpenEXR image file format library

## Build Instructions

```bash
rez-build -i
```

## Package Structure

```
openexr/
├── 3.3.3/
│   ├── package.py      # Rez package configuration
│   ├── rezbuild.py     # Build script
│   ├── get_source.sh   # Source download script (if applicable)
│   └── README.md       # This file
```

## Installation

When built with `install` target, installs to: `/core/Linux/APPZ/packages/openexr/3.3.3`

## Version Strategy

This repository contains **Major Version 3** of openexr. Different major versions are maintained in separate repositories:

- Major v3: `vfxplatform-2025/openexr-3`

## VFX Platform 2025

This package is part of the VFX Platform 2025 initiative, ensuring compatibility across the VFX industry standard software stack.
