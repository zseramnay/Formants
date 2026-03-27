#!/usr/bin/env python3
"""
make_voyelles_IPA.py
Génère le fichier media/voyelles_IPA.svg — espace vocalique IPA F1/F2
d'après Meyer (2009) et Giesler (1985).

Usage :
    python3 make_voyelles_IPA.py
Sortie :
    Versions-html-and-docx/media/voyelles_IPA.svg
    (chemin relatif depuis la racine du repo)
"""

import os

# ─── Chemin de sortie ───────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Remonter à la racine du repo si le script est dans Scripts/
OUT_PATH = os.path.join(SCRIPT_DIR, '..', 'Versions-html-and-docx', 'media', 'voyelles_IPA.svg')
# Si le script est lancé depuis la racine du repo :
# OUT_PATH = 'Versions-html-and-docx/media/voyelles_IPA.svg'

# ─── Paramètres du graphique ────────────────────────────────────
W, H = 1100, 640          # dimensions SVG
X0, Y0 = 75, 450          # origine axe F2 (bas gauche)
X_MAX = 1060              # fin axe F2
F2_MIN, F2_MAX = 0, 3000  # plage F2 Hz
F2_LINE_Y = 190           # ligne de référence F2
F1_LINE_Y = 360           # ligne de référence F1

def f2_to_x(hz):
    """Convertit une fréquence F2 (Hz) en coordonnée X."""
    return X0 + (hz / F2_MAX) * (X_MAX - X0)

# ─── Données voyelles ────────────────────────────────────────────
# (symbole, F1_Hz, F2_Hz, couleur, fond, taille_cercle, note)
VOYELLES = [
    # Fermées /i/ /y/ /u/
    ('i',  280, 2600, '#1a3a8b', 'white',   11, False),
    ('y',  280, 1900, '#1a3a8b', 'white',   11, False),
    ('u',  310,  750, '#1a3a8b', 'white',   11, False),
    # Mi-fermées /e/ — vert
    ('e',  400, 2150, '#2a7a2a', 'white',   11, False),
    # Mi-fermées cluster /ø/ /o/ /ə/ — doré
    ('ø',  400, 1550, '#b8860b', '#fffbe6', 13, True),
    ('o',  460,  850, '#b8860b', '#fffbe6', 13, True),
    ('ə',  480, 1550, '#b8860b', '#fffbe6', 13, True),
    # Mi-ouvertes /ɛ/ /œ/ /ɔ/ — marron
    ('ɛ',  580, 1800, '#8b4500', 'white',   11, False),
    ('œ',  580, 1400, '#8b4500', 'white',   11, False),
    ('ɔ',  560,  900, '#8b4500', 'white',   11, False),
    # Ouvertes /a/ /ɑ/ — rouge sombre
    ('a',  800, 1300, '#6b0000', 'white',   11, False),
    ('ɑ',  750,  950, '#6b0000', 'white',   11, False),
]

# Positions manuelles des points sur F2 (rangée haute) et F1 (rangée basse)
# Format : (symbole, cx_f2, cy_f2_offset, cx_f1, cy_f1_offset)
# offset : 'up' = au-dessus de la ligne, 'down' = en-dessous
POSITIONS_F2 = {
    'i':  (f2_to_x(2600), 'up'),
    'y':  (f2_to_x(1900), 'up'),
    'u':  (f2_to_x(750),  'up'),
    'e':  (f2_to_x(2150), 'up'),
    'ø':  (f2_to_x(1550), 'up'),
    'o':  (f2_to_x(850),  'down'),
    'ə':  (f2_to_x(1550), 'down'),
    'ɛ':  (f2_to_x(1800), 'up'),
    'œ':  (f2_to_x(1400), 'down'),
    'ɔ':  (f2_to_x(900),  'up'),
    'a':  (f2_to_x(1300), 'up'),
    'ɑ':  (f2_to_x(950),  'down'),
}

POSITIONS_F1 = {
    'i':  (155, 'up'),
    'y':  (180, 'down'),
    'u':  (205, 'up'),
    'e':  (230, 'down'),
    'ø':  (257, 'up'),
    'o':  (286, 'down'),
    'ə':  (315, 'up'),
    'ɛ':  (367, 'up'),
    'œ':  (392, 'down'),
    'ɔ':  (342, 'down'),
    'a':  (442, 'down'),
    'ɑ':  (417, 'up'),
}

