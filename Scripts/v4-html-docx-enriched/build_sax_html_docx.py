#!/usr/bin/env python3
"""
build_sax_html_docx.py — Section Saxophones v4
Saxophone alto (SOL2020) — seul saxophone disponible dans le corpus.
Références académiques, doublures, analyse spectrale complète.
Mention des saxophones absents (ténor, baryton, soprano).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# INSTRUMENTS
# ═══════════════════════════════════════════════════════════
SAX = [
    ('Sax_Alto', 'Saxophone alto', 'sax_alto', 'ordinario', 1440, '#AD1457'),
]

# ─── Références académiques ──────────────────────────────────
REF_TABLES = {
    'Saxophone alto': [
        {'source':'Giesler (1985)',  'f1':'~1 000–1 200','f2':'—','f3':'—','f4':'—','voyelle':'a-ähnlich','n':'—','accord':'approx'},
        {'source':'Backus (1969)',   'f1':'~1 100',      'f2':'~2 200','f3':'—','f4':'—','voyelle':'—','n':'—','accord':'approx'},
        {'source':'SOL2020',         'f1':'398 ±89',     'f2':'1 217 ±312','f3':'2 355 ±498','f4':'—','voyelle':'o (oh)','n':'41','accord':'—'},
    ],
}

# ─── Note sur le saxophone ténor dans le cluster /o/ ─────────
SAX_TENOR_NOTE = """
<div class="note-v4">
<strong>Point remarquable — Saxophone ténor dans le cluster de convergence :</strong><br/>
Giesler (1985) écrit explicitement à propos du saxophone ténor :
<em>«&nbsp;Formantähnliches Maximum bei etwa 400–600 Hz mit o-ähnlicher Vokalfärbung…
(vergl. z.B. Fagott, Horn, Posaune)&nbsp;»</em> — Giesler cite EXPLICITEMENT
Basson, Cor et Trombone comme partageant le même formant que le saxophone ténor.
<br/>
Le saxophone ténor est donc un membre potentiel de la zone de convergence
/o/–/å/ (377–510 Hz), mais <strong>absent du corpus SOL2020/Yan_Adds</strong>.
Données Giesler : F1 ≈ 400–600 Hz → correspondance directe avec la zone /o/.
</div>
"""

ANALYSIS = {
    'Saxophone alto': """Son chaud et expressif, grande flexibilité timbrale et dynamique.
        <strong>F1=398 Hz (zone /o/)</strong> — le saxophone alto s'inscrit dans la zone de
        convergence /o/–/å/ (377–510 Hz), aux côtés du cor (388 Hz) et du cor anglais (452 Hz).
        Tuyau conique (comme le hautbois et le basson) produisant un spectre riche en harmoniques
        pairs et impairs. Fp centroïde à 1 440 Hz (zone /e/).
        Le saxophone alto est le seul saxophone présent dans la base SOL2020 IRCAM.
        Les saxophones soprano, ténor et baryton sont absents du corpus.
        <br/>
        <strong>Convergences clés :</strong> Sax alto (398) + Cor (388) Δ=10 Hz,
        Sax alto (398) + Cor anglais (452) Δ=54 Hz, Sax alto (398) + Alto (377) Δ=21 Hz.""",
}

DOUBLURES = {
    'Saxophone alto': [
        {'instr':'Cor anglais',  'f1_a':'398','f1_b':'452','delta':54,  'quality':'Excellente','rapport':'Unisson','note':'Δ=54 Hz — zone /o/ proche, bois graves expressifs'},
        {'instr':'Cor',          'f1_a':'398','f1_b':'388','delta':10,  'quality':'Quasi-parfaite','rapport':'Unisson','note':'Δ=10 Hz — convergence sax-cor, zone /o/–/å/'},
        {'instr':'Basson',       'f1_a':'398','f1_b':'495','delta':97,  'quality':'Bonne','rapport':'Unisson','note':'Zone /o/ partagée — couleur boisée chaude'},
        {'instr':'Alto',         'f1_a':'398','f1_b':'377','delta':21,  'quality':'Quasi-parfaite','rapport':'Unisson','note':'Δ=21 Hz — sax alto + alto, convergence /o/–/å/'},
        {'instr':'Violoncelle',  'f1_a':'398','f1_b':'205','delta':193, 'quality':'Bonne','rapport':'Octave','note':'Sax /o/, violoncelle /u/ — complémentarité'},
        {'instr':'Clarinette Sib','f1_a':'398','f1_b':'463','delta':65, 'quality':'Excellente','rapport':'Unisson','note':'Zone /o/ commune — Δ=65 Hz'},
    ],
}

# ─── Génération graphiques ────────────────────────────────────
all_info = {}
for csv_name, display, gfx, tech, fp, color in SAX:
    d = get_f(csv_name, tech)
    if not d:
        print(f"  ⚠ MANQUANT: {csv_name}/{tech}")
        continue
    img = make_graph(display, gfx, d['n'], d['F'], fp,
                     family_color=color, family_label='Saxophones')
    img_rel = os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None
    all_info[gfx] = {
        'csv': csv_name, 'display': display, 'tech': tech,
        'data': d, 'fp': fp, 'img': img, 'img_rel': img_rel,
    }
    print(f"  ✓ {display:<38s} N={d['n']:>4d} F1={d['F'][0]:>5d}")


# ═══════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════

def instrument_html(gfx):
    info = all_info.get(gfx)
    if not info:
        return ''
    display = info['display']
    csv_name = info['csv']
    fp = info['fp']
    data = info['data']

    fp_html = f'<p class="fp-note">◆ Fp (centroïde) = {fp} Hz</p>' if fp else ''
    analysis = ANALYSIS.get(display, '')
    ref_rows = REF_TABLES.get(display, [])
    ref_html = ('<h4>Valeurs de référence (sources académiques)</h4>'
                + ref_table_html(ref_rows)) if ref_rows else ''
    tech_html = '<h4>Analyse spectrale complète (toutes techniques sustained)</h4>' + tech_table_html(csv_name)
    dbl_items = DOUBLURES.get(display, [])
    dbl_html = doublures_html(dbl_items)

    return f"""
