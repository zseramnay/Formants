#!/usr/bin/env python3
"""
build_bois_html_docx.py — Section Bois v4
Enrichi : tableaux de références (Backus/Giesler/Meyer/McCarty),
doublures par instrument, analyse spectrale complète, paragraphes introductifs.
Basson+sourdine et Hautbois+sourdine EXCLUS.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# DONNÉES PAR INSTRUMENT
# format : (csv_name, display_name, gfx_filename, tech, fp_hz, famille_couleur)
# ═══════════════════════════════════════════════════════════
BOIS = [
    ('Piccolo',         'Petite flûte',                 'bois_piccolo',            'ordinario',  None,  '#7B1FA2'),
    ('Flute',           'Flûte',                        'bois_flute',              'ordinario',  1535,  '#2E7D32'),
    ('Bass_Flute',      'Flûte basse',                  'bois_bass_flute',         'ordinario',  1338,  '#2E7D32'),
    ('Contrabass_Flute','Flûte contrebasse',             'bois_contrabass_flute',   'ordinario',  1092,  '#2E7D32'),
    ('Oboe',            'Hautbois',                     'bois_hautbois',           'ordinario',  1485,  '#E65100'),
    ('English_Horn',    'Cor anglais',                  'bois_cor_anglais',        'ordinario',  1135,  '#BF360C'),
    ('Clarinet_Eb',     'Clarinette en Mib',            'bois_clarinet_eb',        'ordinario',  1266,  '#1565C0'),
    ('Clarinet_Bb',     'Clarinette en Sib',            'bois_clarinet_bb',        'ordinario',  1412,  '#1565C0'),
    ('Bass_Clarinet_Bb','Clarinette basse en Sib',      'bois_clarinet_basse',     'ordinario',  1204,  '#0D47A1'),
    ('Contrabass_Clarinet_Bb','Clarinette contrebasse en Sib','bois_clarinet_cb',  'ordinario',  1090,  '#0D47A1'),
    ('Bassoon',         'Basson',                       'bois_basson',             'ordinario',  1079,  '#4E342E'),
    ('Contrabassoon',   'Contrebasson',                 'bois_contrebasson',       'non-vibrato',1279,  '#3E2723'),
]

# Instruments Yan_Adds (badge orange)
YAN_ADDS = {
    'Petite flûte','Flûte basse','Flûte contrebasse',
    'Cor anglais','Clarinette en Mib','Clarinette basse en Sib',
    'Clarinette contrebasse en Sib','Contrebasson'
}

# ─── Tableaux de référence (Backus, Giesler, Meyer + SOL) ───
# Format : {display_name: [{'source':..,'f1':..,'f2':..,'voyelle':..,'n':..,'accord':..},..]}
REF_TABLES = {
    'Petite flûte': [
        {'source':'Backus (1969)',   'f1':'~3 400', 'f2':'—',   'f3':'—',   'f4':'—',   'voyelle':'—',          'n':'—', 'accord':'approx'},
        {'source':'Yan_Adds',        'f1':'2 336 ±852','f2':'3 866 ±790','f3':'5 291','f4':'6 931','voyelle':'i (ee)', 'n':'111','accord':'oui'},
    ],
    'Flûte': [
        {'source':'Backus (1969)',   'f1':'~1 700', 'f2':'—',   'f3':'—',   'f4':'—',   'voyelle':'—',             'n':'—', 'accord':'approx'},
        {'source':'Giesler (1985)',  'f1':'—',      'f2':'—',   'f3':'—',   'f4':'—',   'voyelle':'pas de formants fixes', 'n':'—', 'accord':'—'},
        {'source':'Meyer (2009)',    'f1':'PAS DE FORMANTS FIXES','f2':'—','f3':'—','f4':'—','voyelle':'o/u variable', 'n':'—', 'accord':'—'},
        {'source':'SOL2020',         'f1':'1 354 ±480','f2':'1 987 ±143','f3':'4 210','f4':'—','voyelle':'(variable)','n':'41','accord':'approx'},
    ],
    'Flûte basse': [
        {'source':'Yan_Adds', 'f1':'301 ±92','f2':'824 ±342','f3':'1 623','f4':'2 681','voyelle':'u (oo)', 'n':'82','accord':'—'},
    ],
    'Flûte contrebasse': [
        {'source':'Yan_Adds', 'f1':'334 ±95','f2':'1 082 ±287','f3':'1 853','f4':'—','voyelle':'u (oo)','n':'44','accord':'—'},
    ],
    'Hautbois': [
        {'source':'Backus (1969)',  'f1':'~1 300','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Giesler (1985)', 'f1':'~1 100','f2':'~2 800','f3':'—','f4':'—','voyelle':'a-ähnlich','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',   'f1':'~1 100','f2':'—','f3':'—','f4':'—','voyelle':'a (ah)','n':'—','accord':'approx'},
        {'source':'SOL2020',        'f1':'743 ±378','f2':'1 460 ±452','f3':'3 177','f4':'—','voyelle':'å/a','n':'41','accord':'approx'},
    ],
    'Cor anglais': [
        {'source':'Backus (1969)',  'f1':'~930','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'Meyer (2009)',   'f1':'~600','f2':'—','f3':'—','f4':'—','voyelle':'å (aw)','n':'—','accord':'—'},
        {'source':'Yan_Adds',       'f1':'452 ±163','f2':'1 045 ±308','f3':'2 205','f4':'—','voyelle':'o (oh)','n':'78','accord':'oui'},
    ],
    'Clarinette en Mib': [
        {'source':'Yan_Adds', 'f1':'678 ±211','f2':'1 540 ±360','f3':'2 849','f4':'—','voyelle':'å (aw)','n':'56','accord':'—'},
    ],
    'Clarinette en Sib': [
        {'source':'Backus (1969)',  'f1':'1 500','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'—'},
        {'source':'Giesler (1985)', 'f1':'3 000–4 000','f2':'—','f3':'—','f4':'—','voyelle':'i-ähnlich','n':'—','accord':'—'},
        {'source':'Meyer (2009)',   'f1':'1 500','f2':'—','f3':'—','f4':'—','voyelle':'(variable)','n':'—','accord':'—'},
        {'source':'SOL2020',        'f1':'1 016 ±478','f2':'1 804 ±463','f3':'2 485 ±895','f4':'—','voyelle':'(variable)','n':'41','accord':'—'},
    ],
    'Clarinette basse en Sib': [
        {'source':'Yan_Adds', 'f1':'323 ±87','f2':'905 ±389','f3':'1 716','f4':'—','voyelle':'u (oo)','n':'72','accord':'—'},
    ],
    'Clarinette contrebasse en Sib': [
        {'source':'Yan_Adds', 'f1':'323 ±95','f2':'937 ±290','f3':'1 791','f4':'—','voyelle':'u (oo)','n':'38','accord':'—'},
    ],
    'Basson': [
        {'source':'Backus (1969)',  'f1':'440–500','f2':'—','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'oui'},
        {'source':'Giesler (1985)', 'f1':'500',    'f2':'—','f3':'—','f4':'—','voyelle':'o-ähnlich','n':'—','accord':'oui'},
        {'source':'Meyer (2009)',   'f1':'~500',   'f2':'~1 000','f3':'—','f4':'—','voyelle':'o (oh)','n':'—','accord':'oui'},
        {'source':'SOL2020',        'f1':'502 ±96','f2':'1 097 ±238','f3':'2 089','f4':'—','voyelle':'o (oh)','n':'41','accord':'oui'},
    ],
    'Contrebasson': [
        {'source':'Yan_Adds (non-vibrato)', 'f1':'226 ±98','f2':'771 ±344','f3':'1 463','f4':'—','voyelle':'u (oo)','n':'44','accord':'—'},
    ],
}

# ─── Commentaires d'analyse par instrument ───────────────────
ANALYSIS = {
    'Petite flûte': """Instrument le plus aigu spectralement de l'orchestre. Comme la grande flûte,
        il ne possède pas de formant fixe au sens strict — son énergie spectrale est concentrée dans les
        hautes fréquences (F1=2 336 Hz, zone frontière /e/–/i/). Backus cite ~3 400 Hz, confirmant
        la tendance spectrale aiguë. Variation dynamique : pp=1 963 Hz, mf=2 469 Hz, ff=2 417 Hz.""",

    'Flûte': """La flûte <strong>ne possède pas de formant fixe</strong> (Meyer, Giesler) : son spectre
        varie fortement avec le registre et le souffle. Les valeurs représentent des zones spectrales moyennes.
        Écart entre sources : Backus (~1 700 Hz) vs SOL2020 (1 354 Hz), Δ=346 Hz.
        Le Fp centroïde à 1 535 Hz est plus stable que F1 (σ F1=480 Hz vs σ Fp≈150 Hz).
        La flûte est l'instrument harmoniquement le plus plastique de l'orchestre.""",

    'Flûte basse': """Son chaud et soufflé, plus riche en harmoniques que la grande flûte.
        F1=301 Hz dans la zone /u/ (profondeur). Timbre velouté avec une composante d'air caractéristique.
        Fp=1 338 Hz capture la résonance principale du tuyau.""",

    'Flûte contrebasse': """Son très grave et breathy, à la limite du souffle perceptible.
        F1=334 Hz (zone /u/). Timbre profond et enveloppant, souvent utilisé pour ses qualités texturales.
        Instrument rare, principalement utilisé dans la musique contemporaine.""",

    'Hautbois': """Son nasal et pénétrant, grande projection. Variabilité importante entre sources :
        Backus (1 300), Meyer/Giesler (~1 100), SOL2020 (1 460) — écart maximal 360 Hz. Cette divergence
        s'explique par la dissociation entre F1 spectral strict (743 Hz, zone /å/) et le Fp (1 460 Hz,
        zone de nasalité et d'intensité caractéristique du hautbois).
        L'anche double produit un spectre riche avec une coloration vocale /a/ médium.""",

    'Cor anglais': """Son plus sombre et mélancolique que le hautbois. <strong>F1=452 Hz tombe dans le
        cluster de convergence 450–502 Hz (zone /o/)</strong> — ce qui explique sa fusion naturelle avec
        le cor (457 Hz), le basson (502 Hz) et le violoncelle (499 Hz). Backus cite ~930 Hz mais correspond
        vraisemblablement au Fp ou F2. Fp=1 135 Hz.""",

    'Clarinette en Mib': """Son brillant et incisif, plus perçant que la clarinette Sib.
        F1=678 Hz (zone /å/). La clarinette Mib est l'instrument le plus aigu de la famille.
        Son spectre est dominé par les harmoniques impairs (tuyau cylindrique fermé),
        mais moins marqué que la Sib car le registre aigu domine.""",

    'Clarinette en Sib': """<strong>Découverte majeure : pas de formant fixe.</strong>
        Le pic spectral suit la fondamentale (ratio 1.0) ou le 3e harmonique (ratio 3.0) — dominance
        des harmoniques impairs (tuyau cylindrique fermé). Backus (1 500 Hz) et Meyer (1 500 Hz)
        capturent le registre clairon, Giesler (3 000–4 000 Hz) l'extrême aigu.
        F1 spectral strict = 463 Hz (1er mode du tuyau cylindrique). Le Fp centroïde à 1 412 Hz
        est 4.7× plus stable que F2. F2 varie de 549 Hz (chalumeau) à 2 638 Hz (registre aigu).""",

    'Clarinette basse en Sib': """Son profond et velouté, riche dans le grave.
        F1=323 Hz (zone /u/). Le registre chalumeau possède une couleur très distinctive.
        Comportement analogue à la clarinette Sib mais transposé d'une octave vers le grave.""",

    'Clarinette contrebasse en Sib': """Son extrêmement grave, puissant et bourdonnant.
        F1=323 Hz identique à la clarinette basse, mais F2=937 Hz montre une résonance plus
        développée dans le medium. Timbre massif et enveloppant. Instrument rare.""",

    'Basson': """<strong>Découverte clé : correction majeure</strong> — ancien F1=317 Hz (erreur de pipeline)
        corrigé en 502 Hz. Accord unanime des 4 sources : Giesler (500) = Backus (440–500) = Meyer (~500) =
        SOL2020 (502 Hz). Le basson est le <em>pivot timbral de l'orchestre</em> (Meyer) avec
        Δ=3 Hz avec le violoncelle — la doublure la plus parfaite du corpus. F1=502 Hz au cœur du
        cluster de convergence /o/ (450–502 Hz).""",

    'Contrebasson': """Son très grave et bourdonnant, fondation des bois graves.
        F1=226 Hz (zone /u/), identique au tuba basse. Fp=1 279 Hz.
        Technique analysée : non-vibrato uniquement (pas d'ordinario dans la base SOL2020/Yan_Adds).
        Son rôle harmonique est identique au tuba contrebasse.""",
}

