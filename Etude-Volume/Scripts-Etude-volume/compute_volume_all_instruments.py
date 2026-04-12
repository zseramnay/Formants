#!/usr/bin/env python3
"""
Système Koechlin étendu — TOUS instruments, sourdines, familles élargies.
Génère les 7 CSVs :
  volume_index_par_registre_all.csv / _mf.csv
  volume_koechlin_v3.csv
  homogeneite_matrix_v3.csv
  mfcc_par_registre.csv
  plans_orchestraux_koechlin.csv
  convergences_par_registre.csv
"""

import os, re, csv, sys
import numpy as np
from scipy.fft import dct
from scipy.stats import spearmanr
from scipy.spatial.distance import cosine

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))  # repo root
RESULTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Resultats-volume'))
os.makedirs(RESULTS_DIR, exist_ok=True)
sys.path.insert(0, os.path.join(BASE, 'Scripts', 'v6-html-docx'))

# ═══════════════════════════════════════════
# Note utilities
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

M = note_to_midi

# ═══════════════════════════════════════════
# Mel filterbank for MFCC
# ═══════════════════════════════════════════
SR, FFT, N_BINS = 44100, 4096, 1024
BIN_HZ = SR / FFT
BIN_1K = int(1000 / BIN_HZ)
N_MELS, N_MFCC = 26, 13

def _build_mel_fb():
    hz2mel = lambda f: 2595*np.log10(1+f/700)
    mel2hz = lambda m: 700*(10**(m/2595)-1)
    pts = np.linspace(hz2mel(0), hz2mel(SR/2), N_MELS+2)
    hz = mel2hz(pts)
    bins = np.floor((FFT+1)*hz/SR).astype(int)
    fb = np.zeros((N_MELS, N_BINS))
    for i in range(N_MELS):
        for k in range(bins[i], min(bins[i+1], N_BINS)):
            fb[i,k] = (k-bins[i]) / max(bins[i+1]-bins[i],1)
        for k in range(bins[i+1], min(bins[i+2], N_BINS)):
            fb[i,k] = (bins[i+2]-k) / max(bins[i+2]-bins[i+1],1)
    return fb
MEL_FB = _build_mel_fb()

def compute_mfcc(spectrum):
    power = spectrum**2
    mel_e = np.maximum(np.dot(MEL_FB, power), 1e-10)
    return dct(np.log(mel_e), type=2, norm='ortho')[:N_MFCC]

# ═══════════════════════════════════════════
# ALL INSTRUMENTS — register definitions
# ═══════════════════════════════════════════
# Format: key → list of (reg_name, midi_lo, midi_hi)
# Muted versions share registers with base instrument.

_REG = {}
# --- Flûtes ---
_REG['Flute']               = [('grave',M('B3'),M('A4')),('médium',M('A4')+1,M('A5')),('aigu',M('A5')+1,M('A6')),('suraigu',M('A6')+1,127)]
_REG['Bass_Flute']          = [('grave',M('A3'),M('D4')),('médium',M('D4')+1,M('A4')),('aigu',M('A4')+1,127)]
_REG['Contrabass_Flute']    = [('grave',M('A2')+1,M('A3')),('médium',M('A3')+1,M('A4')),('aigu',M('A4')+1,127)]
_REG['Piccolo']             = [('grave',M('A5')+1,M('D6')+1),('médium',M('E6'),M('A6')+1),('aigu',M('B6'),127)]
# --- Hautbois ---
_REG['Oboe']                = [('grave',M('A3')+1,M('G4')),('médium',M('G4')+1,M('G5')),('aigu',M('G5')+1,M('D6')),('suraigu',M('D6')+1,127)]
_REG['English_Horn']        = [('grave',M('A3')+1,M('E4')),('médium',M('F4'),M('E5')),('aigu',M('F5'),127)]
# --- Clarinettes ---
_REG['Clarinet_Bb']         = [('chalumeau',M('D3'),M('D4')),('gorge',M('D4')+1,M('G4')+1),('clarine',M('A4'),M('A5')+1),('suraigu',M('B5'),127)]
_REG['Clarinet_Eb']         = [('chalumeau',M('A3')+1,M('A4')+1),('médium',M('B4'),M('A5')+1),('aigu',M('B5'),127)]
_REG['Bass_Clarinet_Bb']    = [('grave',M('A1')+1,M('D3')),('médium',M('D3')+1,M('G3')+1),('aigu',M('A3'),M('A4')+1),('suraigu',M('B4'),127)]
_REG['Contrabass_Clarinet_Bb']=[('grave',M('A0')+1,M('A1')+1),('médium',M('B1'),M('A2')+1),('aigu',M('B2'),127)]
# --- Bassons ---
_REG['Bassoon']             = [('grave',M('A1')+1,M('A2')),('bas_médium',M('A2')+1,M('A3')),('haut_médium',M('A3')+1,M('A4')),('aigu',M('A4')+1,127)]
_REG['Contrebasson']        = [('grave',M('A0')+1,M('A1')+1),('médium',M('B1'),M('A2')+1),('aigu',M('B2'),127)]
# --- Cuivres ---
_REG['Horn']                = [('pédale',M('F1'),M('A1')),('grave',M('A1')+1,M('B2')),('médium',M('C3'),M('E4')),('aigu',M('F4'),M('F5')),('suraigu',M('F5')+1,127)]
_REG['Horn+sordina']        = _REG['Horn']
_REG['Trumpet_C']           = [('grave',M('E3'),M('B3')),('médium',M('C4'),M('G4')),('aigu',M('G4')+1,M('C5')),('suraigu',M('C5')+1,127)]
for sm in ('cup','harmon','straight','wah'):
    _REG[f'Trumpet_C+sordina_{sm}'] = _REG['Trumpet_C']
