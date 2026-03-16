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
        {'source':'SOL2020',        'f1':'457 ±97', 'f2':'1 106 ±734','f3':'2 048','f4':'—','voyelle':'o (oh)','n':'41','accord':'oui'},
    ],
    'Trompette en Ut': [
        {'source':'Backus (1969)',  'f1':'1 000–1 500','f2':'~2 000','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Giesler (1985)', 'f1':'1 200–1 500','f2':'—','f3':'—','f4':'—','voyelle':'e-ähnlich','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',   'f1':'~1 000','f2':'—','f3':'—','f4':'—','voyelle':'a/e','n':'—','accord':'approx'},
        {'source':'SOL2020',        'f1':'786 ±642','f2':'1 324 ±1018','f3':'2 588','f4':'—','voyelle':'(variable)','n':'41','accord':'approx'},
    ],
    'Trombone ténor': [
        {'source':'Backus (1969)',  'f1':'500',    'f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'oui'},
        {'source':'Giesler (1985)', 'f1':'520–600','f2':'—','f3':'—','f4':'—','voyelle':'o-ähnlich','n':'—','accord':'oui'},
        {'source':'Meyer (2009)',   'f1':'480–600','f2':'~1 200','f3':'—','f4':'—','voyelle':'o (oh)','n':'—','accord':'oui'},
        {'source':'SOL2020',        'f1':'491 ±137','f2':'1 218 ±312','f3':'2 310','f4':'—','voyelle':'o (oh)','n':'41','accord':'oui'},
    ],
    'Trombone basse': [
        {'source':'Backus/Meyer',  'f1':'—','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'—'},
        {'source':'Yan_Adds',      'f1':'894 ±257','f2':'1 496 ±292','f3':'2 652','f4':'—','voyelle':'a (ah)','n':'44','accord':'—'},
    ],
    'Tuba basse': [
        {'source':'Backus (1969)', 'f1':'200–400','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',  'f1':'210–250','f2':'—','f3':'—','f4':'—','voyelle':'u (oo)','n':'—','accord':'approx'},
        {'source':'Giesler (1985)','f1':'200–350','f2':'—','f3':'—','f4':'—','voyelle':'u-ähnlich','n':'—','accord':'approx'},
        {'source':'SOL2020',       'f1':'249 ±89','f2':'627 ±423','f3':'1 239 Fp','f4':'—','voyelle':'u (oo)','n':'41','accord':'approx'},
    ],
    'Tuba contrebasse': [
        {'source':'Yan_Adds',      'f1':'471 ±155','f2':'1 304 ±576','f3':'2 317','f4':'—','voyelle':'o (oh)','n':'78','accord':'—'},
    ],
}

# ─── Analyses par instrument ──────────────────────────────────
ANALYSIS = {
    'Cor en Fa': """Son rond et chaleureux, emblématique de la noblesse orchestrale.
        <strong>F1=457 Hz se situe dans le cluster de convergence 450–502 Hz (zone /o/)</strong>.
        Accord unanime des 4 sources (Backus 400–500, Giesler 250–500, Meyer ~450, SOL 457 Hz).
        Le Fp centroïde à 738 Hz est 6.5× plus stable que F2 (σ=734 Hz). Grande homogénéité
        spectrale inter-dynamiques. Le cor est l'instrument cuivre le plus versatile en termes de
        doublures orchestrales.""",

    'Trompette en Ut': """Son brillant et incisif, grande projection.
        <strong>F1 extrêmement variable</strong> (σ=642 Hz) selon le registre et la dynamique :
        pp=523 Hz, mf=786 Hz, ff=1 134 Hz. Le Fp centroïde à 1 046 Hz est remarquablement stable
        (σ=98 Hz), 10.4× plus stable que F2 (σ=1 018 Hz). Les sources divergent fortement
        (Backus 1 000–1 500, SOL 786–1 324) car chaque source capture un registre différent.
        Fp=1 046 Hz est la mesure la plus représentative du timbre global.""",

    'Trombone ténor': """Son plein et puissant, grande projection, très grande homogénéité spectrale.
        <strong>F1=491 Hz dans le cluster de convergence</strong> (zone /o/).
        Accord excellent entre toutes les sources (Backus 500, Giesler 520–600, Meyer 480–600,
        SOL 491 Hz — variation max 109 Hz). Fp centroïde à 1 218 Hz. Instrument qui maintient
        remarquablement sa couleur vocalique /o/ à travers toute la dynamique.""",

    'Trombone basse': """Son profond et puissant, plus sombre que le ténor.
        <strong>F1=894 Hz (zone /a/)</strong> — contrairement au trombone ténor (491 Hz, zone /o/),
        le trombone basse est acoustiquement hors du cluster /o/. Sa tessiture grave déplace le
        formant principal vers la zone de puissance /a/. Fp=1 335 Hz. Pas de données dans les
        sources académiques classiques (instrument moins étudié).""",

    'Tuba basse': """Son profond et rond, fondation harmonique de l'orchestre.
        <strong>F1=249 Hz (zone /u/)</strong> — profondeur extrême. Accord entre sources approximatif
        car chaque source mesure un registre différent (Backus 200–400, Meyer 210–250). Fp=1 239 Hz
        capture la zone d'énergie principale du pavillon. Le tuba est le seul cuivre dont F1 ne
        rejoint jamais le cluster /o/.""",

    'Tuba contrebasse': """Son extrêmement grave et massif. <strong>F1=471 Hz dans le cluster
        de convergence</strong> — contrairement au tuba basse (249 Hz), le tuba contrebasse
        rejoint le cluster /o/ aux côtés du cor et du trombone. Cette découverte explique son
        rôle de fondation harmonique des cuivres graves dans un registre différent du tuba standard.
        Fp=1 182 Hz.""",
}

ANALYSIS_SORDINES = {
    'Cor + sourdine': "F1 descend de 457 à 344 Hz, la sourdine déplace les formants vers le grave avec une légère nasalité. Son voilé et lointain.",
    'Trombone + sourd. cup': "Son voilé et sombre, projection réduite. La sourdine cup absorbe les harmoniques aigus, produisant un timbre mat.",
    'Trombone + sourd. sèche': "Son nasal et métallique. La sourdine straight comprime le spectre et renforce la zone 800–1 500 Hz.",
    'Trombone + sourd. harmon': "Son très concentré, quasi sinusoïdal. F1=162 Hz, timbre jazz intime.",
    'Trombone + sourd. wah (ouvert)': "Position ouverte : son brillant et nasal. F1=226 Hz, spectre riche.",
    'Trombone + sourd. wah (fermé)': "Position fermée : son très étouffé et nasal. F1 remonte à 398 Hz.",
    'Trompette + sourd. cup': "Son doux et arrondi, perd la brillance caractéristique. Timbre proche du bugle.",
    'Trompette + sourd. sèche': "Son piquant et nasal, le plus utilisé en orchestre. Caractère pointu et projeté.",
    'Trompette + sourd. harmon': "Son miles-davisien. F1=2 358 Hz — tout le spectre propulsé dans la zone /i/, brillance extrême.",
    'Trompette + sourd. wah (ouvert)': "Tige insérée, position ouverte : son nasal et brillant.",
    'Trompette + sourd. wah (fermé)': "Tige insérée, position fermée : son très étouffé. Spectre fortement filtré.",
    'Tuba basse + sourdine': "Son assourdi et compact. F1 reste à 249 Hz, projection réduite.",
}

DOUBLURES = {
    'Cor en Fa': [
        {'instr':'Basson',           'f1_a':'457','f1_b':'502','delta':45,'quality':'Excellente','note':'Cluster /o/ — doublure cor-basson classique'},
        {'instr':'Violoncelle',      'f1_a':'457','f1_b':'499','delta':42,'quality':'Excellente','note':'Cluster /o/ — chant lyrique bois-cordes'},
        {'instr':'Trombone',         'f1_a':'457','f1_b':'491','delta':34,'quality':'Excellente','note':'Homogénéité cuivres, cluster /o/'},
        {'instr':'Cor anglais',      'f1_a':'457','f1_b':'452','delta':5, 'quality':'Quasi-parfaite','note':'Cluster /o/ — convergence maximale bois-cuivres'},
        {'instr':'Tuba contrebasse', 'f1_a':'457','f1_b':'471','delta':14,'quality':'Quasi-parfaite','note':'Cluster /o/ — cuivres graves'},
    ],
    'Trompette en Ut': [
        {'instr':'Basson',       'f1_a':'457 (Fp)','f1_b':'502','delta':45,'quality':'Excellente','note':'Transition classique bois-cuivres, zone /o/'},
        {'instr':'Trombone',     'f1_a':'457 (Fp)','f1_b':'491','delta':34,'quality':'Excellente','note':'Homogénéité section cuivres'},
        {'instr':'Violoncelle',  'f1_a':'457 (Fp)','f1_b':'499','delta':42,'quality':'Excellente','note':'Chant lyrique cuivres-cordes'},
        {'instr':'Violon',       'f1_a':'1 046 (Fp)','f1_b':'893 (Fp)','delta':153,'quality':'Bonne','note':'Zone /a/–/e/ — brillance partagée'},
    ],
    'Trombone ténor': [
        {'instr':'Cor',         'f1_a':'491','f1_b':'457','delta':34,'quality':'Excellente','note':'Cluster /o/ — homogénéité cuivres'},
        {'instr':'Basson',      'f1_a':'491','f1_b':'502','delta':11,'quality':'Quasi-parfaite','note':'Cluster /o/ — cuivres graves + bois'},
        {'instr':'Violoncelle', 'f1_a':'491','f1_b':'499','delta':8, 'quality':'Quasi-parfaite','note':'Cluster /o/ — doublure trombone-violoncelle'},
        {'instr':'Cor anglais', 'f1_a':'491','f1_b':'452','delta':39,'quality':'Excellente','note':'Cluster /o/ — bois-cuivres'},
        {'instr':'Tuba contrebasse','f1_a':'491','f1_b':'471','delta':20,'quality':'Quasi-parfaite','note':'Cluster /o/ — fondation grave'},
    ],
    'Trombone basse': [
        {'instr':'Clarinette basse', 'f1_a':'894','f1_b':'909','delta':15,'quality':'Quasi-parfaite','note':'Zone /a/ — convergence excellente'},
        {'instr':'Clarinette Sib',   'f1_a':'894','f1_b':'1 016','delta':122,'quality':'Bonne','note':'Zone /a/ — bonne proximité'},
        {'instr':'Alto',             'f1_a':'894','f1_b':'369','delta':525,'quality':'Complémentaire','note':'Complémentarité grave-medium'},
    ],
    'Tuba basse': [
        {'instr':'Contrebasse',    'f1_a':'249','f1_b':'200','delta':49,'quality':'Bonne','note':'Fondation grave cuivres-cordes'},
        {'instr':'Contrebasson',   'f1_a':'249','f1_b':'226','delta':23,'quality':'Excellente','note':'Fondation grave cuivres-bois'},
        {'instr':'Cor anglais',    'f1_a':'249','f1_b':'452','delta':203,'quality':'Complémentaire','note':'Enrichissement medium'},
    ],
    'Tuba contrebasse': [
        {'instr':'Cor',          'f1_a':'471','f1_b':'457','delta':14,'quality':'Quasi-parfaite','note':'Cluster /o/ — fondation grave cuivres'},
        {'instr':'Trombone',     'f1_a':'471','f1_b':'491','delta':20,'quality':'Quasi-parfaite','note':'Cluster /o/ — section graves'},
        {'instr':'Basson',       'f1_a':'471','f1_b':'502','delta':31,'quality':'Excellente','note':'Cluster /o/ — bois-cuivres'},
        {'instr':'Violoncelle',  'f1_a':'471','f1_b':'499','delta':28,'quality':'Excellente','note':'Cluster /o/ — cordes'},
    ],
}

# ─── Génération graphiques ────────────────────────────────────
all_info = {}
for csv_name, display, gfx, tech, fp, color in CUIVRES_PRINCIPAUX + CUIVRES_SOURDINES:
    d = get_f(csv_name, tech)
    if not d:
        print(f"  ⚠ MANQUANT: {csv_name}/{tech}")
        continue
    img = make_graph(display, gfx, d['n'], d['F'], fp,
                     family_color=color, family_label='Cuivres')
    img_rel = os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None
    all_info[gfx] = {
        'csv': csv_name, 'display': display, 'tech': tech,
        'data': d, 'fp': fp, 'img': img, 'img_rel': img_rel,
    }
    print(f"  ✓ {display:<40s} N={d['n']:>4d} F1={d['F'][0]:>5d}")


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
<p><strong>Le cluster de convergence 450–502 Hz (zone /o/)</strong> rassemble
cor (457), trombone (491), tuba contrebasse (471) — fondement acoustique des doublures
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
        add_paragraph(doc, analysis, italic=True, size=10)
    if fp:
        add_paragraph(doc, f"Fp (centroïde) = {fp} Hz", bold=True, size=10, color=(27,94,32))

    if show_ref:
        ref_rows = REF_TABLES.get(display, [])
        if ref_rows:
            add_heading(doc, "Valeurs de référence", level=3)
            ref_table_docx(doc, ref_rows)

    if show_all_tech:
        add_heading(doc, "Analyse spectrale complète", level=3)
        tech_table_docx(doc, csv_name)

    dbl_items = DOUBLURES.get(display, [])
    if dbl_items:
        add_heading(doc, "Doublures recommandées", level=3, color=(245, 127, 23))
        table = doc.add_table(rows=1, cols=5)
        table.style = 'Table Grid'
        for idx, h in enumerate(['Instrument associé','F1','F1 associé','Écart','Qualité']):
            set_cell_text(table.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
            set_cell_shading(table.rows[0].cells[idx], 'F57F17')
        for it in dbl_items:
            row = table.add_row().cells
            delta = it.get('delta','')
            delta_str = f"Δ={delta} Hz" if isinstance(delta, (int,float)) else str(delta)
            for idx, v in enumerate([it.get('instr',''), it.get('f1_a','—'),
                                      it.get('f1_b','—'), delta_str, it.get('quality','')]):
                set_cell_text(row[idx], v, bold=(idx==0), size=9)
        for row_obj in table.rows:
            for cell, w in zip(row_obj.cells, [3.5,1.8,1.8,2.0,3.0]):
                cell.width = Cm(w)

    doc.add_paragraph()


def build_docx(output_path):
    doc = new_docx()
    add_heading(doc, "III. Les Cuivres", level=1, color=(26, 35, 126))
    p = doc.add_paragraph()
    p.add_run("Cluster de convergence 450–502 Hz (zone /o/) : ").bold = True
    p.add_run("Cor (457), Trombone (491), Tuba contrebasse (471) + Basson et Violoncelle.")

    add_heading(doc, "Cuivres principaux", level=1, color=(198, 40, 40))
    for *_, gfx, __ in [(x[0],x[1],x[2],x[3]) for x in CUIVRES_PRINCIPAUX]:
        add_instrument_docx(doc, gfx)

    add_heading(doc, "Cuivres avec sourdine", level=1, color=(198, 40, 40))
    for gfx in (['cuivres_cor_sord'] +
                ['cuivres_trb_cup','cuivres_trb_straight','cuivres_trb_harmon',
                 'cuivres_trb_wah_open','cuivres_trb_wah_closed'] +
                ['cuivres_tpt_cup','cuivres_tpt_straight','cuivres_tpt_harmon',
                 'cuivres_tpt_wah_open','cuivres_tpt_wah_closed'] +
                ['cuivres_tuba_sord']):
        add_instrument_docx(doc, gfx, show_ref=False, show_all_tech=False)

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
