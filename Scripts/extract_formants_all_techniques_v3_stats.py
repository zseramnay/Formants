#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
EXTRACTEUR DE FORMANTS ORCHIDEA SOL — TOUTES TECHNIQUES
Version 2.0 — Analyse étendue par technique de jeu
═══════════════════════════════════════════════════════════════════════════════

DESCRIPTION
-----------
Ce script analyse les bases de données Orchidea (FullSOL2020 et Yan_Adds) en
traitant CHAQUE combinaison instrument×technique comme une entité distincte.

Chaque entrée de sortie représente le profil formantique moyen d'un instrument
dans une technique de jeu donnée, enrichi de trois méta-descripteurs :

  • reliability_score  [0–1]  Stabilité des pics formantiques inter-notes
  • rugosity          [0–1]  Rugosité spectrale (sons bruités / flatterzunge)
  • suddenness        [0–1]  Caractère transitoire (col legno, slap, etc.)

SOURCES REQUISES (fichiers .db.txt Orchidea)
--------------------------------------------
  Obligatoires :
    FullSOL2020_specenv.db.txt     — enveloppes spectrales
    Yan_Adds-Divers_specenv_db.txt — idem pour instruments additionnels

  Fortement recommandés (améliore reliability) :
    FullSOL2020_specpeaks.db.txt
    Yan_Adds-Divers_specpeaks.db.txt

  Optionnels (active Rugosity mesurée) :
    FullSOL2020_moments.db.txt     — centroïde, spread, skewness, kurtosis
    Yan_Adds-Divers_moments.db.txt

USAGE
-----
  # Usage simple (auto-détection dans un dossier) :
  python3 extract_formants_all_techniques.py /chemin/vers/dossier/

  # Avec fichiers explicites :
  python3 extract_formants_all_techniques.py \
      --specenv  FullSOL2020_specenv.db.txt Yan_Adds-Divers_specenv_db.txt \
      --specpeaks FullSOL2020_specpeaks.db.txt Yan_Adds-Divers_specpeaks.db.txt \
      --moments  FullSOL2020_moments.db.txt Yan_Adds-Divers_moments.db.txt \
      --output   formants_all_techniques.csv --raw

  # Ajouter --raw pour obtenir aussi le CSV brut par échantillon

SORTIES
-------
  formants_all_techniques.csv      — 1 ligne par instrument×technique
  formants_all_techniques_raw_samples.csv  (avec --raw) — 1 ligne par échantillon

═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import csv
import re
import math
import argparse
import glob
from collections import defaultdict


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_RATE   = 44100
FFT_SIZE      = 4096
FREQ_RES      = SAMPLE_RATE / FFT_SIZE   # ≈ 10.77 Hz/bin

FORMANT_MIN_HZ      = 80
FORMANT_MAX_HZ      = 6000
FORMANT_MIN_BIN     = int(FORMANT_MIN_HZ / FREQ_RES)
FORMANT_MAX_BIN     = int(FORMANT_MAX_HZ / FREQ_RES)

MAX_FORMANTS        = 6
PEAK_THRESHOLD_DB   = 30
MIN_PEAK_DIST_HZ    = 70
MIN_PEAK_DIST_BINS  = max(1, int(MIN_PEAK_DIST_HZ / FREQ_RES))

SPECPEAKS_MATCH_HZ  = 60
MIN_SAMPLES_FOR_PROFILE = 2


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — CLASSIFICATION SOUDAINETÉ (Suddenness)
# Annotation sémantique par nom de technique — plus fiable que logAttackTime
# absent des fichiers Orchidea (tous steady-state).
# ─────────────────────────────────────────────────────────────────────────────

SUDDEN_HIGH = {
    'col_legno_battuto', 'slap_pitched', 'slap_unpitched', 'key_click',
    'tongue_ram', 'pizzicato', 'bartok_pizzicato', 'snap_pizzicato',
    'col_legno', 'palm_mute', 'staccatissimo', 'sforzando',
}

SUDDEN_MED = {
    'staccato', 'spiccato', 'portato', 'accent', 'sfz',
    'note_bend', 'glissando', 'portamento',
    'breath_attack', 'double_tonguing', 'triple_tonguing',
}