_REG['Trombone']            = [('pédale',M('E1'),M('A1')+1),('grave',M('A1')+1,M('E3')),('médium',M('E3')+1,M('E4')),('aigu',M('E4')+1,127)]
for sm in ('cup','harmon','straight','wah'):
    _REG[f'Trombone+sordina_{sm}'] = _REG['Trombone']
_REG['Bass_Trombone']       = [('pédale',M('A0')+1,M('E1')),('grave',M('F1'),M('E3')),('médium',M('F3'),M('E4')),('aigu',M('F4'),127)]
_REG['Bass_Tuba']           = [('grave',M('C1'),M('F2')),('médium',M('F2')+1,M('F3')),('aigu',M('F3')+1,M('D4')),('suraigu',M('D4')+1,127)]
_REG['Bass_Tuba+sordina']   = _REG['Bass_Tuba']
_REG['Contrabass_Tuba']     = [('grave',M('A0')+1,M('F2')),('médium',M('F2')+1,M('F3')),('aigu',M('F3')+1,127)]
# --- Saxophone ---
_REG['Sax_Alto']            = [('grave',M('A3')+1,M('A4')+1),('médium',M('B4'),M('A5')+1),('aigu',M('B5'),127)]
# --- Cordes solo ---
_REG['Violin']              = [('grave',M('G3'),M('C4')),('médium',M('C4')+1,M('C5')),('aigu',M('C5')+1,M('C6')),('suraigu',M('C6')+1,127)]
_REG['Violin+sordina']      = _REG['Violin']
_REG['Violin+sordina_piombo']=_REG['Violin']
_REG['Viola']               = [('grave',M('C3'),M('G3')),('médium',M('G3')+1,M('G4')),('aigu',M('G4')+1,M('G5')),('suraigu',M('G5')+1,127)]
_REG['Viola+sordina']       = _REG['Viola']
_REG['Viola+sordina_piombo']= _REG['Viola']
_REG['Violoncello']         = [('grave',M('C2'),M('G2')),('médium',M('G2')+1,M('G3')),('aigu',M('G3')+1,M('G4')),('suraigu',M('G4')+1,127)]
_REG['Violoncello+sordina'] = _REG['Violoncello']
_REG['Violoncello+sordina_piombo']=_REG['Violoncello']
_REG['Contrabass']          = [('grave',M('C1'),M('C2')),('médium',M('C2')+1,M('C3')),('aigu',M('C3')+1,M('C4')),('suraigu',M('C4')+1,127)]
_REG['Contrabass+sordina']  = _REG['Contrabass']
# --- Ensembles ---
_REG['Violin_Ensemble']     = _REG['Violin']
_REG['Violin_Ensemble+sordina']=_REG['Violin']
_REG['Viola_Ensemble']      = _REG['Viola']
_REG['Viola_Ensemble+sordina']=_REG['Viola']
_REG['Violoncello_Ensemble']= _REG['Violoncello']
_REG['Violoncello_Ensemble+sordina']=_REG['Violoncello']
_REG['Contrabass_Ensemble'] = _REG['Contrabass']
# --- Cordes pincées ---
_REG['Guitar']              = [('grave',M('A2')+1,M('A3')),('médium',M('A3')+1,M('A4')),('aigu',M('A4')+1,M('A5')),('suraigu',M('A5')+1,127)]
_REG['Harp']                = [('grave',M('A0')+1,M('C2')),('médium',M('C2')+1,M('C4')),('aigu',M('C4')+1,M('C6')),('suraigu',M('C6')+1,127)]
# --- Percussions ---
_REG['Marimba']             = [('grave',M('A2')+1,M('A3')),('médium',M('A3')+1,M('A4')),('aigu',M('A4')+1,127)]
_REG['Vibraphone']          = [('grave',M('A3')+1,M('A4')),('aigu',M('A4')+1,127)]

