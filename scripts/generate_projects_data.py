#!/usr/bin/env python3
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_INDEX = ROOT / "assets" / "projects" / "projects-index.md"
OUTPUT_FILE = ROOT / "assets" / "projects" / "projects-data.json"
PROJECTS_DIR = ROOT / "assets" / "projects"

KEY_ALIASES = {
    "title image": "image",
    "representative text": "excerpt",
    "read more": "readMore",
}


def normalize_key(raw_key: str) -> str:
    key = raw_key.strip().lower()
    key = re.sub(r"^#+", "", key).strip()
    return KEY_ALIASES.get(key, key)


def parse_markdown_metadata(text: str) -> dict:
    lines = text.splitlines()
    data = {}
    idx = 0

    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            idx += 1
            if line.strip() == "---":
                break
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[normalize_key(key)] = value.strip()
        else:
            idx = 0

    if not data:
        for line in lines:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[normalize_key(key)] = value.strip()

    return {
        "title": data.get("title", ""),
        "date": data.get("date", ""),
        "group": data.get("group", ""),
        "image": data.get("image", ""),
        "excerpt": data.get("excerpt", ""),
        "readMore": data.get("readMore", ""),
    }


def project_files_from_manifest(index_text: str) -> list[str]:
    lines = index_text.splitlines()
    files = []
    for line in lines:
        line = line.strip()
        if line.startswith("- ") and line.endswith(".md"):
            files.append(line[2:].strip())
    return files


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    if not PROJECTS_INDEX.exists():
        raise FileNotFoundError(f"Missing manifest: {PROJECTS_INDEX}")

    manifest_text = load_file(PROJECTS_INDEX)
    project_files = project_files_from_manifest(manifest_text)

    entries = []
    for index, relative_path in enumerate(project_files):
        file_path = PROJECTS_DIR / relative_path
        if not file_path.exists():
            print(f"Skipping missing file: {relative_path}")
            continue

        metadata_text = load_file(file_path)
        metadata = parse_markdown_metadata(metadata_text)
        missing_fields = [k for k in ("title", "date", "image", "excerpt", "readMore") if not metadata.get(k)]
        if missing_fields:
            print(f"Skipping {relative_path}, missing fields: {', '.join(missing_fields)}")
            continue

        entries.append({**metadata, "__manifestOrder": index})

    OUTPUT_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} project entries to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
