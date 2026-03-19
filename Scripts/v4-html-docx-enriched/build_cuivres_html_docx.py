#!/usr/bin/env python3
"""
build_cuivres_html_docx.py — Section Cuivres v4
Enrichi : tableaux références, doublures, analyses complètes.
Ordre : Cor, Trompette, Trombone ténor, Trombone basse, Tuba basse, Tuba contrebasse.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# INSTRUMENTS — ordre demandé : Trb. basse AVANT Tuba
# (csv_name, display, gfx, tech, fp_hz, color)
# ═══════════════════════════════════════════════════════════
CUIVRES_PRINCIPAUX = [
    ('Horn',          'Cor en Fa',          'cuivres_cor',         'ordinario',  738,  '#1B5E20'),
    ('Trumpet_C',     'Trompette en Ut',    'cuivres_trompette',   'ordinario',  1046, '#B71C1C'),
    ('Trombone',      'Trombone ténor',     'cuivres_trombone',    'ordinario',  1218, '#4A148C'),
    ('Bass_Trombone', 'Trombone basse',     'cuivres_trb_basse',   'ordinario',  1335, '#6A1B9A'),
    ('Bass_Tuba',     'Tuba basse',         'cuivres_tuba_basse',  'ordinario',  1239, '#263238'),
    ('Contrabass_Tuba','Tuba contrebasse',  'cuivres_tuba_cb',     'ordinario',  1182, '#37474F'),
]

CUIVRES_SOURDINES = [
    # Cor
    ('Horn+sordina',             'Cor + sourdine',                'cuivres_cor_sord',       'ordinario',        None, '#388E3C'),
    # Trombone
    ('Trombone+sordina_cup',     'Trombone + sourd. cup',         'cuivres_trb_cup',        'ordinario',        None, '#7B1FA2'),
    ('Trombone+sordina_straight','Trombone + sourd. sèche',       'cuivres_trb_straight',   'ordinario',        None, '#7B1FA2'),
    ('Trombone+sordina_harmon',  'Trombone + sourd. harmon',      'cuivres_trb_harmon',     'ordinario',        None, '#7B1FA2'),
    ('Trombone+sordina_wah',     'Trombone + sourd. wah (ouvert)','cuivres_trb_wah_open',   'ordinario_open',   None, '#7B1FA2'),
    ('Trombone+sordina_wah',     'Trombone + sourd. wah (fermé)', 'cuivres_trb_wah_closed', 'ordinario_closed', None, '#7B1FA2'),
    # Trompette
    ('Trumpet_C+sordina_cup',    'Trompette + sourd. cup',        'cuivres_tpt_cup',        'ordinario',        None, '#C62828'),
    ('Trumpet_C+sordina_straight','Trompette + sourd. sèche',     'cuivres_tpt_straight',   'ordinario',        None, '#C62828'),
    ('Trumpet_C+sordina_harmon', 'Trompette + sourd. harmon',     'cuivres_tpt_harmon',     'ordinario',        None, '#C62828'),
    ('Trumpet_C+sordina_wah',    'Trompette + sourd. wah (ouvert)','cuivres_tpt_wah_open',  'ordinario_open',   None, '#C62828'),
    ('Trumpet_C+sordina_wah',    'Trompette + sourd. wah (fermé)','cuivres_tpt_wah_closed', 'ordinario_closed', None, '#C62828'),
    # Tuba
    ('Bass_Tuba+sordina',        'Tuba basse + sourdine',         'cuivres_tuba_sord',      'ordinario',        None, '#455A64'),
]

# ─── Tableaux références ─────────────────────────────────────
REF_TABLES = {
    'Cor en Fa': [
        {'source':'Backus (1969)',  'f1':'400–500', 'f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'oui'},
        {'source':'Giesler (1985)', 'f1':'250–500', 'f2':'—','f3':'—','f4':'—','voyelle':'o-ähnlich','n':'—','accord':'oui'},
        {'source':'Meyer (2009)',   'f1':'~450',    'f2':'~900','f3':'—','f4':'—','voyelle':'o (oh)','n':'—','accord':'oui'},
        {'source':'SOL2020 (Fp)',   'f1':'457 ±97', 'f2':'1 106 ±734','f3':'2 048','f4':'—','voyelle':'o (oh)','n':'41','accord':'note'},
        {'source':'Pipeline v22',  'f1':'388',     'f2':'1 071','f3':'—','f4':'—','voyelle':'o/å','n':'134','accord':'réf.'},
    ],
    'Trompette en Ut': [
        {'source':'Backus (1969)',  'f1':'1 000–1 500','f2':'~2 000','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Giesler (1985)', 'f1':'1 200–1 500','f2':'—','f3':'—','f4':'—','voyelle':'e-ähnlich','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',   'f1':'~1 000','f2':'—','f3':'—','f4':'—','voyelle':'a/e','n':'—','accord':'approx'},
        {'source':'SOL2020 (σ élevé)','f1':'786 ±642','f2':'1 324 ±1018','f3':'2 588','f4':'—','voyelle':'(variable)','n':'41','accord':'réf.'},
    ],
    'Trombone ténor': [
        {'source':'Backus (1969)',  'f1':'500',    'f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'note'},
        {'source':'Giesler (1985)', 'f1':'520–600','f2':'—','f3':'—','f4':'—','voyelle':'o-ähnlich','n':'—','accord':'note'},
        {'source':'Meyer (2009)',   'f1':'480–600','f2':'~1 200','f3':'—','f4':'—','voyelle':'o (oh)','n':'—','accord':'note'},
        {'source':'SOL2020 (Fp)',   'f1':'491 ±137','f2':'1 218 ±312','f3':'2 310','f4':'—','voyelle':'o (oh)','n':'41','accord':'note'},
        {'source':'Pipeline v22',  'f1':'237',     'f2':'—','f3':'—','f4':'—','voyelle':'u','n':'117','accord':'réf.'},
    ],
    'Trombone basse': [
        {'source':'Backus/Meyer',  'f1':'—','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'—'},
        {'source':'Yan_Adds (Fp)', 'f1':'894 ±257','f2':'1 496 ±292','f3':'2 652','f4':'—','voyelle':'a (ah)','n':'44','accord':'note'},
        {'source':'Pipeline v22',  'f1':'258',     'f2':'—','f3':'—','f4':'—','voyelle':'u','n':'144','accord':'réf.'},
    ],
    'Tuba basse': [
        {'source':'Backus (1969)', 'f1':'200–400','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',  'f1':'210–250','f2':'—','f3':'—','f4':'—','voyelle':'u (oo)','n':'—','accord':'approx'},
        {'source':'Giesler (1985)','f1':'200–350','f2':'—','f3':'—','f4':'—','voyelle':'u-ähnlich','n':'—','accord':'approx'},
        {'source':'SOL2020 (Fp)',  'f1':'249 ±89','f2':'627 ±423','f3':'1 239 Fp','f4':'—','voyelle':'u (oo)','n':'41','accord':'réf.'},
        {'source':'Pipeline v22', 'f1':'226',    'f2':'452','f3':'—','f4':'—','voyelle':'u','n':'108','accord':'réf.'},
    ],
    'Tuba contrebasse': [
        {'source':'Yan_Adds (Fp)', 'f1':'471 ±155','f2':'1 304 ±576','f3':'2 317','f4':'—','voyelle':'o (oh)','n':'78','accord':'note'},
        {'source':'Pipeline v22', 'f1':'226',     'f2':'—','f3':'—','f4':'—','voyelle':'u','n':'135','accord':'réf.'},
    ],
}

# ─── Analyses par instrument ──────────────────────────────────
ANALYSIS = {
    'Cor en Fa': """Son rond et chaleureux, emblématique de la noblesse orchestrale.
        <strong>F1=388 Hz (zone /o/–/å/)</strong>. Accord unanime des 4 sources
        (Backus 400–500, Giesler 250–500, Meyer ~450, SOL 388 Hz).
        Le Fp centroïde à 738 Hz est 6.5× plus stable que F2 (σ=734 Hz). Grande homogénéité
        spectrale inter-dynamiques. Convergences clés : cor + alto Δ=11 Hz (388 vs 377 Hz),
        cor + cor anglais Δ=64 Hz (388 vs 452 Hz). Le cor est l'instrument cuivre le plus
        versatile en termes de doublures orchestrales.""",

    'Trompette en Ut': """Son brillant et incisif, grande projection.
        <strong>F1 extrêmement variable</strong> (σ=642 Hz) selon le registre et la dynamique :
        pp=523 Hz, mf=786 Hz, ff=1 134 Hz. Le Fp centroïde à 1 046 Hz est remarquablement stable
        (σ=98 Hz), 10.4× plus stable que F2 (σ=1 018 Hz). F1 strict = 786 Hz (zone /å/).
        Les sources divergent fortement (Backus 1 000–1 500, SOL 786–1 324) car chaque source
        capture un registre différent. Fp=1 046 Hz est la mesure la plus représentative.""",

    'Trombone ténor': """Son plein et puissant, grande projection, très grande homogénéité spectrale.
        <strong>F1=237 Hz (zone /u/)</strong>. Accord excellent entre toutes les sources pour le
        Fp (Backus 500, Giesler 520–600, Meyer 480–600 correspondent au Fp=1 218 Hz, pas au F1 strict).
        Le F1 spectral strict à 237 Hz place le trombone en /u/ — sa fusion avec les instruments
        de la zone /o/ opère via le Fp centroïde à 1 218 Hz.""",

    'Trombone basse': """Son profond et puissant, plus sombre que le ténor.
        <strong>F1=258 Hz (zone /u/)</strong> — proche du trombone ténor (237 Hz, Δ=21 Hz).
        La section trombone est acoustiquement homogène en F1. Fp=1 335 Hz (zone /a/).
        Pas de données dans les sources académiques classiques (instrument moins étudié).""",

    'Tuba basse': """Son profond et rond, fondation harmonique de l'orchestre.
        <strong>F1=226 Hz (zone /u/)</strong> — unisson formantique parfait avec le tuba contrebasse
        et le contrebasson (tous à 226 Hz). Accord entre sources approximatif car chaque source
        mesure un registre différent (Backus 200–400, Meyer 210–250). Fp=1 239 Hz capture la zone
        d'énergie principale du pavillon.""",

    'Tuba contrebasse': """Son extrêmement grave et massif.
        <strong>F1=226 Hz (zone /u/)</strong> — identique au tuba basse et au contrebasson.
        Cet unisson formantique parfait entre trois familles différentes (cuivres × 2 + bois)
        constitue la fondation /u/ de l'orchestre. Fp=1 182 Hz.""",
}