# ═══════════════════════════════════════════
# INSTRUMENT TABLE: key → (source, file_key, accepted_techniques)
# ═══════════════════════════════════════════
# accepted_techniques: tuple of technique subfolders to include
# None = use default sustained filter

def _std():      return ('ordinario',)
def _std_ext():   return ('ordinario','non_vibrato','flautando','aeolian_and_ordinario')
def _nonvib():    return ('non_vibrato',)
def _wah():       return ('ordinario_open','ordinario_closed')
def _any_sust():  return None  # fallback: accept all

INSTRUMENTS = {
    # Flûtes
    'Flute':                  ('SOL','Flute',                _std_ext()),
    'Bass_Flute':             ('YAN','Bass-Flute',           _std()),
    'Contrabass_Flute':       ('YAN','Contrabass-Flute',     _std()),
    'Piccolo':                ('YAN','Piccolo',              _std()),
    # Hautbois
    'Oboe':                   ('SOL','Oboe',                 _std()),
    'English_Horn':           ('YAN','EnglishHorn',          _std()),
    # Clarinettes
    'Clarinet_Bb':            ('SOL','Clarinet_Bb',          _std()),
    'Clarinet_Eb':            ('YAN','Clarinet-Eb',          _std()),
    'Bass_Clarinet_Bb':       ('YAN','Bass-Clarinet-Bb',     _std()),
    'Contrabass_Clarinet_Bb': ('YAN','Contrabass-Clarinet-Bb',_std()),
    # Bassons
    'Bassoon':                ('SOL','Bassoon',              _std()),
    'Contrebasson':           ('YAN','Contrebasson',         ('non-vibrato',)),
    # Cuivres
    'Horn':                   ('SOL','Horn',                 _std()),
    'Horn+sordina':           ('SOL','Horn+sordina',         _std()),
    'Trumpet_C':              ('SOL','Trumpet_C',            _std()),
    'Trumpet_C+sordina_cup':  ('SOL','Trumpet_C+sordina_cup',_std()),
    'Trumpet_C+sordina_harmon':('SOL','Trumpet_C+sordina_harmon',_std()),
    'Trumpet_C+sordina_straight':('SOL','Trumpet_C+sordina_straight',_std()),
    'Trumpet_C+sordina_wah':  ('SOL','Trumpet_C+sordina_wah',_wah()),
    'Trombone':               ('SOL','Trombone',             _std()),
    'Trombone+sordina_cup':   ('SOL','Trombone+sordina_cup', _std()),
    'Trombone+sordina_harmon':('SOL','Trombone+sordina_harmon',_std()),
    'Trombone+sordina_straight':('SOL','Trombone+sordina_straight',_std()),
    'Trombone+sordina_wah':   ('SOL','Trombone+sordina_wah', _wah()),
    'Bass_Trombone':          ('YAN','Bass-Trombone',        _std()),
    'Bass_Tuba':              ('SOL','Bass_Tuba',            _std()),
    'Bass_Tuba+sordina':      ('SOL','Bass_Tuba+sordina',    _std()),
    'Contrabass_Tuba':        ('YAN','Contrabass-Tuba',      _std()),
    # Saxophone
    'Sax_Alto':               ('SOL','Sax_Alto',             _std()),
    # Cordes solo
    'Violin':                 ('SOL','Violin',               _std()),
    'Violin+sordina':         ('SOL','Violin+sordina',       _nonvib()),
    'Violin+sordina_piombo':  ('SOL','Violin+sordina_piombo',('ordinario','non_vibrato')),
    'Viola':                  ('SOL','Viola',                _std()),
    'Viola+sordina':          ('SOL','Viola+sordina',        _nonvib()),
    'Viola+sordina_piombo':   ('SOL','Viola+sordina_piombo', ('ordinario','non_vibrato')),
    'Violoncello':            ('SOL','Violoncello',          _std()),
    'Violoncello+sordina':    ('SOL','Violoncello+sordina',  _nonvib()),
    'Violoncello+sordina_piombo':('SOL','Violoncello+sordina_piombo',('ordinario','non_vibrato')),
    'Contrabass':             ('SOL','Contrabass',           _std()),
    'Contrabass+sordina':     ('SOL','Contrabass+sordina',   _nonvib()),
    # Ensembles
    'Violin_Ensemble':        ('YAN','Violin-Ensemble',      _std()),
    'Violin_Ensemble+sordina':('YAN','Violin-Ensemble-sordina',_std()),
    'Viola_Ensemble':         ('YAN','Viola-Ensemble',       _std()),
    'Viola_Ensemble+sordina': ('YAN','Viola-Ensemble-sordina',_std()),
    'Violoncello_Ensemble':   ('YAN','Violoncello-Ensemble', _std()),
    'Violoncello_Ensemble+sordina':('YAN','Violoncello-Ensemble-sordina',_std()),
    'Contrabass_Ensemble':    ('YAN','Contrabass-Ensemble',  ('non-vibrato','flautando')),
    # Cordes pincées
    'Guitar':                 ('SOL','Guitar',               _std()),
    'Harp':                   ('SOL','Harp',                 _std()),
    # Percussions
    'Marimba':                ('YAN','Marimba',              ('ordinario-soft-mallet',)),
    'Vibraphone':             ('YAN','Vibra',                ('vibrato-soft-mallet',)),
}