# Légende bas de page
LEGEND_L = [
    ('i',  '/i/', 'vie',   'fermée',     280,  2600, '#1a3a8b', 'white',   False),
    ('y',  '/y/', 'lune',  'fermée',     280,  1900, '#1a3a8b', 'white',   False),
    ('u',  '/u/', 'tout',  'fermée',     310,   750, '#1a3a8b', 'white',   False),
    ('e',  '/e/', 'été',   'mi-fermée',  400,  2150, '#2a7a2a', 'white',   False),
    ('ø',  '/ø/', 'feu',   'mi-fermée',  400,  1550, '#b8860b', '#fffbe6', True),
    ('o',  '/o/', 'eau',   'mi-fermée',  460,   850, '#b8860b', '#fffbe6', True),
]
LEGEND_R = [
    ('ə',  '/ə/', 'le',    'mi-fermée',  480,  1550, '#b8860b', '#fffbe6', True),
    ('ɛ',  '/ɛ/', 'fête',  'mi-ouverte', 580,  1800, '#8b4500', 'white',   False),
    ('œ',  '/œ/', 'peur',  'mi-ouverte', 580,  1400, '#8b4500', 'white',   False),
    ('ɔ',  '/ɔ/', 'or',    'mi-ouverte', 560,   900, '#8b4500', 'white',   False),
    ('a',  '/a/', 'patte', 'ouverte',    800,  1300, '#6b0000', 'white',   False),
    ('ɑ',  '/ɑ/', 'pâte',  'ouverte',    750,   950, '#6b0000', 'white',   False),
]

# ─── Fonctions helpers ───────────────────────────────────────────

def circle(cx, cy, r, fill, stroke, sw=1.3, dasharray=None):
    d = f' stroke-dasharray="{dasharray}"' if dasharray else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

def text(x, y, content, size, fill, anchor='middle', weight='normal', style='normal'):
    attrs = f'text-anchor="{anchor}" font-size="{size}" fill="{fill}"'
    if weight != 'normal':
        attrs += f' font-weight="{weight}"'
    if style != 'normal':
        attrs += f' font-style="{style}"'
    return f'<text x="{x}" y="{y}" {attrs}>{content}</text>'

def line(x1, y1, x2, y2, stroke, sw=1.0, dasharray=None, opacity=None):
    d = f' stroke-dasharray="{dasharray}"' if dasharray else ''
    o = f' opacity="{opacity}"' if opacity else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'

def connector(x_line, y_line, cx, cy, stroke):
    """Trait pointillé de la ligne de référence vers le cercle."""
    return line(x_line, y_line, cx, cy, stroke, 0.7, '3,4', 0.5)

# ─── Construction SVG ────────────────────────────────────────────

