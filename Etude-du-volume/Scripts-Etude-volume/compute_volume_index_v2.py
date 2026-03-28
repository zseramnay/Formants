#!/usr/bin/env python3
"""
Calcul de l'indice de Volume spectral (Koechlin) par registre.
Version avec filtre dynamique (mf) et comparaison au tableau de Koechlin.
"""

import os, re, csv, sys
import numpy as np
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Resultats-volume'))
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Note utilities ──
NOTE_MAP = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def note_to_midi(s):
    m = re.match(r'^([A-G])(#?)(\d)$', s)
    if not m: return None
    return (int(m.group(3)) + 1) * 12 + NOTE_MAP[m.group(1)] + (1 if m.group(2) else 0)

def midi_to_hz(m): return 440.0 * 2**((m - 69) / 12.0)

def extract_note(path):
    for p in path.split('/')[-1].replace('.wav','').split('-'):
        if re.match(r'^[A-G]#?\d$', p): return p
    return None

def extract_technique(path):
    parts = path.strip().split('/')
    return parts[-2] if len(parts) >= 3 else ''

def extract_dynamic(path):
    for p in path.split('/')[-1].replace('.wav','').split('-'):
        if p in ('pp','p','mp','mf','f','ff','fff'): return p
    return None

def is_sustained(t):
    t = t.lower()
    return ('ordinario' in t or 'ord' in t or 
            t in ('arco','non-vibrato','flautando','aeolian_and_ordinario'))

# ── Registers ──
M = note_to_midi
REGISTERS = {
    'Flute':       [('grave',M('B3'),M('A4')),('médium',M('A4')+1,M('A5')),('aigu',M('A5')+1,M('A6')),('suraigu',M('A6')+1,127)],
    'Oboe':        [('grave',M('A3')+1,M('G4')),('médium',M('G4')+1,M('G5')),('aigu',M('G5')+1,M('D6')),('suraigu',M('D6')+1,127)],
    'Clarinet_Bb': [('chalumeau',M('D3'),M('D4')),('gorge',M('D4')+1,M('G4')+1),('clarine',M('A4'),M('A5')+1),('suraigu',M('B5'),127)],
    'Bass_Clarinet_Bb': [('grave',M('A1')+1,M('D3')),('médium',M('D3')+1,M('G3')+1),('aigu',M('A3'),M('A4')+1),('suraigu',M('B4'),127)],
    'Bassoon':     [('grave',M('A1')+1,M('A2')),('bas_médium',M('A2')+1,M('A3')),('haut_médium',M('A3')+1,M('A4')),('aigu',M('A4')+1,127)],
    'Horn':        [('pédale',M('F1'),M('A1')),('grave',M('A1')+1,M('B2')),('médium',M('C3'),M('E4')),('aigu',M('F4'),M('F5')),('suraigu',M('F5')+1,127)],
    'Trumpet_C':   [('grave',M('E3'),M('B3')),('médium',M('C4'),M('G4')),('aigu',M('G4')+1,M('C5')),('suraigu',M('C5')+1,127)],
    'Trombone':    [('pédale',M('E1'),M('A1')+1),('grave',M('A1')+1,M('E3')),('médium',M('E3')+1,M('E4')),('aigu',M('E4')+1,127)],
    'Bass_Tuba':   [('grave',M('C1'),M('F2')),('médium',M('F2')+1,M('F3')),('aigu',M('F3')+1,M('D4')),('suraigu',M('D4')+1,127)],
    'Violin':      [('grave',M('G3'),M('C4')),('médium',M('C4')+1,M('C5')),('aigu',M('C5')+1,M('C6')),('suraigu',M('C6')+1,127)],
    'Viola':       [('grave',M('C3'),M('G3')),('médium',M('G3')+1,M('G4')),('aigu',M('G4')+1,M('G5')),('suraigu',M('G5')+1,127)],
    'Violoncello': [('grave',M('C2'),M('G2')),('médium',M('G2')+1,M('G3')),('aigu',M('G3')+1,M('G4')),('suraigu',M('G4')+1,127)],
    'Contrabass':  [('grave',M('C1'),M('C2')),('médium',M('C2')+1,M('C3')),('aigu',M('C3')+1,M('C4')),('suraigu',M('C4')+1,127)],
}
for ens, solo in [('Violin_Ensemble','Violin'),('Viola_Ensemble','Viola'),
                   ('Violoncello_Ensemble','Violoncello'),('Contrabass_Ensemble','Contrabass')]:
    REGISTERS[ens] = REGISTERS[solo]

