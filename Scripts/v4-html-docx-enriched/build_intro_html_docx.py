#!/usr/bin/env python3
"""
build_intro_html_docx.py — Introduction + méthodologie + tableau voyelles
Section I du document de référence formantique
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# CONTENU TEXTUEL
# ═══════════════════════════════════════════════════════════

INTRO_TEXT = """
Ce document constitue la référence quantitative la plus complète disponible
pour l'analyse formantique des instruments de l'orchestre. Il examine comment
les doublures orchestrales classiques s'expliquent par l'assemblage complémentaire
des formants spectraux instrumentaux. Les formants sont les zones de résonance
définissant le timbre : lorsque deux instruments sont doublés, leurs spectres se
combinent pour créer une couleur timbrale homogène ou complémentaire.
"""

METHODO_TEXT = """
L'analyse repose sur 5 914 échantillons professionnels couvrant 30 instruments
de l'orchestre, validée contre quatre sources académiques indépendantes.
Le taux de concordance global est de 93 % (27/29 instruments comparables).
"""

FP_EXPLANATION = """
<h3 id="fp-centroide">Le Formant Principal (Fp) par centroïde spectral — pourquoi et comment</h3>

<p>Pour les instruments à large tessiture, le formant F1 (premier pic spectral) est
<strong>extrêmement instable</strong> d'un registre à l'autre : il ne caractérise pas
le timbre global de l'instrument, mais seulement la note jouée à ce moment.</p>

<p>Exemple démonstratif : le violon présente un F1 dont l'écart-type atteint σ=651 Hz
selon le registre — soit une variation de plus d'une octave. Cette instabilité rend
F1 peu exploitable comme signature timbrale.</p>

<p>La mesure <strong>Fp (Formant Principal)</strong> — centroïde spectral pondéré en
énergie dans une bande fréquentielle optimisée par instrument — résout ce problème.
Le centroïde est la « moyenne de masse » du spectre dans une bande donnée : il
intègre la contribution de toutes les fréquences au lieu d'isoler un pic unique.</p>

<div class="fp-explanation">
<strong>Formule :</strong>
Fp = Σ(fᵢ × Aᵢ) / Σ(Aᵢ)
où fᵢ est la fréquence du bin i, Aᵢ son amplitude, et la somme porte sur une bande
choisie par instrument (typiquement 600–1 400 Hz ou 1 000–2 000 Hz).
</div>

<p>Comparaison Fp vs F2 (écart-type σ, instrument ordinario) :</p>
<table class="ref-table">
<tr class="header"><th>Instrument</th><th>Fp (Hz)</th><th>σ Fp</th><th>F2 (Hz)</th><th>σ F2</th><th>Gain de stabilité</th></tr>
<tr><td>Violon</td><td>893</td><td>92</td><td>1 518</td><td>651</td><td><strong>7.1×</strong></td></tr>
<tr><td>Trompette</td><td>1 046</td><td>98</td><td>1 324</td><td>1 018</td><td><strong>10.4×</strong></td></tr>
<tr><td>Clarinette Sib</td><td>1 412</td><td>169</td><td>1 130</td><td>795</td><td><strong>4.7×</strong></td></tr>
<tr><td>Cor</td><td>738</td><td>112</td><td>1 106</td><td>734</td><td><strong>6.5×</strong></td></tr>
</table>

<p>Le Fp est systématiquement plus stable que F1 ou F2 et correspond au
<em>Hauptformant</em> (formant principal perceptif) décrit par Meyer (2009) pour les
cordes. Il représente la coloration timbrale globale de l'instrument telle que
l'oreille la perçoit, indépendamment de la note jouée.</p>