# ═══════════════════════════════════════════
# Data loading
# ═══════════════════════════════════════════
def _mom_path(source, fk):
    d = 'FullSOL2020_moments par instrument' if source=='SOL' else 'Yan_Adds-Divers_moments par instrument'
    p = 'FullSOL2020_moments.db_' if source=='SOL' else 'Yan_Adds-Divers_moments.db_'
    return os.path.join(BASE, 'Data', d, f'{p}{fk}.txt')

def _spec_path(source, fk):
    d = 'FullSOL2020.spectrum_par_instrument' if source=='SOL' else 'Yan_Adds-Divers.spectrum_par_instrument'
    return os.path.join(BASE, 'Data', d, f'{fk}_spectrum.txt')

def load_data(source, file_key, accepted_techs, dynamic_filter=None):
    """Returns list of (midi, centroid, spread, spectrum_array)."""
    mp = _mom_path(source, file_key)
    sp = _spec_path(source, file_key)
    if not os.path.exists(mp) or not os.path.exists(sp):
        return []

    mom = {}
    with open(mp) as f:
        for line in f:
            if line.startswith(('moments','#','Yan','Full')): continue
            parts = line.strip().split(';')
            if len(parts) < 5: continue
            path = parts[0]
            tech = extract_technique(path)
            if accepted_techs is not None and tech not in accepted_techs:
                continue
            note = extract_note(path)
            if not note: continue
            dyn = extract_dynamic(path)
            if dynamic_filter and dyn != dynamic_filter: continue
            midi = note_to_midi(note)
            if midi is None: continue
            fname = path.split('/')[-1]
            mom[fname] = (midi, float(parts[1]), float(parts[2]))

    spec = {}
    with open(sp) as f:
        for line in f:
            if line.startswith(('spectrum','#')): continue
            parts = line.strip().split(';')
            if len(parts) < 10: continue
            fname = parts[0].split('/')[-1]
            if fname in mom:
                spec[fname] = np.array([float(x) for x in parts[1:]])

    return [(midi, c, s, spec[fn]) for fn, (midi, c, s) in mom.items() if fn in spec]

