#!/usr/bin/env python3
"""
Système complet des attributs du timbre selon Koechlin — v3
Volume · Densité · Transparence · Homogénéité

Volume = composite de:
  V₁ = Spread/Centroid        (largeur spectrale relative)
  V₂ = E<1kHz / E_total       (poids grave)
  V₃ = 1/ΔF_mean              (taille apparente du résonateur)
  V₄ = MFCC₁                  (pente spectrale — calculé depuis spectrum)

Densité ∝ 1/Volume (Stevens: Loudness = Volume × Density, à intensité constante)
Transparence = Volume / Densité → grand volume + faible densité = transparent

Homogénéité = proximité du Volume_index + similarité du profil MFCC
"""

import os, re, csv
import numpy as np
from scipy.fft import dct
from scipy.stats import spearmanr
from scipy.spatial.distance import cosine

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Resultats-volume'))
os.makedirs(RESULTS_DIR, exist_ok=True)

# ═══════════════════════════════════════════
# Utilitaires
# ═══════════════════════════════════════════
NOTE_MAP = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}

def note_to_midi(s):
    m = re.match(r'^([A-G])(#?)(\d)$', s)
    if not m: return None
    return (int(m.group(3))+1)*12 + NOTE_MAP[m.group(1)] + (1 if m.group(2) else 0)

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

# ═══════════════════════════════════════════
# Mel filterbank pour MFCC
# ═══════════════════════════════════════════
SR, FFT, N_BINS = 44100, 4096, 1024
BIN_HZ = SR / FFT
BIN_1K = int(1000 / BIN_HZ)
N_MELS, N_MFCC = 26, 13

def _build_mel_fb():
    hz2mel = lambda f: 2595*np.log10(1+f/700)
    mel2hz = lambda m: 700*(10**(m/2595)-1)
    mel_pts = np.linspace(hz2mel(0), hz2mel(SR/2), N_MELS+2)
    hz_pts = mel2hz(mel_pts)
    bin_pts = np.floor((FFT+1)*hz_pts/SR).astype(int)
    fb = np.zeros((N_MELS, N_BINS))
    for i in range(N_MELS):
        for k in range(bin_pts[i], min(bin_pts[i+1], N_BINS)):
            fb[i,k] = (k-bin_pts[i]) / max(bin_pts[i+1]-bin_pts[i],1)
        for k in range(bin_pts[i+1], min(bin_pts[i+2], N_BINS)):
            fb[i,k] = (bin_pts[i+2]-k) / max(bin_pts[i+2]-bin_pts[i+1],1)
    return fb

MEL_FB = _build_mel_fb()

def compute_mfcc(spectrum):
    """Compute MFCCs from linear amplitude spectrum (1024 bins)."""
    power = spectrum**2
    mel_e = np.dot(MEL_FB, power)
    mel_e = np.maximum(mel_e, 1e-10)
    return dct(np.log(mel_e), type=2, norm='ortho')[:N_MFCC]

