#!/usr/bin/env python3
"""
build_cordes_html_docx.py — Section Cordes v4
Enrichi : tableaux références, doublures tous instruments (solistes + ensembles),
analyses complètes.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# INSTRUMENTS
# ═══════════════════════════════════════════════════════════
CORDES_SOLISTES = [
    ('Violin',              'Violon',            'cordes_violon',        'ordinario',  893,   '#B71C1C'),
    ('Violin+sordina',      'Violon+sourdine',   'cordes_vln_sord',      'ordinario',  None,  '#C62828'),
    ('Violin+sordina_piombo','Violon+sourd. piombo','cordes_vln_piombo', 'ordinario',  None,  '#D32F2F'),
    ('Viola',               'Alto',              'cordes_alto',          'ordinario',  None,  '#1565C0'),
    ('Viola+sordina',       'Alto+sourdine',     'cordes_alt_sord',      'ordinario',  None,  '#1976D2'),
    ('Viola+sordina_piombo','Alto+sourd. piombo','cordes_alt_piombo',    'ordinario',  None,  '#1E88E5'),
    ('Violoncello',         'Violoncelle',       'cordes_violoncelle',   'ordinario',  None,  '#1B5E20'),
    ('Violoncello+sordina', 'Violoncelle+sourdine','cordes_vcl_sord',    'ordinario',  None,  '#2E7D32'),
    ('Violoncello+sordina_piombo','Violoncelle+sourd. piombo','cordes_vcl_piombo','ordinario',None,'#388E3C'),
    ('Contrabass',          'Contrebasse',       'cordes_contrebasse',   'ordinario',  None,  '#4A148C'),
    ('Contrabass+sordina',  'Contrebasse+sourdine','cordes_cb_sord',     'ordinario',  None,  '#6A1B9A'),
]
CORDES_ENSEMBLES = [
    ('Violin_Ensemble',          'Ensemble de violons',           'cordes_vln_ens',    'ordinario', None, '#B71C1C'),
    ('Violin_Ensemble+sordina',  'Ensemble de violons+sourdine',  'cordes_vln_ens_sord','ordinario',None,'#C62828'),
    ('Viola_Ensemble',           "Ensemble d'altos",              'cordes_alt_ens',    'ordinario', None, '#1565C0'),
    ('Viola_Ensemble+sordina',   "Ensemble d'altos+sourdine",     'cordes_alt_ens_sord','ordinario',None,'#1976D2'),
    ('Violoncello_Ensemble',     'Ensemble de violoncelles',      'cordes_vcl_ens',    'ordinario', None, '#1B5E20'),
    ('Violoncello_Ensemble+sordina','Ensemble de violoncelles+sourdine','cordes_vcl_ens_sord','ordinario',None,'#2E7D32'),
    ('Contrabass_Ensemble',      'Ensemble de contrebasses',      'cordes_cb_ens',     'non-vibrato',None,'#4A148C'),
]

# ─── Références académiques ──────────────────────────────────
REF_TABLES = {
    'Violon': [
        {'source':'Backus (1969)',  'f1':'~2 000–3 000','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'—'},
        {'source':'Giesler (1985)', 'f1':'1 000–1 200','f2':'~2 400','f3':'—','f4':'—','voyelle':'e-ähnlich','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',   'f1':'~800–1 200 (Hauptformant)','f2':'~2 800–3 400','f3':'—','f4':'—','voyelle':'e (eh)','n':'—','accord':'approx'},
        {'source':'SOL2020',        'f1':'506 ±235','f2':'1 518 ±651','f3':'2 532','f4':'3 478','voyelle':'(variable)','n':'41','accord':'—'},
        {'source':'SOL2020 Fp',     'f1':'893 ±92 (Fp)','f2':'—','f3':'—','f4':'—','voyelle':'a (ah)','n':'284','accord':'approx'},
    ],
    'Alto': [
        {'source':'Giesler (1985)', 'f1':'220–600','f2':'—','f3':'—','f4':'—','voyelle':'registre-dépendant','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',   'f1':'~400–600','f2':'~800–1 200','f3':'—','f4':'—','voyelle':'o–a','n':'—','accord':'approx'},
        {'source':'SOL2020',        'f1':'377 ±14','f2':'766 ±217','f3':'1 282','f4':'1 957','voyelle':'å/a','n':'35','accord':'approx'},
    ],
    'Violoncelle': [
        {'source':'Backus (1969)',  'f1':'600–900','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Giesler (1985)', 'f1':'300–500','f2':'—','f3':'—','f4':'—','voyelle':'o-ähnlich','n':'—','accord':'oui'},
        {'source':'Meyer (2009)',   'f1':'~500 (Hauptformant)','f2':'—','f3':'—','f4':'—','voyelle':'o (oh)','n':'—','accord':'oui'},
        {'source':'Yan_Adds',       'f1':'499 ±155','f2':'1 304 ±576','f3':'2 317','f4':'—','voyelle':'o (oh)','n':'158','accord':'oui'},
    ],
    'Contrebasse': [
        {'source':'Giesler (1985)', 'f1':'70–250','f2':'400 (secondaire)','f3':'—','f4':'—','voyelle':'u/o','n':'—','accord':'approx'},
        {'source':'SOL2020',        'f1':'200 ±169','f2':'593 ±312','f3':'1 200','f4':'—','voyelle':'u (oo)','n':'41','accord':'approx'},
    ],
    'Ensemble de violons': [
        {'source':'SOL2020 (N=166)',  'f1':'495 ±89','f2':'1 163 ±312','f3':'1 970 ±389','f4':'—','voyelle':'o (oh)','n':'166','accord':'—'},
    ],
    "Ensemble d'altos": [
        {'source':'SOL2020 (N=148)',  'f1':'366 ±62','f2':'764 ±198','f3':'1 389 ±287','f4':'—','voyelle':'å/o','n':'148','accord':'—'},
    ],
    'Ensemble de violoncelles': [
        {'source':'SOL2020 (N=147)', 'f1':'205 ±48','f2':'474 ±156','f3':'775 ±201','f4':'—','voyelle':'u (oo)','n':'147','accord':'—'},
    ],
    'Ensemble de contrebasses': [
        {'source':'SOL2020 (non-vibrato, N=76)', 'f1':'172 ±44','f2':'441 ±112','f3':'754 ±189','f4':'—','voyelle':'u (oo)','n':'76','accord':'—'},
    ],
}

# ─── Analyses ────────────────────────────────────────────────
ANALYSIS = {
    'Violon': """Son brillant et expressif, extrêmement large tessiture spectrale.
        <strong>F1 spectral strict = 506 Hz (zone /o/) mais très variable (σ=235 Hz).</strong>
        F2 extrêmement instable (σ=651 Hz). Le Fp centroïde à <strong>893 Hz (σ=92 Hz)</strong>
        est 7.1× plus stable et correspond au Hauptformant de Meyer (800–1 200 Hz, zone /a/).
        Sources divergentes : Backus (2 000–3 000) capturait une zone de brillance haute ; Giesler
        et Meyer convergent sur 1 000–1 200 Hz. SOL2020 Fp=893 Hz confirme la zone /a/ comme
        signature timbrale perceptive du violon.""",

    'Violon+sourdine': "Son plus doux, atténuation des harmoniques aigus. F1 peut descendre ou rester stable selon la sourdine. Timbre plus mat et intimiste.",
    'Violon+sourd. piombo': "Sourdine lourde en plomb. Amortissement maximum, son extrêmement étouffé. Utilisée en musique contemporaine pour effets timbraux extrêmes.",

    'Alto': """Son plus sombre et mélancolique que le violon.
        <strong>F1=369 Hz (zone /å/).</strong> Giesler note une grande dépendance au registre
        (220–600 Hz). Meyer situe le formant principal dans la zone /o/–/a/ (400–1 200 Hz).
        F1 SOL2020 (369 Hz) est plus stable que le violon. L'alto est acoustiquement dans la zone
        de transition /å/–/o/, ce qui lui confère sa couleur caractéristique — ni la brillance du
        violon ni la plénitude du violoncelle.""",

    'Alto+sourdine': "Son voilé, atténuation des partiels médiums. Timbre plus intimiste et introspectif.",
    'Alto+sourd. piombo': "Sourdine lourde. Amortissement maximal, utilisée pour les effets timbraux extrêmes.",

    'Violoncelle': """Son chaud et expressif, grande profondeur harmonique.
        <strong>F1=499 Hz dans le cluster de convergence 450–502 Hz (zone /o/).</strong>
        Accord remarquable entre toutes les sources : Giesler (300–500), Meyer (~500),
        Yan_Adds (499 Hz). Le violoncelle est le <em>centre harmonique de l'orchestre</em> selon
        Meyer — sa convergence avec le basson (Δ=3 Hz) est la plus parfaite du corpus.
        Convergence avec le cor (Δ=42 Hz) et le trombone (Δ=8 Hz).""",

    'Violoncelle+sourdine': "F1 légèrement modifié. Son plus mat, projection réduite. Atténuation des harmoniques aigus.",
    'Violoncelle+sourd. piombo': "Sourdine lourde. Amortissement maximal des partiels aigus.",

    'Contrebasse': """Son très grave, rôle de fondation harmonique de l'orchestre.
        <strong>F1=200 Hz (zone /u/)</strong> — la résonance fondamentale de la caisse.
        Giesler note une zone basse 70–250 Hz avec un formant secondaire à 400 Hz.
        Grande variabilité : la contrebasse est l'instrument à cordes le moins formulable
        par un F1 unique.""",

    'Contrebasse+sourdine': "Son très étouffé. La sourdine affecte principalement les harmoniques médiums.",

    # Ensembles
    'Ensemble de violons': """F1 ensemble = 495 Hz — <strong>quasi-identique au solo (506 Hz, Δ=−2 %)</strong>.
        L'effet de section ne déplace pas F1 mais <em>lisse les harmoniques supérieurs</em> :
        F2 passe de 1 518 Hz (solo) à 1 163 Hz (ensemble, −23 %) ; F3 de 2 347 à 1 970 Hz (−16 %).
        Le résultat perceptif est un timbre plus <em>fondu</em> et homogène — moins de relief spectral
        individuel, plus de continuité collective. C'est cet aplatissement de F2–F3 qui donne
        aux sections de violons leur texture caractéristique, distincte du soliste.""",

    "Ensemble d'altos": """F1 ensemble = 366 Hz (zone /å/–/o/) — proche du solo (377 Hz, Δ=−3 %).
        F2 passe de 829 Hz (solo) à 764 Hz (ensemble, −8 %). L'effet de section est plus modeste
        pour l'alto que pour le violon, mais suit le même schéma d'homogénéisation des harmoniques
        supérieurs. La couleur sombre et mélancolique de l'instrument est préservée en section.""",

    'Ensemble de violoncelles': """F1 ensemble = 205 Hz — identique au solo.
        F2 passe de 506 Hz (solo) à 474 Hz (ensemble, −6 %). La section violoncelle maintient
        intégralement la couleur /o/ du soliste, avec un léger lissage des harmoniques supérieurs.
        Elle reste dans la zone de convergence du cluster /o/ (450–502 Hz).""",

    'Ensemble de contrebasses': """Technique non-vibrato (seule disponible dans la base).
        F1=172 Hz — identique au solo. F2 passe de 474 Hz (solo) à 441 Hz (ensemble, −7 %).
        La fondation grave de l'orchestre reste strictement dans la zone /u/, avec
        une homogénéisation légère des harmoniques médiums en section.""",

    'Ensemble de violons+sourdine': "Section avec sourdines. Atténuation collective, timbre soyeux et unifié.",
    "Ensemble d'altos+sourdine": "Section avec sourdines. Son plus intimiste et homogène.",
    'Ensemble de violoncelles+sourdine': "Section avec sourdines. Conservation de la couleur /o/ avec une projection réduite.",
}