# ─── Sections doublures par instrument ───────────────────────
DOUBLURES = {
    'Petite flûte': [
        {'instr':'Flûte',       'f1_a':'2 336','f1_b':'1 354','delta':'982','quality':'Complémentaire','note':'Piccolo ajoute la brillance extrême, doublure à l\'octave'},
        {'instr':'Violon',      'f1_a':'2 336','f1_b':'1 034','delta':'1 302','quality':'Complémentaire','note':'Renforcement zone aiguë 2 000–3 000 Hz'},
    ],
    'Flûte': [
        {'instr':'Violon',       'f1_a':'1 354','f1_b':'1 034','delta':320,'quality':'Bonne','note':'Convergence zone 1 000–1 500 Hz, brillance partagée'},
        {'instr':'Hautbois',     'f1_a':'1 354','f1_b':'1 460','delta':106,'quality':'Bonne','note':'Zone /e/ commune, légère différenciation de timbre'},
        {'instr':'Clarinette Sib','f1_a':'1 354','f1_b':'1 016','delta':338,'quality':'Complémentaire','note':'Flûte + clarté de la clarinette dans le medium'},
    ],
    'Flûte basse': [
        {'instr':'Cor anglais',  'f1_a':'301','f1_b':'452','delta':151,'quality':'Bonne','note':'Complémentarité grave-medium, couleur sombre'},
        {'instr':'Clarinette basse','f1_a':'301','f1_b':'323','delta':22,'quality':'Excellente','note':'Convergence zone /u/, fusion timbrale profonde'},
    ],
    'Flûte contrebasse': [
        {'instr':'Contrebasse', 'f1_a':'334','f1_b':'200','delta':134,'quality':'Bonne','note':'Zone graves partagée /u/'},
        {'instr':'Tuba basse',  'f1_a':'334','f1_b':'249','delta':85,'quality':'Bonne','note':'Renforcement des graves extrêmes'},
    ],
    'Hautbois': [
        {'instr':'Cor anglais',  'f1_a':'743','f1_b':'452','delta':291,'quality':'Complémentaire','note':'Hautbois + chaleur du cor anglais au grave'},
        {'instr':'Violon',       'f1_a':'743','f1_b':'1 034','delta':291,'quality':'Complémentaire','note':'Enrichissement spectral bidirectionnel'},
    ],
    'Cor anglais': [
        {'instr':'Clarinette Sib','f1_a':'452','f1_b':'1 016','delta':564,'quality':'Complémentaire','note':'Complémentarité parfaite grave-aigu'},
        {'instr':'Cor',          'f1_a':'452','f1_b':'457','delta':5,'quality':'Quasi-parfaite','note':'Cluster /o/ — convergence formantique maximale'},
        {'instr':'Basson',       'f1_a':'452','f1_b':'502','delta':50,'quality':'Excellente','note':'Famille /o/ — bois graves homogènes'},
        {'instr':'Violoncelle',  'f1_a':'452','f1_b':'499','delta':47,'quality':'Excellente','note':'Couleur /o/ commune — doublure bois-cordes classique'},
    ],
    'Clarinette en Mib': [
        {'instr':'Petite flûte', 'f1_a':'678','f1_b':'2 336','delta':'1 658','quality':'Complémentaire','note':'Cl. Mib dans medium, Piccolo dans aigu'},
        {'instr':'Violon',       'f1_a':'678','f1_b':'1 034','delta':356,'quality':'Bonne','note':'Enrichissement du medium aigu'},
    ],
    'Clarinette en Sib': [
        {'instr':'Cor anglais',  'f1_a':'1 016','f1_b':'1 045','delta':29,'quality':'Excellente','note':'Convergence Fp quasi-parfaite'},
        {'instr':'Hautbois',     'f1_a':'1 016','f1_b':'1 460','delta':444,'quality':'Complémentaire','note':'Complémentarité chalumeau-registre moyen'},
        {'instr':'Alto',         'f1_a':'1 016','f1_b':'369','delta':647,'quality':'Complémentaire','note':'Enrichissement spectral large bande'},
    ],
    'Clarinette basse en Sib': [
        {'instr':'Trombone basse', 'f1_a':'909','f1_b':'894','delta':15,'quality':'Quasi-parfaite','note':'Convergence dans la zone /a/'},
        {'instr':'Clarinette Sib', 'f1_a':'909','f1_b':'1 016','delta':107,'quality':'Bonne','note':'Complémentarité grave-medium'},
        {'instr':'Basson',         'f1_a':'909','f1_b':'502','delta':407,'quality':'Complémentaire','note':'Enrichissement spectral grave-medium'},
    ],
    'Clarinette contrebasse en Sib': [
        {'instr':'Contrebasson',  'f1_a':'323','f1_b':'226','delta':97,'quality':'Bonne','note':'Doublure contrebasse des bois'},
        {'instr':'Tuba basse',    'f1_a':'323','f1_b':'249','delta':74,'quality':'Bonne','note':'Fondation grave commune'},
    ],
    'Basson': [
        {'instr':'Violoncelle',  'f1_a':'502','f1_b':'499','delta':3,'quality':'Quasi-parfaite ★','note':'Doublure la plus parfaite du corpus — Δ=3 Hz'},
        {'instr':'Cor',          'f1_a':'502','f1_b':'457','delta':45,'quality':'Excellente','note':'Cluster /o/ — timbres frères (Meyer)'},
        {'instr':'Trombone',     'f1_a':'502','f1_b':'491','delta':11,'quality':'Quasi-parfaite','note':'Cluster /o/ — doublure classique'},
        {'instr':'Cor anglais',  'f1_a':'502','f1_b':'452','delta':50,'quality':'Excellente','note':'Famille /o/ des bois graves'},
        {'instr':'Trompette',    'f1_a':'502','f1_b':'457','delta':45,'quality':'Complémentaire','note':'Transition bois-cuivres classique'},
    ],
    'Contrebasson': [
        {'instr':'Tuba basse',        'f1_a':'226','f1_b':'249','delta':23,'quality':'Excellente','note':'Unisson des graves extrêmes'},
        {'instr':'Contrebasse',       'f1_a':'226','f1_b':'200','delta':26,'quality':'Excellente','note':'Fondation grave bois-cordes'},
        {'instr':'Tuba contrebasse',  'f1_a':'226','f1_b':'471','delta':245,'quality':'Complémentaire','note':'Extension harmonique vers le medium'},
    ],
}