<p><strong>22 instruments sur 30 bénéficient d'une mesure Fp</strong> validée dans
cette étude. Pour les 8 instruments restants (dont la flûte et le hautbois qui ont
un spectre très variable), F1 ou F2 reste utilisé.</p>
"""

# Tableau des voyelles complet (incluant i/ee >2600 Hz)
VOWEL_TABLE_ROWS = [
    {'voyelle': 'u (oo)',  'freq': '200–400',   'perception': 'Profondeur, gravité',
     'instruments': 'Tuba basse (249), Contrebasse (200), Contrebasson (226), Flûte basse (301)',
     'color': '#DCEEFB'},
    {'voyelle': 'o (oh)',  'freq': '400–600',   'perception': 'Plénitude, rondeur',
     'instruments': 'Cor (457), Tuba contrebasse (471), Contrebasson (478), Trombone (491), Violoncelle (499), Basson (502), Cor anglais (452), Vcl-Ens (587)',
     'color': '#D5ECD5'},
    {'voyelle': 'å (aw)',  'freq': '~600–800',  'perception': 'Transition, chaleur',
     'instruments': 'Vcl-Ens sourdine (587), Alto sourdine (683), Flûte basse (737)',
     'color': '#FDE8CE'},
    {'voyelle': 'a (ah)',  'freq': '800–1 250', 'perception': 'Puissance, présence',
     'instruments': 'Trb. basse (894), Cl. basse (909), Cl. Sib (1 016), Cor anglais Fp (1 135), Trompette (1 046, Fp), Alto-Ens (1 190), Basson Fp (1 079)',
     'color': '#F8D5D5'},
    {'voyelle': 'e (eh)',  'freq': '1 250–2 600', 'perception': 'Clarté, brillance',
     'instruments': 'Flûte (1 354), Hautbois (1 460), Vln-Ens (1 556), Cl. Mib (1 747), Piccolo (2 336), Violon Fp (893)',
     'color': '#E8D5F0'},
    {'voyelle': 'i (ee)',  'freq': '> 2 600',   'perception': 'Brillance extrême, stridence',
     'instruments': 'Petite flûte (2 336 ≈ limite), Trompette+sourdine harmon (2 358)',
     'color': '#FFF8D0'},
]

SOURCES_ROWS = [
    ('Backus (1969)', 'The Acoustical Foundations of Music', 'Référence historique, mesures ciblées cuivres et bois', 'W.W. Norton & Co.'),
    ('Giesler (1985)', 'Instrumentation: Ein Hand- und Lehrbuch', 'Mesures détaillées, associations vocaliques explicites, 13 instruments', 'Breitkopf & Härtel'),
    ('Meyer (2009)', 'Acoustics and the Performance of Music (5e éd.)', 'Analyse acoustique avec couleurs vocales, zones vocaliques définies', 'Springer-Verlag'),
    ('SOL2020 IRCAM', 'Studio On Line', '12 instruments solistes, 2 391 échantillons sustained analysés', 'IRCAM / EIC'),
    ('Yan_Adds', 'Extension personnelle', '18 instruments supplémentaires, 1 646 échantillons (ensembles, bois auxiliaires, cuivres graves)', 'VSL, Con Timbre, échantillons personnels'),
    ('McCarty/CCRMA (2003)', 'Vowel space chart for orchestral instruments', 'Référence directionnelle — limitations d\'exactitude reconnues par l\'auteur', 'CCRMA Stanford'),
]

PARAMS_ROWS = [
    ('FFT Size', '4 096 samples'),
    ('Sample Rate', '44 100 Hz'),
    ('Résolution fréquentielle', '~10,8 Hz/bin'),
    ('Plage analysée', '100–3 000 Hz'),
    ('Algorithme', 'scipy.signal.find_peaks — pic le plus proéminent (pas premier pic)'),
    ('Hauteur minimale', '10 % de l\'amplitude maximale'),
    ('Distance minimale', '10 bins (~50 Hz)'),
    ('Proéminence minimale', '5 % de l\'amplitude maximale'),
]

# ═══════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════

def build_html(output_path):
    html = html_head("Référence Formantique — Introduction et Méthodologie")

    # Page de garde
    html += """
