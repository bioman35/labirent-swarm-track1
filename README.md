# Labirent: a sandbox where gates, not the model, carry the safety

Swarm Alignment Hackathon 2026 (Apart Research), Track 1: Sandboxes and Testbeds. Submission deadline 8 Nov 2026.

**Live replay (3D and 2D):** see GitHub Pages for this repository (`docs/`). Four unedited run records: a 7B model finishing the courier job, an outside covert agent falling into the yellow maze, an inside sleeper with a valid token, and another 7B model (Mistral) that cannot operate the world.

## Preexisting work (read this first)

Everything in this repository that was committed **before 6 November 2026 21:30 UTC** is preexisting work and is not part of the sprint submission's scored effort. It is listed file by file, with SHA256, in `oyun_alani_v4/PREEXISTING_EK_31eki.md` and sealed by the freeze list `oyun_alani_v4/DONDURMA_4KAS.sha256` (2,327 files, 4 November 2026 20:10 UTC, ledger entry 24 in `oyun_alani_v3/KILIT_DEFTERI.jsonl`, freeze commit `7391603`). This covers:

- the world code and gate rules (`oyun_alani_v4/`, frozen v4), the agent cards, the run drivers, the judge-summary generators;
- all run records made before the sprint (`oyun_alani_v4/kosular/`), including the development nights of 28-31 October and the 2 November single test run of the API driver;
- the pre-registration lock ledger and every lock text (EK1 to EK5b, entries 0-23), written and hashed before any scored run;
- the 3D replay stage (`film_labirent/`), built for our own run records before the sprint; three raw test clips, no narration, no editing.

**Work done during the sprint (6-8 November 2026):** the scored runs (Koşu 4, 5a, 5b, 5c; Luna judge EK5a and EK5b), their records and tables, the figures, the sprint film made on the replay stage, the report, and documentation edits such as this section. Each sprint-time file is listed in Appendix D of the report with its timestamp. The ledger hash chain shows that no lock text changed after the first scored run.

**What is not here:** the hidden answer keys for the judge runs (`luna/gizli/`) stay out of the repository until the report is submitted; the API keys are never in the repository.

**How to re-run:** see `README_RUN.md` (rebuild every table from the records at no cost, local re-runs, paid re-runs).

Team: Turan Kayık (design, decisions), with LLM assistance for code, measurement and writing (stated in the report).