# ── Instrument file mapping: key → (source, file_key) ──
INSTR_FILES = {
    'Flute':('SOL','Flute'), 'Oboe':('SOL','Oboe'), 'Clarinet_Bb':('SOL','Clarinet_Bb'),
    'Bassoon':('SOL','Bassoon'), 'Horn':('SOL','Horn'), 'Trumpet_C':('SOL','Trumpet_C'),
    'Trombone':('SOL','Trombone'), 'Bass_Tuba':('SOL','Bass_Tuba'),
    'Violin':('SOL','Violin'), 'Viola':('SOL','Viola'), 'Violoncello':('SOL','Violoncello'),
    'Contrabass':('SOL','Contrabass'),
    'Bass_Clarinet_Bb':('YAN','Bass-Clarinet-Bb'),
    'Violin_Ensemble':('YAN','Violin-Ensemble'), 'Viola_Ensemble':('YAN','Viola-Ensemble'),
    'Violoncello_Ensemble':('YAN','Violoncello-Ensemble'), 'Contrabass_Ensemble':('YAN','Contrabass-Ensemble'),
}

# ── Spectrum constants ──
SR, FFT = 44100, 4096
BIN_HZ = SR / FFT
BIN_1K = int(1000 / BIN_HZ)

# ── Koechlin reference scale (vol I p.288) ──
KOECHLIN_RANK = {
    'Bass_Tuba': 1, 'Contrabass_Ensemble': 1,
    'Horn': 2,
    'Trombone': 3,
    'Trumpet_C': 4, 'Flute': 4, 'Bassoon': 4,
    'Clarinet_Bb': 5, 'Oboe': 5, 'Bass_Clarinet_Bb': 5,
    'Violin': 6, 'Viola': 6, 'Violoncello': 4, 'Contrabass': 2,
    'Violin_Ensemble': 6, 'Viola_Ensemble': 6,
    'Violoncello_Ensemble': 4,
}

# ── Load functions ──
def load_data(source, file_key, dynamic_filter=None):
    """Load moments + spectrum, return list of (midi, centroid, spread, spectrum)"""
    if source == 'SOL':
        mom_path = os.path.join(BASE, 'Data', 'FullSOL2020_moments par instrument',
                                f'FullSOL2020_moments.db_{file_key}.txt')
        spec_path = os.path.join(BASE, 'Data', 'FullSOL2020.spectrum_par_instrument',
                                 f'{file_key}_spectrum.txt')
    else:
        mom_path = os.path.join(BASE, 'Data', 'Yan_Adds-Divers_moments par instrument',
                                f'Yan_Adds-Divers_moments.db_{file_key}.txt')
        spec_path = os.path.join(BASE, 'Data', 'Yan_Adds-Divers.spectrum_par_instrument',
                                 f'{file_key}_spectrum.txt')
    
    # Load moments: path → (centroid, spread)
    mom_dict = {}
    with open(mom_path) as f:
        for line in f:
            if line.startswith('moments') or line.startswith('#'): continue
            parts = line.strip().split(';')
            if len(parts) < 5: continue
            path = parts[0]
            technique = extract_technique(path)
            if not is_sustained(technique): continue
            note = extract_note(path)
            if note is None: continue
            dyn = extract_dynamic(path)
            if dynamic_filter and dyn != dynamic_filter: continue
            fname = path.split('/')[-1]
            midi = note_to_midi(note)
            if midi is None: continue
            mom_dict[fname] = (midi, float(parts[1]), float(parts[2]))
    
    # Load spectra for matching filenames
    spec_dict = {}
    with open(spec_path) as f:
        for line in f:
            if line.startswith('spectrum') or line.startswith('#'): continue
            parts = line.strip().split(';')
            if len(parts) < 10: continue
            fname = parts[0].split('/')[-1]
            if fname in mom_dict:
                spec_dict[fname] = np.array([float(x) for x in parts[1:]])
    
    # Merge
    results = []
    for fname, (midi, centroid, spread) in mom_dict.items():
        spectrum = spec_dict.get(fname)
        if spectrum is not None:
            results.append((midi, centroid, spread, spectrum))
    
    return results

