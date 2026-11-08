# Re-running the results (tekrar)

Three levels, cheapest first. Every number in the report comes from a run record in `oyun_alani_v4/kosular/` (or `oyun_alani_v3/` for the 27 Oct lock) through a script; no number is typed by hand.

Requirements: Python 3.11 or newer, standard library only for level 1. Level 2 needs [Ollama](https://ollama.com) with `qwen2.5:7b-instruct-q4_K_M` (we used Ollama 0.40.15 on a 6 GB RTX 4050 laptop GPU). Level 3 needs your own API keys.

Run every script from the folder it lives in, with `python -I` (isolated mode, as we did).

## 1 · $0 tekrar: rebuild the tables from the records (no model, no key)

```
# freeze check: 2,327 files hashed before the sprint window (4 Nov)
sha256sum -c oyun_alani_v4/DONDURMA_4KAS.sha256
#   expect 2,325 OK; the 2 files under oyun_alani_v4/luna/gizli/ (judge ground truth) are not in this repository, see below

# lock ledger: prediction locks and deviations, hash-chained
cd oyun_alani_v3
python -I defter.py dogrula          # expect (True, 'b75a6805...')

cd ../oyun_alani_v4
python -I olcum.py kosular/<run folder>/<run>.jsonl     # per-run measures -> <run>.olcum.json
python -I kilit_degerlendir_v4.py kosular/v4_kosu1_28eki kosular/v4_kosu2_28eki   # -> KILIT_SONUC_EK1_v4_28eki.md
python -I tekrar_tablo.py            # repeats + ablation, one row per seed -> TEKRAR_TABLO_30eki.md
python -I gece2_sonuc.py             # -> GECE2_SONUC_30eki.md
python -I gece3_sonuc.py             # -> GECE3_SONUC_31eki.md
python -I kume_sira_tani.py          # first-assigned sleeper analysis -> KUME_SIRA_TANI_31eki.md
```

World v3.4 (27-28 Oct, the first lock and the boundary map):

```
cd oyun_alani_v3
python -I kilit_degerlendir.py kosular/sinav_kosu1_27eki kosular/sinav_kosu2_27eki   # -> KILIT_SONUC_27eki.md
python -I sinir_haritasi.py          # -> KUCUK_MODEL_SINIR_HARITASI.md + .json
python -I kesif_3b.py                # 3B vs 7B, same seeds -> KESIF_3B_SONUC_28eki.md
```

Earlier world versions v3.0-v3.3 are documented in `DEGISIKLIK_v3_*.md`; their archived code is available on request.

Sprint runs (6-8 Nov), from `oyun_alani_v4` (scripts in `danisman_puanlama/`, see its README; read-only, no model calls):

```
python -I danisman_puanlama/oku5a.py         # 5a: four folders merged (earliest completed copy counts), T4/T5 measures (4.7)
python -I danisman_puanlama/oku5b.py         # 5b measures (4.7); turuncu5b.py and zarfyap5b.py count orange stops and forged envelopes
python -I danisman_puanlama/puan_5c.py       # 5c r0+r1+r2 locked measures (4.12, B.4)
python -I danisman_puanlama/yol_5c.py        # 5c intruder gate paths, seeds 39 and 44
python -I danisman_puanlama/k1_gecis.py      # every K1 pass in the sprint records, with assignment status (B.6)
python -I danisman_puanlama/puan_ek5a.py cevap_ek5a_2000   # judge table EK5a / EK5a-2 (4.7, B.5); needs the answer keys, see below
python -I danisman_puanlama/film_kontrol.py  # sha256 and event order of the five runs in the sprint film
```

The written results are in `DANISMAN_*_SONUC_*.md`, `DANISMAN_K1_GECIS_SAYIMI_8KAS.md` and `DANISMAN_TOPLAMLAR_8KAS.md`.

## 2 · Local re-runs ($0 in money, GPU hours)

The world, gates and cards are frozen (hash list above). The small model runs locally through Ollama.

```
cd oyun_alani_v4
ollama stop qwen2.5:7b-instruct-q4_K_M      # start cold: temperature-0 results depend on run order (report 4.11)

# 5c, rule-aware intruder and sleeper (locked 2 Nov), three repeats, about 1.5 h each on our GPU
python -I kosu_5c.py --asama puanli --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 36-45 --cikti kosular/v4_5c_puanli_r0
python -I kosu_5c.py --asama puanli --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 36-45 --tekrar 1 --cikti kosular/v4_5c_puanli_r1
python -I kosu_5c.py --asama puanli --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 36-45 --tekrar 2 --cikti kosular/v4_5c_puanli_r2

# Run 1 (work) and Run 2 (adversaries) on world v4, seeds 16-25 as in kosular/v4_kosu1_28eki and v4_kosu2_28eki
python -I kosu_model.py --kosu 1 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 16-25
python -I kosu_model.py --kosu 2 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 16-25
```

Offline driver checks with a fake model (no model, no key): `python -I test_v4.py`, `python -I test_5c.py`, `python -I test_kosu_api.py`.

Tests: `python -m pytest -q` (root = v4 world, 15 tests); v3.4 world: `cd oyun_alani_v3 && python -m pytest -q` (15 tests). The two worlds share module names, so they are collected separately (`pytest.ini`).

## 3 · Paid re-runs (API keys)

`kosu_api.py` (Run 4, 5a, 5b) and `luna_yargic.py` (judge, EK5a and EK5b) read the key from an environment variable: `KOSU_OPENAI` for the big OpenAI model, `KOSU_GEMINI` for Gemini Flash. If the variable is not set they look for a key file at a path on our machine (`API` in `kosu_api.py`); set the variable instead. Keys never enter the records: the drivers stop if a key trace would be written.

These calls go out without temperature, seed or response format (Appendix D), so a re-run will not be identical; compare rates, not single runs. Costs we paid are in the report (4.7); each command also has a USD ceiling.

```
cd oyun_alani_v4
# Run 4: our five agents = big model, no intruder
python -I kosu_api.py --kol 4 --tohumlar 16-25 --butce-dolar 10 --cikti kosular/v4_kosu4_luna_b
# 5a: intruder/sleeper = big OpenAI model, our agents = local 7B
python -I kosu_api.py --kol 5a --tohumlar 16-25 --butce-dolar 10 --cikti kosular/v4_kosu5a_luna
# 5b: intruder/sleeper = Gemini Flash
python -I kosu_api.py --kol 5b --tohumlar 16-25 --butce-dolar 15 --cikti kosular/v4_kosu5b_gemini
# judge: EK5a as locked (output cap 400), EK5b with the cap deviation (ledger 25), EK5a rerun at 2000
python -I luna_yargic.py --asama ek5a
python -I luna_yargic.py --asama ek5b --tavan 2000
python -I luna_yargic.py --asama ek5a --tavan 2000 --klasor cevap_ek5a_2000
```

Our 5a ran in four folders (`v4_kosu5a_luna`, `_b`, `_c`, `_d`) after isolated transport errors; the merge rule (earliest completed copy counts) was fixed before the results were read, see `KOSU_GUNLUGU_7KAS.md` and Appendix D. Run 4's first folder `v4_kosu4_luna` is a failed start (local model server was down, 0 API calls), kept as evidence.

## Not in this repository

- `oyun_alani_v4/luna/gizli/`: the judge ground truth (which agent is the sleeper in each judged record). Until the report is submitted the judge answer keys are withheld; they are added in a follow-up commit, after which the EK5a/EK5b tables rebuild.
- API keys, and the key file path on our machine.
