#!/usr/bin/env bash
# Downloads audio for the cliniciansbrief source. Unlike the other download_*.sh
# scripts, this one pulls from SoundCloud (each recording is a private/secret-token
# SoundCloud "set" embedded in its article page, not a direct file URL) so it needs
# yt-dlp rather than curl. See sources/cliniciansbrief/ATTRIBUTION.md for the license
# caveat before re-running or redistributing this.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/sources/cliniciansbrief/manifest.csv"
OUTDIR="$ROOT/sources/cliniciansbrief/audio"

command -v yt-dlp >/dev/null || { echo "yt-dlp is required: https://github.com/yt-dlp/yt-dlp"; exit 1; }

mkdir -p "$OUTDIR/normal" "$OUTDIR/congenital" "$OUTDIR/acquired_valvular_disease" "$OUTDIR/arrhythmia" "$OUTDIR/other"

fail=0
tail -n +2 "$MANIFEST" | while IFS=, read -r id category url rest; do
  dest_dir="$OUTDIR/$category"
  local_filename="${url##*/sets/}"
  stem="$(basename "$id" | sed 's/^cb-//')"
  dest="$dest_dir/$stem.mp3"
  if [ -s "$dest" ]; then
    echo "SKIP (exists): $stem.mp3"
    continue
  fi
  echo "GET $url"
  if yt-dlp --playlist-items 1 -x --audio-format mp3 --audio-quality 5 \
      -o "$dest_dir/$stem.%(ext)s" "$url" >/dev/null 2>&1; then
    size=$(stat -c%s "$dest" 2>/dev/null || echo 0)
    echo "OK   $stem.mp3 ($size bytes)"
  else
    echo "FAIL $url"
    fail=1
  fi
done

echo "Done."
