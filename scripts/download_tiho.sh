#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/sources/tiho-hannover/manifest.csv"
OUTDIR="$ROOT/sources/tiho-hannover/audio"

mkdir -p "$OUTDIR/grading" "$OUTDIR/examples" "$OUTDIR/arrhythmia"

fail=0
tail -n +2 "$MANIFEST" | while IFS=, read -r id category url local_filename rest; do
  case "$category" in
    grading) sub="grading" ;;
    examples) sub="examples" ;;
    arrhythmia) sub="arrhythmia" ;;
    *) sub="misc" ;;
  esac
  dest="$OUTDIR/$sub/$local_filename"
  if [ -s "$dest" ]; then
    echo "SKIP (exists): $local_filename"
    continue
  fi
  echo "GET $url"
  if curl -fsSL --retry 3 -o "$dest" "$url"; then
    size=$(stat -c%s "$dest" 2>/dev/null || echo 0)
    echo "OK   $local_filename ($size bytes)"
  else
    echo "FAIL $url"
    rm -f "$dest"
    fail=1
  fi
done

echo "Done."