<div class="doc-header">
  <h1>Référence Formantique de l'Orchestre</h1>
  <p class="subtitle">Étude quantitative des formants spectraux instrumentaux</p>
  <p class="subtitle">Analyse de 5 914 échantillons · 30 instruments · Mars 2026</p>
  <p class="meta">
    Sources : SOL2020 (IRCAM) · Yan_Adds · Backus (1969) · Giesler (1985) · Meyer (2009) · McCarty/CCRMA (2003)<br>
    Méthode : centroïde spectral Fp · pipeline v22 validé (16/16 CSV à Δ=0 Hz) · 93 % de concordance multi-sources
  </p>
</div>
"""

    # Table des matières
    html += """
<h2>Table des matières</h2>
<nav style="background:white;border:1px solid #ddd;border-radius:6px;padding:18px 24px;margin:16px 0;">
<ol style="line-height:2.2;">
  <li><a href="#i-introduction">I. Introduction et Méthodologie</a>
    <ul style="margin:4px 0 4px 20px;">
      <li><a href="#sources">Sources des données</a></li>
      <li><a href="#methodo">Méthodologie d'extraction</a></li>
      <li><a href="#fp-centroide">Le Formant Principal (Fp)</a></li>
      <li><a href="#voyelles">Correspondance voyelles–fréquences</a></li>
    </ul>
  </li>
  <li><a href="#ii-bois">II. Les Bois</a></li>
  <li><a href="#iii-cuivres">III. Les Cuivres</a></li>
  <li><a href="#iv-saxophones">IV. Les Saxophones</a></li>
  <li><a href="#v-cordes">V. Les Cordes</a></li>
  <li><a href="#vi-synthese">VI. Synthèse — Convergences Formantiques</a></li>
</ol>
</nav>
"""

    # Section I
    html += f'<h1 id="i-introduction">I. Introduction et Méthodologie</h1>\n'
    html += f'<div class="section-intro intro"><p>{INTRO_TEXT.strip()}</p><p>{METHODO_TEXT.strip()}</p></div>\n'

    # Sources
    html += '<h3 id="sources">Sources des données</h3>\n'
    html += '<table class="ref-table"><tr class="header"><th>Source</th><th>Titre / Base</th><th>Description</th><th>Éditeur</th></tr>\n'
    for src, title, desc, publisher in SOURCES_ROWS:
        html += f'<tr><td><b>{src}</b></td><td>{title}</td><td>{desc}</td><td>{publisher}</td></tr>\n'
    html += '</table>\n'

    # Méthodologie
    html += '<h3 id="methodo">Méthodologie d\'extraction formantique</h3>\n'
    html += """
<div class="section-intro general">
<p><strong>Techniques INCLUSES :</strong> normal, arco, sustain, ordinario, vibrato,
non-vibrato, flautando — dynamiques pp à ff. Ces techniques produisent les formants
structurels stables de l'instrument.</p>
<p><strong>Techniques EXCLUES :</strong> pizzicato, col legno, tremolo, trilles,
harmoniques artificiels, multiphoniques, flutter tongue, sourdines (analysées
séparément), glissandi, portamento. Ces techniques modifient radicalement le spectre
et ne représentent pas le timbre fondamental.</p>
</div>
"""
    html += '<table class="ref-table"><tr class="header"><th>Paramètre</th><th>Valeur / Description</th></tr>\n'
    for p, v in PARAMS_ROWS:
        html += f'<tr><td><b>{p}</b></td><td>{v}</td></tr>\n'
    html += '</table>\n'
    html += '<p><em>Choix méthodologique critique : la détection du pic le plus proéminent (et non du premier pic) capture le formant perceptuel principal, évite les résonances basses secondaires, et est cohérente avec la perception auditive.</em></p>\n'

    # Fp
    html += FP_EXPLANATION

    # Tableau voyelles
    html += '<h3 id="voyelles">Correspondance voyelles–fréquences (Meyer 2009)</h3>\n'
    html += """
