#!/usr/bin/env python3
"""
Plans orchestraux de Koechlin — Prédiction des fusions timbrales.

Croise :
  - Matrice d'homogénéité H (Volume + profil MFCC)
  - Convergence formantique ΔF1 et ΔFp par registre

Classifie chaque paire instrument×registre :
  ★ Plan fondu       : H ≥ 0.80 ET ΔF1 ≤ 30 Hz
  ● Plan semi-fondu  : H ≥ 0.70 ET ΔF1 ≤ 80 Hz  (ou H ≥ 0.80)
  ○ Plan hétérogène  : reste
"""

import sys, os, csv
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v6-html-docx'))
import common

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ═══════════════════════════════════════════
# 1. Extraire F1 + Fp par registre depuis common.py
# ═══════════════════════════════════════════
INSTRUMENTS = [
    ('Flute',              'ordinario'),
    ('Oboe',               'ordinario'),
    ('Clarinet_Bb',        'ordinario'),
    ('Bass_Clarinet_Bb',   'ordinario'),
    ('Bassoon',            'ordinario'),
    ('Horn',               'ordinario'),
    ('Trumpet_C',          'ordinario'),
    ('Trombone',           'ordinario'),
    ('Bass_Tuba',          'ordinario'),
    ('Violin',             'ordinario'),
    ('Viola',              'ordinario'),
    ('Violoncello',        'ordinario'),
    ('Contrabass',         'ordinario'),
    ('Violin_Ensemble',    'ordinario'),
    ('Viola_Ensemble',     'ordinario'),
    ('Violoncello_Ensemble','ordinario'),
    ('Contrabass_Ensemble','non-vibrato'),
]

SHORT = {
    'Flute':'Fl','Oboe':'Hb','Clarinet_Bb':'Cl','Bass_Clarinet_Bb':'ClB',
    'Bassoon':'Bn','Horn':'Cor','Trumpet_C':'Tp','Trombone':'Tbn',
    'Bass_Tuba':'Tba','Violin':'Vn','Viola':'Va','Violoncello':'Vc',
    'Contrabass':'Cb','Violin_Ensemble':'VnE','Viola_Ensemble':'VaE',
    'Violoncello_Ensemble':'VcE','Contrabass_Ensemble':'CbE',
}

# Registre préférentiel pour l'analyse croisée
REG_PRIO = ['Médium', 'médium', 'Grave', 'grave', 'Bas médium', 'bas_médium',
            'Chalumeau', 'chalumeau', 'Clairon', 'clarine']

def get_profiles():
    """Returns {instr: {reg_name_lower: {'f1':int, 'fp':int, 'n':int}}}"""
    data = {}
    for instr, tech in INSTRUMENTS:
        techs_to_try = [tech, 'ordinario', 'non-vibrato', 'flautando']
        profiles = None
        for t in techs_to_try:
            profiles = common.compute_register_profiles(instr, techs=(t,))
            if profiles:
                break
        if not profiles:
            print(f"  SKIP {instr}: no data")
            continue
        data[instr] = {}
        for reg_name, p in profiles:
            if reg_name == 'GLOBAL':
                continue
            f1 = int(p['peaks'][0][0]) if p['peaks'] else None
            fp = int(p['fp']) if p['fp'] else None
            data[instr][reg_name.lower()] = {
                'f1': f1, 'fp': fp, 'n': p['n'],
                'reg_display': reg_name,
            }
    return data

# ═══════════════════════════════════════════
# 2. Charger la matrice d'homogénéité v3
# ═══════════════════════════════════════════
def load_homo_matrix():
    """Returns {(instrA, instrB): H_value}"""
    path = os.path.join(BASE, 'Resultats', 'homogeneite_matrix_v3.csv')
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader)
        instrs = header[1:]
        matrix = {}
        for row in reader:
            i_name = row[0]
            for j_idx, val in enumerate(row[1:]):
                j_name = instrs[j_idx]
                matrix[(i_name, j_name)] = float(val)
    return matrix

# ═══════════════════════════════════════════
# 3. Charger Volume_index depuis v3
# ═══════════════════════════════════════════
def load_volume_indices():
    """Returns {(instr, register): volume_index}"""
    path = os.path.join(BASE, 'Resultats', 'volume_koechlin_v3.csv')
    data = {}
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            key = (row['instrument'], row['register'])
            vi = row['Volume_index']
            data[key] = float(vi) if vi else None
    return data