# ─── Génération graphiques et collecte des infos ─────────────
all_info = {}
for csv_name, display, gfx, tech, fp, color in BOIS:
    d = get_f(csv_name, tech)
    if not d:
        print(f"  ⚠ MANQUANT: {csv_name}/{tech}")
        continue
    img = make_graph(display, gfx, d['n'], d['F'], fp,
                     family_color=color, family_label='Bois')
    img_rel = os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None
    all_info[gfx] = {
        'csv': csv_name, 'display': display, 'tech': tech,
        'data': d, 'fp': fp, 'img': img, 'img_rel': img_rel,
        'color': color,
    }
    print(f"  ✓ {display:<38s} N={d['n']:>4d} F1={d['F'][0]:>5d}")


# ═══════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════

def instrument_html(gfx, show_ref=True):
    info = all_info.get(gfx)
    if not info:
        return ''
    display = info['display']
    csv_name = info['csv']
    fp = info['fp']
    data = info['data']
    is_yan = display in YAN_ADDS
    in_cluster = data['F'][0] in range(420, 560)

    badge = '<span class="yan-badge">Yan_Adds</span>' if is_yan else ''
    cluster = '<span class="cluster-badge">Cluster /o/</span>' if in_cluster else ''

    # Analyse
    analysis = ANALYSIS.get(display, '')
    # Fp note
    fp_html = f'<p class="fp-note">◆ Fp (centroïde) = {fp} Hz</p>' if fp else ''

    # Note technique pour contrebasson
    tech_note = ''
    if csv_name == 'Contrabassoon':
        tech_note = '<p class="note-v4">⚠ Technique analysée : <b>non-vibrato</b> (pas d\'ordinario disponible dans la base).</p>'

    # Tableau références
    ref_rows = REF_TABLES.get(display, [])
    ref_html = ''
    if ref_rows and show_ref:
        ref_html = '<h4>Valeurs de référence (sources académiques)</h4>' + ref_table_html(ref_rows)

    # Analyse spectrale complète
    tech_html = '<h4>Analyse spectrale complète (toutes techniques sustained)</h4>' + tech_table_html(csv_name)

    # Doublures
    dbl_items = DOUBLURES.get(display, [])
    dbl_html = doublures_html(dbl_items)

    return f"""
<div class="instrument-card" id="{gfx}">
  <h3>{display}{badge}{cluster}</h3>
  <img src="{info['img_rel']}" alt="{display}" class="formant-graph"/>
  <div class="description">{analysis}</div>
  {fp_html}
  {tech_note}
  {ref_html}
  {tech_html}
  {dbl_html}
</div>"""