def get_suddenness(technique):
    t = technique.lower().replace('-', '_').replace(' ', '_')
    for keyword in SUDDEN_HIGH:
        if keyword.lower() in t:
            return 1.0
    for keyword in SUDDEN_MED:
        if keyword.lower() in t:
            return 0.5
    return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — CLASSIFICATION FAMILLE TIMBRALE
# ─────────────────────────────────────────────────────────────────────────────

def get_technique_family(technique):
    t = technique.lower()
    # Mutes must be checked BEFORE ordinario — SOL uses 'ordinario+sordina_cup' etc.
    if 'sordina' in t or 'sourdine' in t or 'mute' in t:
        if 'cup'      in t: return 'mute_cup'
        if 'harmon'   in t: return 'mute_harmon'
        if 'straight' in t: return 'mute_straight'
        if 'wah'      in t or 'plunger' in t: return 'mute_wah'
        if 'bucket'   in t: return 'mute_bucket'
        return 'mute_other'
    if 'ordinario' in t or t in ('normal', 'sustain', 'arco'):
        return 'ordinario'
    if 'sul_ponticello' in t or 'ponticello' in t: return 'sul_ponticello'
    if 'sul_tasto'      in t or 'tasto' in t:      return 'sul_tasto'
    if 'col_legno'      in t:                      return 'col_legno'
    if 'pizzicato'      in t or 'pizz' in t:       return 'pizzicato'
    if 'harmonic'       in t:                      return 'harmonics'
    if 'tremolo'        in t:                      return 'tremolo'
    if 'behind_the_bridge' in t:                   return 'behind_bridge'
    if 'flatterzunge'   in t or 'flutter' in t or 'frullato' in t: return 'flutter'
    if 'brassy'         in t or 'cuivré' in t:     return 'brassy'
    if 'multiphonic'    in t:                      return 'multiphonic'
    if 'breath'         in t or 'aeolian' in t:    return 'breath_tone'
    if 'double_tonguing' in t or 'triple_tonguing' in t: return 'tonguing'
    if 'slap'           in t:                      return 'slap'
    if 'key_click'      in t:                      return 'key_click'
    if 'tongue_ram'     in t:                      return 'tongue_ram'
    if 'bisbigliando'   in t:                      return 'bisbigliando'
    if 'buzz'           in t:                      return 'buzz'
    if 'crescendo'      in t:                      return 'crescendo'
    if 'trill'          in t:                      return 'trill'
    if 'vibrato'        in t:                      return 'vibrato'
    if 'glissando'      in t:                      return 'glissando'
    if 'portamento'     in t:                      return 'portamento'
    if 'staccato'       in t:                      return 'staccato'
    if 'sforzando'      in t or 'sfz' in t:        return 'sforzando'
    return 'other'


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — PARSING DES FICHIERS DB.TXT ORCHIDEA
# ─────────────────────────────────────────────────────────────────────────────

def parse_header(line):
    parts = line.strip().split()
    if len(parts) < 4:
        raise ValueError(f"Header invalid: '{line}'")
    return parts[0], int(parts[1]), int(parts[2]), int(parts[3])


def parse_db_file(filepath, expected_type=None, verbose=False):
    """
    Lit un fichier .db.txt Orchidea.
    Retourne dict { sample_path_str : [float, ...] }
    """
    data = {}
    if not os.path.isfile(filepath):
        if verbose:
            print(f"  [WARNING] File not found: {filepath}")
        return data

    if verbose or True:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  Reading {os.path.basename(filepath)} ({size_mb:.1f} MB)...")

    n_values = None
    header_read = False

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            if not header_read:
                try:
                    db_type, fft_sz, hop_sz, n_val = parse_header(line)
                    n_values = n_val
                    if verbose and expected_type and db_type != expected_type:
                        print(f"  [INFO] Detected type: '{db_type}' (expected '{expected_type}')")
                    header_read = True
                    continue
                except (ValueError, IndexError):
                    header_read = True

            parts = line.split(';')
            if len(parts) < 2:
                continue

            sample_path = parts[0]
            try:
                values = [float(v) for v in parts[1:] if v.strip()]
            except ValueError:
                continue

            if n_values is not None and abs(len(values) - n_values) > 2:
                continue

            data[sample_path] = values

    print(f"    → {len(data):,} samples loaded")
    return data