def load_formants():
    formants = {}
    for csv_file in ['Resultats/formants_all_techniques.csv', 'Resultats/formants_yan_adds.csv']:
        fpath = os.path.join(BASE, csv_file)
        with open(fpath, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                instr = row['instrument'].strip()
                tech = row['technique'].strip()
                tech_fam = row.get('technique_family', '').strip()
                if not (tech in ('ordinario','non-vibrato','flautando','aeolian_and_ordinario') 
                        or tech_fam == 'ordinario'):
                    continue
                if instr in formants and tech != 'ordinario': continue
                try:
                    fs = [float(row[f'F{i}_hz']) for i in range(1, 7)]
                    if any(f == 0 for f in fs): continue
                except: continue
                formants[instr] = fs
    return formants

def compute_v2(spectrum):
    if len(spectrum) < BIN_1K + 1: return None
    total = np.sum(spectrum**2)
    if total <= 0: return None
    return np.sum(spectrum[:BIN_1K+1]**2) / total

def compute_v3(fs):
    if fs is None or len(fs) < 2: return None
    diffs = [fs[i+1]-fs[i] for i in range(len(fs)-1)]
    md = np.mean(diffs)
    return 1.0/md if md > 0 else None

# ── Main ──
def run(dynamic_filter=None, label='all'):
    formants_db = load_formants()
    results = []
    
    for instr_key, (source, file_key) in INSTR_FILES.items():
        if instr_key not in REGISTERS: continue
        
        try:
            data = load_data(source, file_key, dynamic_filter)
        except FileNotFoundError as e:
            print(f"  SKIP {instr_key}: {e}")
            continue
        
        if not data:
            print(f"  SKIP {instr_key}: no samples after filtering (dyn={dynamic_filter})")
            continue
        
        v3_val = compute_v3(formants_db.get(instr_key))
        
        for reg_name, midi_lo, midi_hi in REGISTERS[instr_key]:
            reg_data = [(c, s, sp) for m, c, s, sp in data if midi_lo <= m <= midi_hi]
            if not reg_data: continue
            
            n = len(reg_data)
            v1_vals = [s/c for c, s, sp in reg_data if c > 0]
            v2_vals = [compute_v2(sp) for c, s, sp in reg_data]
            v2_vals = [v for v in v2_vals if v is not None]
            
            results.append({
                'instrument': instr_key, 'register': reg_name, 'n': n,
                'mean_centroid': np.mean([c for c,s,sp in reg_data]),
                'mean_spread': np.mean([s for c,s,sp in reg_data]),
                'V1': np.mean(v1_vals) if v1_vals else None,
                'V2': np.mean(v2_vals) if v2_vals else None,
                'V3': v3_val,
                'koechlin_rank': KOECHLIN_RANK.get(instr_key, 7),
            })
    
    # Z-score normalization
    for key in ('V1','V2','V3'):
        vals = [r[key] for r in results if r[key] is not None]
        if not vals: continue
        mu, sigma = np.mean(vals), np.std(vals)
        for r in results:
            r[f'{key}_z'] = (r[key] - mu) / sigma if r[key] is not None and sigma > 0 else 0
    
    for r in results:
        components = [r.get(f'{k}_z', 0) for k in ('V1','V2','V3') if r.get(k) is not None]
        r['Volume_index'] = np.mean(components) if components else None
    
    results.sort(key=lambda x: -(x['Volume_index'] or -999))
    
    # Write CSV
    out_path = os.path.join(RESULTS_DIR, f'volume_index_par_registre_{label}.csv')
    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument','register','n_samples','mean_centroid_hz','mean_spread_hz',
                     'V1_spread_over_centroid','V2_energy_ratio_1khz','V3_inv_formant_disp',
                     'V1_z','V2_z','V3_z','Volume_index','koechlin_rank'])
        for r in results:
            w.writerow([
                r['instrument'], r['register'], r['n'],
                f"{r['mean_centroid']:.1f}", f"{r['mean_spread']:.1f}",
                f"{r['V1']:.4f}" if r['V1'] is not None else '',
                f"{r['V2']:.4f}" if r['V2'] is not None else '',
                f"{r['V3']:.6f}" if r['V3'] is not None else '',
                f"{r.get('V1_z',0):.3f}", f"{r.get('V2_z',0):.3f}", f"{r.get('V3_z',0):.3f}",
                f"{r['Volume_index']:.3f}" if r['Volume_index'] is not None else '',
                r['koechlin_rank']
            ])
    
    # Console output
    print(f"\n{'='*110}")
    print(f"  INDICE DE VOLUME SPECTRAL — dynamique: {label.upper()}")
    print(f"  {len(results)} registres, {sum(r['n'] for r in results)} échantillons")
    print(f"{'='*110}")
    print(f"{'Instrument':<25} {'Registre':<14} {'N':>4} {'Centr':>6} {'Sprd':>6} {'V1':>6} {'V2':>6} {'V3':>8} {'V_idx':>7} {'K_rk':>4}")
    print("─" * 110)
    
    for r in results:
        vi = f"{r['Volume_index']:.2f}" if r['Volume_index'] is not None else '  -'
        v1 = f"{r['V1']:.2f}" if r['V1'] is not None else '  -'
        v2 = f"{r['V2']:.2f}" if r['V2'] is not None else '  -'
        v3 = f"{r['V3']:.4f}" if r['V3'] is not None else '    -'
        ct = f"{r['mean_centroid']:.0f}"
        sp = f"{r['mean_spread']:.0f}"
        print(f"{r['instrument']:<25} {r['register']:<14} {r['n']:>4} {ct:>6} {sp:>6} {v1:>6} {v2:>6} {v3:>8} {vi:>7} {r['koechlin_rank']:>4}")
    
    print(f"\nCSV → {out_path}")
    return results