def build_html(output_path):
    html = html_head("Référence Formantique — Section Bois")

    html += '<h1 id="ii-bois">II. Les Bois</h1>\n'
    html += """
<div class="section-intro bois">
<p><strong>Plage formantique :</strong> 226–2 638 Hz (voyelles /u/ → /i/).
Grande diversité timbrale selon le type d'anche et le profil du tuyau.</p>
<p><strong>Caractéristiques principales :</strong></p>
<ul>
<li>Les <em>anches doubles</em> (hautbois, cor anglais, basson, contrebasson) partagent une zone
formantique commune autour de 900–1 200 Hz, avec une coloration vocalique /a/ caractéristique.</li>
<li>Les <em>clarinettes</em> (tuyau cylindrique, harmoniques impairs) n'ont pas de formant fixe au
sens strict — le spectre dépend fortement du registre.</li>
<li>Les <em>flûtes</em> (tuyau ouvert) n'ont pas non plus de formant fixe — le spectre décroît
linéairement au-dessus du fondamental.</li>
</ul>
<p><strong>Découverte clé :</strong> le <strong>cor anglais (F1=452 Hz)</strong> et le
<strong>basson (F1=502 Hz)</strong> tombent dans le <em>cluster de convergence 450–502 Hz</em>,
aux côtés du cor, du trombone et du violoncelle. Le basson présente une convergence Δ=3 Hz avec le
violoncelle — la doublure formantiquement la plus parfaite du corpus.</p>
</div>
"""

    html += '<h2>Flûtes</h2>\n'
    html += '<p>La famille des flûtes se distingue par l\'absence de formant fixe strict. Le spectre est dominé par la fondamentale, avec une décroissance des harmoniques suivant un profil quasi-linéaire en dB. Le Fp (centroïde spectral) permet néanmoins de caractériser la zone d\'énergie principale.</p>\n'
    for gfx in ['bois_piccolo', 'bois_flute', 'bois_bass_flute', 'bois_contrabass_flute']:
        html += instrument_html(gfx)

    html += '<h2>Anches doubles</h2>\n'
    html += '<p>Les instruments à anche double (hautbois, cor anglais, basson, contrebasson) partagent un profil formantique similaire avec une zone d\'énergie principale autour de 900–1 200 Hz. Cette famille acoustique explique leur tendance à fusionner naturellement dans l\'orchestre.</p>\n'
    for gfx in ['bois_hautbois', 'bois_cor_anglais', 'bois_basson', 'bois_contrebasson']:
        html += instrument_html(gfx)

    html += '<h2>Clarinettes</h2>\n'
    html += '<p>La famille des clarinettes (tuyau cylindrique fermé) présente un comportement acoustique radicalement différent des autres bois : suppression des harmoniques pairs, dominance des partiels impairs. Cette spécificité rend difficile la définition d\'un formant fixe et explique les divergences entre sources académiques.</p>\n'
    for gfx in ['bois_clarinet_eb', 'bois_clarinet_bb', 'bois_clarinet_basse', 'bois_clarinet_cb']:
        html += instrument_html(gfx)

    html += f'<p class="source-note"><strong>Source des données :</strong> formants_all_techniques.csv + formants_yan_adds.csv — pipeline v22 validé (Δ=0 Hz, 16/16 instruments). Basson+sourdine et Hautbois+sourdine exclus de cette étude.<br/><strong>Références :</strong> Backus (1969) · Giesler (1985) · Meyer (2009) · SOL2020 IRCAM.</p>\n'
    html += html_foot()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ HTML: {output_path}")