def parse_filename(sample_path):
    """
    Extrait (instrument, technique, note, dynamic) d'un chemin SOL.
    Format attendu : /Family/Instrument/Technique/filename.wav
    """
    path = sample_path.replace('\\', '/')
    basename = os.path.basename(path)
    parts = path.strip('/').split('/')

    if len(parts) >= 3:
        instrument = parts[-3]
        technique  = parts[-2]
    else:
        instrument = 'Unknown'
        technique  = 'Unknown'

    instrument = instrument.strip().replace(' ', '_')
    technique  = technique.strip()

    note_match = re.search(r'[-_](([A-Gb#]+)(\d{1,2}))[-_]', basename, re.IGNORECASE)
    dyn_match  = re.search(r'[-_](ppp|pp|p|mp|mf|f|ff|fff)[-_.]', basename, re.IGNORECASE)

    note    = note_match.group(1)           if note_match else 'unknown'
    dynamic = dyn_match.group(1).lower()    if dyn_match  else 'unknown'

    return instrument, technique, note, dynamic


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — DÉTECTION DE FORMANTS
# ─────────────────────────────────────────────────────────────────────────────

def bin_to_hz(bin_idx):
    return bin_idx * FREQ_RES

def find_formant_peaks(envelope, max_peaks=MAX_FORMANTS):
    """
    Retourne [(freq_hz, amplitude_db), ...] triés par fréquence.
    """
    if not envelope or len(envelope) < FORMANT_MIN_BIN + 1:
        return []

    # Specenv values are already in dB (negative floats) — use directly
    env_db = list(envelope)

    lo = max(FORMANT_MIN_BIN, 1)
    hi = min(FORMANT_MAX_BIN, len(env_db) - 1)
    if hi <= lo:
        return []

    region = env_db[lo:hi]
    max_val = max(region) if region else -120.0
    threshold = max_val - PEAK_THRESHOLD_DB

    peaks = []
    for i in range(1, len(region) - 1):
        v = region[i]
        if v < threshold:
            continue
        if v >= region[i - 1] and v >= region[i + 1]:
            freq_hz = bin_to_hz(lo + i)
            peaks.append((freq_hz, v))

    # Garder les plus forts, distance minimum
    peaks.sort(key=lambda x: x[1], reverse=True)
    selected = []
    for freq, amp in peaks:
        if not any(abs(freq - sf) < MIN_PEAK_DIST_HZ for sf, _ in selected):
            selected.append((freq, amp))
        if len(selected) >= max_peaks:
            break

    selected.sort(key=lambda x: x[0])
    return selected


def specpeaks_contains(peaks_vector, target_hz, tolerance_hz=SPECPEAKS_MATCH_HZ):
    """
    Vérifie si peaks_vector (format alternant freq/amp) contient un pic
    proche de target_hz.
    """
    if not peaks_vector:
        return False
    for i in range(0, len(peaks_vector) - 1, 2):
        if abs(peaks_vector[i] - target_hz) <= tolerance_hz:
            return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — RUGOSITÉ SPECTRALE
# ─────────────────────────────────────────────────────────────────────────────

def compute_spectral_irregularity(envelope):
    """
    Méthode Jensen (1999) : mesure la déviation de chaque bin par rapport
    à la moyenne locale de ses voisins.
    Son harmonique lisse → faible. Son bruité/rugueux → élevé.
    """
    if len(envelope) < 3:
        return 0.0
    lo = max(FORMANT_MIN_BIN, 1)
    hi = min(FORMANT_MAX_BIN, len(envelope) - 1)
    # Specenv values are already in dB — use directly
    total, count = 0.0, 0
    for i in range(lo, hi):
        dp = envelope[i-1]
        dc = envelope[i]
        dn = envelope[i+1]
        local_mean = (dp + dc + dn) / 3.0
        total += (dc - local_mean) ** 2
        count += 1
    return total / count if count > 0 else 0.0


def compute_rugosity(irregularity, kurtosis=None):
    """
    Score de Rugosité [0–1] combinant irrégularité specenv et kurtosis moments.
    Kurtosis Orchidea élevé (>5) → spectre piqué/harmonique → rugosité faible.
    Kurtosis faible (<1) → spectre plat/bruité → rugosité élevée.
    """
    irr_norm = min(1.0, irregularity / 50.0)
    if kurtosis is not None and kurtosis > 0:
        kurt_norm = 1.0 - min(1.0, max(0.0, (kurtosis - 0.5) / 20.0))
        return min(1.0, 0.6 * irr_norm + 0.4 * kurt_norm)
    return min(1.0, irr_norm)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — SCORE DE FIABILITÉ