<div class="instrument-card" id="{gfx}">
  <h3>{display}</h3>
  <img src="{info['img_rel']}" alt="{display}" class="formant-graph"/>
  <div class="description">{analysis}</div>
  {fp_html}
  {ref_html}
  {tech_html}
  {SAX_TENOR_NOTE}
  {dbl_html}
</div>"""


def build_html(output_path):
    html = html_head("Référence Formantique — Section Saxophones")

    html += '<h1 id="iv-saxophones">IV. Les Saxophones</h1>\n'
    html += """
<div class="section-intro sax">
<p><strong>Corpus disponible :</strong> saxophone alto uniquement (base SOL2020 IRCAM).
Les saxophones soprano, ténor et baryton ne disposent pas de données specenv dans le corpus actuel.</p>
<p><strong>Intérêt acoustique :</strong> le saxophone est le seul instrument de l'orchestre à
combiner un tuyau conique (comme le basson et le hautbois) avec une anche simple (comme la clarinette).
Cette dualité acoustique lui confère un spectre riche et une grande versatilité timbrale.</p>
<p><strong>Position dans la zone de convergence :</strong> F1=398 Hz — dans la zone /o/–/å/ (377–510 Hz),
aux côtés du cor (388 Hz, Δ=10 Hz) et de l'alto (377 Hz, Δ=21 Hz). Giesler (1985) place explicitement
le saxophone <em>ténor</em> dans le groupe /o/ avec basson, cor et trombone.
Le saxophone alto s'inscrit pleinement dans cette zone de convergence.</p>
</div>
"""

    html += instrument_html('sax_alto')

    html += '<h2>Saxophones absents du corpus</h2>\n'
    html += """
