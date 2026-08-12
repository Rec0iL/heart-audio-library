# Source: Clinician's Brief — Cardiac Library: Cardiac Sounds

**Original pages:**
- https://www.cliniciansbrief.com/custom/cardiac-sounds (index)
- https://www.cliniciansbrief.com/custom/feline-heart-sounds-cardiac-sounds
- https://www.cliniciansbrief.com/custom/equine-heart-sounds-cardiac-sounds
- https://www.cliniciansbrief.com/custom/normal-heart-sounds-cardiac-sounds
- https://www.cliniciansbrief.com/custom/bradyarrhythmias-cardiac-sounds
- https://www.cliniciansbrief.com/custom/tachyarrhythmias-cardiac-sounds
- https://www.cliniciansbrief.com/custom/left-apical-murmurs-and-sounds-cardiac-sounds
- https://www.cliniciansbrief.com/custom/left-crainal-or-basilar-mitral-murmurs-cardiac-sounds
- https://www.cliniciansbrief.com/custom/left-crainal-or-basilar-murmurs-cardiac-sounds
- https://www.cliniciansbrief.com/custom/right-sided-murmurs-cardiac-sounds
- https://www.cliniciansbrief.com/custom/miscellaneous-sounds-cardiac-sounds
- individual recordings at `https://www.cliniciansbrief.com/cardiac-library/heart-sound/<slug>`

**Publisher:** Clinician's Brief (Educational Concepts, LLC), a commercial veterinary continuing-education publication.

## ⚠️ License status — NOT openly licensed

Unlike every other source in this library, **this content carries no Creative Commons or other open license**. The site displays a standard copyright/DMCA notice and no CC statement was found anywhere in the page markup. Recordings are embedded via **private, "secret-token" SoundCloud tracks** (e.g. `soundcloud.com/cliniciansbrief/sets/<slug>/s-<token>`) — unlisted and reachable only through the token-bearing link Clinician's Brief itself publishes, which is a signal they are not intended for open redistribution.

This source was added to the repository **at the explicit, informed request of the repository owner**, who was told of the above before deciding to proceed (2026-08-12). It does **not** meet this project's normal inclusion bar (see main README: "only add sources with a clear, verifiable open license"). Treat everything under this folder as **all rights reserved, personal/educational reference use only** — do not redistribute, publish, or use commercially without contacting Clinician's Brief / Educational Concepts, LLC for permission.

**Suggested citation:**
> Clinician's Brief. *Cardiac Library: Cardiac Sounds.* Educational Concepts, LLC. https://www.cliniciansbrief.com/custom/cardiac-sounds (accessed 2026-08-12).

## What was extracted

Each recording page embeds a SoundCloud player (a 2-track set: normal speed + a half-speed variant). Only the **first/normal-speed track** of each set was kept, downloaded via `yt-dlp` (re-encoded from SoundCloud's HLS/AAC stream to mono-compatible MP3 — this is a lossy re-encode, not a bit-exact copy of the original file, since SoundCloud does not expose the original upload for download).

**54 of 55** listed recordings were retrieved. `feline-murmur-with-purring` (`s-AW4MG`, SoundCloud playlist id 51476902) returns HTTP 404 from SoundCloud's own API as of the access date — the track appears to have been removed or unpublished on SoundCloud's side, independent of this scrape. Not included.

Site text notes: *"These recordings, taken with an electronic stethoscope on actual patients, may include some background noise... Unless specified, all sounds are from canine patients."*

## Diagnosis-category classification

`diagnosis_category` values were assigned programmatically from each recording's title (first matching lesion/rhythm keyword wins, left-to-right) with a fallback to the Clinician's Brief category page it was listed under, then spot-checked against the full article body text. One title (`Valvular Aortic Stenosis and Aortic Insufficiency`) was reclassified from its title-implied bucket to `congenital` because the article body explicitly describes "congenital aortic valve stenosis." This is a best-effort classification for study purposes, not a clinical coding exercise — consult the `description` field (drawn directly from the original article body) for the actual clinical detail.

This source also introduces a fifth `diagnosis_category`, **`other`**, for sounds that are named phenomena rather than a specific lesion/rhythm (gallop sounds, systolic clicks, split S2, pericardial friction rub, hypertrophic cardiomyopathy with dynamic outflow obstruction, and murmurs the source itself leaves etiologically unspecified).

## Species

`feline-heart-sounds` and `equine-heart-sounds` page membership (or an explicit species word in the title) drove the `animal` field; everything else defaults to `dog` per the site's own stated default.