# ─────────────────────────────────────────────────────────────────────────────

def compute_reliability(formant_lists, specpeaks_confirmations, sample_count):
    """
    Score de fiabilité [0–1] d'un profil instrument×technique.

    Critère 1 (45%) — Cohérence F1 inter-notes : std < 300 Hz → score ↑
    Critère 2 (35%) — Confirmation specpeaks pour F1
    Critère 3 (20%) — Bonus logarithmique taille d'échantillon (max à N=30)
    """
    if sample_count < MIN_SAMPLES_FOR_PROFILE:
        return 0.0

    # Cohérence F1
    f1_values = [fl[0][0] for fl in formant_lists if fl]
    consistency_score = 0.0
    if len(f1_values) >= 2:
        mean_f1 = sum(f1_values) / len(f1_values)
        std_f1  = math.sqrt(sum((f - mean_f1)**2 for f in f1_values) / len(f1_values))
        consistency_score = max(0.0, 1.0 - std_f1 / 300.0)

    # Confirmation specpeaks
    if specpeaks_confirmations:
        confirmed = sum(1 for c in specpeaks_confirmations if c)
        confirmation_score = confirmed / len(specpeaks_confirmations)
    else:
        confirmation_score = 0.5  # neutre si absents

    # Bonus taille
    sample_bonus = min(1.0, math.log(sample_count + 1) / math.log(31))

    score = (0.45 * consistency_score +
             0.35 * confirmation_score +
             0.20 * sample_bonus)
    return round(min(1.0, max(0.0, score)), 3)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — AGRÉGATION PAR INSTRUMENT × TECHNIQUE
# ─────────────────────────────────────────────────────────────────────────────