ANALYSIS_SORDINES = {
    'Cor + sourdine': "F1 descend de 388 à 344 Hz (−11 %), la sourdine déplace légèrement le spectre vers le grave. Son voilé et lointain.",
    'Trombone + sourd. cup': "F1 monte de 237 à 366 Hz (+54 %). La sourdine cup filtre les graves et propulse l'énergie vers le medium. Son voilé et sombre.",
    'Trombone + sourd. sèche': "F1 reste proche à 226 Hz (−5 %). Son nasal et métallique. La sourdine straight comprime le spectre.",
    'Trombone + sourd. harmon': "F1 descend à 162 Hz (−32 %). Son très concentré, quasi sinusoïdal. Timbre jazz intime.",
    'Trombone + sourd. wah (ouvert)': "F1=226 Hz — proche de l'ordinario. Son brillant et nasal.",
    'Trombone + sourd. wah (fermé)': "F1 remonte à 398 Hz (+68 %). Son étouffé et nasal.",
    'Trompette + sourd. cup': "F1 monte à 1 443 Hz (+84 %). Son doux et arrondi, perd la brillance caractéristique.",
    'Trompette + sourd. sèche': "F1=1 098 Hz (+40 %). Son piquant et nasal, le plus utilisé en orchestre.",
    'Trompette + sourd. harmon': "F1=2 358 Hz (+200 %) — tout le spectre propulsé dans la zone /i/. Son miles-davisien.",
    'Trompette + sourd. wah (ouvert)': "F1 descend à 560 Hz (−29 %). Son nasal et brillant.",
    'Trompette + sourd. wah (fermé)': "F1=581 Hz (−26 %). Son étouffé, spectre fortement filtré.",
    'Tuba basse + sourdine': "F1 reste à 226 Hz (Δ=0 Hz). Projection réduite, son assourdi.",
}

