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

<div style="background:#f3e5f5;border:2px solid #7b1fa2;border-radius:8px;padding:14px 18px;margin:20px 0;">
<h4 style="color:#4a148c;margin:0 0 10px 0;">σ(Fp) comme indicateur de sélectivité spectrale</h4>
<p style="margin:0;">L'écart-type σ du Fp reflète indirectement la <strong>largeur de bande</strong>
(bandwidth) de la résonance principale de l'instrument. Un σ(Fp) faible indique un
formant étroit et bien défini (forte sélectivité, Q élevé) ; un σ(Fp) élevé indique un
formant large et diffus. Ainsi, le violon (σ=92 Hz) possède un timbre spectralement
plus focalisé que la clarinette Sib (σ=169 Hz), ce qui se confirme perceptivement :
le violon a une « couleur vocalique » plus identifiable que la clarinette dont le
spectre évolue fortement selon le registre.</p>
</div>
"""

# Tableau des voyelles complet (incluant i/ee >2600 Hz)
VOWEL_TABLE_ROWS = [
    {'voyelle': 'u (oo)',  'freq': '200–400',
     'perception': 'Profondeur, gravité',
     'exemples_fr': 'b<u>ou</u>che, t<u>ou</u>r',
     'instruments': 'Contrebasse (172), Tuba basse (226), Tuba CB (226), Contrebasson (226), Trombone (237), Flûte basse (301)',
     'color': '#DCEEFB'},
    {'voyelle': 'o (oh)',  'freq': '400–600',
     'perception': 'Plénitude, rondeur',
     'exemples_fr': 'b<u>eau</u>, v<u>eau</u>',
     'instruments': 'Alto (377), Cor (388), Sax alto (398), Cor anglais (452), Cl. Sib (463), Basson (495), Ens. Violons (495), Violon (506)',
     'color': '#D5ECD5'},
    {'voyelle': 'å (aw)',  'freq': '~600–800',
     'perception': 'Transition, chaleur',
     'exemples_fr': 'p<u>â</u>te, âm<u>e</u>, (entre o et a)',
     'instruments': 'Cl. Mib (678), Flûte (743), Hautbois (743), Trompette (786)',
     'color': '#FDE8CE'},
    {'voyelle': 'a (ah)',  'freq': '800–1 250',
     'perception': 'Puissance, présence',
     'exemples_fr': 'p<u>a</u>s, cl<u>a</u>sse',
     'instruments': 'Cor Fp (738), Violon Fp (893), Basson Fp (1 079), Trompette Fp (1 046), Cor anglais Fp (1 135)',
     'color': '#F8D5D5'},
    {'voyelle': 'e (eh)',  'freq': '1 250–2 600',
     'perception': 'Clarté, brillance',
     'exemples_fr': 'f<u>é</u>e, <u>é</u>toile',
     'instruments': 'Cl. Sib Fp (1 412), Flûte Fp (1 535), Hautbois Fp (1 485), Cl. Mib Fp (1 266), Petite flûte (1 109)',
     'color': '#E8D5F0'},
    {'voyelle': 'i (ee)',  'freq': '> 2 600',
     'perception': 'Brillance extrême, stridence',
     'exemples_fr': 'v<u>i</u>e, s<u>i</u>ffler',
     'instruments': 'Petite flûte (1 992 F2), Trompette+sourdine harmon (2 358)',
     'color': '#FFF8D0'},
]

SOURCES_ROWS = [
    ('Backus (1969)', 'The Acoustical Foundations of Music', 'Référence historique, mesures ciblées cuivres et bois', 'W.W. Norton & Co.'),
    ('Giesler (1985)', 'Instrumentation: Ein Hand- und Lehrbuch', 'Mesures détaillées, associations vocaliques explicites, 13 instruments', 'Breitkopf & Härtel'),
    ('Meyer (2009)', 'Acoustics and the Performance of Music (5e éd.)', 'Analyse acoustique avec couleurs vocales, zones vocaliques définies', 'Springer-Verlag'),
    ('SOL2020 Orchidea', 'Studio On Line', '12 instruments solistes, 2 391 échantillons sustained analysés', 'Orchidea / EIC'),
    ('Yan_Adds', 'Ajouts de provenances diverses', '18 instruments supplémentaires, 1 646 échantillons (ensembles, bois auxiliaires, cuivres graves)', 'VSL, Con Timbre, échantillons personnels'),
    ('McCarty/CCRMA (2003)', 'Vowel space chart for orchestral instruments', 'Référence directionnelle — limitations d\'exactitude reconnues par l\'auteur', 'CCRMA Stanford'),
]

PARAMS_ROWS = [
    ('FFT Size', '4 096 samples'),
    ('Sample Rate', '44 100 Hz'),
    ('Résolution fréquentielle', '~10,8 Hz/bin'),
    ('Plage analysée', '100–3 000 Hz'),
    ('Données d\'entrée', 'Enveloppes spectrales pré-calculées (specenv, 1 024 bins) — fenêtrage Hann + lissage appliqués en amont par le pipeline Orchidea'),
    ('Algorithme', 'Détection de pics sur enveloppe spectrale — pic le plus proéminent (pas premier pic)'),
    ('Seuil d\'amplitude', '−30 dB sous le pic maximum de la région'),
    ('Distance minimale', '70 Hz entre pics (~6.5 bins)'),
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
    Sources : SOL2020 (Orchidea) · Yan_Adds · Backus (1969) · Giesler (1985) · Meyer (2009) · McCarty/CCRMA (2003)<br>
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

    # ── Point B (v5) : Clause "sustained ordinario only" bien visible ──
    html += """