def build_svg():
    lines = []
    a = lines.append

    a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
      f'font-family="Georgia,\'Times New Roman\',serif">')

    # Fond
    a(f'  <rect width="{W}" height="{H}" fill="#fafaf7"/>')

    # Titre
    a(f'  {text(550, 26, "POSITIONS FORMANTIQUES DES VOYELLES — ALPHABET PHONÉTIQUE INTERNATIONAL", 14, "#1a1a2e", weight="bold")}')
    # a(f'  {text(550, 42, "F1 et F2 sur axe fréquentiel linéaire · d\'après Meyer (2009), Giesler (1985)", 9.5, "#666", style="italic")}')
    a(f'  {text(550, 42, "F1 et F2 sur axe fréquentiel linéaire d’après Meyer (2009), Giesler (1985)", 9.5, "#666", style="italic")}')
    
    # Zone cluster (420–550 Hz)
    x_cl1 = f2_to_x(420)
    w_cl  = f2_to_x(550) - x_cl1
    a(f'  <rect x="{x_cl1:.0f}" y="54" width="{w_cl:.0f}" height="380" fill="#f5c542" fill-opacity="0.13"/>')
    x_cl_mid = round(x_cl1 + w_cl / 2)
    a(f'  {text(x_cl_mid, 51, "cluster 420–550 Hz", 7.5, "#b8860b", weight="bold")}')

    # Zones colorées F2 (antérieures / postérieures)
    a(f'  <rect x="274" y="150" width="569" height="76" rx="5" fill="#f5e8e8" fill-opacity="0.4"/>')
    a(f'  <rect x="146" y="316" width="185" height="76" rx="5" fill="#e8e8f5" fill-opacity="0.4"/>')

    # Axe F2 principal
    a(f'  {line(X0, Y0, X_MAX, Y0, "#333", 1.5)}')
    a(f'  <polygon points="{X_MAX+10},{Y0} {X_MAX},{Y0-5} {X_MAX},{Y0+5}" fill="#333"/>')
    a(f'  {text(X_MAX+16, Y0+4, "Hz", 10, "#444", anchor="start", style="italic")}')

    # Graduations axe F2
    a('  <g text-anchor="middle" font-size="9">')
    ticks = [(0, '0', '#444', 1.2), (500, '500', '#999', 0.8),
             (1000, '1k', '#444', 1.2), (1500, '1500', '#999', 0.8),
             (2000, '2k', '#444', 1.2), (2500, '2500', '#999', 0.8),
             (3000, '3k', '#444', 1.2)]
    for hz, label, col, sw in ticks:
        x = f2_to_x(hz)
        a(f'    {line(x, Y0-3, x, Y0+4, "#444", sw)}')
        a(f'    {text(x, Y0+15, label, 9, col)}')
    a('  </g>')

    # Grille verticale pointillée
    a('  <g stroke="#e0ddd4" stroke-width="0.7" stroke-dasharray="3,5">')
    for hz in [500, 1000, 1500, 2000, 2500, 3000]:
        x = f2_to_x(hz)
        a(f'    {line(x, 54, x, Y0-2, "#e0ddd4")}')
    a('  </g>')

    # Lignes de référence F2 et F1
    a(f'  {line(X0, F2_LINE_Y, 1050, F2_LINE_Y, "#cc9999", 0.8, "2,5")}')
    a(f'  {text(X0-8, F2_LINE_Y+4, "F2", 10, "#aa5555", anchor="end", weight="bold")}')
    a(f'  {text(X0+2, F2_LINE_Y-30, "antériorité →", 8, "#aa5555", anchor="start", style="italic")}')
    a(f'  {line(X0, F1_LINE_Y, 1050, F1_LINE_Y, "#9999cc", 0.8, "2,5")}')
    a(f'  {text(X0-8, F1_LINE_Y+4, "F1", 10, "#5555aa", anchor="end", weight="bold")}')
    a(f'  {text(X0+2, F1_LINE_Y-30, "hauteur →", 8, "#5555aa", anchor="start", style="italic")}')

    # ── Cercles F2 (rangée haute) ────────────────────────────────
    a('  <!-- F2 -->')
    for sym, f1, f2, col, bg, r, cluster in VOYELLES:
        cx, direction = POSITIONS_F2[sym]
        cx = round(cx)
        cy = F2_LINE_Y - 24 if direction == 'up' else F2_LINE_Y + 20
        # connecteur
        cx_conn = round(f2_to_x(f2))
        a(f'  {connector(cx_conn, F2_LINE_Y, cx, cy, col)}')
        # cercle
        sw = 2 if cluster else 1.3
        a(f'  {circle(cx, cy, r, bg, col, sw)}')
        # symbole
        a(f'  {text(cx, cy+5, sym, 13 if len(sym)==1 else 12, col, weight="bold")}')
        # fréquence
        a(f'  {text(cx, cy+r+9, str(f2), 6, "#888")}')

    # ── Cercles F1 (rangée basse) ────────────────────────────────
    a('  <!-- F1 -->')
    for sym, f1, f2, col, bg, r, cluster in VOYELLES:
        cx, direction = POSITIONS_F1[sym]
        cy = F1_LINE_Y - 24 if direction == 'up' else F1_LINE_Y + 20
        # connecteur depuis la ligne F1
        cx_f1 = round(X0 + (f1 / F2_MAX) * (X_MAX - X0))
        a(f'  {connector(cx_f1, F1_LINE_Y, cx, cy, col)}')
        # cercle
        sw = 2 if cluster else 1.3
        dash = '4,2' if sym == 'ɑ' else None
        a(f'  {circle(cx, cy, r, bg, col, sw, dash)}')
        # symbole
        a(f'  {text(cx, cy+5, sym, 13 if len(sym)==1 else 12, col, weight="bold")}')
        # fréquence
        a(f'  {text(cx, cy+r+9, str(f1), 6, "#888")}')

    # ── Séparateur légende ───────────────────────────────────────
    a(f'  {line(X0, 478, 1070, 478, "#ccc", 0.8)}')
    a(f'  {text(550, 491, "Correspondances IPA · exemples en français standard", 8.5, "#555", style="italic")}')

    # ── En-têtes catégories ──────────────────────────────────────
    cats = [
        (75,  504, 'white',   '#1a3a8b', 'Fermées'),
        (205, 504, '#fffbe6', '#b8860b', 'Mi-fermées (cluster)'),
        (370, 504, 'white',   '#2a7a2a', 'Mi-fermées'),
        (500, 504, 'white',   '#8b4500', 'Mi-ouvertes'),
        (630, 504, 'white',   '#6b0000', 'Ouvertes'),
    ]
    for cx, cy, bg, col, label in cats:
        a(f'  {circle(cx, cy, 5, bg, col, 1.2)}')
        a(f'  {text(cx+9, cy+4, label, 8, col, anchor="start")}')

    # ── Lignes de légende ────────────────────────────────────────
    def legend_row(x_base, y, sym, ipa, example, categorie, f1, f2, col, bg, cluster):
        sw = 1.2
        a(f'  {circle(x_base, y, 5, bg, col, sw)}')
        a(f'  {text(x_base, y+3, sym, 7, col)}')
        a(f'  {text(x_base+11, y+4, ipa, 8.5, "#222", anchor="start")}')
        a(f'  {text(x_base+37, y+4, f"« {example} »", 8.5, "#555", anchor="start", style="italic")}')
        a(f'  {text(x_base+100, y+4, f"— {categorie}  ·  F1 {f1} Hz · F2 {f2} Hz", 7.5, "#888", anchor="start")}')

    for i, row in enumerate(LEGEND_L):
        y = 519 + i * 17
        legend_row(80, y, *row)

    for i, row in enumerate(LEGEND_R):
        y = 519 + i * 17
        legend_row(580, y, *row)

    # Séparateur vertical légende
    a(f'  {line(555, 516, 555, 632, "#e0e0e0", 0.8)}')

    a('</svg>')
    return '\n'.join(lines)


# ─── Écriture ────────────────────────────────────────────────────

if __name__ == '__main__':
    svg = build_svg()
    os.makedirs(os.path.dirname(os.path.abspath(OUT_PATH)), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'✓ SVG écrit : {OUT_PATH}')
    print(f'  {len(svg)} caractères')