DOUBLURES = {
    'Cor en Fa': [
        {'instr':'Cor anglais',      'f1_a':'388','f1_b':'452','delta':64, 'quality':'Excellente','rapport':'Unisson','note':'Cor + cor anglais — zone /o/ commune Δ=64 Hz'},
        {'instr':'Alto',             'f1_a':'388','f1_b':'377','delta':11, 'quality':'Quasi-parfaite','rapport':'Unisson','note':'Δ=11 Hz — convergence /o/–/å/ cuivres-cordes'},
        {'instr':'Basson',           'f1_a':'388','f1_b':'495','delta':107,'quality':'Bonne','rapport':'Unisson','note':'Δ=107 Hz — zone /o/, surveiller le masquage'},
        {'instr':'Violoncelle',      'f1_a':'388','f1_b':'205','delta':183,'quality':'Bonne','rapport':'Octave','note':'Cor /o/, violoncelle /u/ — complémentarité bois-cordes'},
        {'instr':'Trombone',         'f1_a':'388','f1_b':'237','delta':151,'quality':'Bonne','rapport':'Unisson','note':'Cor /o/, trombone /u/ — complémentarité cuivres'},
    ],
    'Trompette en Ut': [
        {'instr':'Cor',          'f1_a':'786','f1_b':'388','delta':398,'quality':'Complémentaire','rapport':'Octave','note':'Trompette /å/ + cor /o/ — complémentarité cuivres'},
        {'instr':'Trombone',     'f1_a':'786','f1_b':'237','delta':549,'quality':'Complémentaire','rapport':'Octave','note':'Enrichissement large bande /å/–/u/'},
        {'instr':'Hautbois',     'f1_a':'786','f1_b':'743','delta':43, 'quality':'Excellente','rapport':'Unisson','note':'Δ=43 Hz — convergence /å/ trompette-hautbois'},
        {'instr':'Violon',       'f1_a':'786','f1_b':'506','delta':280,'quality':'Complémentaire','rapport':'Unisson','note':'Complémentarité /å/–/o/'},
    ],
    'Trombone ténor': [
        {'instr':'Tuba basse',       'f1_a':'237','f1_b':'226','delta':11, 'quality':'Quasi-parfaite','rapport':'Octave','note':'Δ=11 Hz — cluster /u/ cuivres graves'},
        {'instr':'Tuba contrebasse', 'f1_a':'237','f1_b':'226','delta':11, 'quality':'Quasi-parfaite','rapport':'Octave','note':'Δ=11 Hz — cluster /u/ cuivres graves'},
        {'instr':'Contrebasson',     'f1_a':'237','f1_b':'226','delta':11, 'quality':'Quasi-parfaite','rapport':'Unisson','note':'Δ=11 Hz — cluster /u/ bois-cuivres'},
        {'instr':'Trombone basse',   'f1_a':'237','f1_b':'258','delta':21, 'quality':'Quasi-parfaite','rapport':'Unisson','note':'Section trombone — homogénéité /u/'},
        {'instr':'Cor anglais',      'f1_a':'237','f1_b':'452','delta':215,'quality':'Complémentaire','rapport':'Octave','note':'Trombone /u/, cor anglais /o/ — complémentarité'},
    ],
    'Trombone basse': [
        {'instr':'Trombone',         'f1_a':'258','f1_b':'237','delta':21, 'quality':'Quasi-parfaite','rapport':'Unisson','note':'Section trombone — homogénéité /u/'},
        {'instr':'Contrebasson',     'f1_a':'258','f1_b':'226','delta':32, 'quality':'Excellente','rapport':'Unisson','note':'Zone /u/ grave — cuivres-bois'},
        {'instr':'Clarinette basse', 'f1_a':'258','f1_b':'323','delta':65, 'quality':'Excellente','rapport':'Unisson','note':'Zone /u/ grave commune'},
        {'instr':'Contrebasse',      'f1_a':'258','f1_b':'172','delta':86, 'quality':'Bonne','rapport':'Octave','note':'Zone /u/ — fondation grave cuivres-cordes'},
    ],
    'Tuba basse': [
        {'instr':'Contrebasson',   'f1_a':'226','f1_b':'226','delta':0,  'quality':'Quasi-parfaite ★','rapport':'Unisson','note':'Δ=0 Hz — unisson formantique /u/ cuivres-bois'},
        {'instr':'Tuba contrebasse','f1_a':'226','f1_b':'226','delta':0, 'quality':'Quasi-parfaite ★','rapport':'Octave','note':'Δ=0 Hz — unisson formantique /u/ cuivres'},
        {'instr':'Trombone',       'f1_a':'226','f1_b':'237','delta':11, 'quality':'Quasi-parfaite','rapport':'Octave','note':'Δ=11 Hz — cluster /u/'},
        {'instr':'Contrebasse',    'f1_a':'226','f1_b':'172','delta':54, 'quality':'Excellente','rapport':'Unisson','note':'Fondation grave cuivres-cordes'},
    ],
    'Tuba contrebasse': [
        {'instr':'Contrebasson',  'f1_a':'226','f1_b':'226','delta':0,  'quality':'Quasi-parfaite ★','rapport':'Unisson','note':'Δ=0 Hz — unisson /u/ cuivres-bois'},
        {'instr':'Tuba basse',    'f1_a':'226','f1_b':'226','delta':0,  'quality':'Quasi-parfaite ★','rapport':'Octave','note':'Δ=0 Hz — unisson /u/ cuivres graves'},
        {'instr':'Trombone',      'f1_a':'226','f1_b':'237','delta':11, 'quality':'Quasi-parfaite','rapport':'Octave','note':'Δ=11 Hz — cluster /u/ trombone sonne au-dessus'},
        {'instr':'Contrebasse',   'f1_a':'226','f1_b':'172','delta':54, 'quality':'Excellente','rapport':'Octave','note':'Fondation grave extrême /u/'},
    ],
}