<div class="section-intro sax">
<table class="ref-table">
<tr class="header"><th>Instrument</th><th>F1 estimé (Giesler)</th><th>Zone vocalique</th><th>Statut corpus</th></tr>
<tr><td>Saxophone soprano</td><td>~1 200–1 500 Hz</td><td>/a/–/e/</td><td>Absent SOL2020 / Yan_Adds</td></tr>
<tr><td>Saxophone ténor</td><td>400–600 Hz</td><td>/o/ — cluster</td><td>Absent SOL2020 / Yan_Adds</td></tr>
<tr><td>Saxophone baryton</td><td>~250–400 Hz</td><td>/u/–/o/</td><td>Absent SOL2020 / Yan_Adds</td></tr>
</table>
<p><em>Ces valeurs sont basées sur Giesler (1985) et la littérature acoustique.
Leur inclusion dans le corpus constitue une extension future du projet.</em></p>
</div>
"""

    html += f'<p class="source-note"><strong>Source :</strong> formants_all_techniques.csv (SOL2020 IRCAM) · pipeline v22.<br/><strong>Références :</strong> Backus (1969) · Giesler (1985) · Meyer (2009).</p>\n'
    html += html_foot()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ HTML: {output_path}")


# ═══════════════════════════════════════════════════════════
# BUILD DOCX
# ═══════════════════════════════════════════════════════════

def build_docx(output_path):
    doc = new_docx()

    add_heading(doc, "IV. Les Saxophones", level=1, color=(26, 35, 126))

    # Intro complète
    p = doc.add_paragraph()
    r = p.add_run("Corpus disponible : ")
    r.bold = True
    p.add_run("saxophone alto uniquement (SOL2020 IRCAM). "
              "Les saxophones soprano, ténor et baryton ne disposent pas de données specenv dans le corpus actuel.")

    p2 = doc.add_paragraph()
    r2 = p2.add_run("Intérêt acoustique : ")
    r2.bold = True
    p2.add_run("le saxophone est le seul instrument de l'orchestre à combiner un tuyau conique "
               "(comme le basson et le hautbois) avec une anche simple (comme la clarinette). "
               "Cette dualité acoustique lui confère un spectre riche et une grande versatilité timbrale.")

    p3 = doc.add_paragraph()
    r3 = p3.add_run("Position dans la zone de convergence : ")
    r3.bold = True
    r3.font.color.rgb = RGBColor(198, 40, 40)
    p3.add_run("F1=398 Hz — dans la zone /o/–/å/ (377–510 Hz), aux côtés du cor (388 Hz, Δ=10 Hz) "
               "et de l'alto (377 Hz, Δ=21 Hz). Giesler (1985) place le saxophone ténor dans ce groupe.")

    info = all_info.get('sax_alto')
    if info:
        add_heading(doc, info['display'], level=2, color=(173, 20, 87))
        if info['img'] and os.path.exists(info['img']):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(info['img'], width=Inches(6.5))

        analysis = ANALYSIS.get(info['display'], '')
        if analysis:
            add_paragraph(doc, clean_text(analysis), italic=True, size=10)
        if info['fp']:
            add_paragraph(doc, f"Fp (centroïde) = {info['fp']} Hz", bold=True, size=10,
                          color=(27, 94, 32))

        ref_rows = REF_TABLES.get(info['display'], [])
        if ref_rows:
            add_heading(doc, "Valeurs de référence (sources académiques)", level=3)
            ref_table_docx(doc, ref_rows)

        add_heading(doc, "Analyse spectrale complète", level=3)
        tech_table_docx(doc, info['csv'])

        # Note saxophone ténor
        p_note = doc.add_paragraph()
        r_note = p_note.add_run("Note — Saxophone ténor dans le cluster /o/ : ")
        r_note.bold = True
        r_note.font.color.rgb = RGBColor(230, 81, 0)
        p_note.add_run("Giesler (1985) cite explicitement le saxophone ténor parmi les instruments "
                       "du cluster 400–600 Hz, aux côtés du Basson, Cor et Trombone. "
                       "Données Giesler : F1 ≈ 400–600 Hz — correspondance directe avec la zone /o/.")

        dbl_items = DOUBLURES.get(info['display'], [])
        if dbl_items:
            add_heading(doc, "Doublures recommandées", level=3, color=(245, 127, 23))
            doublures_table_docx(doc, dbl_items)

    # Saxophones absents
    add_heading(doc, "Saxophones absents du corpus", level=2, color=(173, 20, 87))
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    for idx, h in enumerate(['Instrument', 'F1 estimé (Giesler)', 'Zone vocalique', 'Statut corpus']):
        set_cell_text(table.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table.rows[0].cells[idx], 'AD1457')
    for row_data in [
        ('Saxophone soprano', '~1 200–1 500 Hz', '/a/–/e/', 'Absent SOL2020 / Yan_Adds'),
        ('Saxophone ténor',   '400–600 Hz',       '/o/ — cluster', 'Absent SOL2020 / Yan_Adds'),
        ('Saxophone baryton', '~250–400 Hz',       '/u/–/o/', 'Absent SOL2020 / Yan_Adds'),
    ]:
        row = table.add_row().cells
        for idx, v in enumerate(row_data):
            set_cell_text(row[idx], v, bold=(idx == 0), size=9)
    for row_obj in table.rows:
        for cell, w in zip(row_obj.cells, [3.5, 3.0, 2.5, 5.0]):
            cell.width = Cm(w)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_sax_v4.html')
    docx_path = os.path.join(OUT_DIR, 'section_sax_v4.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
    print(f"Graphiques : {len(all_info)}")