# ─── Doublures ───────────────────────────────────────────────
DOUBLURES = {
    'Violon': [
        {'instr':'Hautbois',        'f1_a':'893 (Fp)','f1_b':'1 460 (Fp)','delta':567,'quality':'Complémentaire','rapport':'Unisson','note':'Doublure Fp : Violon Fp=893, Hautbois Fp=1460 — zone /a/–/e/ partagée'},
        {'instr':'Flûte',           'f1_a':'893 (Fp)','f1_b':'1 354 (Fp)','delta':461,'quality':'Complémentaire','rapport':'Unisson','note':'Doublure Fp : Violon Fp=893, Flûte Fp=1354 — enrichissement aigu'},
        {'instr':'Clarinette Sib',  'f1_a':'893 (Fp)','f1_b':'1 016 (Fp)','delta':123,'quality':'Bonne','rapport':'Unisson','note':'Doublure Fp : Violon Fp=893, Cl.Sib Fp=1016 — zone /a/ commune'},
        {'instr':'Trompette',       'f1_a':'893 (Fp)','f1_b':'1 046 (Fp)','delta':153,'quality':'Bonne','rapport':'Octave','note':'Trompette sonne généralement une octave au-dessus'},
    ],
    'Ensemble de violons': [
        {'instr':'Hautbois',        'f1_a':'495','f1_b':'743 (F1)','delta':248,'quality':'Complémentaire','rapport':'Unisson','note':'F1 ens. violons proche de /o/, hautbois en /å/ — complémentarité'},
        {'instr':'Flûte',           'f1_a':'495','f1_b':'743','delta':248,'quality':'Complémentaire','rapport':'Unisson','note':'Zone /o/–/å/ partagée'},
        {'instr':'Violoncelle',     'f1_a':'495','f1_b':'205','delta':290,'quality':'Complémentaire','rapport':'Octave','note':'Complémentarité /o/–/u/ violons+violoncelles'},
        {'instr':'Clarinette Sib',  'f1_a':'495','f1_b':'463','delta':32, 'quality':'Excellente','rapport':'Unisson','note':'Convergence /o/ — fusion cordes-bois'},
    ],
    'Alto': [
        {'instr':'Cor anglais',     'f1_a':'377','f1_b':'452','delta':75,'quality':'Bonne','rapport':'Unisson','note':'Zone /o/–/å/ — couleur mélancolique'},
        {'instr':'Clarinette basse','f1_a':'377','f1_b':'323','delta':54,'quality':'Excellente','rapport':'Octave','note':'Clarinette basse sonne environ une octave en dessous'},
        {'instr':'Cor',             'f1_a':'377','f1_b':'388','delta':11,'quality':'Quasi-parfaite','rapport':'Unisson','note':'Convergence /o/–/å/ — couleur sombre commune'},
    ],
    "Ensemble d'altos": [
        {'instr':'Cor anglais',     'f1_a':'366','f1_b':'452','delta':86,'quality':'Bonne','rapport':'Unisson','note':'Zone /o/–/å/ — couleur mélancolique partagée'},
        {'instr':'Clarinette Sib',  'f1_a':'366','f1_b':'463','delta':97,'quality':'Bonne','rapport':'Unisson','note':'Zone /o/–/å/ — fondu section médium'},
        {'instr':'Cor',             'f1_a':'366','f1_b':'388','delta':22,'quality':'Excellente','rapport':'Unisson','note':'Convergence /o/–/å/ — couleur sombre commune'},
    ],
    'Violoncelle': [
        {'instr':'Basson',          'f1_a':'205','f1_b':'495','delta':290,'quality':'Complémentaire','rapport':'Unisson','note':'Basson en /o/ (495 Hz), violoncelle en /u/ (205 Hz) — complémentarité classique'},
        {'instr':'Cor',             'f1_a':'205','f1_b':'388','delta':183,'quality':'Bonne','rapport':'Octave','note':'Cor en /o/ (388 Hz), violoncelle en /u/ — complémentarité /u/–/o/'},
        {'instr':'Trombone',        'f1_a':'205','f1_b':'237','delta':32,'quality':'Excellente','rapport':'Octave','note':'Trombone F1=237 Hz, violoncelle F1=205 Hz — deux instruments en /u/'},
        {'instr':'Cor anglais',     'f1_a':'205','f1_b':'452','delta':247,'quality':'Complémentaire','rapport':'Octave','note':'Complémentarité /u/–/o/'},
        {'instr':'Tuba contrebasse','f1_a':'205','f1_b':'226','delta':21,'quality':'Quasi-parfaite','rapport':'Octave','note':'Tuba CB F1=226 Hz, violoncelle F1=205 Hz — convergence /u/'},
    ],
    'Ensemble de violoncelles': [
        {'instr':'Cor anglais',     'f1_a':'205','f1_b':'452','delta':247,'quality':'Complémentaire','rapport':'Unisson','note':'Complémentarité /u/–/o/ — couleur grave + chaud'},
        {'instr':'Basson',          'f1_a':'205','f1_b':'495','delta':290,'quality':'Complémentaire','rapport':'Octave','note':'Fondation grave + zone /o/ basson'},
        {'instr':'Cor',             'f1_a':'205','f1_b':'388','delta':183,'quality':'Bonne','rapport':'Octave','note':'Zone /u/–/o/ complémentaire'},
    ],
    'Contrebasse': [
        {'instr':'Tuba basse',      'f1_a':'172','f1_b':'226','delta':54,'quality':'Excellente','rapport':'Unisson','note':'Fondation grave cordes-cuivres — Δ=54 Hz'},
        {'instr':'Contrebasson',    'f1_a':'172','f1_b':'226','delta':54,'quality':'Excellente','rapport':'Unisson','note':'Fondation grave cordes-bois — Δ=54 Hz'},
        {'instr':'Clarinette contrebasse','f1_a':'172','f1_b':'323','delta':151,'quality':'Bonne','rapport':'Octave','note':'Cl. contrebasse sonne une octave au-dessus'},
    ],
    'Ensemble de contrebasses': [
        {'instr':'Tuba basse',      'f1_a':'172','f1_b':'226','delta':54,'quality':'Excellente','rapport':'Unisson','note':'Fondation grave sections — Δ=54 Hz'},
        {'instr':'Contrebasson',    'f1_a':'172','f1_b':'226','delta':54,'quality':'Excellente','rapport':'Unisson','note':'Bois + cordes graves — Δ=54 Hz'},
        {'instr':'Tuba contrebasse','f1_a':'172','f1_b':'226','delta':54,'quality':'Excellente','rapport':'Unisson','note':'Tuba CB F1=226 Hz — convergence /u/'},
    ],
}