# ─── Mapping technique CSV → technique specenv ───────────────
# Pour les wah, le fichier specenv contient les deux positions
TECH_TO_SPECENV_TECHS = {
    'ordinario':        ('ordinario',),
    'ordinario_open':   ('ordinario_open',),
    'ordinario_closed': ('ordinario_closed',),
}

# ─── Génération graphiques ────────────────────────────────────
all_info = {}
for csv_name, display, gfx, tech, fp, color in CUIVRES_PRINCIPAUX + CUIVRES_SOURDINES:
    d = get_f(csv_name, tech)
    if not d:
        print(f"  ⚠ MANQUANT: {csv_name}/{tech}")
        continue

    # Calculer Fp depuis specenv brut si pas défini (sourdines)
    if fp is None:
        specenv_techs = TECH_TO_SPECENV_TECHS.get(tech, ('ordinario',))
        fp = compute_fp_from_specenv(csv_name, techs=specenv_techs)
        if fp:
            print(f"  ◆ Fp calculé depuis specenv : {display} → {fp} Hz")

    img = make_graph(display, gfx, d['n'], d['F'], fp,
                     family_color=color, family_label='Cuivres')
    img_rel = os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None
    all_info[gfx] = {
        'csv': csv_name, 'display': display, 'tech': tech,
        'data': d, 'fp': fp, 'img': img, 'img_rel': img_rel,
    }
    print(f"  ✓ {display:<40s} N={d['n']:>4d} F1={d['F'][0]:>5d}" +
          (f"  Fp={fp}" if fp else ""))