<div style="background:#fff8e1;border:2px solid #f9a825;border-radius:8px;padding:14px 18px;margin:16px 0;">
<strong style="color:#e65100;">🎵 Périmètre de mesure — Tenues soutenues uniquement</strong><br>
Toutes les valeurs formantiques de ce document sont mesurées sur des <strong>tenues soutenues
(sustained)</strong> en jeu <strong>ordinario</strong>. Cela exclut les transitoires d'attaque
(où les formants ne sont pas encore stabilisés), les modes de jeu étendus, et les
dynamiques extrêmes. Les sourdines sont traitées séparément dans les sections correspondantes.
</div>
"""

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

    # ── Point A (v5) : Note terminologique F1/F2 vs formants vocaux ──
    html += """
<div style="background:#e3f2fd;border:2px solid #1565c0;border-radius:8px;padding:16px 20px;margin:24px 0;">
<h4 style="color:#0d47a1;margin:0 0 10px 0;">⚠ Note terminologique : F1–F6 dans ce document</h4>
<p style="margin:0;">Dans cette étude, <strong>F1, F2, … F6</strong> désignent les <strong>pics spectraux
principaux</strong> extraits par analyse d'enveloppe spectrale (<code>scipy.signal.find_peaks</code>).
Ces pics correspondent aux résonances principales du système acoustique de l'instrument
(corps, colonne d'air, cavités) et sont mis en regard des <strong>voyelles cardinales par analogie
perceptive</strong> — sans prétendre à une équivalence stricte avec les formants du tractus
vocal humain (résonances du conduit vocal au sens de Fant, 1960).</p>
<p style="margin:8px 0 0 0;">Pour les instruments à vent cylindriques (clarinette, flûte), où aucun formant fixe
n'existe au sens strict, la notation F1 désigne la <strong>zone d'énergie spectrale
dominante</strong> — terminologie plus exacte que « formant » pour ces familles.</p>
</div>
"""

    # Fp
    html += FP_EXPLANATION

    # ── Note méthodologique : deux représentations complémentaires ──
    html += """
<div style="background:#fff3e0;border:2px solid #e65100;border-radius:8px;padding:16px 20px;margin:24px 0;">
<h4 style="color:#bf360c;margin:0 0 10px 0;">⚠ Deux représentations complémentaires : Profil formantique vs Carte spectrale vocalique</h4>
<p style="margin:0;">Ce document utilise deux types de graphiques pour chaque instrument. Ils ne mesurent pas
exactement la même chose et peuvent donc montrer des valeurs légèrement différentes :</p>
<table style="margin:12px 0;width:100%;border-collapse:collapse;font-size:0.9em;">
<tr style="background:#fff8e1;"><td style="padding:8px;border:1px solid #e0e0e0;width:50%;vertical-align:top;">
<strong>Profil formantique moyen</strong> (courbes de cloche)<br/>
Données : <em>CSV v3</em> — médiane des positions de pics F1–F6 calculée sur chaque échantillon
individuellement, puis agrégée. L'amplitude (dB) est lue sur l'enveloppe spectrale moyenne
à la fréquence médiane du formant.<br/>
<em>Ce qu'il montre :</em> la position « typique » de chaque formant et sa largeur de bande (BW -3 dB).
</td>
<td style="padding:8px;border:1px solid #e0e0e0;width:50%;vertical-align:top;">
<strong>Carte spectrale vocalique</strong> (enveloppe + zones vocaliques)<br/>
Données : <em>enveloppe specenv Orchidea</em> — moyenne de toutes les enveloppes spectrales
du registre, puis détection des pics directement sur cette moyenne.<br/>
<em>Ce qu'il montre :</em> la forme réelle du spectre moyen avec ses zones de résonance,
ses vallées, et le contexte vocalique.
</td></tr>
</table>
<p style="margin:8px 0 0 0;">Les deux approches convergent pour les formants bien définis (instruments à anche, cuivres)
mais peuvent diverger pour les instruments à grande tessiture (cordes, flûtes) où la moyenne
de l'enveloppe « lisse » les pics individuels. <strong>Le profil formantique donne les positions
de référence ; la carte spectrale donne le contexte acoustique complet par registre.</strong></p>
</div>
"""

    # Tableau voyelles
    html += '<h3 id="voyelles">Correspondance voyelles–fréquences (Meyer 2009)</h3>\n'
    html += """
<p>Le système vocalique fournit un cadre intuitif pour décrire le timbre instrumental.
Meyer (2009) établit des correspondances entre zones formantiques et voyelles de la
langue allemande/française. Ce tableau étend cette correspondance à l'ensemble du
corpus SOL2020 + Yan_Adds.</p>
"""
    html += '<table class="vowel-table">\n'
    html += '<tr class="header"><th>Voyelle</th><th>Fréquence (Hz)</th><th>Exemples français</th><th>Perception timbrale</th><th>Instruments représentatifs (F1 ou Fp)</th></tr>\n'
    for row in VOWEL_TABLE_ROWS:
        bg = f' style="background-color:{row["color"]}40;"'
        html += (f'<tr{bg}>'
                 f'<td><strong>{row["voyelle"]}</strong></td>'
                 f'<td>{row["freq"]}</td>'
                 f'<td style="font-style:italic;color:#444;">{row["exemples_fr"]}</td>'
                 f'<td>{row["perception"]}</td>'
                 f'<td style="text-align:left;">{row["instruments"]}</td>'
                 f'</tr>\n')
    html += '</table>\n'

    # SVG voyelles IPA — inline depuis le fichier média
    svg_rel = 'media/voyelles_IPA.svg'
    html += f'''
<div style="margin:24px 0;">
<figure style="margin:0;">
  <img src="{svg_rel}" alt="Positions formantiques des voyelles IPA — F1 et F2 sur axe fréquentiel"
       style="max-width:100%;display:block;margin:0 auto;border:1px solid #eee;border-radius:6px;"/>
  <figcaption style="text-align:center;font-size:0.85em;color:#666;margin-top:8px;font-style:italic;">
    Positions F1 et F2 des 11 voyelles cardinales françaises sur axe fréquentiel linéaire ·
    zone cluster /o/–/å/ surlignée · d'après Meyer (2009), Giesler (1985)
  </figcaption>
</figure>
</div>
'''
    html += """
<div class="note-v4">
<strong>Note sur le i (ee) &gt;2 600 Hz :</strong> Très peu d'instruments de l'orchestre
symphonique présentent un F1 dans cette zone en ordinario. La petite flûte atteint
2 336 Hz (zone frontière /e/–/i/). La trompette+sourdine harmon propulse son spectre
à 2 358 Hz, atteignant la zone /i/. Cette brillance extrême est l'effet recherché
dans les sourdines harmon jazz.
</div>
"""

    html += '<p class="source-note"><strong>Sources :</strong> Meyer (2009) — Acoustics and the Performance of Music (5e éd.) · SOL2020 Orchidea · Yan_Adds · pipeline v22 validé.</p>\n'
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

    # ── Point B (v5) : Clause sustained ordinario ──
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("🎵 Périmètre de mesure — Tenues soutenues uniquement").bold = True
    p = doc.add_paragraph()
    p.add_run("Toutes les valeurs formantiques sont mesurées sur des tenues soutenues (sustained) "
              "en jeu ordinario. Cela exclut les transitoires d'attaque, les modes de jeu étendus "
              "et les dynamiques extrêmes. Les sourdines sont traitées séparément.")

    # ── Point A (v5) : Note terminologique ──
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("⚠ Note terminologique : F1–F6 dans ce document").bold = True
    p = doc.add_paragraph()
    p.add_run("Dans cette étude, F1–F6 désignent les pics spectraux principaux extraits par "
              "analyse d'enveloppe spectrale (find_peaks). Ces pics correspondent aux résonances "
              "principales du système acoustique de l'instrument et sont mis en regard des voyelles "
              "cardinales par analogie perceptive — sans prétendre à une équivalence stricte avec "
              "les formants du tractus vocal humain (résonances du conduit vocal au sens de Fant, 1960).")

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

    # ── Note méthodologique : deux représentations ──
    doc.add_paragraph()
    add_heading(doc, "Deux représentations complémentaires", level=2, color=(230, 81, 0))
    add_paragraph(doc,
        "Ce document utilise deux types de graphiques pour chaque instrument :", size=10)
    add_paragraph(doc,
        "Profil formantique moyen (courbes de cloche) — Données CSV v3 : médiane des positions "
        "de pics F1–F6 calculée sur chaque échantillon individuellement, puis agrégée. "
        "L'amplitude (dB) est lue sur l'enveloppe spectrale moyenne à la fréquence médiane du formant. "
        "Montre la position « typique » de chaque formant et sa largeur de bande (BW -3 dB).",
        size=10)
    add_paragraph(doc,
        "Carte spectrale vocalique (enveloppe + zones vocaliques) — Données specenv Orchidea : "
        "moyenne de toutes les enveloppes spectrales du registre, puis détection des pics sur cette moyenne. "
        "Montre la forme réelle du spectre moyen avec ses zones de résonance, ses vallées, et le contexte vocalique.",
        size=10)
    add_paragraph(doc,
        "Les deux approches convergent pour les formants bien définis (instruments à anche, cuivres) "
        "mais peuvent diverger pour les instruments à grande tessiture (cordes, flûtes). "
        "Le profil formantique donne les positions de référence ; "
        "la carte spectrale donne le contexte acoustique complet par registre.",
        italic=True, size=10)

    # ── Point F (v5) : σ comme proxy de bandwidth/Q ──
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("σ(Fp) comme indicateur de sélectivité spectrale").bold = True
    p = doc.add_paragraph()
    p.add_run("L'écart-type σ du Fp reflète indirectement la largeur de bande (bandwidth) "
              "de la résonance principale. Un σ(Fp) faible indique un formant étroit et bien "
              "défini (forte sélectivité, Q élevé) ; un σ(Fp) élevé indique un formant large "
              "et diffus. Ainsi, le violon (σ=92 Hz) possède un timbre spectralement plus "
              "focalisé que la clarinette Sib (σ=169 Hz).")

    # Tableau voyelles
    doc.add_paragraph()
    add_heading(doc, "Correspondance voyelles–fréquences (Meyer 2009)", level=2, color=(46, 125, 50))
    table4 = doc.add_table(rows=1, cols=5)
    table4.style = 'Table Grid'
    for idx, h in enumerate(['Voyelle', 'Fréquence (Hz)', 'Exemples français', 'Perception', 'Instruments représentatifs']):
        set_cell_text(table4.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table4.rows[0].cells[idx], '4A148C')
    for v_row in VOWEL_TABLE_ROWS:
        row = table4.add_row().cells
        # Nettoyer les balises HTML <u> pour le DOCX
        import re as _re
        exemples_clean = _re.sub(r'<[^>]+>', '', v_row['exemples_fr'])
        vals = [v_row['voyelle'], v_row['freq'], exemples_clean,
                v_row['perception'], v_row['instruments']]
        for idx, v in enumerate(vals):
            set_cell_text(row[idx], v, bold=(idx==0), size=9,
                          align=WD_ALIGN_PARAGRAPH.LEFT if idx in (2,4) else WD_ALIGN_PARAGRAPH.CENTER)
    for row_obj in table4.rows:
        for cell, w in zip(row_obj.cells, [1.8, 2.0, 3.5, 2.5, 8.5]):
            cell.width = Cm(w)
            cell.width = Cm(w)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_intro_v6.html')
    docx_path = os.path.join(OUT_DIR, 'section_intro_v6.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
