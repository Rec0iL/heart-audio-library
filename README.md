# Heart Audio Library

An organized, locally-hosted archive of openly-licensed animal (mainly companion animal) heart sound recordings, grouped by species and cardiac diagnosis, for veterinary auscultation education and research. Includes **Stethoscape**, a self-contained web player and ear-training quiz — see [Stethoscape player](#stethoscape-player-quiz) below.

## Structure

```
HeartAudioLibrary/
├── index.html                    # Stethoscape — the player/quiz web app (open directly, or serve via GitHub Pages)
├── sources/                     # One folder per original source, kept intact & unmodified
│   └── <source-slug>/
│       ├── audio/                # Original audio files, organized in subfolders by category
│       ├── images/                # Optional: paired phonograms/spectrograms/photos, same naming convention as audio
│       ├── raw/                   # Optional: original downloaded archive, kept locally for provenance (gitignored — not committed)
│       ├── manifest.csv          # Per-recording metadata for this source (feeds the master catalog)
│       └── ATTRIBUTION.md        # License, authors, citation for this source
├── catalog/
│   ├── catalog.csv               # Master index of every recording across all sources
│   └── catalog.json              # Same data, JSON (for scripts/tools)
├── index/
│   ├── by-species/<species>.md   # Recordings grouped by animal species
│   └── by-disease/<category>.md  # Recordings grouped by diagnosis category
├── scripts/
│   ├── download_<source>.sh      # Fetches a source's audio files per its manifest
│   ├── build_catalog.py          # Regenerates catalog/ and index/ from all sources/*/manifest.csv
│   ├── build_player.py           # Regenerates index.html (Stethoscape) from catalog/catalog.csv
│   ├── player_template.html      # Hand-edited source template for the player (no embedded media)
│   └── assets/fonts/             # Vendored variable fonts (Fraunces, IBM Plex Sans/Mono) used by the player
└── README.md
```

**Design rationale:**
- Audio lives once, under its originating `sources/<slug>/`, next to that source's own license and manifest — this keeps attribution unambiguous per CC BY-NC-ND-style "ND" (no-derivatives) requirements, since we never copy/rename files into multiple disease or species folders.
- The `index/by-species/` and `by-disease/` folders are **generated views** (markdown tables linking back to the canonical audio files) — not copies — so a single recording can appear in multiple views (e.g. a dog + mitral-insufficiency page) without duplication.
- `catalog.csv` / `catalog.json` is the single machine-readable source of truth; regenerate it any time with `python3 scripts/build_catalog.py` after adding a new source.
- A recording's paired image (phonogram/spectrogram screenshot or a photo) is matched automatically by filename: any file under `sources/<slug>/images/` whose name **starts with** the audio file's stem (e.g. `aortic_valve_normal.wav` ↔ `aortic_valve_normal_phonogram.png`) is picked up as that recording's `image_path` in the catalog.

## Stethoscape player & quiz

`index.html` is **Stethoscape** — a single, fully self-contained web app (no build step, no external requests, no CDN) with two modes:

- **Browse** — filter by species and diagnosis category, search, play any recording, and expand a card for its full description, paired phonogram image, and attribution.
- **Quiz** — pick a scope (species / diagnosis groups / question count), listen, and pick the correct diagnosis from 4 options; get instant feedback with the phonogram and a score/streak readout, then a per-category accuracy breakdown at the end.

Every recording (transcoded to a small mono MP3) and every phonogram image is embedded directly in the file as base64 — that's why it's ~9.5 MB. This is deliberate: it means the exact same file works with **zero configuration** in three places:

1. **Double-click it locally** — `open index.html` (or drag it into a browser tab).
2. **GitHub Pages** — commit it at the repo root (already done) and enable Pages (Settings → Pages → Deploy from branch → `/ (root)`). It'll be live at `https://<user>.github.io/<repo>/` with no relative-path or CORS issues, since there are no external assets to break.
3. **As a Claude Artifact** — the strict artifact sandbox blocks all external requests, which is exactly why everything is embedded; the same file (minus the `<!DOCTYPE>`/`<html>` wrapper, see `scripts/build/artifact_fragment.html`) publishes directly.

**Regenerating it** after adding/editing a source: run `python3 scripts/build_catalog.py` first (to refresh `catalog/catalog.csv`), then `python3 scripts/build_player.py`. The build script transcodes audio to mono MP3 (~64 kbps, 11025 Hz — plenty for auscultation content, keeps total size small) and images to compressed JPEGs, then injects everything into `scripts/player_template.html` to produce both `index.html` (full document, doctype-wrapped, for GitHub/local use) and `scripts/build/artifact_fragment.html` (headless fragment, for Artifact publishing). Edit `scripts/player_template.html` for any design/logic changes — it contains no embedded media, so it's easy to diff and edit directly.

## Adding a new source

1. Create `sources/<slug>/manifest.csv` with columns:
   `id,category,url,local_filename,animal,breed,age,diagnosis_category,diagnosis,grade,description,source_page`
2. Write `sources/<slug>/download_<slug>.sh` (or reuse the pattern in `scripts/download_tiho.sh`) to fetch files into `sources/<slug>/audio/<category>/`.
3. Write `sources/<slug>/ATTRIBUTION.md` documenting the exact license, authors, and citation — **only add sources with a clear, verifiable open license** (CC of any variant, public domain, or explicit "free for education/research use").
4. Run `python3 scripts/build_catalog.py` to fold it into the master catalog and indexes.

## Diagnosis categories used

- `normal` — physiologic/no murmur, reference recordings
- `congenital` — congenital defects (PDA, VSD, pulmonic/subaortic stenosis, etc.)
- `acquired_valvular_disease` — degenerative/acquired valve disease (e.g. myxomatous mitral valve disease)
- `arrhythmia` — rate/rhythm disturbances (bradycardia, tachycardia, AV block, fibrillation, extrasystoles)

## Current sources

| Source | Species | Recordings | License |
|---|---|---|---|
| [tiho-hannover](sources/tiho-hannover/ATTRIBUTION.md) | Dog | 32 | CC BY-NC-ND 4.0 |
| [uq-equine-auscultation](sources/uq-equine-auscultation/ATTRIBUTION.md) | Horse | 16 (each with a paired phonogram image) | CC BY 4.0 |

See `catalog/catalog.csv` for the full per-recording index (48 recordings total).

## On expanding further

A broad search (vet schools, Merck Vet Manual, Zenodo, Figshare, Dryad, Kaggle, Mendeley Data, GitHub, PhysioNet, Hugging Face, IEEE DataPort, and arXiv/PubMed data-availability statements) found the open veterinary heart-sound-audio landscape to be thin beyond these two sources — most real datasets referenced in research papers (canine/feline/multi-species) are kept proprietary by the institutions that recorded them (e.g. Boehringer Ingelheim/Fraunhofer, Sonus Health, M3dicine/Stethee). Treat that as a real finding rather than incomplete search effort before re-running the same search. A promising next step if more sources are wanted: directly email corresponding authors of papers with real but unreleased datasets to ask about a CC-licensed release.

## Licensing note

Every source folder carries its own `ATTRIBUTION.md`. Several CC variants restrict commercial use (NC) and/or derivative works (ND) — check the specific source's license before any reuse beyond personal study/teaching. This repository does not relicense or waive any original license terms.
