# Motion VOL. 3 — Batch 001 Preflight (2026-10-29)

**Status:** BLOCKED — 0/3 videos rendered, 0/3 episodes completed. This is a QA report, **not a rendered video deliverable**.

**Authoritative script:** [30 HARI Vol. 3](../naskah_40detik_unik_30hari_vol3.md).
**Engine:** [OpenMontage-portable-neon.zip](../OpenMontage-portable-neon.zip).
**Ledger:** [reels-production-ledger.json](../reels-production-ledger.json) — **unchanged**.

## Episode queue (not marked completed)
| HARI | Title | catalog_id | Status |
| --- | --- | --- | --- |
| 01 | 3 PAJAK PALING ANEH YANG PERNAH BERLAKU DI DUNIA | topic-13085e42c924e4c9 | pending |
| 02 | 3 PULAU DENGAN FENOMENA PALING UNIK DI BUMI | topic-5a48c39a912394e6 | pending |
| 03 | 3 TRIK PEMASARAN PALING CERDAS DALAM SEJARAH BISNIS | topic-414a57b203709403 | pending |

Catalog IDs are derived from NFKC-normalized casefolded title using SHA256 as specified by reels-batch-task.txt. No matching completed titles in current ledger.

## Technical blockers
- ZIP source is 77,579,166 bytes on GitHub but not mounted in the rendering container. Connected GitHub fetch_file(base64) returned empty content and fetch_blob raised UnicodeDecodeError; the GitHub connector cannot transfer this binary to the runtime.
- Container outbound network DNS to github.com and raw.githubusercontent.com failed, so archive/model/bootstrap dependencies could not be downloaded.
- Expected ZIP SHA256: `47841ff0b849209933d8a581423d1d252c4a46f92ca7ec4ee0d015092fbe7dc3`. Verification **not run** (no ZIP bytes).
- Piper neural Indonesia model and executable not present; original OpenMontage portable profile/skills inside ZIP could not be inspected. **No eSpeak or 2.5D fallback** was used.
- No native 3D render, audio alignment, subtitle, ffprobe/decode QC, or MP4 export was performed.

## Factual QA flags (original script remains unchanged)
- **HARI 01:** Peter I was **Tsar** in 1698, formally emperor only from 1721; "Kaisar Rusia" is anachronistic. Roman urine tax existed but the exclusive claim about whitening **nobility's** clothing is over-specific. Sources: https://www.britishmuseum.org/collection/object/C_C-3701 ; https://www.worldhistory.org/Peter_the_Great/ ; https://www.auajournals.org/doi/10.1016/j.juro.2010.02.2330
- **HARI 02:** Aoshima cat population **is no longer hundreds** (reported ~80 cats and ~3 residents in April 2026); the 6× ratio is not reliable as a current number. Sable Island horse counts fluctuate; Vulcan Point was affected by the 2020 Taal eruption. Sources: https://www.livescience.com/planet-earth/aoshima-japans-tiny-cat-island-where-felines-hugely-outnumber-humans ; https://www.parcs.canada.ca/pn-np/ns/sable/nature/animaux-animals/chevaux-horses ; https://www.geographyrealm.com/third-order-islands/
- **HARI 03:** Empty Red Bull cans in London bins and exactly 20% larger sauce-bottle openings **lack verified primary sourcing**. Diamond engagement rings **predate** the De Beers 1947 slogan; marketing popularized them, not invented them. Source: https://www.marketingsociety.com/the-library/tagline-forever

## Resume conditions
1. Provide an authorized runtime that can retrieve ZIP/model/dependencies, or mount the exact source archive and caches; verify SHA256 and run portable/bootstrap.py, portable/doctor.py and portable/smoke.py.
2. Resolve script factual QA flags **with approval**; do not silently alter final text.
3. Render 3 original native 1080x1920/30fps H264/AAC MP4s with Piper Indonesia, verify frames/audio/subtitles/CTA, then atomically update the completed ledger and deliver 3 real links.

**No MP4 or completed ledger entry was fabricated.**