# ═══════════════════════════════════════════════════════════
# BUILD DOCX
# ═══════════════════════════════════════════════════════════

def add_instrument_docx(doc, gfx):
    info = all_info.get(gfx)
    if not info:
        return
    display = info['display']
    csv_name = info['csv']
    fp = info['fp']
    is_yan = display in YAN_ADDS

    title = display + (' [Yan_Adds]' if is_yan else '')
    add_heading(doc, title, level=2, color=(27, 94, 32))

    if info['img'] and os.path.exists(info['img']):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(info['img'], width=Inches(6.5))

    analysis = ANALYSIS.get(display, '')
    if analysis:
        add_paragraph(doc, analysis, italic=True, size=10)

    if fp:
        add_paragraph(doc, f"Fp (centroïde) = {fp} Hz", bold=True, size=10,
                      color=(27, 94, 32))

    # Ref table
    ref_rows = REF_TABLES.get(display, [])
    if ref_rows:
        add_heading(doc, "Valeurs de référence", level=3)
        ref_table_docx(doc, ref_rows)

    # Techniques table
    add_heading(doc, "Analyse spectrale complète (toutes techniques)", level=3)
    tech_table_docx(doc, csv_name)

    # Doublures
    dbl_items = DOUBLURES.get(display, [])
    if dbl_items:
        add_heading(doc, "Doublures recommandées", level=3, color=(245, 127, 23))
        table = doc.add_table(rows=1, cols=5)
        table.style = 'Table Grid'
        for idx, h in enumerate(['Instrument associé', 'F1', 'F1 associé', 'Écart', 'Qualité']):
            set_cell_text(table.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
            set_cell_shading(table.rows[0].cells[idx], 'F57F17')
        for it in dbl_items:
            row = table.add_row().cells
            delta = it.get('delta','')
            if isinstance(delta, (int, float)):
                delta_str = f"Δ={delta} Hz"
            else:
                delta_str = str(delta)
            vals = [it.get('instr',''), it.get('f1_a','—'), it.get('f1_b','—'),
                    delta_str, it.get('quality','')]
            for idx, v in enumerate(vals):
                set_cell_text(row[idx], v, bold=(idx==0), size=9)
        for row_obj in table.rows:
            for cell, w in zip(row_obj.cells, [3.5, 1.8, 1.8, 2.0, 3.0]):
                cell.width = Cm(w)

    doc.add_paragraph()


def build_docx(output_path):
    doc = new_docx()

    add_heading(doc, "II. Les Bois", level=1, color=(26, 35, 126))
    p = doc.add_paragraph()
    p.add_run("Plage formantique : ").bold = True
    p.add_run("226–2 638 Hz (voyelles /u/ → /i/). ")
    p.add_run("Découverte clé : ").bold = True
    p.add_run("cor anglais (452 Hz) et basson (502 Hz) dans le cluster de convergence 450–502 Hz. "
              "Basson–violoncelle : Δ=3 Hz — la doublure formantiquement la plus parfaite du corpus.")

    add_heading(doc, "Flûtes", level=1, color=(46, 125, 50))
    for gfx in ['bois_piccolo', 'bois_flute', 'bois_bass_flute', 'bois_contrabass_flute']:
        add_instrument_docx(doc, gfx)

    add_heading(doc, "Anches doubles", level=1, color=(46, 125, 50))
    for gfx in ['bois_hautbois', 'bois_cor_anglais', 'bois_basson', 'bois_contrebasson']:
        add_instrument_docx(doc, gfx)

    add_heading(doc, "Clarinettes", level=1, color=(46, 125, 50))
    for gfx in ['bois_clarinet_eb', 'bois_clarinet_bb', 'bois_clarinet_basse', 'bois_clarinet_cb']:
        add_instrument_docx(doc, gfx)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_bois_v4.html')
    docx_path = os.path.join(OUT_DIR, 'section_bois_v4.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
    print(f"Graphiques : {len(all_info)}")