# ═══════════════════════════════════════════
# Registres (depuis registres.md)
# ═══════════════════════════════════════════
M = note_to_midi
REGISTERS = {
    'Flute':       [('grave',M('B3'),M('A4')),('médium',M('A4')+1,M('A5')),('aigu',M('A5')+1,M('A6')),('suraigu',M('A6')+1,127)],
    'Oboe':        [('grave',M('A3')+1,M('G4')),('médium',M('G4')+1,M('G5')),('aigu',M('G5')+1,M('D6')),('suraigu',M('D6')+1,127)],
    'Clarinet_Bb': [('chalumeau',M('D3'),M('D4')),('gorge',M('D4')+1,M('G4')+1),('clarine',M('A4'),M('A5')+1),('suraigu',M('B5'),127)],
    'Bass_Clarinet_Bb':[('grave',M('A1')+1,M('D3')),('médium',M('D3')+1,M('G3')+1),('aigu',M('A3'),M('A4')+1),('suraigu',M('B4'),127)],
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

INSTR_FILES = {
    'Flute':('SOL','Flute'),'Oboe':('SOL','Oboe'),'Clarinet_Bb':('SOL','Clarinet_Bb'),
    'Bassoon':('SOL','Bassoon'),'Horn':('SOL','Horn'),'Trumpet_C':('SOL','Trumpet_C'),
    'Trombone':('SOL','Trombone'),'Bass_Tuba':('SOL','Bass_Tuba'),
    'Violin':('SOL','Violin'),'Viola':('SOL','Viola'),'Violoncello':('SOL','Violoncello'),
    'Contrabass':('SOL','Contrabass'),
    'Bass_Clarinet_Bb':('YAN','Bass-Clarinet-Bb'),
    'Violin_Ensemble':('YAN','Violin-Ensemble'),'Viola_Ensemble':('YAN','Viola-Ensemble'),
    'Violoncello_Ensemble':('YAN','Violoncello-Ensemble'),'Contrabass_Ensemble':('YAN','Contrabass-Ensemble'),
}

# Koechlin volume scale (1=gros, 7=mince)
KOECHLIN_RANK = {
    'Bass_Tuba':1,'Contrabass_Ensemble':1,'Contrabass':2,
    'Horn':2,'Trombone':3,
    'Trumpet_C':4,'Flute':4,'Bassoon':4,'Violoncello':4,'Violoncello_Ensemble':4,
    'Clarinet_Bb':5,'Oboe':5,'Bass_Clarinet_Bb':5,
    'Violin':6,'Viola':6,'Violin_Ensemble':6,'Viola_Ensemble':6,
}

# ═══════════════════════════════════════════
# Chargement données (moments + spectrum)
# ═══════════════════════════════════════════
def load_data(source, file_key, dynamic_filter=None):
    """Returns list of (midi, centroid, spread, spectrum_array)."""
    if source == 'SOL':
        mom_p = os.path.join(BASE,'Data','FullSOL2020_moments par instrument',
                             f'FullSOL2020_moments.db_{file_key}.txt')
        spec_p = os.path.join(BASE,'Data','FullSOL2020.spectrum_par_instrument',
                              f'{file_key}_spectrum.txt')
    else:
        mom_p = os.path.join(BASE,'Data','Yan_Adds-Divers_moments par instrument',
                             f'Yan_Adds-Divers_moments.db_{file_key}.txt')
        spec_p = os.path.join(BASE,'Data','Yan_Adds-Divers.spectrum_par_instrument',
                              f'{file_key}_spectrum.txt')

    # Moments
    mom = {}
    with open(mom_p) as f:
        for line in f:
            if line.startswith('moments'): continue
            parts = line.strip().split(';')
            if len(parts) < 5: continue
            path = parts[0]
            if not is_sustained(extract_technique(path)): continue
            note = extract_note(path)
            if not note: continue
            dyn = extract_dynamic(path)
            if dynamic_filter and dyn != dynamic_filter: continue
            midi = note_to_midi(note)
            if midi is None: continue
            fname = path.split('/')[-1]
            mom[fname] = (midi, float(parts[1]), float(parts[2]))

    # Spectra (only for filenames present in moments)
    spec = {}
    with open(spec_p) as f:
        for line in f:
            if line.startswith('spectrum'): continue
            parts = line.strip().split(';')
            if len(parts) < 10: continue
            fname = parts[0].split('/')[-1]
            if fname in mom:
                spec[fname] = np.array([float(x) for x in parts[1:]])

    return [(midi, c, s, spec[fn]) for fn, (midi, c, s) in mom.items() if fn in spec]

# ═══════════════════════════════════════════
# Formants depuis CSVs
# ═══════════════════════════════════════════
def load_formants():
    formants = {}
    for csv_f in ['Resultats/formants_all_techniques.csv','Resultats/formants_yan_adds.csv']:
        fp = os.path.join(BASE, csv_f)
        with open(fp, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                instr = row['instrument'].strip()
                tech = row['technique'].strip()
                tf = row.get('technique_family','').strip()
                if not (tech in ('ordinario','non-vibrato','flautando','aeolian_and_ordinario') or tf=='ordinario'):
                    continue
                if instr in formants and tech != 'ordinario': continue
                try:
                    fs = [float(row[f'F{i}_hz']) for i in range(1,7)]
                    if any(v==0 for v in fs): continue
                except: continue
                formants[instr] = fs
    return formants

def compute_v3(fs):
    if not fs or len(fs) < 2: return None
    diffs = [fs[i+1]-fs[i] for i in range(len(fs)-1)]
    md = np.mean(diffs)
    return 1.0/md if md > 0 else None

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
def main():
    formants_db = load_formants()
    all_results = []

    for instr_key, (source, file_key) in INSTR_FILES.items():
        if instr_key not in REGISTERS: continue
        try:
            data = load_data(source, file_key, dynamic_filter=None)
        except FileNotFoundError:
            print(f"  SKIP {instr_key}: file not found"); continue
        if not data:
            print(f"  SKIP {instr_key}: no sustained samples"); continue

        v3_val = compute_v3(formants_db.get(instr_key))

        for reg_name, midi_lo, midi_hi in REGISTERS[instr_key]:
            reg = [(c, s, sp) for m, c, s, sp in data if midi_lo <= m <= midi_hi]
            if not reg: continue

            # V1: spread/centroid
            v1_vals = [s/c for c,s,sp in reg if c > 0]
            v1 = np.mean(v1_vals) if v1_vals else None

            # V2: energy < 1kHz
            v2_vals = []
            for c,s,sp in reg:
                total = np.sum(sp**2)
                if total > 0:
                    v2_vals.append(np.sum(sp[:BIN_1K+1]**2) / total)
            v2 = np.mean(v2_vals) if v2_vals else None

            # V3: inverse formant dispersion (constant per instrument)
            v3 = v3_val

            # V4: MFCC₁ mean (spectral slope — higher = more energy in lows)
            mfcc_all = []
            for c,s,sp in reg:
                mfcc = compute_mfcc(sp)
                mfcc_all.append(mfcc)
            mfcc_mean = np.mean(mfcc_all, axis=0) if mfcc_all else None
            v4 = mfcc_mean[1] if mfcc_mean is not None else None  # MFCC₁

            all_results.append({
                'instrument': instr_key, 'register': reg_name,
                'n': len(reg),
                'mean_centroid': np.mean([c for c,s,sp in reg]),
                'mean_spread': np.mean([s for c,s,sp in reg]),
                'V1': v1, 'V2': v2, 'V3': v3, 'V4': v4,
                'mfcc_profile': mfcc_mean,  # full MFCC vector for homogeneity
                'koechlin_rank': KOECHLIN_RANK.get(instr_key, 7),
            })

    # ── Z-score normalization ──
    for key in ('V1','V2','V3','V4'):
        vals = [r[key] for r in all_results if r[key] is not None]
        if not vals: continue
        mu, sigma = np.mean(vals), np.std(vals)
        for r in all_results:
            r[f'{key}_z'] = (r[key]-mu)/sigma if r[key] is not None and sigma > 0 else 0

    for r in all_results:
        comps = [r.get(f'{k}_z',0) for k in ('V1','V2','V3','V4') if r.get(k) is not None]
        r['Volume_index'] = np.mean(comps) if comps else None

    # ── Density & Transparency (Stevens model) ──
    # At constant loudness: Density ∝ 1/Volume
    # Transparency: high volume + low density (= low intensity relative)
    # We approximate: Density_z = -Volume_z, Transparency_z = Volume_z (pure inverse at mf)
    for r in all_results:
        if r['Volume_index'] is not None:
            r['Density_index'] = -r['Volume_index']
            r['Transparency_index'] = r['Volume_index']  # Transparent = voluminous but not dense
        else:
            r['Density_index'] = None
            r['Transparency_index'] = None

    all_results.sort(key=lambda x: -(x['Volume_index'] or -999))

    # ═══════════════════════════════════════════
    # OUTPUT 1: Volume index CSV
    # ═══════════════════════════════════════════
    out1 = os.path.join(RESULTS_DIR, 'volume_koechlin_v3.csv')
    with open(out1, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument','register','n_samples',
                     'mean_centroid_hz','mean_spread_hz',
                     'V1_spread_centroid','V2_energy_1khz','V3_inv_formant_disp','V4_mfcc1',
                     'V1_z','V2_z','V3_z','V4_z',
                     'Volume_index','Density_index','Transparency_index',
                     'koechlin_rank'])
        for r in all_results:
            w.writerow([
                r['instrument'], r['register'], r['n'],
                f"{r['mean_centroid']:.1f}", f"{r['mean_spread']:.1f}",
                f"{r['V1']:.4f}" if r['V1'] is not None else '',
                f"{r['V2']:.4f}" if r['V2'] is not None else '',
                f"{r['V3']:.6f}" if r['V3'] is not None else '',
                f"{r['V4']:.2f}" if r['V4'] is not None else '',
                f"{r.get('V1_z',0):.3f}", f"{r.get('V2_z',0):.3f}",
                f"{r.get('V3_z',0):.3f}", f"{r.get('V4_z',0):.3f}",
                f"{r['Volume_index']:.3f}" if r['Volume_index'] is not None else '',
                f"{r['Density_index']:.3f}" if r['Density_index'] is not None else '',
                f"{r['Transparency_index']:.3f}" if r['Transparency_index'] is not None else '',
                r['koechlin_rank'],
            ])

    # ═══════════════════════════════════════════
    # Console: tableau principal
    # ═══════════════════════════════════════════
    print(f"\n{'='*120}")
    print(f"  INDICE DE VOLUME SPECTRAL (KOECHLIN) — v3 avec MFCC₁")
    print(f"  {len(all_results)} registres, {sum(r['n'] for r in all_results)} échantillons")
    print(f"{'='*120}")
    hdr = f"{'Instrument':<25} {'Registre':<14} {'N':>4} {'Centr':>6} {'V1':>6} {'V2':>6} {'V3':>8} {'V4':>7} {'Vol':>7} {'Dens':>7} {'Transp':>7} {'K':>3}"
    print(hdr)
    print("─"*120)
    for r in all_results:
        fmt = lambda v, d=2: f"{v:.{d}f}" if v is not None else '  -'
        print(f"{r['instrument']:<25} {r['register']:<14} {r['n']:>4} "
              f"{r['mean_centroid']:>6.0f} "
              f"{fmt(r['V1']):>6} {fmt(r['V2']):>6} {fmt(r['V3'],4):>8} {fmt(r['V4']):>7} "
              f"{fmt(r['Volume_index']):>7} {fmt(r['Density_index']):>7} {fmt(r['Transparency_index']):>7} "
              f"{r['koechlin_rank']:>3}")

    # ═══════════════════════════════════════════
    # Corrélation Spearman avec Koechlin
    # ═══════════════════════════════════════════
    # Registre médium (ou grave si pas de médium)
    char = {}
    prio = {'médium':1,'grave':2,'bas_médium':3,'chalumeau':3,'clarine':4}
    for r in all_results:
        if r['Volume_index'] is None: continue
        i, reg = r['instrument'], r['register']
        p = prio.get(reg, 5)
        if i not in char or p < char[i][0]:
            char[i] = (p, r)

    pairs = [(r['Volume_index'], r['koechlin_rank']) for _,(_, r) in char.items()]
    if len(pairs) >= 3:
        vi, kr = zip(*pairs)
        rho, p = spearmanr(vi, kr)
        print(f"\n{'='*120}")
        print(f"  CORRÉLATION KOECHLIN: Spearman ρ = {rho:.3f} (p={p:.4f}), n={len(pairs)}")
        print(f"  (ρ négatif attendu: Volume_index ↑ = gros, Koechlin_rank ↓ = gros)")
        print(f"{'='*120}")
        print(f"  {'Instrument':<25} {'Reg':<14} {'Vol_idx':>7} {'K_rank':>6}")
        print(f"  {'─'*55}")
        for i in sorted(char.keys(), key=lambda x: -char[x][1]['Volume_index']):
            _, r = char[i]
            print(f"  {i:<25} {r['register']:<14} {r['Volume_index']:>7.2f} {r['koechlin_rank']:>6}")

    # ═══════════════════════════════════════════
    # OUTPUT 2: Matrice d'homogénéité
    # ═══════════════════════════════════════════
    # Homogénéité entre deux instruments dans un registre commun:
    #   H = 1 - α·|ΔVolume| - β·cosine_distance(MFCC_profile)
    # α=0.5, β=0.5

    print(f"\n{'='*120}")
    print(f"  MATRICE D'HOMOGÉNÉITÉ (registre médium)")
    print(f"{'='*120}")

    # Collect médium-register data for each instrument
    med_data = {}
    for r in all_results:
        i = r['instrument']
        reg = r['register']
        if reg in ('médium','grave','chalumeau','bas_médium') and r['mfcc_profile'] is not None:
            p = prio.get(reg, 5)
            if i not in med_data or p < med_data[i][0]:
                med_data[i] = (p, r['Volume_index'], r['mfcc_profile'])

    instrs = sorted(med_data.keys())
    n_instr = len(instrs)

    # Normalize Volume_index to [0,1]
    vol_vals = [med_data[i][1] for i in instrs]
    vol_min, vol_max = min(vol_vals), max(vol_vals)
    vol_range = vol_max - vol_min if vol_max > vol_min else 1

    homo_matrix = np.zeros((n_instr, n_instr))
    for i_idx, i_name in enumerate(instrs):
        for j_idx, j_name in enumerate(instrs):
            if i_idx == j_idx:
                homo_matrix[i_idx][j_idx] = 1.0
                continue
            _, vi, mfcc_i = med_data[i_name]
            _, vj, mfcc_j = med_data[j_name]
            # Volume proximity [0,1]
            delta_vol = abs(vi - vj) / vol_range
            # MFCC cosine similarity [0,1] — use MFCC[1:] (skip C0=energy)
            cos_dist = cosine(mfcc_i[1:], mfcc_j[1:])
            cos_dist = min(cos_dist, 1.0)  # clamp
            # Homogeneity
            H = 1.0 - 0.5*delta_vol - 0.5*cos_dist
            homo_matrix[i_idx][j_idx] = max(0, H)

    # Short instrument names for display
    short = {
        'Flute':'Fl','Oboe':'Hb','Clarinet_Bb':'Cl','Bass_Clarinet_Bb':'ClB',
        'Bassoon':'Bn','Horn':'Cor','Trumpet_C':'Tp','Trombone':'Tbn',
        'Bass_Tuba':'Tba','Violin':'Vn','Viola':'Va','Violoncello':'Vc',
        'Contrabass':'Cb','Violin_Ensemble':'VnE','Viola_Ensemble':'VaE',
        'Violoncello_Ensemble':'VcE','Contrabass_Ensemble':'CbE',
    }

    # Print matrix
    hdr = "        " + " ".join(f"{short.get(i,i[:3]):>5}" for i in instrs)
    print(hdr)
    for i_idx, i_name in enumerate(instrs):
        row = f"{short.get(i_name,i_name[:3]):>7} "
        for j_idx in range(n_instr):
            v = homo_matrix[i_idx][j_idx]
            if i_idx == j_idx:
                row += "  1.0 "
            elif v >= 0.85:
                row += f" \033[92m{v:.2f}\033[0m "  # green = very homogeneous
            elif v >= 0.70:
                row += f" \033[93m{v:.2f}\033[0m "  # yellow = moderately
            else:
                row += f" {v:.2f} "
        print(row)

    # ═══════════════════════════════════════════
    # Top homogeneous pairs (= Koechlin's "mélanges fondus")
    # ═══════════════════════════════════════════
    pairs_h = []
    for i_idx in range(n_instr):
        for j_idx in range(i_idx+1, n_instr):
            pairs_h.append((instrs[i_idx], instrs[j_idx], homo_matrix[i_idx][j_idx]))

    pairs_h.sort(key=lambda x: -x[2])

    print(f"\n  TOP 20 PAIRES HOMOGÈNES (mélanges fondus potentiels)")
    print(f"  {'─'*60}")
    for i, (a, b, h) in enumerate(pairs_h[:20]):
        marker = "★" if h >= 0.85 else "●" if h >= 0.75 else "○"
        print(f"  {marker} {h:.3f}  {a:<25} + {b}")

    # Save homogeneity matrix CSV
    out2 = os.path.join(RESULTS_DIR, 'homogeneite_matrix_v3.csv')
    with open(out2, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([''] + instrs)
        for i_idx, i_name in enumerate(instrs):
            w.writerow([i_name] + [f"{homo_matrix[i_idx][j]:.3f}" for j in range(n_instr)])

    # ═══════════════════════════════════════════
    # Write full MFCC profiles per register CSV (for future use)
    # ═══════════════════════════════════════════
    out3 = os.path.join(RESULTS_DIR, 'mfcc_par_registre.csv')
    with open(out3, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument','register','n_samples'] +
                    [f'MFCC_{i}' for i in range(N_MFCC)])
        for r in all_results:
            if r['mfcc_profile'] is not None:
                w.writerow([r['instrument'], r['register'], r['n']] +
                           [f"{v:.4f}" for v in r['mfcc_profile']])

    print(f"\n  Fichiers produits:")
    print(f"    {out1}")
    print(f"    {out2}")
    print(f"    {out3}")

if __name__ == '__main__':
    main()