# ─── Génération graphiques ────────────────────────────────────
all_info = {}
for lst in [CORDES_SOLISTES, CORDES_ENSEMBLES]:
    for csv_name, display, gfx, tech, fp, color in lst:
        d = get_f(csv_name, tech)
        if not d:
            print(f"  ⚠ MANQUANT: {csv_name}/{tech}")
            continue
        img = make_graph(display, gfx, d['n'], d['F'], fp,
                         family_color=color, family_label='Cordes')
        img_rel = os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None
        all_info[gfx] = {
            'csv': csv_name, 'display': display, 'tech': tech,
            'data': d, 'fp': fp, 'img': img, 'img_rel': img_rel,
        }
        print(f"  ✓ {display:<42s} N={d['n']:>4d} F1={d['F'][0]:>5d}")


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
    analysis = ANALYSIS.get(display, '')
    ref_rows = REF_TABLES.get(display, [])
    ref_html = ('<h4>Valeurs de référence (sources académiques)</h4>' + ref_table_html(ref_rows)) if ref_rows and show_ref else ''
    tech_html = ('<h4>Analyse spectrale complète</h4>' + tech_table_html(csv_name)) if show_all_tech else ''
    dbl_items = DOUBLURES.get(display, [])
    dbl_html = doublures_html(dbl_items)

    # Note technique pour ensemble contrebasses
    tech_note = ''
    if csv_name == 'Contrabass_Ensemble':
        tech_note = '<p class="note-v4">⚠ Technique : non-vibrato uniquement dans la base.</p>'

    return f"""
<div class="instrument-card" id="{gfx}">
  <h3>{display}{cluster}</h3>
  <img src="{info['img_rel']}" alt="{display}" class="formant-graph"/>
  <div class="description">{analysis}</div>
  {fp_html}
  {tech_note}
  {ref_html}
  {tech_html}
  {dbl_html}
</div>"""