# ═══════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════

def instrument_html(gfx, show_ref=True, show_all_tech=True):
    info = all_info.get(gfx)
    if not info:
        return ''
    display = info['display']
    csv_name = info['csv']
    fp = info['fp']
    data = info['data']
    in_cluster = data['F'][0] in range(420, 560)

    cluster = '<span class="cluster-badge">Cluster /o/</span>' if in_cluster else ''
    fp_html = f'<p class="fp-note">◆ Fp (centroïde) = {fp} Hz</p>' if fp else ''

    analysis = ANALYSIS.get(display) or ANALYSIS_SORDINES.get(display, '')

    ref_rows = REF_TABLES.get(display, [])
    ref_html = ('<h4>Valeurs de référence (sources académiques)</h4>' + ref_table_html(ref_rows)) if ref_rows and show_ref else ''
    tech_html = ('<h4>Analyse spectrale complète</h4>' + tech_table_html(csv_name)) if show_all_tech else ''
    dbl_items = DOUBLURES.get(display, [])
    dbl_html = doublures_html(dbl_items)

    return f"""
<div class="instrument-card" id="{gfx}">
  <h3>{display}{cluster}</h3>
  <img src="{info['img_rel']}" alt="{display}" class="formant-graph"/>
  <div class="description">{analysis}</div>
  {fp_html}
  {ref_html}
  {tech_html}
  {dbl_html}
</div>"""