<p>Le système vocalique fournit un cadre intuitif pour décrire le timbre instrumental.
Meyer (2009) établit des correspondances entre zones formantiques et voyelles de la
langue allemande/française. Ce tableau étend cette correspondance à l'ensemble du
corpus SOL2020 + Yan_Adds.</p>
"""
    html += '<table class="vowel-table">\n'
    html += '<tr class="header"><th>Voyelle</th><th>Fréquence (Hz)</th><th>Perception timbrale</th><th>Instruments représentatifs (F1 ou Fp)</th></tr>\n'
    for row in VOWEL_TABLE_ROWS:
        bg = f' style="background-color:{row["color"]}40;"'
        html += f'<tr{bg}><td><strong>{row["voyelle"]}</strong></td><td>{row["freq"]}</td><td>{row["perception"]}</td><td style="text-align:left;">{row["instruments"]}</td></tr>\n'
    html += '</table>\n'
    html += """
<div class="note-v4">
<strong>Note sur le i (ee) &gt;2 600 Hz :</strong> Très peu d'instruments de l'orchestre
symphonique présentent un F1 dans cette zone en ordinario. La petite flûte atteint
2 336 Hz (zone frontière /e/–/i/). La trompette+sourdine harmon propulse son spectre
à 2 358 Hz, atteignant la zone /i/. Cette brillance extrême est l'effet recherché
dans les sourdines harmon jazz.
</div>
"""

    html += '<p class="source-note"><strong>Sources :</strong> Meyer (2009) — Acoustics and the Performance of Music (5e éd.) · SOL2020 IRCAM · Yan_Adds · pipeline v22 validé.</p>\n'
    html += html_foot()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ HTML: {output_path}")


# ═══════════════════════════════════════════════════════════
# BUILD DOCX
# ═══════════════════════════════════════════════════════════

def build_docx(output_path):
    doc = new_docx()

    # Titre
    p = doc.add_paragraph()
    p.style = doc.styles['Title']
    r = p.add_run("Référence Formantique de l'Orchestre")
    r.font.color.rgb = RGBColor(26, 35, 126)

    add_paragraph(doc, "Étude quantitative des formants spectraux instrumentaux", italic=True, size=12)
    add_paragraph(doc, "5 914 échantillons · 30 instruments · Mars 2026 · Pipeline v22 validé", size=10, color=(100, 100, 100))
    doc.add_paragraph()

    # Section I
    add_heading(doc, "I. Introduction et Méthodologie", level=1, color=(26, 35, 126))
    add_paragraph(doc, INTRO_TEXT.strip(), size=10)
    add_paragraph(doc, METHODO_TEXT.strip(), size=10)

    # Sources
    add_heading(doc, "Sources des données", level=2, color=(46, 125, 50))
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    for idx, h in enumerate(['Source', 'Titre / Base', 'Description', 'Éditeur']):
        set_cell_text(table.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table.rows[0].cells[idx], '37474F')
    for src, title, desc, pub in SOURCES_ROWS:
        row = table.add_row().cells
        for idx, v in enumerate([src, title, desc, pub]):
            set_cell_text(row[idx], v, bold=(idx==0), size=9,
                          align=WD_ALIGN_PARAGRAPH.LEFT if idx > 0 else WD_ALIGN_PARAGRAPH.CENTER)
    for row_obj in table.rows:
        for cell, w in zip(row_obj.cells, [3.0, 4.5, 5.5, 3.5]):
            cell.width = Cm(w)

    # Méthodologie
    doc.add_paragraph()
    add_heading(doc, "Méthodologie d'extraction formantique", level=2, color=(46, 125, 50))
    p = doc.add_paragraph()
    p.add_run("Techniques INCLUSES : ").bold = True
    p.add_run("ordinario, vibrato, non-vibrato, arco, flautando — dynamiques pp à ff.")
    p = doc.add_paragraph()
    p.add_run("Techniques EXCLUES : ").bold = True
    p.add_run("pizzicato, col legno, tremolo, trilles, harmoniques artificiels, multiphoniques, flutter tongue, sourdines (traitées séparément), glissandi.")

    add_heading(doc, "Paramètres d'analyse", level=3)
    table2 = doc.add_table(rows=1, cols=2)
    table2.style = 'Table Grid'
    for idx, h in enumerate(['Paramètre', 'Valeur / Description']):
        set_cell_text(table2.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table2.rows[0].cells[idx], '37474F')
    for param, val in PARAMS_ROWS:
        row = table2.add_row().cells
        set_cell_text(row[0], param, bold=True, size=9)
        set_cell_text(row[1], val, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
    for row_obj in table2.rows:
        for cell, w in zip(row_obj.cells, [5.0, 11.5]):
            cell.width = Cm(w)

    # Fp
    doc.add_paragraph()
    add_heading(doc, "Le Formant Principal (Fp) par centroïde spectral", level=2, color=(27, 94, 32))
    add_paragraph(doc,
        "Pour les instruments à large tessiture, F1 (premier pic spectral) est extrêmement instable "
        "d'un registre à l'autre. La mesure Fp — centroïde spectral pondéré en énergie dans une bande "
        "fréquentielle optimisée par instrument — résout ce problème.",
        size=10)
    add_paragraph(doc,
        "Fp = Σ(fᵢ × Aᵢ) / Σ(Aᵢ)  "
        "où fᵢ est la fréquence du bin i, Aᵢ son amplitude, "
        "et la somme porte sur une bande choisie par instrument.",
        bold=True, size=10)

    # Table Fp vs F2
    table3 = doc.add_table(rows=1, cols=6)
    table3.style = 'Table Grid'
    for idx, h in enumerate(['Instrument','Fp (Hz)','σ Fp','F2 (Hz)','σ F2','Gain stabilité']):
        set_cell_text(table3.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table3.rows[0].cells[idx], '1B5E20')
    for row_data in [
        ('Violon',       '893',   '92',  '1 518', '651',  '7.1×'),
        ('Trompette',    '1 046', '98',  '1 324', '1 018','10.4×'),
        ('Clarinette Sib','1 412','169', '1 130', '795',  '4.7×'),
        ('Cor',          '738',   '112', '1 106', '734',  '6.5×'),
    ]:
        row = table3.add_row().cells
        for idx, v in enumerate(row_data):
            set_cell_text(row[idx], v, bold=(idx==0), size=9)
    for row_obj in table3.rows:
        for cell, w in zip(row_obj.cells, [3.5, 1.5, 1.5, 1.5, 1.5, 2.0]):
            cell.width = Cm(w)

    # Tableau voyelles
    doc.add_paragraph()
    add_heading(doc, "Correspondance voyelles–fréquences (Meyer 2009)", level=2, color=(46, 125, 50))
    table4 = doc.add_table(rows=1, cols=4)
    table4.style = 'Table Grid'
    for idx, h in enumerate(['Voyelle', 'Fréquence (Hz)', 'Perception', 'Instruments représentatifs']):
        set_cell_text(table4.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table4.rows[0].cells[idx], '4A148C')
    for v_row in VOWEL_TABLE_ROWS:
        row = table4.add_row().cells
        vals = [v_row['voyelle'], v_row['freq'], v_row['perception'], v_row['instruments']]
        for idx, v in enumerate(vals):
            set_cell_text(row[idx], v, bold=(idx==0), size=9,
                          align=WD_ALIGN_PARAGRAPH.LEFT if idx==3 else WD_ALIGN_PARAGRAPH.CENTER)
    for row_obj in table4.rows:
        for cell, w in zip(row_obj.cells, [1.8, 2.0, 2.5, 10.2]):
            cell.width = Cm(w)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_intro_v4.html')
    docx_path = os.path.join(OUT_DIR, 'section_intro_v4.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
