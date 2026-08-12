#!/usr/bin/env python3
"""
Merge per-source manifest.csv files (sources/<slug>/manifest.csv) into a
master catalog (catalog/catalog.csv + catalog/catalog.json), verify local
audio files exist, probe duration with ffprobe, and generate markdown
indexes grouped by species and by disease category.

Each source manifest must have at minimum these columns:
  id,category,url,local_filename,animal,breed,age,diagnosis_category,
  diagnosis,grade,description,source_page

The audio file for a row is expected at:
  sources/<slug>/audio/<category-folder>/<local_filename>
where <category-folder> is one of: grading, examples, arrhythmia, misc
(falls back to searching the whole sources/<slug>/audio tree if not found
at the expected path, to tolerate sources with a flatter layout).
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "sources"
CATALOG_DIR = ROOT / "catalog"
INDEX_DIR = ROOT / "index"

CATEGORY_FOLDER = {
    "grading": "grading",
    "examples": "examples",
    "arrhythmia": "arrhythmia",
}


def ffprobe_duration(path: Path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=20,
        )
        val = out.stdout.strip()
        return round(float(val), 1) if val else None
    except Exception:
        return None


def find_audio_file(slug: str, category: str, local_filename: str):
    audio_root = SOURCES_DIR / slug / "audio"
    sub = CATEGORY_FOLDER.get(category, category)
    candidate = audio_root / sub / local_filename
    if candidate.exists():
        return candidate
    # fallback: search recursively
    matches = list(audio_root.rglob(local_filename))
    return matches[0] if matches else None


def find_image_file(slug: str, local_filename: str):
    """Look for a paired image (e.g. phonogram screenshot) whose filename
    stem matches the audio file's stem, anywhere under sources/<slug>/images/."""
    images_root = SOURCES_DIR / slug / "images"
    if not images_root.exists():
        return None
    stem = Path(local_filename).stem
    matches = list(images_root.rglob(f"{stem}*"))
    return matches[0] if matches else None


def load_source_manifest(slug: str, manifest_path: Path):
    rows = []
    with open(manifest_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            audio_path = find_audio_file(slug, row["category"], row["local_filename"])
            status = "ok" if audio_path else "MISSING"
            duration = ffprobe_duration(audio_path) if audio_path and audio_path.suffix.lower() in (".mp3", ".wav", ".ogg", ".flac", ".m4a") else None
            rel_path = str(audio_path.relative_to(ROOT)) if audio_path else ""
            image_path = find_image_file(slug, row["local_filename"])
            rel_image_path = str(image_path.relative_to(ROOT)) if image_path else ""
            rows.append({
                "recording_id": row["id"],
                "source": slug,
                "category": row["category"],
                "animal": row.get("animal", "").strip(),
                "breed": row.get("breed", "").strip(),
                "age": row.get("age", "").strip(),
                "diagnosis_category": row.get("diagnosis_category", "").strip(),
                "diagnosis": row.get("diagnosis", "").strip(),
                "grade": row.get("grade", "").strip(),
                "description": row.get("description", "").strip(),
                "duration_sec": duration if duration is not None else "",
                "audio_path": rel_path,
                "audio_format": audio_path.suffix.lstrip(".").lower() if audio_path else "",
                "image_path": rel_image_path,
                "source_url": row.get("url", "").strip(),
                "source_page": row.get("source_page", "").strip(),
                "status": status,
            })
    return rows


def main():
    all_rows = []
    for source_dir in sorted(SOURCES_DIR.iterdir()):
        if not source_dir.is_dir():
            continue
        manifest = source_dir / "manifest.csv"
        if not manifest.exists():
            continue
        slug = source_dir.name
        rows = load_source_manifest(slug, manifest)
        missing = [r for r in rows if r["status"] == "MISSING"]
        if missing:
            print(f"WARNING: {len(missing)} missing audio files in source '{slug}':", file=sys.stderr)
            for m in missing:
                print(f"    {m['recording_id']} -> expected {m['audio_path'] or '(not found)'}", file=sys.stderr)
        all_rows.extend(rows)

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = list(all_rows[0].keys()) if all_rows else []

    with open(CATALOG_DIR / "catalog.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    with open(CATALOG_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, indent=2, ensure_ascii=False)

    print(f"Catalog built: {len(all_rows)} recordings from "
          f"{len({r['source'] for r in all_rows})} source(s).")

    build_indexes(all_rows)


def slugify(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-") or "unspecified"


def build_indexes(rows):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    by_species_dir = INDEX_DIR / "by-species"
    by_disease_dir = INDEX_DIR / "by-disease"
    by_species_dir.mkdir(parents=True, exist_ok=True)
    by_disease_dir.mkdir(parents=True, exist_ok=True)

    species_groups = {}
    disease_groups = {}
    for r in rows:
        species_groups.setdefault(r["animal"] or "unspecified", []).append(r)
        disease_groups.setdefault(r["diagnosis_category"] or "unspecified", []).append(r)

    for species, items in species_groups.items():
        path = by_species_dir / f"{slugify(species)}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {species.title()} — Heart Sound Recordings ({len(items)})\n\n")
            f.write("| Recording | Diagnosis | Grade | Breed | Source | Audio | Image | Duration |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            for r in sorted(items, key=lambda x: (x["diagnosis_category"], x["recording_id"])):
                audio_link = f"[{Path(r['audio_path']).name}](../../{r['audio_path']})" if r["audio_path"] else "MISSING"
                image_link = f"[phonogram](../../{r['image_path']})" if r.get("image_path") else ""
                dur = f"{r['duration_sec']}s" if r["duration_sec"] != "" else ""
                f.write(f"| {r['recording_id']} | {r['diagnosis']} | {r['grade']} | {r['breed']} | {r['source']} | {audio_link} | {image_link} | {dur} |\n")

    for disease, items in disease_groups.items():
        path = by_disease_dir / f"{slugify(disease)}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {disease.replace('_', ' ').title()} — Heart Sound Recordings ({len(items)})\n\n")
            f.write("| Recording | Animal | Diagnosis | Grade | Breed | Source | Audio | Image | Duration |\n")
            f.write("|---|---|---|---|---|---|---|---|---|\n")
            for r in sorted(items, key=lambda x: (x["animal"], x["recording_id"])):
                audio_link = f"[{Path(r['audio_path']).name}](../../{r['audio_path']})" if r["audio_path"] else "MISSING"
                image_link = f"[phonogram](../../{r['image_path']})" if r.get("image_path") else ""
                dur = f"{r['duration_sec']}s" if r["duration_sec"] != "" else ""
                f.write(f"| {r['recording_id']} | {r['animal']} | {r['diagnosis']} | {r['grade']} | {r['breed']} | {r['source']} | {audio_link} | {image_link} | {dur} |\n")

    print(f"Indexes built: {len(species_groups)} species page(s), {len(disease_groups)} disease page(s).")


if __name__ == "__main__":
    main()