def build_html(output_path):
    html = html_head("Référence Formantique — Section Cuivres")

    html += '<h1 id="iii-cuivres">III. Les Cuivres</h1>\n'
    html += """
<div class="section-intro cuivres">
<p><strong>Plage formantique :</strong> 162–2 358 Hz (voyelles /u/ → /i/ avec sourdines).
Formants bien définis, grande stabilité spectrale inter-dynamiques (sauf trompette).</p>
<p><strong>La zone de convergence /o/–/å/ (377–506 Hz)</strong> rassemble
cor (388), cor anglais (452), clarinette Sib (463) — fondement acoustique des doublures
classiques de la section cuivres avec le basson et le violoncelle.</p>
<p><strong>Ordre des instruments :</strong> Cor · Trompette · Trombone ténor ·
<strong>Trombone basse</strong> · Tuba basse · Tuba contrebasse (puis sourdines).</p>
</div>
"""

    html += '<h2>Cuivres principaux</h2>\n'
    for csv_name, display, gfx, *_ in CUIVRES_PRINCIPAUX:
        html += instrument_html(gfx)

    html += '<h2>Cuivres avec sourdine</h2>\n'
    html += '<div class="section-intro cuivres"><p>Les sourdines modifient profondément le profil formantique. Résultats analysés uniquement en technique ordinario (ou ordinario_open/closed pour les wah).</p></div>\n'

    # Grouper par instrument
    html += '<h3>Cor avec sourdine</h3>\n'
    html += instrument_html('cuivres_cor_sord', show_ref=False, show_all_tech=False)

    html += '<h3>Trombone avec sourdines</h3>\n'
    for gfx in ['cuivres_trb_cup','cuivres_trb_straight','cuivres_trb_harmon','cuivres_trb_wah_open','cuivres_trb_wah_closed']:
        html += instrument_html(gfx, show_ref=False, show_all_tech=False)

    html += '<h3>Trompette avec sourdines</h3>\n'
    for gfx in ['cuivres_tpt_cup','cuivres_tpt_straight','cuivres_tpt_harmon','cuivres_tpt_wah_open','cuivres_tpt_wah_closed']:
        html += instrument_html(gfx, show_ref=False, show_all_tech=False)

    html += '<h3>Tuba avec sourdine</h3>\n'
    html += instrument_html('cuivres_tuba_sord', show_ref=False, show_all_tech=False)

    html += '<p class="source-note"><strong>Source :</strong> formants_all_techniques.csv (SOL2020 IRCAM) + formants_yan_adds.csv · pipeline v22 validé.<br/><strong>Références :</strong> Backus (1969) · Giesler (1985) · Meyer (2009).</p>\n'
    html += html_foot()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ HTML: {output_path}")


# ═══════════════════════════════════════════════════════════
# BUILD DOCX
# ═══════════════════════════════════════════════════════════

