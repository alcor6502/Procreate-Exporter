# Procreate Recovery & Timestamp Rebuilder <img align="right" src="https://img.shields.io/badge/License-MIT-yellow.svg">

*A Python tool to extract, fix, rename, and rebuild Procreate documents from an iPad backup.*



## Overview

Procreate stores its documents inside a complex private directory structure on the iPad.
When users back up their devices, Procreate’s files often appear with missing names,
generic identifiers, or no recognizable `.procreate` files at all.

This project provides a Python script that:

- Traverses the extracted Procreate “Application Support” folder  
- Locates every hidden Procreate document (`Document.archive`)  
- Reads each document’s internal metadata  
- Reconstructs a proper human-readable file name based on creation date  
- Rebuilds a valid `.procreate` file  
- Applies the original creation/modification timestamps  
- Outputs thousands of recoverable files—properly named and sorted

## Important: Where to obtain the data

You must extract the folder:

```
AppDomain-au.com.savageinteractive.procreate
    → Library
        → Application Support   ← THIS folder
```
from your iPad backup using **iMazing** or any other iOS backup extractor.

![image info](Examples/Pics/iMazing-Procreate.png)



## How it works

Each Procreate document is stored as a folder containing:

- `Document.archive` — a binary plist holding the project name  
- Several subfolders representing layers, tiles, strokes, etc.

The script:

1. Recursively scans all directories inside Application Support  
2. Identifies valid Procreate projects by checking for Document.archive  
3. Reads project names using plistlib  
4. Extracts the folder’s creation date  
5. Generates a timestamp string (e.g., `25.11.21-14.32`)  
6. Prepends or replaces the project name with this timestamp  
7. Rewrites the archive with the updated name  
8. Zips the entire folder into a valid `.procreate` file  
9. Applies the original timestamp using macOS `SetFile`  
10. Saves the reconstructed and renamed project

## Requirements

- macOS 10.15 or newer  
- Python 3.9+  
- Xcode Command Line Tools (for SetFile)

In a new Terminal window install the tools if needed:

```bash
xcode-select --install
```

## Usage

```bash
python3 export_procreate.py /path/to/Application\ Support/
```

## What the script does

- Recovers files with missing names  
- Generates a clear chronological naming structure  
- Preserves creation/modification dates  
- Rebuilds valid `.procreate` files  
- Handles malformed archives safely  

## What it does NOT do

- Modify or recompress Procreate pixel data  
- Repair corrupted tiles  
- Handle iCloud-synced assets  

## Notes

Procreate uses a proprietary, undocumented storage format with Apple-specific LZ4 compression.  
This script does **not** attempt to decode internal tile data.  
It only reconstructs the outer `.procreate` bundle so that Procreate can load it again.

## License

Open source — free to use and modify.  
If you find this helpful, please star the project on GitHub!
