#!/usr/bin/env python3
"""
Builds the self-contained index.html player/quiz app from catalog/catalog.csv.

Transcodes every recording to a small mono MP3 and every paired image to a
compressed JPEG, base64-embeds everything (plus the vendored variable
fonts) directly into scripts/player_template.html, and writes the result
to index.html at the repo root. The output has zero external dependencies,
so it works identically as a Claude Artifact and as a GitHub Pages site.
"""
import base64
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
TEMPLATE = ROOT / "scripts" / "player_template.html"
FONTS_DIR = ROOT / "scripts" / "assets" / "fonts"
OUTPUT = ROOT / "index.html"
ARTIFACT_OUTPUT = ROOT / "scripts" / "build" / "artifact_fragment.html"

AUDIO_BITRATE = "64k"
AUDIO_SAMPLE_RATE = "11025"
IMAGE_MAX_WIDTH = 640
IMAGE_QUALITY = 5  # ffmpeg mjpeg qscale: 2 (best) - 31 (worst); 5 is high quality, small size

SOURCE_META = {
    "tiho-hannover": {
        "name": "TiHo Hannover / Vet Budapest Heartsound Library",
        "license": "CC BY-NC-ND 4.0",
        "citation": "Vörös, Ehlers, Kleinsorgen & Nolte — University of Veterinary Medicine Hannover & University of Veterinary Medicine Budapest",
        "url": "https://www.tiho-hannover.de/studium-lehre/zel/e-learning-beratung/service-materialien-und-lernprogramme/heartsound-library",
    },
    "uq-equine-auscultation": {
        "name": "UQ Equine Cardiac Auscultation Learning Resource",
        "license": "CC BY 4.0",
        "citation": "Wood, Shapter & Stewart (2024), Animals 14(9):1341 — University of Queensland",
        "url": "https://doi.org/10.3390/ani14091341",
    },
}


def transcode_audio(src: Path, tmp_dir: Path) -> bytes:
    out = tmp_dir / (src.stem + ".mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-ac", "1", "-ar", AUDIO_SAMPLE_RATE, "-b:a", AUDIO_BITRATE,
         str(out)],
        check=True,
    )
    return out.read_bytes()


def transcode_image(src: Path, tmp_dir: Path) -> bytes:
    out = tmp_dir / (src.stem + ".jpg")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-vf", f"scale={IMAGE_MAX_WIDTH}:-1",
         "-q:v", str(IMAGE_QUALITY),
         str(out)],
        check=True,
    )
    return out.read_bytes()


def b64_data_uri(data: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def main():
    rows = list(csv.DictReader(open(CATALOG, encoding="utf-8")))
    library = []
    total_audio_bytes = 0
    total_image_bytes = 0

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for row in rows:
            if row["status"] != "ok" or not row["audio_path"]:
                print(f"SKIP {row['recording_id']}: no audio", file=sys.stderr)
                continue
            if row["audio_format"] == "mpg":
                print(f"SKIP {row['recording_id']}: video file, audio duplicates another recording", file=sys.stderr)
                continue
            audio_src = ROOT / row["audio_path"]
            audio_bytes = transcode_audio(audio_src, tmp_dir)
            total_audio_bytes += len(audio_bytes)
            audio_uri = b64_data_uri(audio_bytes, "audio/mpeg")

            image_uri = None
            if row.get("image_path"):
                image_src = ROOT / row["image_path"]
                image_bytes = transcode_image(image_src, tmp_dir)
                total_image_bytes += len(image_bytes)
                image_uri = b64_data_uri(image_bytes, "image/jpeg")

            src_meta = SOURCE_META.get(row["source"], {})
            library.append({
                "id": row["recording_id"],
                "animal": row["animal"],
                "breed": row["breed"] if row["breed"] != "unspecified" else None,
                "age": row["age"] if row["age"] != "unspecified" else None,
                "category": row["diagnosis_category"],
                "diagnosis": row["diagnosis"],
                "grade": row["grade"] or None,
                "description": row["description"],
                "duration": float(row["duration_sec"]) if row["duration_sec"] else None,
                "audio": audio_uri,
                "image": image_uri,
                "sourceName": src_meta.get("name", row["source"]),
                "sourceLicense": src_meta.get("license", ""),
                "sourceCitation": src_meta.get("citation", ""),
                "sourceUrl": src_meta.get("url", ""),
            })
            print(f"OK   {row['recording_id']}  audio={len(audio_bytes)/1024:.0f}KB"
                  + (f"  image={len(image_bytes)/1024:.0f}KB" if image_uri else ""))

    print(f"\nTotal recordings: {len(library)}")
    print(f"Total audio (post-transcode): {total_audio_bytes/1024/1024:.2f} MB")
    print(f"Total images (post-transcode): {total_image_bytes/1024/1024:.2f} MB")

    fonts = {}
    for name, fname in [
        ("FRAUNCES", "fraunces.woff2"),
        ("PLEX_SANS", "plexsans.woff2"),
        ("PLEX_MONO_400", "plexmono400.woff2"),
        ("PLEX_MONO_500", "plexmono500.woff2"),
    ]:
        data = (FONTS_DIR / fname).read_bytes()
        fonts[name] = b64_data_uri(data, "font/woff2")

    template = TEMPLATE.read_text(encoding="utf-8")
    library_json = json.dumps(library, ensure_ascii=False, separators=(",", ":"))

    fragment = template.replace("__LIBRARY_JSON__", library_json)
    for key, uri in fonts.items():
        fragment = fragment.replace(f"__FONT_{key}__", uri)

    ARTIFACT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_OUTPUT.write_text(fragment, encoding="utf-8")

    wrapped = f'<!DOCTYPE html>\n<html lang="en">\n{fragment}\n</html>\n'
    OUTPUT.write_text(wrapped, encoding="utf-8")

    size_mb = OUTPUT.stat().st_size / 1024 / 1024
    print(f"\nWrote {OUTPUT} ({size_mb:.2f} MB) — full document, for GitHub Pages")
    print(f"Wrote {ARTIFACT_OUTPUT} — content fragment, for Artifact publish")


if __name__ == "__main__":
    main()