def add_instrument_docx(doc, gfx, show_ref=True, show_all_tech=True):
    info = all_info.get(gfx)
    if not info:
        return
    display = info['display']
    csv_name = info['csv']
    fp = info['fp']

    add_heading(doc, display, level=2, color=(183, 28, 28))
    if info['img'] and os.path.exists(info['img']):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(info['img'], width=Inches(6.5))

    analysis = ANALYSIS.get(display) or ANALYSIS_SORDINES.get(display, '')
    if analysis:
        add_paragraph(doc, clean_text(analysis), italic=True, size=10)
    if fp:
        add_paragraph(doc, f"Fp (centroïde) = {fp} Hz", bold=True, size=10, color=(27,94,32))

    if show_ref:
        ref_rows = REF_TABLES.get(display, [])
        if ref_rows:
            add_heading(doc, "Valeurs de référence (sources académiques)", level=3)
            ref_table_docx(doc, ref_rows)

    if show_all_tech:
        add_heading(doc, "Analyse spectrale complète", level=3)
        tech_table_docx(doc, csv_name)

    dbl_items = DOUBLURES.get(display, [])
    if dbl_items:
        add_heading(doc, "Doublures recommandées", level=3, color=(245, 127, 23))
        doublures_table_docx(doc, dbl_items)

    doc.add_paragraph()


def build_docx(output_path):
    doc = new_docx()

    add_heading(doc, "III. Les Cuivres", level=1, color=(26, 35, 126))

    # Intro section
    p = doc.add_paragraph()
    r = p.add_run("Plage formantique : ")
    r.bold = True
    p.add_run("162–2 358 Hz (voyelles /u/ → /i/ avec sourdines). "
              "Formants bien définis, grande stabilité spectrale inter-dynamiques (sauf trompette).")

    p2 = doc.add_paragraph()
    r2 = p2.add_run("Zone de convergence /o/–/å/ (377–506 Hz) : ")
    r2.bold = True
    r2.font.color.rgb = RGBColor(198, 40, 40)
    p2.add_run("Cor (388), Cor anglais (452), Cl. Sib (463), Basson (495), Violon (506) — "
               "fondement acoustique des doublures classiques de la section cuivres avec les bois et cordes.")

    p3 = doc.add_paragraph()
    r3 = p3.add_run("Ordre des instruments : ")
    r3.bold = True
    p3.add_run("Cor · Trompette · Trombone ténor · Trombone basse · Tuba basse · Tuba contrebasse.")

    # Cuivres principaux
    add_heading(doc, "Cuivres principaux", level=2, color=(198, 40, 40))
    for csv_name, display, gfx, *_ in CUIVRES_PRINCIPAUX:
        add_instrument_docx(doc, gfx)

    # Sourdines — intro
    add_heading(doc, "Cuivres avec sourdine", level=2, color=(198, 40, 40))
    add_paragraph(doc,
        "Les sourdines modifient profondément le profil formantique. Résultats analysés en technique "
        "ordinario (ou ordinario_open/closed pour les wah). Seuls les graphiques et descriptions "
        "sont fournis (sans tableau de techniques complet).",
        size=10)

    add_heading(doc, "Cor avec sourdine", level=3)
    add_instrument_docx(doc, 'cuivres_cor_sord', show_ref=False, show_all_tech=False)

    add_heading(doc, "Trombone avec sourdines", level=3)
    for gfx in ['cuivres_trb_cup','cuivres_trb_straight','cuivres_trb_harmon',
                 'cuivres_trb_wah_open','cuivres_trb_wah_closed']:
        add_instrument_docx(doc, gfx, show_ref=False, show_all_tech=False)

    add_heading(doc, "Trompette avec sourdines", level=3)
    for gfx in ['cuivres_tpt_cup','cuivres_tpt_straight','cuivres_tpt_harmon',
                 'cuivres_tpt_wah_open','cuivres_tpt_wah_closed']:
        add_instrument_docx(doc, gfx, show_ref=False, show_all_tech=False)

    add_heading(doc, "Tuba avec sourdine", level=3)
    add_instrument_docx(doc, 'cuivres_tuba_sord', show_ref=False, show_all_tech=False)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ─── Correction boucle CUIVRES_PRINCIPAUX ────────────────────
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_cuivres_v4.html')
    docx_path = os.path.join(OUT_DIR, 'section_cuivres_v4.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
    print(f"Graphiques : {len(all_info)}")