# ═══════════════════════════════════════════
# 4. Analyse croisée
# ═══════════════════════════════════════════
def select_register(instr_data):
    """Select the reference register (médium first)."""
    for prio in REG_PRIO:
        p = prio.lower()
        if p in instr_data:
            return p, instr_data[p]
    # Fallback: first available
    for k, v in instr_data.items():
        if k != 'global':
            return k, v
    return None, None

def classify(H, delta_f1, delta_fp):
    """Classify a pair according to Koechlin's system."""
    if H >= 0.80 and delta_f1 is not None and delta_f1 <= 30:
        return 'FONDU', '★'
    if H >= 0.80 and delta_fp is not None and delta_fp <= 50:
        return 'FONDU_Fp', '★'
    if (H >= 0.70 and delta_f1 is not None and delta_f1 <= 80):
        return 'SEMI-FONDU', '●'
    if (H >= 0.80):
        return 'SEMI-FONDU_H', '●'
    if (delta_f1 is not None and delta_f1 <= 30):
        return 'CONVERGENT', '◆'
    return 'HÉTÉROGÈNE', '○'


def main():
    print("Chargement des données...")
    profiles = get_profiles()
    homo = load_homo_matrix()
    vol_idx = load_volume_indices()

    instrs = sorted(profiles.keys())
    pairs = []

    for i, a in enumerate(instrs):
        for b in instrs[i+1:]:
            reg_a_name, reg_a = select_register(profiles[a])
            reg_b_name, reg_b = select_register(profiles[b])
            if reg_a is None or reg_b is None:
                continue

            H = homo.get((a, b), homo.get((b, a), None))
            if H is None:
                continue

            f1_a, f1_b = reg_a['f1'], reg_b['f1']
            fp_a, fp_b = reg_a['fp'], reg_b['fp']

            delta_f1 = abs(f1_a - f1_b) if f1_a and f1_b else None
            delta_fp = abs(fp_a - fp_b) if fp_a and fp_b else None

            # Volume indices for these registers
            vi_a = vol_idx.get((a, reg_a_name), vol_idx.get((a, reg_a.get('reg_display','').lower()), None))
            vi_b = vol_idx.get((b, reg_b_name), vol_idx.get((b, reg_b.get('reg_display','').lower()), None))
            delta_vol = abs(vi_a - vi_b) if vi_a is not None and vi_b is not None else None

            cat, marker = classify(H, delta_f1, delta_fp)

            pairs.append({
                'a': a, 'b': b,
                'reg_a': reg_a_name, 'reg_b': reg_b_name,
                'f1_a': f1_a, 'f1_b': f1_b,
                'fp_a': fp_a, 'fp_b': fp_b,
                'delta_f1': delta_f1, 'delta_fp': delta_fp,
                'H': H,
                'vol_a': vi_a, 'vol_b': vi_b, 'delta_vol': delta_vol,
                'category': cat, 'marker': marker,
                'fusion_score': compute_fusion_score(H, delta_f1, delta_fp),
            })

    pairs.sort(key=lambda x: -x['fusion_score'])

    # ═══════════════════════════════════════════
    # Console output
    # ═══════════════════════════════════════════
    print(f"\n{'='*140}")
    print(f"  PLANS ORCHESTRAUX DE KOECHLIN — PRÉDICTION DE FUSION TIMBRALE")
    print(f"  {len(pairs)} paires analysées, registre médium (ou équivalent)")
    print(f"{'='*140}")

    # Count categories
    cats = {}
    for p in pairs:
        cats[p['category']] = cats.get(p['category'], 0) + 1
    for c, n in sorted(cats.items()):
        print(f"  {n:3d} paires {c}")

    # ─── Plans fondus ───
    fondus = [p for p in pairs if 'FONDU' in p['category']]
    print(f"\n{'─'*140}")
    print(f"  ★ PLANS FONDUS ({len(fondus)} paires) — H ≥ 0.80 ET (ΔF1 ≤ 30 Hz OU ΔFp ≤ 50 Hz)")
    print(f"{'─'*140}")
    print(f"  {'A':<22} {'B':<22} {'F1_A':>5} {'F1_B':>5} {'ΔF1':>5} {'Fp_A':>5} {'Fp_B':>5} {'ΔFp':>5} {'H':>6} {'Fusion':>7}  Cat")
    print(f"  {'─'*130}")
    for p in fondus:
        df1 = f"{p['delta_f1']:>5}" if p['delta_f1'] is not None else '    -'
        dfp = f"{p['delta_fp']:>5}" if p['delta_fp'] is not None else '    -'
        print(f"  {p['a']:<22} {p['b']:<22} {p['f1_a'] or 0:>5} {p['f1_b'] or 0:>5} {df1} "
              f"{p['fp_a'] or 0:>5} {p['fp_b'] or 0:>5} {dfp} {p['H']:>6.3f} {p['fusion_score']:>7.3f}  {p['category']}")

    # ─── Semi-fondus ───
    semis = [p for p in pairs if 'SEMI' in p['category']]
    print(f"\n{'─'*140}")
    print(f"  ● PLANS SEMI-FONDUS ({len(semis)} paires)")
    print(f"{'─'*140}")
    for p in semis:
        df1 = f"{p['delta_f1']:>5}" if p['delta_f1'] is not None else '    -'
        dfp = f"{p['delta_fp']:>5}" if p['delta_fp'] is not None else '    -'
        print(f"  {p['a']:<22} {p['b']:<22} {p['f1_a'] or 0:>5} {p['f1_b'] or 0:>5} {df1} "
              f"{p['fp_a'] or 0:>5} {p['fp_b'] or 0:>5} {dfp} {p['H']:>6.3f} {p['fusion_score']:>7.3f}  {p['category']}")

    # ─── Convergences formantiques sans homogénéité ───
    conv = [p for p in pairs if p['category'] == 'CONVERGENT']
    if conv:
        print(f"\n{'─'*140}")
        print(f"  ◆ CONVERGENCES FORMANTIQUES SANS HOMOGÉNÉITÉ DE VOLUME ({len(conv)} paires)")
        print(f"  (ΔF1 ≤ 30 Hz mais H < 0.70 — instruments acoustiquement proches mais de 'volume' différent)")
        print(f"{'─'*140}")
        for p in conv:
            df1 = f"{p['delta_f1']:>5}" if p['delta_f1'] is not None else '    -'
            dfp = f"{p['delta_fp']:>5}" if p['delta_fp'] is not None else '    -'
            print(f"  {p['a']:<22} {p['b']:<22} {p['f1_a'] or 0:>5} {p['f1_b'] or 0:>5} {df1} "
                  f"{p['fp_a'] or 0:>5} {p['fp_b'] or 0:>5} {dfp} {p['H']:>6.3f} {p['fusion_score']:>7.3f}")

    # ═══════════════════════════════════════════
    # Analyse par registre croisé (tous registres)
    # ═══════════════════════════════════════════
    print(f"\n{'='*140}")
    print(f"  ANALYSE PAR REGISTRES CROISÉS — Convergences F1 ≤ 30 Hz entre registres différents")
    print(f"{'='*140}")

    cross_pairs = []
    for a in instrs:
        for b in instrs:
            if a >= b:
                continue
            for reg_a_name, reg_a_data in profiles[a].items():
                for reg_b_name, reg_b_data in profiles[b].items():
                    f1_a = reg_a_data['f1']
                    f1_b = reg_b_data['f1']
                    if f1_a and f1_b and abs(f1_a - f1_b) <= 30:
                        fp_a = reg_a_data['fp']
                        fp_b = reg_b_data['fp']
                        delta_fp = abs(fp_a - fp_b) if fp_a and fp_b else None
                        H = homo.get((a, b), homo.get((b, a), 0))
                        cross_pairs.append({
                            'a': a, 'reg_a': reg_a_name,
                            'b': b, 'reg_b': reg_b_name,
                            'f1_a': f1_a, 'f1_b': f1_b,
                            'delta_f1': abs(f1_a - f1_b),
                            'fp_a': fp_a, 'fp_b': fp_b,
                            'delta_fp': delta_fp,
                            'H': H,
                        })

    cross_pairs.sort(key=lambda x: (x['delta_f1'], -(x['H'] or 0)))

    # Cluster /o/–/å/ zone (350-520 Hz)
    cluster_oa = [p for p in cross_pairs if 350 <= p['f1_a'] <= 520 and 350 <= p['f1_b'] <= 520]
    cluster_u = [p for p in cross_pairs if p['f1_a'] <= 250 and p['f1_b'] <= 250]
    cluster_other = [p for p in cross_pairs if p not in cluster_oa and p not in cluster_u]

    for label, group, zone in [
        ('CLUSTER /u/ (≤ 250 Hz)', cluster_u, '/u/'),
        ('CLUSTER /o/–/å/ (350–520 Hz)', cluster_oa, '/o/–/å/'),
        ('AUTRES CONVERGENCES F1 ≤ 30 Hz', cluster_other, 'divers'),
    ]:
        if not group:
            continue
        print(f"\n  ── {label} ({len(group)} paires) ──")
        print(f"  {'A':<20} {'reg_A':<12} {'B':<20} {'reg_B':<12} {'F1_A':>5} {'F1_B':>5} {'ΔF1':>4} {'ΔFp':>5} {'H':>6}")
        for p in group:
            dfp = f"{p['delta_fp']:>5}" if p['delta_fp'] else '    -'
            marker = '★' if p['H'] >= 0.80 and p['delta_f1'] <= 11 else '●' if p['H'] >= 0.70 else ' '
            print(f"  {p['a']:<20} {p['reg_a']:<12} {p['b']:<20} {p['reg_b']:<12} "
                  f"{p['f1_a']:>5} {p['f1_b']:>5} {p['delta_f1']:>4} {dfp} {p['H']:>6.3f} {marker}")

    # ═══════════════════════════════════════════
    # CSV output
    # ═══════════════════════════════════════════
    out_path = os.path.join(BASE, 'Resultats', 'plans_orchestraux_koechlin.csv')
    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument_A','register_A','instrument_B','register_B',
                     'F1_A_hz','F1_B_hz','delta_F1_hz',
                     'Fp_A_hz','Fp_B_hz','delta_Fp_hz',
                     'Homogeneity_H','fusion_score','category'])
        for p in pairs:
            w.writerow([
                p['a'], p['reg_a'], p['b'], p['reg_b'],
                p['f1_a'] or '', p['f1_b'] or '',
                p['delta_f1'] if p['delta_f1'] is not None else '',
                p['fp_a'] or '', p['fp_b'] or '',
                p['delta_fp'] if p['delta_fp'] is not None else '',
                f"{p['H']:.3f}", f"{p['fusion_score']:.3f}", p['category'],
            ])

    out2 = os.path.join(BASE, 'Resultats', 'convergences_par_registre.csv')
    with open(out2, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument_A','register_A','instrument_B','register_B',
                     'F1_A_hz','F1_B_hz','delta_F1_hz',
                     'Fp_A_hz','Fp_B_hz','delta_Fp_hz',
                     'Homogeneity_H','zone'])
        for p in cross_pairs:
            zone = '/u/' if p['f1_a'] <= 250 and p['f1_b'] <= 250 else \
                   '/o/–/å/' if 350 <= p['f1_a'] <= 520 and 350 <= p['f1_b'] <= 520 else 'autre'
            w.writerow([
                p['a'], p['reg_a'], p['b'], p['reg_b'],
                p['f1_a'], p['f1_b'], p['delta_f1'],
                p['fp_a'] or '', p['fp_b'] or '',
                p['delta_fp'] if p['delta_fp'] is not None else '',
                f"{p['H']:.3f}", zone,
            ])

    print(f"\n  Fichiers produits :")
    print(f"    {out_path}")
    print(f"    {out2}")


def compute_fusion_score(H, delta_f1, delta_fp):
    """
    Score de fusion : combine H et proximité formantique.
    Plus élevé = plus susceptible de former un plan fondu.
    """
    # Normaliser ΔF1 sur [0,1] (0=parfait, 500+=pire)
    if delta_f1 is not None:
        f1_score = max(0, 1 - delta_f1 / 500)
    else:
        f1_score = 0.3  # valeur neutre si pas de données

    # Normaliser ΔFp sur [0,1]
    if delta_fp is not None:
        fp_score = max(0, 1 - delta_fp / 500)
    else:
        fp_score = 0.3

    # Fusion = 40% H + 30% F1_proximity + 30% Fp_proximity
    return 0.40 * H + 0.30 * f1_score + 0.30 * fp_score


if __name__ == '__main__':
    main()