# ═══════════════════════════════════════════
# Formants
# ═══════════════════════════════════════════
def load_formants():
    formants = {}
    for csv_f in ['Etude-Formants/Resultats/formants_all_techniques_v3.csv','Etude-Formants/Resultats/formants_yan_adds_v2.csv']:
        fp = os.path.join(BASE, csv_f)
        if not os.path.exists(fp): continue
        with open(fp, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                instr = row['instrument'].strip()
                tech = row['technique'].strip()
                tf = row.get('technique_family','').strip()
                is_ord = tech in ('ordinario','non-vibrato','flautando','aeolian_and_ordinario',
                                  'ordinario_open','ordinario_closed','non_vibrato',
                                  'ordinario-soft-mallet','vibrato-soft-mallet')
                if not (is_ord or tf == 'ordinario'): continue
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
# PHASE 1: Volume index computation
# ═══════════════════════════════════════════
def compute_volume(dynamic_filter=None, label='all'):
    formants_db = load_formants()
    results = []

    for instr_key, (source, file_key, techs) in INSTRUMENTS.items():
        if instr_key not in _REG:
            continue
        data = load_data(source, file_key, techs, dynamic_filter)
        if not data:
            # Fallback: accept any technique
            data = load_data(source, file_key, None, dynamic_filter)
        if not data:
            continue

        # Match formant key (try several variants)
        v3_val = None
        for fk in [instr_key, instr_key.replace('+','_'), 
                    instr_key.replace('+sordina','').replace('+sordina_piombo','')]:
            fk2 = fk.replace('_Ensemble','_Ensemble').replace('-','_')
            if fk2 in formants_db:
                v3_val = compute_v3(formants_db[fk2])
                break
        # Try the base instrument name from formants
        if v3_val is None:
            base = instr_key.split('+')[0]
            if base in formants_db:
                v3_val = compute_v3(formants_db[base])

        for reg_name, midi_lo, midi_hi in _REG[instr_key]:
            reg = [(c,s,sp) for m,c,s,sp in data if midi_lo <= m <= midi_hi]
            if not reg: continue

            v1_vals = [s/c for c,s,sp in reg if c > 0]
            v2_vals = [np.sum(sp[:BIN_1K+1]**2)/t if (t:=np.sum(sp**2)) > 0 else None for c,s,sp in reg]
            v2_vals = [v for v in v2_vals if v is not None]
            mfcc_all = [compute_mfcc(sp) for c,s,sp in reg]
            mfcc_mean = np.mean(mfcc_all, axis=0) if mfcc_all else None

            results.append({
                'instrument': instr_key, 'register': reg_name, 'n': len(reg),
                'mean_centroid': np.mean([c for c,s,sp in reg]),
                'mean_spread': np.mean([s for c,s,sp in reg]),
                'V1': np.mean(v1_vals) if v1_vals else None,
                'V2': np.mean(v2_vals) if v2_vals else None,
                'V3': v3_val,
                'V4': mfcc_mean[1] if mfcc_mean is not None else None,
                'mfcc_profile': mfcc_mean,
            })

    # Z-score normalization
    for key in ('V1','V2','V3','V4'):
        vals = [r[key] for r in results if r[key] is not None]
        if not vals: continue
        mu, sigma = np.mean(vals), np.std(vals)
        for r in results:
            r[f'{key}_z'] = (r[key]-mu)/sigma if r[key] is not None and sigma > 0 else 0

    for r in results:
        comps = [r.get(f'{k}_z',0) for k in ('V1','V2','V3','V4') if r.get(k) is not None]
        r['Volume_index'] = np.mean(comps) if comps else None
        r['Density_index'] = -r['Volume_index'] if r['Volume_index'] is not None else None

    results.sort(key=lambda x: -(x['Volume_index'] or -999))
    return results

def write_volume_csv(results, filename):
    out = os.path.join(RESULTS_DIR, filename)
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument','register','n_samples','mean_centroid_hz','mean_spread_hz',
                     'V1_spread_centroid','V2_energy_1khz','V3_inv_formant_disp','V4_mfcc1',
                     'V1_z','V2_z','V3_z','V4_z',
                     'Volume_index','Density_index'])
        for r in results:
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
            ])
    print(f"  ✓ {filename}: {len(results)} lignes")
    return out

def write_mfcc_csv(results, filename):
    out = os.path.join(RESULTS_DIR, filename)
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument','register','n_samples'] + [f'MFCC_{i}' for i in range(N_MFCC)])
        for r in results:
            if r['mfcc_profile'] is not None:
                w.writerow([r['instrument'], r['register'], r['n']] +
                           [f"{v:.4f}" for v in r['mfcc_profile']])
    print(f"  ✓ {filename}: {sum(1 for r in results if r['mfcc_profile'] is not None)} lignes")
    return out