if __name__ == '__main__':
    print("━" * 110)
    print("  PHASE 1: TOUTES DYNAMIQUES")
    print("━" * 110)
    r_all = run(dynamic_filter=None, label='all')
    
    print("\n\n")
    print("━" * 110)
    print("  PHASE 2: DYNAMIQUE mf UNIQUEMENT")
    print("━" * 110)
    r_mf = run(dynamic_filter='mf', label='mf')
    
    # ── Correlation with Koechlin rank ──
    print("\n\n")
    print("━" * 110)
    print("  CORRÉLATION AVEC LE CLASSEMENT DE KOECHLIN")
    print("━" * 110)
    
    for label, results in [('all', r_all), ('mf', r_mf)]:
        # Take the "characteristic" register for each instrument (médium or grave)
        char_regs = {}
        for r in results:
            instr = r['instrument']
            reg = r['register']
            if r['Volume_index'] is None: continue
            # Prefer médium, then grave, then bas_médium, then chalumeau
            priority = {'médium': 1, 'grave': 2, 'bas_médium': 3, 'chalumeau': 3, 'clarine': 4}
            p = priority.get(reg, 5)
            if instr not in char_regs or p < char_regs[instr][0]:
                char_regs[instr] = (p, r)
        
        pairs = [(r['Volume_index'], r['koechlin_rank']) for _, (_, r) in char_regs.items()]
        if len(pairs) >= 3:
            from scipy.stats import spearmanr
            vi, kr = zip(*pairs)
            rho, p = spearmanr(vi, kr)
            print(f"\n  [{label}] Spearman ρ = {rho:.3f} (p={p:.4f}) — n={len(pairs)} instruments")
            print(f"  (ρ négatif attendu: Volume_index ↑ quand Koechlin_rank ↓ [gros=1, mince=7])")
            
            print(f"\n  {'Instrument':<25} {'Registre':<14} {'Vol_idx':>7} {'K_rank':>6}")
            print(f"  " + "─" * 55)
            for instr in sorted(char_regs.keys(), key=lambda i: -char_regs[i][1]['Volume_index']):
                _, r = char_regs[instr]
                print(f"  {instr:<25} {r['register']:<14} {r['Volume_index']:>7.2f} {r['koechlin_rank']:>6}")
