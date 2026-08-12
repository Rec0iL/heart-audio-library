# Source: UQ Equine Cardiac Auscultation Learning Resource

**Original publication:** Wood, A., Shapter, F. M., & Stewart, A. J. (2024). *Assessment of a Teaching Module for Cardiac Auscultation of Horses by Veterinary Students.* Animals (Basel), 14(9), 1341. https://doi.org/10.3390/ani14091341

**Institution:** School of Veterinary Science, University of Queensland (UQ), Australia.

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) — https://creativecommons.org/licenses/by/4.0/
Quoted from the article: *"This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license."* CC BY permits commercial use and derivative works, provided attribution is given.

**Original supplementary file:** `animals-14-01341-s001.zip` ("File S1. Final Student Version Cardiovascular Recordings.pptx"), retrieved from the PubMed Central mirror: https://pmc.ncbi.nlm.nih.gov/articles/instance/11083587/bin/animals-14-01341-s001.zip — kept as-downloaded under `raw/` for provenance (local only; `sources/*/raw/` is gitignored due to size — re-fetch from the PMC URL above if needed).

**What was extracted:** The supplementary file is a PowerPoint teaching deck with 16 embedded audio recordings (PCM WAV, 4 kHz mono — consistent with the Eko CORE digital stethoscope used for capture) and their paired phonocardiogram waveform screenshots. Audio and images were extracted programmatically from the `.pptx` (itself a zip container); no audio content was edited, cropped, or re-encoded — only repackaged into individual files with descriptive names.

**Animals recorded:** ~51 horses per the paper (35 healthy adults, 10 foals, 6 clinical cardiac cases); individual horse identity is only named in the source material for the Pentalogy of Fallot case ("UQ Billy"). Other recordings do not specify which individual horse they came from.

**Suggested citation:**
> Wood, A., Shapter, F. M., & Stewart, A. J. (2024). Assessment of a Teaching Module for Cardiac Auscultation of Horses by Veterinary Students. *Animals*, 14(9), 1341. https://doi.org/10.3390/ani14091341. Supplementary File S1, CC BY 4.0.

## Contents of this source folder
- `audio/normal/` — 5 recordings: aortic/mitral/tricuspid valve normal sounds, a "realistic" tricuspid recording with GIT noise, and a physiologic S3 gallop
- `audio/acquired/` — 2 recordings: mitral regurgitation (auscultated at the mitral valve, and its radiated murmur at the aortic valve)
- `audio/congenital/` — 5 recordings: ventricular septal defect (2 valve positions) and Pentalogy of Fallot (3 valve positions, "UQ Billy")
- `audio/arrhythmia/` — 4 recordings: atrial fibrillation and 2nd degree AV block, each at 2 valve positions
- `images/<category>/` — the paired phonocardiogram waveform screenshot for each recording above
- `images/general/` — one representative photo of the Eko CORE auscultation technique used to record this dataset (from the same slide deck)
