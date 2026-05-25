
#!/usr/bin/env python3

import argparse
import json
import urllib.request
from pathlib import Path

# Base download directory
base_dir = Path("build")


def download_file(url, subfolder, filename=None, version=None):

    if not filename:
        filename = Path(url.split("?")[0]).name

    if not filename:
        raise ValueError(f"Cannot determine filename from URL: {url}")

    # Create target directory
    target_dir = base_dir / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / filename

    print(f"Downloading {subfolder} {version or ''}: {url}")

    try:
        urllib.request.urlretrieve(url, target_file)
        print(f"Saved to {target_file}")
    except Exception as err:
        print(f"Download failed: {url}: {err}")


def main():

    parser = argparse.ArgumentParser(
        description="Download packages from a JSON definition file"
    )

    parser.add_argument(
        "json_file",
        nargs="?",
        default="packages.json",
        help="JSON file (default: packages.json)"
    )

    args = parser.parse_args()

    json_file = Path(args.json_file)

    if not json_file.is_file():
        parser.error(f"JSON file not found: {json_file}")

    try:
        with json_file.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as err:
        parser.error(f"Invalid JSON: {err}")

    print(f"Package definition version: {config.get('version', 'unknown')}")
    print(f"Download directory: {base_dir.resolve()}")
    print()

    # Process platform sections
    for platform, packages in config.items():

        # Skip global metadata
        if platform == "version":
            continue

        if not isinstance(packages, dict):
            continue

        print(f"\n=== {platform.upper()} ===")

        for package, details in packages.items():

            # Skip version-only entries (e.g. exomizer, jre)
            if not isinstance(details, dict):
                continue

            url = details.get("url")

            if not url:
                continue
                
            download_file(
                url=url,
                subfolder=Path(platform),
                filename=details.get("file"),
                version=details.get("version")
            )                


if __name__ == "__main__":
    main()