def build_html(output_path):
    html = html_head("Référence Formantique — Section Cordes")

    html += '<h1 id="v-cordes">V. Les Cordes</h1>\n'
    html += """
<div class="section-intro cordes">
<p><strong>Plage formantique :</strong> 200–1 556 Hz (voyelles /u/ → /e/).
La famille des cordes présente la plus grande variabilité spectrale de l'orchestre,
compensée par la mesure Fp (centroïde).</p>
<p><strong>Découverte clé :</strong> le <strong>violoncelle (F1=499 Hz)</strong>
est au cœur du cluster de convergence 450–502 Hz, avec Δ=3 Hz avec le basson —
la doublure la plus parfaite du corpus. L'ensemble de violons (F1=1 556 Hz)
développe une zone /e/ de brillance très différente du soliste (506 Hz / 893 Hz Fp) :
<em>effet de section spectral</em> clairement quantifié.</p>
</div>
"""

    html += '<h2>Cordes solistes</h2>\n'

    # Violon
    html += '<h3 class="sub-family">Violon</h3>\n'
    for gfx in ['cordes_violon', 'cordes_vln_sord', 'cordes_vln_piombo']:
        html += instrument_html(gfx, show_ref=(gfx=='cordes_violon'))

    # Alto
    html += '<h3 class="sub-family">Alto</h3>\n'
    for gfx in ['cordes_alto', 'cordes_alt_sord', 'cordes_alt_piombo']:
        html += instrument_html(gfx, show_ref=(gfx=='cordes_alto'))

    # Violoncelle
    html += '<h3 class="sub-family">Violoncelle</h3>\n'
    for gfx in ['cordes_violoncelle', 'cordes_vcl_sord', 'cordes_vcl_piombo']:
        html += instrument_html(gfx, show_ref=(gfx=='cordes_violoncelle'))

    # Contrebasse
    html += '<h3 class="sub-family">Contrebasse</h3>\n'
    for gfx in ['cordes_contrebasse', 'cordes_cb_sord']:
        html += instrument_html(gfx, show_ref=(gfx=='cordes_contrebasse'))

    html += '<h2>Cordes d\'ensemble</h2>\n'
    html += """
<div class="section-intro cordes">
<p>Les données d'ensemble montrent un <strong>effet de section (compression formantique)</strong>
systématique : le F1 collectif est significativement plus haut que le F1 du soliste.
Exemple le plus marqué : Violon solo F1=506 Hz (Fp=893) → Ensemble de violons F1=1 556 Hz (+50%).</p>
</div>
"""
    for gfx in ['cordes_vln_ens', 'cordes_vln_ens_sord', 'cordes_alt_ens', 'cordes_alt_ens_sord',
                'cordes_vcl_ens', 'cordes_vcl_ens_sord', 'cordes_cb_ens']:
        display = all_info.get(gfx, {}).get('display', '')
        is_base = gfx in ['cordes_vln_ens', 'cordes_alt_ens', 'cordes_vcl_ens', 'cordes_cb_ens']
        html += instrument_html(gfx, show_ref=is_base, show_all_tech=is_base)

    html += '<p class="source-note"><strong>Source :</strong> formants_all_techniques.csv (SOL2020) + formants_yan_adds.csv · pipeline v22.<br/><strong>Références :</strong> Backus (1969) · Giesler (1985) · Meyer (2009).</p>\n'
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

    add_heading(doc, display, level=2, color=(21, 101, 192))
    if info['img'] and os.path.exists(info['img']):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(info['img'], width=Inches(6.5))

    analysis = ANALYSIS.get(display, '')
    if analysis:
        add_paragraph(doc, clean_text(analysis), italic=True, size=10)
    if fp:
        add_paragraph(doc, f"Fp (centroïde) = {fp} Hz", bold=True, size=10, color=(27,94,32))

    if csv_name == 'Contrabass_Ensemble':
        add_paragraph(doc, "⚠ Technique : non-vibrato uniquement dans la base.", italic=True, size=9)

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

    add_heading(doc, "V. Les Cordes", level=1, color=(26, 35, 126))

    # Intro
    p = doc.add_paragraph()
    r = p.add_run("Plage formantique : ")
    r.bold = True
    p.add_run("200–1 556 Hz (voyelles /u/ → /e/). La famille des cordes présente la plus grande "
              "variabilité spectrale de l'orchestre, compensée par la mesure Fp (centroïde).")

    p2 = doc.add_paragraph()
    r2 = p2.add_run("Découverte clé : ")
    r2.bold = True
    r2.font.color.rgb = RGBColor(198, 40, 40)
    p2.add_run("Violoncelle (499 Hz) + Basson (502 Hz) = Δ=3 Hz — la doublure la plus parfaite du corpus. "
               "L'ensemble de violons (F1=1 556 Hz) développe une zone /e/ très différente "
               "du soliste (893 Hz Fp) : effet de section spectral clairement quantifié.")

    # Cordes solistes
    add_heading(doc, "Cordes solistes", level=2, color=(21, 101, 192))

    add_heading(doc, "Violon", level=3, color=(183, 28, 28))
    for gfx in ['cordes_violon', 'cordes_vln_sord', 'cordes_vln_piombo']:
        add_instrument_docx(doc, gfx,
                            show_ref=(gfx == 'cordes_violon'),
                            show_all_tech=(gfx == 'cordes_violon'))

    add_heading(doc, "Alto", level=3, color=(21, 101, 192))
    for gfx in ['cordes_alto', 'cordes_alt_sord', 'cordes_alt_piombo']:
        add_instrument_docx(doc, gfx,
                            show_ref=(gfx == 'cordes_alto'),
                            show_all_tech=(gfx == 'cordes_alto'))

    add_heading(doc, "Violoncelle", level=3, color=(27, 94, 32))
    for gfx in ['cordes_violoncelle', 'cordes_vcl_sord', 'cordes_vcl_piombo']:
        add_instrument_docx(doc, gfx,
                            show_ref=(gfx == 'cordes_violoncelle'),
                            show_all_tech=(gfx == 'cordes_violoncelle'))

    add_heading(doc, "Contrebasse", level=3, color=(74, 20, 140))
    for gfx in ['cordes_contrebasse', 'cordes_cb_sord']:
        add_instrument_docx(doc, gfx,
                            show_ref=(gfx == 'cordes_contrebasse'),
                            show_all_tech=(gfx == 'cordes_contrebasse'))

    # Cordes d'ensemble
    add_heading(doc, "Cordes d'ensemble", level=2, color=(21, 101, 192))
    add_paragraph(doc,
        "Les données d'ensemble montrent un effet de section (compression formantique) systématique : "
        "le F1 collectif est significativement plus haut qu'en solo. "
        "Exemple le plus marqué : Violon solo F1=506 Hz (Fp=893) → Ensemble de violons F1=1 556 Hz.",
        size=10)

    for gfx in ['cordes_vln_ens','cordes_vln_ens_sord',
                'cordes_alt_ens','cordes_alt_ens_sord',
                'cordes_vcl_ens','cordes_vcl_ens_sord',
                'cordes_cb_ens']:
        is_base = gfx in ['cordes_vln_ens','cordes_alt_ens','cordes_vcl_ens','cordes_cb_ens']
        add_instrument_docx(doc, gfx, show_ref=is_base, show_all_tech=is_base)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_cordes_v4.html')
    docx_path = os.path.join(OUT_DIR, 'section_cordes_v4.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
    print(f"Graphiques : {len(all_info)}")