def aggregate_profiles(samples):
    groups = defaultdict(list)
    for path, s in samples.items():
        groups[(s['instrument'], s['technique'])].append(s)

    profiles = {}
    for (inst, tech), group in groups.items():
        n = len(group)
        formant_lists    = [s['formants'] for s in group]
        sp_confirmations = [s['specpeaks_confirm'] for s in group]
        irregularities   = [s['irregularity'] for s in group]
        kurtosis_vals    = [s['kurtosis'] for s in group if s['kurtosis'] is not None]

        # Statistiques complètes de chaque formant Fi
        formant_medians = []
        formant_stats = []  # list of dicts: mean, std, q25, q75 per formant
        for fi in range(MAX_FORMANTS):
            fi_freqs = [fl[fi][0] for fl in formant_lists if fi < len(fl)]
            fi_amps  = [fl[fi][1] for fl in formant_lists if fi < len(fl)]
            if fi_freqs:
                sf = sorted(fi_freqs)
                nn = len(sf)
                median_freq = sf[nn // 2]
                median_amp  = sorted(fi_amps)[len(fi_amps) // 2]
                formant_medians.append((round(median_freq, 1), round(median_amp, 2)))
                # Mean
                mean_f = sum(fi_freqs) / nn
                # Std
                if nn > 1:
                    std_f = math.sqrt(sum((x - mean_f)**2 for x in fi_freqs) / nn)
                else:
                    std_f = 0.0
                # Q25 / Q75
                q25_f = sf[max(0, int(nn * 0.25))]
                q75_f = sf[min(nn - 1, int(nn * 0.75))]
                formant_stats.append({
                    'mean': round(mean_f, 1),
                    'std':  round(std_f, 1),
                    'q25':  round(q25_f, 1),
                    'q75':  round(q75_f, 1),
                })
            else:
                formant_stats.append(None)

        mean_irr  = sum(irregularities) / len(irregularities) if irregularities else 0.0
        mean_kurt = sum(kurtosis_vals)  / len(kurtosis_vals)  if kurtosis_vals  else None
        rugosity  = round(compute_rugosity(mean_irr, mean_kurt), 3)
        suddenness   = get_suddenness(tech)
        reliability  = compute_reliability(formant_lists, sp_confirmations, n)
        tech_family  = get_technique_family(tech)

        def fhz(i): return formant_medians[i][0] if i < len(formant_medians) else None
        def fstat(i, key): return formant_stats[i][key] if i < len(formant_stats) and formant_stats[i] else None

        profiles[(inst, tech)] = {
            'instrument':        inst,
            'technique':         tech,
            'technique_family':  tech_family,
            'n_samples':         n,
            'F1_hz':  fhz(0), 'F2_hz': fhz(1), 'F3_hz': fhz(2),
            'F4_hz':  fhz(3), 'F5_hz': fhz(4), 'F6_hz': fhz(5),
            # ── v3: statistiques descriptives par formant ──
            'F1_mean': fstat(0,'mean'), 'F1_std': fstat(0,'std'), 'F1_q25': fstat(0,'q25'), 'F1_q75': fstat(0,'q75'),
            'F2_mean': fstat(1,'mean'), 'F2_std': fstat(1,'std'), 'F2_q25': fstat(1,'q25'), 'F2_q75': fstat(1,'q75'),
            'F3_mean': fstat(2,'mean'), 'F3_std': fstat(2,'std'), 'F3_q25': fstat(2,'q25'), 'F3_q75': fstat(2,'q75'),
            'F4_mean': fstat(3,'mean'), 'F4_std': fstat(3,'std'),
            'F5_mean': fstat(4,'mean'), 'F5_std': fstat(4,'std'),
            'F6_mean': fstat(5,'mean'), 'F6_std': fstat(5,'std'),
            'reliability_score': reliability,
            'rugosity':          rugosity,
            'suddenness':        suddenness,
            'mean_kurtosis':     round(mean_kurt, 3) if mean_kurt is not None else None,
            'mean_irregularity': round(mean_irr, 3),
        }
    return profiles


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 — ÉCRITURE DES CSV
# ─────────────────────────────────────────────────────────────────────────────

PROFILE_COLS = [
    'instrument', 'technique', 'technique_family', 'n_samples',
    'F1_hz', 'F2_hz', 'F3_hz', 'F4_hz', 'F5_hz', 'F6_hz',
    # ── v3: statistiques descriptives ──
    'F1_mean', 'F1_std', 'F1_q25', 'F1_q75',
    'F2_mean', 'F2_std', 'F2_q25', 'F2_q75',
    'F3_mean', 'F3_std', 'F3_q25', 'F3_q75',
    'F4_mean', 'F4_std',
    'F5_mean', 'F5_std',
    'F6_mean', 'F6_std',
    'reliability_score', 'rugosity', 'suddenness',
    'mean_kurtosis', 'mean_irregularity',
]

RAW_COLS = [
    'sample_path', 'instrument', 'technique', 'note', 'dynamic',
    'F1_hz', 'F1_db', 'F2_hz', 'F2_db', 'F3_hz', 'F3_db',
    'F4_hz', 'F4_db', 'F5_hz', 'F5_db', 'F6_hz', 'F6_db',
    'irregularity', 'kurtosis', 'specpeaks_confirm',
]


def write_profiles_csv(profiles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=PROFILE_COLS, extrasaction='ignore')
        w.writeheader()
        for key in sorted(profiles.keys()):
            w.writerow(profiles[key])
    print(f"\n✔ Profiles written : {output_path}  ({len(profiles)} rows)")


def write_raw_csv(samples, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=RAW_COLS, extrasaction='ignore')
        w.writeheader()
        for path, s in sorted(samples.items()):
            row = {
                'sample_path':  path,
                'instrument':   s['instrument'],
                'technique':    s['technique'],
                'note':         s['note'],
                'dynamic':      s['dynamic'],
                'irregularity': round(s['irregularity'], 3),
                'kurtosis':     round(s['kurtosis'], 3) if s['kurtosis'] is not None else '',
                'specpeaks_confirm': '1' if s['specpeaks_confirm'] else '0',
            }
            for fi, (fhz, fdb) in enumerate(s['formants']):
                row[f'F{fi+1}_hz'] = fhz
                row[f'F{fi+1}_db'] = fdb
            w.writerow(row)
    print(f"✔ Raw samples written: {output_path}  ({len(samples)} rows)")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 — PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def find_db_files(folder, suffix):
    return sorted(glob.glob(os.path.join(folder, f'*{suffix}*')))


def run(specenv_files, specpeaks_files, moments_files, output_profile,
        output_raw, verbose):

    print("\n═══════════════════════════════════════════════════════")
    print("  FORMANT EXTRACTOR — ALL TECHNIQUES v2.0")
    print("═══════════════════════════════════════════════════════\n")

    print("── LOADING FILES ───────────────────────────────────────")
    all_specenv   = {}
    all_specpeaks = {}
    all_moments   = {}

    for fp in specenv_files:
        all_specenv.update(parse_db_file(fp, 'specenv', verbose))
    for fp in specpeaks_files:
        all_specpeaks.update(parse_db_file(fp, 'specpeaks', verbose))
    for fp in moments_files:
        all_moments.update(parse_db_file(fp, 'moments', verbose))

    print(f"\n  specenv  : {len(all_specenv):,} samples")
    print(f"  specpeaks: {len(all_specpeaks):,} samples")
    print(f"  moments  : {len(all_moments):,} samples")

    if not all_specenv:
        print("\n[ERROR] No specenv data loaded. Check your file paths.")
        sys.exit(1)

    # ── Per-sample analysis ──────────────────────────────────────────────────
    print("\n── FORMANT DETECTION ───────────────────────────────────")
    samples_data = {}
    unknown_count = 0

    for path, envelope in all_specenv.items():
        inst, tech, note, dyn = parse_filename(path)
        if inst == 'Unknown':
            unknown_count += 1
            continue

        formants     = find_formant_peaks(envelope)
        irregularity = compute_spectral_irregularity(envelope)

        kurtosis = None
        if path in all_moments:
            m = all_moments[path]
            if len(m) >= 4:
                kurtosis = m[3]   # moments order: centroid, spread, skewness, kurtosis

        specpeaks_confirm = False
        if path in all_specpeaks and formants:
            specpeaks_confirm = specpeaks_contains(all_specpeaks[path], formants[0][0])

        samples_data[path] = {
            'instrument':        inst,
            'technique':         tech,
            'note':              note,
            'dynamic':           dyn,
            'formants':          formants,
            'irregularity':      irregularity,
            'kurtosis':          kurtosis,
            'specpeaks_confirm': specpeaks_confirm,
        }

    print(f"  {len(samples_data):,} samples analysed")
    if unknown_count > 0:
        print(f"  {unknown_count:,} unparsable paths skipped")

    tech_counter = defaultdict(int)
    for s in samples_data.values():
        tech_counter[(s['instrument'], s['technique'])] += 1
    print(f"  {len(tech_counter):,} unique instrument×technique combinations\n")

    # ── Aggregate ───────────────────────────────────────────────────────────
    print("── AGGREGATING PROFILES ────────────────────────────────")
    profiles = aggregate_profiles(samples_data)
    print(f"  {len(profiles):,} profiles generated")

    fam_counter = defaultdict(int)
    for p in profiles.values():
        fam_counter[p['technique_family']] += 1

    print("\n  Breakdown by technique family:")
    for fam in sorted(fam_counter, key=lambda x: fam_counter[x], reverse=True):
        print(f"    {fam:<25} {fam_counter[fam]:>4} profiles")

    # ── Write outputs ────────────────────────────────────────────────────────
    print("\n── WRITING OUTPUTS ─────────────────────────────────────")
    write_profiles_csv(profiles, output_profile)
    if output_raw:
        write_raw_csv(samples_data, output_raw)

    # ── Terminal preview ─────────────────────────────────────────────────────
    print("\n── PREVIEW — first 20 profiles ─────────────────────────")
    hdr = "{:<28} {:<30} {:>5}  {:>7}  {:>7}  {:>7}  {:>7}  {:>7}"
    row = "{:<28} {:<30} {:>5}  {:>7.1f}  {:>7.3f}  {:>7.3f}  {:>7.3f}  {:>7.1f}"
    print(hdr.format("Instrument","Technique","N","F1(Hz)","Reliab.","Rugosity","Sudden.","Kurt."))
    print("─" * 105)
    for i, key in enumerate(sorted(profiles.keys())):
        if i >= 20:
            print(f"  ... ({len(profiles)-20} more profiles in CSV)")
            break
        p = profiles[key]
        print(row.format(
            p['instrument'][:28], p['technique'][:30], p['n_samples'],
            p['F1_hz'] or 0.0, p['reliability_score'],
            p['rugosity'], p['suddenness'],
            p['mean_kurtosis'] or 0.0
        ))

    print("\n═══════════════════════════════════════════════════════")
    print("  DONE")
    print(f"  → {output_profile}")
    if output_raw:
        print(f"  → {output_raw}")
    print("═══════════════════════════════════════════════════════\n")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 11 — CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Orchidea SOL Formant Extractor — All Techniques v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 extract_formants_all_techniques.py /path/to/db/folder/

  python3 extract_formants_all_techniques.py \\
      --specenv  FullSOL2020_specenv.db.txt Yan_Adds-Divers_specenv_db.txt \\
      --specpeaks FullSOL2020_specpeaks.db.txt Yan_Adds-Divers_specpeaks.db.txt \\
      --moments  FullSOL2020_moments.db.txt Yan_Adds-Divers_moments.db.txt \\
      --output   formants_all_techniques.csv --raw
        """
    )
    parser.add_argument('folder', nargs='?', default=None,
                        help='Folder with .db.txt files (auto-detection)')
    parser.add_argument('--specenv',   nargs='+', default=[])
    parser.add_argument('--specpeaks', nargs='+', default=[])
    parser.add_argument('--moments',   nargs='+', default=[])
    parser.add_argument('--output', default='formants_all_techniques.csv')
    parser.add_argument('--raw', action='store_true',
                        help='Also write per-sample raw CSV')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    specenv_files   = list(args.specenv)
    specpeaks_files = list(args.specpeaks)
    moments_files   = list(args.moments)

    if args.folder and os.path.isdir(args.folder):
        folder = args.folder
        KNOWN_SPECENV = [
            'FullSOL2020_specenv.db.txt',
            'Brass.specenv.db.txt', 'Winds.specenv.db.txt', 'Strings.specenv.db.txt',
            'Yan_Adds-Divers_specenv_db.txt',
        ]
        KNOWN_SPECPEAKS = [
            'FullSOL2020_specpeaks.db.txt',
            'Brass.specpeaks.db.txt', 'Winds.specpeaks.db.txt', 'Strings.specpeaks.db.txt',
            'Yan_Adds-Divers_specpeaks.db.txt',
        ]
        KNOWN_MOMENTS = [
            'FullSOL2020_moments.db.txt',
            'Brass.moments.db.txt', 'Winds.moments.db.txt', 'Strings.moments.db.txt',
            'Yan_Adds-Divers_moments.db.txt',
        ]
        if not specenv_files:
            specenv_files   = [os.path.join(folder,f) for f in KNOWN_SPECENV
                               if os.path.isfile(os.path.join(folder,f))]
            if not specenv_files:
                specenv_files = find_db_files(folder, 'specenv')
        if not specpeaks_files:
            specpeaks_files = [os.path.join(folder,f) for f in KNOWN_SPECPEAKS
                               if os.path.isfile(os.path.join(folder,f))]
            if not specpeaks_files:
                specpeaks_files = find_db_files(folder, 'specpeaks')
        if not moments_files:
            moments_files   = [os.path.join(folder,f) for f in KNOWN_MOMENTS
                               if os.path.isfile(os.path.join(folder,f))]
            if not moments_files:
                moments_files = find_db_files(folder, 'moments')

    # Fallback: current directory
    if not specenv_files:
        for name in ['FullSOL2020_specenv.db.txt','Brass.specenv.db.txt',
                     'Yan_Adds-Divers_specenv_db.txt']:
            if os.path.isfile(name):
                specenv_files.append(name)

    specenv_files   = [f for f in specenv_files   if os.path.isfile(f)]
    specpeaks_files = [f for f in specpeaks_files if os.path.isfile(f)]
    moments_files   = [f for f in moments_files   if os.path.isfile(f)]

    if not specenv_files:
        print("[ERROR] No specenv files found.")
        print("Usage: python3 extract_formants_all_techniques.py /path/to/folder/")
        sys.exit(1)

    print(f"specenv  : {[os.path.basename(f) for f in specenv_files]}")
    print(f"specpeaks: {[os.path.basename(f) for f in specpeaks_files]}")
    print(f"moments  : {[os.path.basename(f) for f in moments_files]}")

    raw_output = None
    if args.raw:
        base = os.path.splitext(args.output)[0]
        raw_output = base + '_raw_samples.csv'

    run(specenv_files, specpeaks_files, moments_files,
        args.output, raw_output, args.verbose)


if __name__ == '__main__':
    main()