# ═══════════════════════════════════════════
# PHASE 2: Homogeneity matrix
# ═══════════════════════════════════════════
def compute_homogeneity(results):
    """Returns {(a,b): H} and writes CSV."""
    # Select reference register per instrument
    prio = {'médium':1,'grave':2,'bas_médium':3,'chalumeau':3,'clarine':4,'pédale':5}
    med_data = {}
    for r in results:
        i, reg = r['instrument'], r['register']
        if r['Volume_index'] is None or r['mfcc_profile'] is None: continue
        p = prio.get(reg, 6)
        if i not in med_data or p < med_data[i][0]:
            med_data[i] = (p, r['Volume_index'], r['mfcc_profile'])

    instrs = sorted(med_data.keys())
    n = len(instrs)
    vol_vals = [med_data[i][1] for i in instrs]
    vol_range = max(vol_vals) - min(vol_vals) if len(vol_vals) > 1 else 1

    matrix = {}
    for i_idx, a in enumerate(instrs):
        for j_idx, b in enumerate(instrs):
            if a == b:
                matrix[(a,b)] = 1.0
                continue
            _, va, ma = med_data[a]
            _, vb, mb = med_data[b]
            delta_vol = abs(va - vb) / vol_range
            cos_d = min(cosine(ma[1:], mb[1:]), 1.0)
            matrix[(a,b)] = max(0, 1.0 - 0.5*delta_vol - 0.5*cos_d)

    # Write CSV
    out = os.path.join(RESULTS_DIR, 'homogeneite_matrix_v3.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([''] + instrs)
        for a in instrs:
            w.writerow([a] + [f"{matrix[(a,b)]:.3f}" for b in instrs])

    print(f"  ✓ homogeneite_matrix_v3.csv: {n}×{n} instruments")
    return matrix, instrs

# ═══════════════════════════════════════════
# PHASE 3: Plans orchestraux + convergences
# ═══════════════════════════════════════════
def _specenv_path(source, fk):
    if source == 'SOL':
        return os.path.join(BASE,'Data','FullSOL2020_specenv par instrument',f'FullSOL2020_specenv.db_{fk}.txt')
    return os.path.join(BASE,'Data','Yan_Adds-Divers_specenv par instrument',f'Yan_Adds-Divers_specenv.db_{fk}.txt')

FREQ_RES = SR / FFT  # ~10.77 Hz

def compute_f1_fp_from_specenv(source, file_key, accepted_techs, registers):
    """Compute F1 (dominant peak) and Fp (centroid 800-1800 Hz) per register from specenv."""
    path = _specenv_path(source, file_key)
    if not os.path.exists(path):
        return {}

    # Load specenv grouped by register
    reg_envs = {r[0]: [] for r in registers}
    with open(path) as f:
        for line in f:
            if line.startswith(('specenv','#','Yan','Full')): continue
            parts = line.strip().split(';')
            if len(parts) < 10: continue
            p0 = parts[0]
            tech = extract_technique(p0)
            if accepted_techs is not None and tech not in accepted_techs: continue
            note = extract_note(p0)
            if not note: continue
            midi = note_to_midi(note)
            if midi is None: continue
            env = np.array([float(x) for x in parts[1:]])
            for reg_name, lo, hi in registers:
                if lo <= midi <= hi:
                    reg_envs[reg_name].append(env)
                    break

    result = {}
    for reg_name, envs in reg_envs.items():
        if not envs: continue
        mean_env = np.mean(envs, axis=0)
        # F1: dominant peak in 80-1500 Hz (in dB envelope)
        lo_bin = max(int(80/FREQ_RES), 1)
        hi_bin = min(int(1500/FREQ_RES), len(mean_env)-1)
        region = mean_env[lo_bin:hi_bin+1]
        f1 = None
        if len(region) > 2:
            peak_idx = np.argmax(region)
            f1 = int((lo_bin + peak_idx) * FREQ_RES)
        # Fp: energy-weighted centroid in 800-1800 Hz
        fp_lo = int(800/FREQ_RES)
        fp_hi = min(int(1800/FREQ_RES), len(mean_env)-1)
        fp_region = mean_env[fp_lo:fp_hi+1]
        linear = np.array([10**(v/10) for v in fp_region])
        total = linear.sum()
        fp = int(sum(linear[i]*(fp_lo+i)*FREQ_RES for i in range(len(linear)))/total) if total > 0 else None
        result[reg_name] = {'f1': f1, 'fp': fp, 'n': len(envs)}
    return result

def compute_plans(results, homo_matrix, homo_instrs):
    """Cross homogeneity with formant convergence — ALL instruments."""
    # Extract F1/Fp per register for ALL instruments via specenv
    profiles = {}
    for instr_key, (source, file_key, techs) in INSTRUMENTS.items():
        if instr_key not in _REG: continue
        prof = compute_f1_fp_from_specenv(source, file_key, techs, _REG[instr_key])
        if not prof:
            # Fallback: try any technique
            prof = compute_f1_fp_from_specenv(source, file_key, None, _REG[instr_key])
        if prof:
            profiles[instr_key] = prof

    def _select_reg(d):
        for p in ['médium','grave','bas_médium','bas médium','chalumeau','clarine','clairon']:
            if p in d: return p, d[p]
        for k,v in d.items():
            if k != 'global': return k, v
        return None, None

    def _fusion_score(H, df1, dfp):
        f1s = max(0, 1-df1/500) if df1 is not None else 0.3
        fps = max(0, 1-dfp/500) if dfp is not None else 0.3
        return 0.40*H + 0.30*f1s + 0.30*fps

    # Pairs analysis (reference register)
    pairs = []
    instr_list = sorted(set(homo_instrs) & set(profiles.keys()))
    for i, a in enumerate(instr_list):
        for b in instr_list[i+1:]:
            rna, da = _select_reg(profiles[a])
            rnb, db = _select_reg(profiles[b])
            if da is None or db is None: continue
            H = homo_matrix.get((a,b), homo_matrix.get((b,a), 0))
            f1a, f1b = da['f1'], db['f1']
            fpa, fpb = da['fp'], db['fp']
            df1 = abs(f1a-f1b) if f1a and f1b else None
            dfp = abs(fpa-fpb) if fpa and fpb else None

            if H >= 0.80 and df1 is not None and df1 <= 30:
                cat = 'FONDU'
            elif H >= 0.80 and dfp is not None and dfp <= 50:
                cat = 'FONDU_Fp'
            elif H >= 0.70 and df1 is not None and df1 <= 80:
                cat = 'SEMI-FONDU'
            elif H >= 0.80:
                cat = 'SEMI-FONDU_H'
            elif df1 is not None and df1 <= 30:
                cat = 'CONVERGENT'
            else:
                cat = 'HÉTÉROGÈNE'

            pairs.append({
                'a':a,'b':b,'reg_a':rna,'reg_b':rnb,
                'f1_a':f1a,'f1_b':f1b,'delta_f1':df1,
                'fp_a':fpa,'fp_b':fpb,'delta_fp':dfp,
                'H':H, 'fusion_score':_fusion_score(H, df1, dfp), 'category':cat,
            })
    pairs.sort(key=lambda x: -x['fusion_score'])

    # Write plans CSV
    out1 = os.path.join(RESULTS_DIR, 'plans_orchestraux_koechlin.csv')
    with open(out1, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument_A','register_A','instrument_B','register_B',
                     'F1_A_hz','F1_B_hz','delta_F1_hz','Fp_A_hz','Fp_B_hz','delta_Fp_hz',
                     'Homogeneity_H','fusion_score','category'])
        for p in pairs:
            w.writerow([p['a'],p['reg_a'],p['b'],p['reg_b'],
                        p['f1_a'] or '',p['f1_b'] or '',
                        p['delta_f1'] if p['delta_f1'] is not None else '',
                        p['fp_a'] or '',p['fp_b'] or '',
                        p['delta_fp'] if p['delta_fp'] is not None else '',
                        f"{p['H']:.3f}",f"{p['fusion_score']:.3f}",p['category']])

    # Cross-register convergences (all registers)
    cross = []
    all_instrs = sorted(set(profiles.keys()))
    for a in all_instrs:
        for b in all_instrs:
            if a >= b: continue
            H = homo_matrix.get((a,b), homo_matrix.get((b,a), 0))
            for rna, da in profiles[a].items():
                for rnb, db in profiles[b].items():
                    f1a, f1b = da['f1'], db['f1']
                    if f1a and f1b and abs(f1a-f1b) <= 30:
                        fpa, fpb = da['fp'], db['fp']
                        dfp = abs(fpa-fpb) if fpa and fpb else None
                        avg_f1 = (f1a + f1b) / 2
                        if avg_f1 <= 250:
                            zone = '/u/'
                        elif avg_f1 <= 400:
                            zone = '/o/'
                        elif avg_f1 <= 520:
                            zone = '/å/'
                        elif avg_f1 <= 800:
                            zone = '/a/'
                        else:
                            zone = '/e/–/i/'
                        cross.append({
                            'a':a,'reg_a':rna,'b':b,'reg_b':rnb,
                            'f1_a':f1a,'f1_b':f1b,'delta_f1':abs(f1a-f1b),
                            'fp_a':fpa,'fp_b':fpb,'delta_fp':dfp,'H':H,'zone':zone,
                        })
    cross.sort(key=lambda x: (x['delta_f1'], -x['H']))

    out2 = os.path.join(RESULTS_DIR, 'convergences_par_registre.csv')
    with open(out2, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['instrument_A','register_A','instrument_B','register_B',
                     'F1_A_hz','F1_B_hz','delta_F1_hz','Fp_A_hz','Fp_B_hz','delta_Fp_hz',
                     'Homogeneity_H','zone'])
        for p in cross:
            w.writerow([p['a'],p['reg_a'],p['b'],p['reg_b'],
                        p['f1_a'],p['f1_b'],p['delta_f1'],
                        p['fp_a'] or '',p['fp_b'] or '',
                        p['delta_fp'] if p['delta_fp'] is not None else '',
                        f"{p['H']:.3f}",p['zone']])

    # Summary
    cats = {}
    for p in pairs:
        cats[p['category']] = cats.get(p['category'], 0) + 1
    print(f"  ✓ plans_orchestraux_koechlin.csv: {len(pairs)} paires")
    for c in sorted(cats): print(f"      {cats[c]:4d} {c}")
    print(f"  ✓ convergences_par_registre.csv: {len(cross)} convergences F1 ≤ 30 Hz")

    return pairs, cross

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
def main():
    print("=" * 100)
    print("  SYSTÈME KOECHLIN ÉTENDU — TOUS INSTRUMENTS + SOURDINES")
    print("=" * 100)

    # Phase 1a: Volume all dynamics
    print("\n─── Phase 1a: Volume index (toutes dynamiques) ───")
    r_all = compute_volume(dynamic_filter=None, label='all')
    write_volume_csv(r_all, 'volume_index_par_registre_all.csv')

    # Phase 1b: Volume mf only
    print("\n─── Phase 1b: Volume index (mf) ───")
    r_mf = compute_volume(dynamic_filter='mf', label='mf')
    write_volume_csv(r_mf, 'volume_index_par_registre_mf.csv')

    # Phase 1c: v3 (= all dynamics, with full attributes)
    print("\n─── Phase 1c: Volume Koechlin v3 ───")
    write_volume_csv(r_all, 'volume_koechlin_v3.csv')

    # Phase 1d: MFCC profiles
    print("\n─── Phase 1d: MFCC par registre ───")
    write_mfcc_csv(r_all, 'mfcc_par_registre.csv')

    # Phase 2: Homogeneity matrix
    print("\n─── Phase 2: Matrice d'homogénéité ───")
    homo_matrix, homo_instrs = compute_homogeneity(r_all)

    # Phase 3: Plans orchestraux
    print("\n─── Phase 3: Plans orchestraux + convergences ───")
    pairs, cross = compute_plans(r_all, homo_matrix, homo_instrs)

    # ─── Console summary ───
    n_instr = len(set(r['instrument'] for r in r_all))
    n_reg = len(r_all)
    n_samples = sum(r['n'] for r in r_all)
    print(f"\n{'=' * 100}")
    print(f"  RÉSUMÉ: {n_instr} instruments, {n_reg} registres, {n_samples} échantillons")
    print(f"  Matrice: {len(homo_instrs)}×{len(homo_instrs)}")
    print(f"  Plans: {len(pairs)} paires | Convergences: {len(cross)}")
    print(f"{'=' * 100}")

    # Top 10 volume
    print(f"\n  TOP 10 VOLUMES (registre médium ou équivalent):")
    seen = set()
    for r in r_all:
        if r['instrument'] in seen: continue
        if r['Volume_index'] is None: continue
        seen.add(r['instrument'])
        print(f"    {r['Volume_index']:>6.2f}  {r['instrument']:<35} ({r['register']})")
        if len(seen) >= 10: break

    # Top 15 plans fondus
    fondus = [p for p in pairs if 'FONDU' in p['category']]
    print(f"\n  TOP 15 PLANS FONDUS (sur {len(fondus)}):")
    for p in fondus[:15]:
        df1 = f"ΔF1={p['delta_f1']:>3}" if p['delta_f1'] is not None else "ΔF1=  -"
        dfp = f"ΔFp={p['delta_fp']:>3}" if p['delta_fp'] is not None else "ΔFp=  -"
        print(f"    {p['fusion_score']:.3f}  H={p['H']:.2f}  {df1}  {dfp}  {p['a']:<30} + {p['b']}")

    # Copy to outputs
    out_dir = '/mnt/user-data/outputs'
    import shutil
    for f in ['volume_index_par_registre_all.csv','volume_index_par_registre_mf.csv',
              'volume_koechlin_v3.csv','homogeneite_matrix_v3.csv','mfcc_par_registre.csv',
              'plans_orchestraux_koechlin.csv','convergences_par_registre.csv']:
        src = os.path.join(RESULTS_DIR, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out_dir, f))

    print(f"\n  7 fichiers copiés vers {out_dir}/")


if __name__ == '__main__':
    main()
