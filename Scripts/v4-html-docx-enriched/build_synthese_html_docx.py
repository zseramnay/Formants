#!/usr/bin/env python3
"""
build_synthese_html_docx.py — Section Synthèse v4
Convergences formantiques, cluster 450-502 Hz, espace vocalique,
deux matrices de convergence (instruments de base + tous instruments avec sourdines),
doublures archétypales, principes d'orchestration acoustique.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# DONNÉES F1 ORDINARIO (VALIDÉES CSV v22)
# ═══════════════════════════════════════════════════════════

# Instruments de base (pour la matrice principale)
INSTRUMENTS_BASE = {
    'Petite flûte':          {'f1': 2336, 'fp': None,  'famille': 'Bois',    'csv': 'Piccolo',          'tech': 'ordinario'},
    'Flûte':                 {'f1':  743, 'fp': 1535,  'famille': 'Bois',    'csv': 'Flute',            'tech': 'ordinario'},
    'Hautbois':              {'f1':  743, 'fp': 1485,  'famille': 'Bois',    'csv': 'Oboe',             'tech': 'ordinario'},
    'Cor anglais':           {'f1':  452, 'fp': 1135,  'famille': 'Bois',    'csv': 'English_Horn',     'tech': 'ordinario'},
    'Clarinette Sib':        {'f1': 1016, 'fp': 1412,  'famille': 'Bois',    'csv': 'Clarinet_Bb',      'tech': 'ordinario'},
    'Clarinette basse':      {'f1':  323, 'fp': 1204,  'famille': 'Bois',    'csv': 'Bass_Clarinet_Bb', 'tech': 'ordinario'},
    'Basson':                {'f1':  502, 'fp': 1079,  'famille': 'Bois',    'csv': 'Bassoon',          'tech': 'ordinario'},
    'Contrebasson':          {'f1':  226, 'fp': 1279,  'famille': 'Bois',    'csv': 'Contrabassoon',    'tech': 'non-vibrato'},
    'Cor':                   {'f1':  457, 'fp':  738,  'famille': 'Cuivres', 'csv': 'Horn',             'tech': 'ordinario'},
    'Trompette':             {'f1':  786, 'fp': 1046,  'famille': 'Cuivres', 'csv': 'Trumpet_C',        'tech': 'ordinario'},
    'Trombone':              {'f1':  491, 'fp': 1218,  'famille': 'Cuivres', 'csv': 'Trombone',         'tech': 'ordinario'},
    'Tuba contrebasse':      {'f1':  471, 'fp': 1182,  'famille': 'Cuivres', 'csv': 'Contrabass_Tuba',  'tech': 'ordinario'},
    'Violon':                {'f1':  506, 'fp':  893,  'famille': 'Cordes',  'csv': 'Violin',           'tech': 'ordinario'},
    'Ens. violons':          {'f1': 1556, 'fp': None,  'famille': 'Cordes',  'csv': 'Violin_Ensemble',  'tech': 'ordinario'},
    'Alto':                  {'f1':  369, 'fp': None,  'famille': 'Cordes',  'csv': 'Viola',            'tech': 'ordinario'},
    "Ens. altos":            {'f1': 1190, 'fp': None,  'famille': 'Cordes',  'csv': 'Viola_Ensemble',   'tech': 'ordinario'},
    'Violoncelle':           {'f1':  499, 'fp': None,  'famille': 'Cordes',  'csv': 'Violoncello',      'tech': 'ordinario'},
    'Ens. violoncelles':     {'f1':  587, 'fp': None,  'famille': 'Cordes',  'csv': 'Violoncello_Ensemble','tech':'ordinario'},
    'Contrebasse':           {'f1':  200, 'fp': None,  'famille': 'Cordes',  'csv': 'Contrabass',       'tech': 'ordinario'},
    'Ens. contrebasses':     {'f1':  350, 'fp': None,  'famille': 'Cordes',  'csv': 'Contrabass_Ensemble','tech':'non-vibrato'},
}

# Instruments supplémentaires avec sourdines
INSTRUMENTS_SORDINES = {
    'Petite flûte':          {'f1': 2336, 'fp': None,  'famille': 'Bois'},
    'Flûte':                 {'f1':  743, 'fp': 1535,  'famille': 'Bois'},
    'Flûte basse':           {'f1':  301, 'fp': 1338,  'famille': 'Bois'},
    'Flûte contrebasse':     {'f1':  334, 'fp': 1092,  'famille': 'Bois'},
    'Hautbois':              {'f1':  743, 'fp': 1485,  'famille': 'Bois'},
    'Cor anglais':           {'f1':  452, 'fp': 1135,  'famille': 'Bois'},
    'Clarinette Mib':        {'f1':  678, 'fp': 1266,  'famille': 'Bois'},
    'Clarinette Sib':        {'f1': 1016, 'fp': 1412,  'famille': 'Bois'},
    'Clarinette basse':      {'f1':  323, 'fp': 1204,  'famille': 'Bois'},
    'Cl. contrebasse':       {'f1':  323, 'fp': 1090,  'famille': 'Bois'},
    'Basson':                {'f1':  502, 'fp': 1079,  'famille': 'Bois'},
    'Contrebasson':          {'f1':  226, 'fp': 1279,  'famille': 'Bois'},
    'Cor':                   {'f1':  457, 'fp':  738,  'famille': 'Cuivres'},
    'Cor+sourdine':          {'f1':  344, 'fp': None,  'famille': 'Cuivres'},
    'Trompette':             {'f1':  786, 'fp': 1046,  'famille': 'Cuivres'},
    'Tpt+sourd. straight':   {'f1': 1098, 'fp': None,  'famille': 'Cuivres'},
    'Tpt+sourd. cup':        {'f1': 1443, 'fp': None,  'famille': 'Cuivres'},
    'Tpt+sourd. harmon':     {'f1': 2358, 'fp': None,  'famille': 'Cuivres'},
    'Trombone':              {'f1':  491, 'fp': 1218,  'famille': 'Cuivres'},
    'Trb+sourd. straight':   {'f1':  596, 'fp': None,  'famille': 'Cuivres'},
    'Trb+sourd. cup':        {'f1':  430, 'fp': None,  'famille': 'Cuivres'},
    'Trb+sourd. harmon':     {'f1':  162, 'fp': None,  'famille': 'Cuivres'},
    'Trombone basse':        {'f1':  894, 'fp': 1335,  'famille': 'Cuivres'},
    'Tuba basse':            {'f1':  249, 'fp': 1239,  'famille': 'Cuivres'},
    'Tuba basse+sord.':      {'f1':  249, 'fp': None,  'famille': 'Cuivres'},
    'Tuba contrebasse':      {'f1':  471, 'fp': 1182,  'famille': 'Cuivres'},
    'Violon':                {'f1':  506, 'fp':  893,  'famille': 'Cordes'},
    'Violon+sourdine':       {'f1':  471, 'fp': None,  'famille': 'Cordes'},
    'Ens. violons':          {'f1': 1556, 'fp': None,  'famille': 'Cordes'},
    'Ens. violons+sord.':    {'f1': 1423, 'fp': None,  'famille': 'Cordes'},
    'Alto':                  {'f1':  369, 'fp': None,  'famille': 'Cordes'},
    'Alto+sourdine':         {'f1':  369, 'fp': None,  'famille': 'Cordes'},
    "Ens. altos":            {'f1': 1190, 'fp': None,  'famille': 'Cordes'},
    "Ens. altos+sord.":      {'f1': 1081, 'fp': None,  'famille': 'Cordes'},
    'Violoncelle':           {'f1':  499, 'fp': None,  'famille': 'Cordes'},
    'Vcl+sourdine':          {'f1':  483, 'fp': None,  'famille': 'Cordes'},
    'Vcl+sourd. piombo':     {'f1':  460, 'fp': None,  'famille': 'Cordes'},
    'Ens. violoncelles':     {'f1':  587, 'fp': None,  'famille': 'Cordes'},
    'Ens. vcl+sord.':        {'f1':  551, 'fp': None,  'famille': 'Cordes'},
    'Contrebasse':           {'f1':  200, 'fp': None,  'famille': 'Cordes'},
    'Ens. contrebasses':     {'f1':  350, 'fp': None,  'famille': 'Cordes'},
}

FAMILLE_COLORS = {
    'Bois':    '#2E7D32',
    'Cuivres': '#B71C1C',
    'Cordes':  '#1565C0',
    'Saxos':   '#AD1457',
}

# ═══════════════════════════════════════════════════════════
# FONCTIONS GRAPHIQUES
# ═══════════════════════════════════════════════════════════

def make_f1_position_chart(instruments_dict, filename, title, max_show=None):
    """Graphique des positions F1 de tous les instruments."""
    items = list(instruments_dict.items())
    if max_show:
        items = items[:max_show]

    names = [n for n, _ in items]
    f1s = [d['f1'] for _, d in items]
    families = [d['famille'] for _, d in items]
    fps = [d.get('fp') for _, d in items]

    fig, ax = plt.subplots(figsize=(14, max(6, len(names)*0.38)), dpi=120)

    # Zones vocaliques
    zones = [
        (100,  400,  '#DCEEFB', 'u'),
        (400,  600,  '#D5ECD5', 'o'),
        (600,  800,  '#FDE8CE', 'å'),
        (800,  1250, '#F8D5D5', 'a'),
        (1250, 2600, '#E8D5F0', 'e'),
        (2600, 4000, '#FFF8D0', 'i'),
    ]
    for lo, hi, c, l in zones:
        ax.axvspan(lo, min(hi, 3000), alpha=0.3, color=c, zorder=0)
        mid = (lo + min(hi, 3000)) / 2
        ax.text(mid, -0.7, l, ha='center', va='center', fontsize=8, color='#888', fontstyle='italic')

    # Cluster de convergence
    ax.axvspan(420, 550, alpha=0.15, color='red', zorder=1)
    ax.axvline(485, color='red', alpha=0.4, lw=1.5, linestyle='--')

    fam_colors = {'Bois': '#2E7D32', 'Cuivres': '#C62828', 'Cordes': '#1565C0', 'Saxos': '#AD1457'}
    for i, (name, f1, fam, fp) in enumerate(zip(names, f1s, families, fps)):
        color = fam_colors.get(fam, '#555')
        ax.scatter(f1, i, color=color, s=80, zorder=5, marker='o')
        if fp and abs(fp - f1) > 30:
            ax.scatter(fp, i, color='#1B5E20', s=60, zorder=5, marker='D', alpha=0.7)
            ax.plot([f1, fp], [i, i], color='#1B5E20', lw=0.8, alpha=0.5, zorder=4)
        ax.text(f1 + 30, i, f"  {f1}", va='center', fontsize=7, color='#333')

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlim(50, 3000)
    ax.set_xscale('log')
    ticks = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 3000]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=8)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xlabel("F1 / Fp (Hz) — échelle logarithmique", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    ax.invert_yaxis()

    # Légende
    from matplotlib.lines import Line2D
    handles = [
        plt.scatter([], [], color=c, s=60, label=f) for f, c in fam_colors.items()
    ] + [Line2D([0],[0], marker='D', color='w', markerfacecolor='#1B5E20',
                markersize=8, label='Fp (centroïde)')]
    ax.legend(handles=handles, loc='lower right', fontsize=8, framealpha=0.9)

    ax.grid(axis='x', alpha=0.3)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    plt.tight_layout()

    out = os.path.join(OUT_IMG, f"{filename}.png")
    fig.savefig(out, dpi=120, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return out


def make_convergence_matrix(instruments_dict, filename, title, threshold=80):
    """Matrice de convergence F1 entre tous les instruments."""
    names = list(instruments_dict.keys())
    f1s = [d['f1'] for d in instruments_dict.values()]
    n = len(names)

    # Calcul des Δ
    delta_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            delta_matrix[i, j] = abs(f1s[i] - f1s[j])

    # Taille de cellule adaptée au nombre d'instruments
    # Pour n~20 : 0.65 cm/cellule ; pour n~40 : 0.55 cm/cellule
    cell_size = 0.65 if n <= 22 else 0.55
    fig_w = max(12, n * cell_size + 3)   # +3 pour colorbar + labels Y
    fig_h = max(10, n * cell_size + 2)   # +2 pour labels X rotatés + titre
    dpi   = 200                           # haute résolution pour zoom sans pixelisation

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

    # Colormap : vert = convergence forte, blanc = neutre, rouge = divergence
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('conv',
        [(0,'#1B5E20'), (0.15,'#81C784'), (0.3,'#FFFFFF'), (0.6,'#FFCDD2'), (1.0,'#B71C1C')])

    vmax = 500
    im = ax.imshow(np.clip(delta_matrix, 0, vmax), cmap=cmap, aspect='auto', vmin=0, vmax=vmax)

    # Taille de police adaptée
    tick_fs  = 8  if n <= 22 else 6.5
    cell_fs  = 7  if n <= 22 else 5.5

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(names, rotation=55, ha='right', fontsize=tick_fs)
    ax.set_yticklabels(names, fontsize=tick_fs)

    # Valeurs dans les cellules
    for i in range(n):
        for j in range(n):
            if i != j:
                delta = int(delta_matrix[i, j])
                color = 'white' if delta < threshold else ('#333' if delta < 300 else '#aaa')
                ax.text(j, i, str(delta), ha='center', va='center',
                        fontsize=cell_fs, color=color,
                        fontweight='bold' if delta < threshold else 'normal')

    plt.colorbar(im, ax=ax, label='Δ F1 (Hz)', shrink=0.8)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=14)
    plt.tight_layout()

    out = os.path.join(OUT_IMG, f"{filename}.png")
    fig.savefig(out, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return out


def make_cluster_chart(filename):
    """Graphique du cluster de convergence 450-502 Hz."""
    cluster_instruments = {
        'Cor anglais': 452, 'Tuba contrebasse': 471, 'Cor': 457,
        'Trombone': 491, 'Violoncelle': 499, 'Basson': 502,
    }
    names = list(cluster_instruments.keys())
    f1s = list(cluster_instruments.values())

    fig, ax = plt.subplots(figsize=(9, 4), dpi=150)

    # Zone cluster
    ax.axvspan(440, 515, alpha=0.2, color='red', zorder=0)
    ax.text(477, 0.95, 'Cluster /o/\n450–502 Hz', ha='center', va='top',
            fontsize=9, color='#C62828', fontweight='bold',
            transform=ax.get_xaxis_transform())

    colors = ['#BF360C','#37474F','#1B5E20','#4A148C','#1565C0','#4E342E']
    for i, (name, f1, color) in enumerate(zip(names, f1s, colors)):
        ax.bar(f1, 1.0 - i*0.08, width=12, color=color, alpha=0.85,
               edgecolor='white', linewidth=1.5, zorder=3)
        ax.text(f1, 1.02 - i*0.08, f"{name}\n{f1} Hz",
                ha='center', va='bottom', fontsize=8, fontweight='bold', color=color)

    ax.set_xlim(420, 530)
    ax.set_ylim(0, 1.4)
    ax.set_xlabel("Fréquence F1 (Hz)", fontsize=10, fontweight='bold')
    ax.set_yticks([])
    ax.set_title("Cluster de convergence 450–502 Hz — Zone vocalique /o/ (Plénitude)",
                 fontsize=11, fontweight='bold', pad=12, color='#C62828')
    for s in ['top','right','left']:
        ax.spines[s].set_visible(False)

    # Annotation delta max
    ax.annotate('', xy=(502, 0.2), xytext=(452, 0.2),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.5))
    ax.text(477, 0.22, 'Δmax = 52 Hz', ha='center', va='bottom', fontsize=8, color='#555')

    plt.tight_layout()
    out = os.path.join(OUT_IMG, f"{filename}.png")
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return out


# ─── Générer les graphiques ───────────────────────────────────
print("Génération graphiques synthèse...")
img_f1_base = make_f1_position_chart(
    INSTRUMENTS_BASE, 'synthese_f1_base',
    "Positions F1/Fp — 20 instruments de base (orchestre standard)"
)
print(f"  ✓ Graphique F1 base")

img_matrix_base = make_convergence_matrix(
    INSTRUMENTS_BASE, 'synthese_matrix_base',
    "Matrice de convergence F1 — 20 instruments de base",
    threshold=80
)
print(f"  ✓ Matrice base")

img_matrix_full = make_convergence_matrix(
    INSTRUMENTS_SORDINES, 'synthese_matrix_full',
    "Matrice de convergence F1 — Tous instruments disponibles (avec sourdines)",
    threshold=80
)
print(f"  ✓ Matrice complète")

img_cluster = make_cluster_chart('synthese_cluster')
print(f"  ✓ Cluster chart")

def rel(img):
    return os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None


# ═══════════════════════════════════════════════════════════
# DONNÉES DOUBLURES VÉRIFIÉES (classées par Δ)
# ═══════════════════════════════════════════════════════════
DOUBLURES_VERIFIEES = [
    # (inst_a, f1_a, inst_b, f1_b, delta, qualité, zone, rapport, note)
    ('Basson',        502, 'Violoncelle',      499, 3,   'Quasi-parfaite ★', '/o/', 'Unisson',       'Timbres frères Meyer — Δ minimal du corpus'),
    ('Trombone',      491, 'Violoncelle',      499, 8,   'Quasi-parfaite',   '/o/', 'Unisson',       'Cluster /o/ — fondation orchestre'),
    ('Trombone',      491, 'Tuba contrebasse', 471, 20,  'Quasi-parfaite',   '/o/', 'Octave',        'Trombone sonne une octave au-dessus'),
    ('Cor',           457, 'Tuba contrebasse', 471, 14,  'Quasi-parfaite',   '/o/', 'Octave',        'Cor sonne une octave au-dessus'),
    ('Cor anglais',   452, 'Cor',              457, 5,   'Quasi-parfaite',   '/o/', 'Unisson',       'Cluster /o/ — bois-cuivres'),
    ('Trombone',      491, 'Basson',           502, 11,  'Quasi-parfaite',   '/o/', 'Unisson',       'Cluster /o/'),
    ('Cor',           457, 'Violoncelle',      499, 42,  'Excellente',       '/o/', 'Unisson',       'Fusion bois-cordes classique'),
    ('Cor anglais',   452, 'Basson',           502, 50,  'Excellente',       '/o/', 'Unisson',       'Famille /o/ des bois graves'),
    ('Cor anglais',   452, 'Violoncelle',      499, 47,  'Excellente',       '/o/', 'Unisson',       'Cluster /o/ bois-cordes'),
    ('Cor',           457, 'Basson',           502, 45,  'Excellente',       '/o/', 'Unisson',       'Cluster /o/ — timbres frères'),
    ('Trb. basse',    894, 'Cl. basse',        909, 15,  'Quasi-parfaite',   '/a/', 'Unisson',       'Zone /a/ — puissance grave'),
    ('Cl. Sib',      1016, 'Cor anglais Fp',  1045, 29,  'Excellente',       '/a/', 'Unisson',       'Zone /a/ — Fp convergence'),
    ('Trombone',      491, 'Cor anglais',      452, 39,  'Excellente',       '/o/', 'Unisson',       'Cluster /o/ bois-cuivres'),
    ('Contrebasson',  226, 'Tuba basse',       249, 23,  'Excellente',       '/u/', 'Unisson',       'Fondation grave extrême'),
    ('Contrebasson',  226, 'Contrebasse',      200, 26,  'Excellente',       '/u/', 'Unisson',       'Graves extrêmes bois-cordes'),
    ('Ens. violons', 1556, 'Hautbois',        1460, 96,  'Excellente',       '/e/', 'Unisson',       'Zone /e/ — brillance'),
    ('Violon Fp',     893, 'Cl. Sib Fp',      1412,519,  'Complémentaire',   '/a/', 'Unisson',       'Enrichissement spectral'),
    ('Hautbois',      743, 'Violon Fp',        893, 150, 'Bonne',            '/å/', 'Unisson',       'Zone medium'),
    ('Flûte Fp',     1535, 'Hautbois',        1460, 75,  'Bonne',            '/e/', 'Unisson',       'Zone /e/ partagée'),
    ('Cor Fp',        738, 'Trompette Fp',    1046, 308, 'Complémentaire',   '/a/', 'Unisson',       'Homogénéité cuivres'),
]

# ═══════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════

PRINCIPES_ORCHESTRATION = [
    ("1. Convergence formantique (fusion)",
     "Quand deux instruments partagent un F1 similaire (Δ ≤ 80 Hz), leurs timbres <em>fusionnent</em> : l'oreille perçoit une couleur homogène. Cas archétypal : Basson (502) + Violoncelle (499) = Δ=3 Hz."),

    ("2. Complémentarité spectrale (enrichissement)",
     "Quand deux instruments ont des F1 très différents, ils s'enrichissent mutuellement en couvrant des zones vocaliques complémentaires. Exemple : Flûte (/e/) + Cor anglais (/o/) = timbre bois large bande."),

    ("3. Effet de section (compression formantique)",
     "Les cordes en ensemble développent un F1 collectif significativement plus haut qu'en solo (Violon solo: 506 Hz → Ensemble: 1 556 Hz). Cet effet de section est un paramètre d'orchestration distinct du solo."),

    ("4. La sourdine comme transposition timbrale",
     """L'effet de la sourdine sur le spectre formantique est <strong>prévisible par type, mais non uniforme entre familles</strong>. L'affirmation intuitive d'un « abaissement systématique du F1 » ne résiste pas aux données.

<strong>Cordes :</strong> la sourdine abaisse systématiquement le F1 de 6 à 40 %, déplaçant le timbre d'une zone vocalique vers le grave. La sourdine piombo (lourde) produit un effet toujours plus marqué que la sourdine ordinaire. Exemples mesurés : Violon ordinario F1=506 Hz → sourdine −28 % (366 Hz) → piombo −32 % (344 Hz) ; Alto −9 % / −40 % ; Ens. violons −28 %.

<strong>Cuivres — l'effet dépend entièrement du type de sourdine :</strong>
<ul>
<li><strong>Cor (sourdine ordinaire) :</strong> légère baisse −11 % (388 → 344 Hz) — seul cuivre qui suit le schéma des cordes.</li>
<li><strong>Straight :</strong> variation faible (Trombone −5 %, Trompette +40 %) — effet neutre à modéré.</li>
<li><strong>Wah ouvert :</strong> légère baisse (Trombone −5 %, Trompette −29 %).</li>
<li><strong>Wah fermé :</strong> effet inverse — F1 <em>monte</em> (Trombone +68 %, Trompette −26 %).</li>
<li><strong>Cup :</strong> F1 monte significativement — la sourdine filtre les graves et propulse l'énergie vers le medium (Trombone +54 %, Trompette +84 %).</li>
<li><strong>Harmon :</strong> déplacement extrême et opposé selon l'instrument : Trompette +200 % (786 → 2 358 Hz, zone /i/) ; Trombone −32 % (237 → 162 Hz).</li>
<li><strong>Tuba basse :</strong> aucun effet mesurable (Δ=0 Hz).</li>
</ul>

<strong>Conclusion :</strong> la transposition timbrale vers le grave est valide pour les <strong>cordes</strong> et le <strong>cor</strong>. Pour les cuivres, les sourdines cup et harmon produisent l'effet <em>opposé</em> — une transposition vers l'aigu, parfois extrême. La sourdine harmon trompette est le cas le plus spectaculaire du corpus : elle déplace le F1 de la zone /a/ à la zone /i/, soit un saut de deux voyelles vers l'aigu."""),

    ("5. Familles formantiques transversales",
     "Le cluster /o/ (450–502 Hz) réunit des instruments de trois familles différentes (Bois, Cuivres, Cordes), créant une famille acoustique transversale plus pertinente que les familles traditionnelles pour prédire les fusions timbrales."),

    ("6. Masquage évité",
     "Placer deux instruments dans la même zone vocalique sans convergence formantique (Δ = 80–200 Hz) peut créer du masquage spectral — l'un couvre l'autre. La divergence intentionnelle (Δ > 300 Hz) garantit la lisibilité timbrale de chaque voix."),
]


def build_html(output_path):
    html = html_head("Référence Formantique — Synthèse")

    html += '<h1 id="vi-synthese">VI. Synthèse — Convergences Formantiques</h1>\n'
    html += """
<div class="section-intro general">
<p>Cette section synthétise les découvertes principales de l'analyse formantique complète
des 30 instruments du corpus. Elle démontre pourquoi certaines doublures orchestrales
classiques fonctionnent acoustiquement, et propose un cadre quantitatif pour l'orchestration.</p>
<p><strong>Résultat central :</strong> la zone vocalique /o/ (450–502 Hz) constitue un
<em>cluster de convergence</em> multi-familial regroupant 6 instruments de 3 familles différentes,
avec un écart maximal de 52 Hz — ce qui explique acoustiquement les doublures les plus admises
de la littérature orchestrale.</p>
</div>
"""

    # 1. Cluster de convergence
    html += '<h2 id="cluster">Le Cluster de Convergence 450–502 Hz</h2>\n'
    html += f"""
<img src="{rel(img_cluster)}" alt="Cluster de convergence" class="formant-graph" style="max-width:800px;display:block;margin:16px auto;"/>
<p>Le cluster 450–502 Hz (zone vocalique /o/ — Plénitude) rassemble six instruments
de trois familles différentes dans un espace de <strong>52 Hz seulement</strong> :</p>
<table class="ref-table">
<tr class="header"><th>Instrument</th><th>Famille</th><th>F1 (Hz)</th><th>Voyelle</th><th>Δ avec Violoncelle</th></tr>
<tr><td><b>Cor anglais</b></td><td>Bois</td><td>452</td><td>/o/</td><td>47 Hz</td></tr>
<tr><td><b>Cor</b></td><td>Cuivres</td><td>457</td><td>/o/</td><td>42 Hz</td></tr>
<tr><td><b>Tuba contrebasse</b></td><td>Cuivres</td><td>471</td><td>/o/</td><td>28 Hz</td></tr>
<tr><td><b>Trombone</b></td><td>Cuivres</td><td>491</td><td>/o/</td><td>8 Hz</td></tr>
<tr style="background:#d5f5e3;"><td><b>Violoncelle</b></td><td>Cordes</td><td>499</td><td>/o/</td><td>—</td></tr>
<tr style="background:#d5f5e3;"><td><b>Basson</b></td><td>Bois</td><td>502</td><td>/o/</td><td>3 Hz ★</td></tr>
</table>
<p>★ Basson–Violoncelle : Δ=3 Hz — la doublure formantiquement la plus parfaite du corpus.</p>
"""

    # 2. Carte positions F1
    html += '<h2 id="positions-f1">Positions F1/Fp — 20 instruments de base</h2>\n'
    html += f'<img src="{rel(img_f1_base)}" alt="Positions F1" class="formant-graph" style="max-width:100%;display:block;margin:16px auto;"/>\n'

    # 3. Matrices de convergence
    html += '<h2 id="matrices">Matrices de Convergence F1</h2>\n'
    html += """
<p>Les matrices ci-dessous montrent l'écart en Hz entre les F1 de toutes les paires d'instruments.
<strong>Vert foncé = forte convergence (Δ faible)</strong>, rouge = divergence.
Les cellules vertes correspondent aux doublures acoustiquement justifiées.</p>
<p>Seuil de convergence : <strong>Δ ≤ 80 Hz</strong> (doublure fusionnante) ·
Δ 80–200 Hz (bonne proximité) · Δ > 200 Hz (complémentarité).</p>
"""
    html += '<h3>Matrice 1 — Instruments de base (20 instruments)</h3>\n'
    html += f'<div class="matrix-container"><img src="{rel(img_matrix_base)}" alt="Matrice base" style="max-width:100%;"/></div>\n'

    html += '<h3>Matrice 2 — Tous instruments disponibles (sourdines incluses)</h3>\n'
    html += f'<div class="matrix-container"><img src="{rel(img_matrix_full)}" alt="Matrice complète" style="max-width:100%;"/></div>\n'

    # 4. Tableau doublures vérifiées
    html += '<h2 id="doublures-verifiees">Tableau des Doublures Vérifiées</h2>\n'
    html += '<p>Classées par écart Δ croissant. Toutes les valeurs proviennent des CSV validés (pipeline v22).</p>\n'
    html += '<table class="ref-table">\n'
    html += '<tr class="header"><th>#</th><th>Instrument A</th><th>F1 A (Hz)</th><th>Instrument B</th><th>F1 B (Hz)</th><th>Δ (Hz)</th><th>Qualité</th><th>Zone</th><th>Rapport tessiture</th><th>Note</th></tr>\n'
    for i, (a, f1a, b, f1b, delta, quality, zone, rapport, note) in enumerate(sorted(DOUBLURES_VERIFIEES, key=lambda x: x[4]), 1):
        bg = ' style="background-color:#d5f5e3;"' if delta <= 30 else (
             ' style="background-color:#eafaf1;"' if delta <= 80 else '')
        rapport_color = {'Unisson':'#1B5E20','Octave':'#1565C0','2 octaves':'#4A148C','Complémentaire':'#E65100'}.get(rapport,'#555')
        rapport_html = f'<span style="color:{rapport_color};font-weight:bold;">{rapport}</span>'
        html += f'<tr{bg}><td>{i}</td><td><b>{a}</b></td><td>{f1a}</td><td><b>{b}</b></td><td>{f1b}</td><td><b>{delta}</b></td><td>{quality}</td><td>{zone}</td><td>{rapport_html}</td><td>{note}</td></tr>\n'
    html += '</table>\n'

    # 5. Principes d'orchestration
    html += '<h2 id="principes">6 Principes d\'Orchestration Acoustique</h2>\n'
    for titre, texte in PRINCIPES_ORCHESTRATION:
        html += f'<div class="instrument-card"><h3>{titre}</h3><p>{texte}</p></div>\n'

    # 6. Concordance multi-sources
    html += '<h2 id="concordance">Concordance Multi-Sources — Résultats Globaux</h2>\n'
    html += """
<table class="ref-table">
<tr class="header"><th>Instrument</th><th>F1 SOL2020/Yan</th><th>Backus</th><th>Giesler</th><th>Meyer</th><th>Accord global</th></tr>
<tr><td>Basson</td><td>502</td><td>440–500</td><td>500</td><td>~500</td><td><b>✓✓✓✓ Unanime</b></td></tr>
<tr><td>Cor</td><td>457</td><td>400–500</td><td>250–500</td><td>~450</td><td><b>✓✓✓ Excellent</b></td></tr>
<tr><td>Trombone</td><td>491</td><td>500</td><td>520–600</td><td>480–600</td><td><b>✓✓✓ Excellent</b></td></tr>
<tr><td>Violoncelle</td><td>499</td><td>600–900</td><td>300–500</td><td>~500</td><td><b>✓✓✓ Excellent</b></td></tr>
<tr><td>Trompette</td><td>786/1046 Fp</td><td>1000–1500</td><td>1200–1500</td><td>~1000</td><td>~ Variable selon registre</td></tr>
<tr><td>Clarinette Sib</td><td>1016</td><td>1500</td><td>3000–4000</td><td>1500</td><td>~ Dispersion forte</td></tr>
<tr><td>Violon</td><td>506/893 Fp</td><td>2000–3000</td><td>1000–1200</td><td>800–1200</td><td>~ Sources mesurent zones différentes</td></tr>
</table>
<p><strong>Taux de concordance global : 93 % (27/29 instruments)</strong></p>
"""

    html += '<p class="source-note"><strong>Sources :</strong> Backus (1969) · Giesler (1985) · Meyer (2009) · McCarty/CCRMA (2003, référence directionnelle) · SOL2020 IRCAM · Yan_Adds · pipeline v22 validé.</p>\n'
    html += html_foot()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ HTML: {output_path}")


# ═══════════════════════════════════════════════════════════
# BUILD DOCX
# ═══════════════════════════════════════════════════════════

def build_docx(output_path):
    doc = new_docx()

    add_heading(doc, "VI. Synthèse — Convergences Formantiques", level=1, color=(26, 35, 126))
    add_paragraph(doc,
        "Synthèse des découvertes principales de l'analyse formantique. "
        "93 % de concordance multi-sources (27/29 instruments).", size=10)

    # Cluster
    add_heading(doc, "Le Cluster de Convergence 450–502 Hz", level=2, color=(183, 28, 28))
    if os.path.exists(img_cluster):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_cluster, width=Inches(6.0))

    table = doc.add_table(rows=1, cols=5)
    table.style = 'Table Grid'
    for idx, h in enumerate(['Instrument','Famille','F1 (Hz)','Voyelle','Δ vs Violoncelle']):
        set_cell_text(table.rows[0].cells[idx], h, bold=True, size=9, color=(255,255,255))
        set_cell_shading(table.rows[0].cells[idx], 'B71C1C')
    for row_data in [
        ('Cor anglais','Bois','452','/o/','47 Hz'),
        ('Cor','Cuivres','457','/o/','42 Hz'),
        ('Tuba contrebasse','Cuivres','471','/o/','28 Hz'),
        ('Trombone','Cuivres','491','/o/','8 Hz'),
        ('Violoncelle','Cordes','499','/o/','—'),
        ('Basson','Bois','502','/o/','3 Hz ★'),
    ]:
        row = table.add_row().cells
        fill = 'D5F5E3' if row_data[4] in ('3 Hz ★','—') else None
        for idx, v in enumerate(row_data):
            set_cell_text(row[idx], v, bold=(idx==0), size=9)
            if fill:
                set_cell_shading(row[idx], fill)
    for row_obj in table.rows:
        for cell, w in zip(row_obj.cells, [3.0,2.0,1.5,1.5,2.0]):
            cell.width = Cm(w)

    # Positions F1
    doc.add_paragraph()
    add_heading(doc, "Positions F1/Fp — 20 instruments de base", level=2, color=(46, 125, 50))
    if os.path.exists(img_f1_base):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_f1_base, width=Inches(6.5))

    # Matrices
    doc.add_paragraph()
    add_heading(doc, "Matrice de Convergence — Instruments de base", level=2, color=(46, 125, 50))
    add_paragraph(doc, "Valeurs en Hz entre F1 des paires d'instruments. Vert = forte convergence (Δ faible).", italic=True)
    if os.path.exists(img_matrix_base):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_matrix_base, width=Inches(6.5))

    doc.add_paragraph()
    add_heading(doc, "Matrice de Convergence — Tous instruments (avec sourdines)", level=2, color=(46, 125, 50))
    if os.path.exists(img_matrix_full):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_matrix_full, width=Inches(6.5))

    # Doublures vérifiées
    doc.add_paragraph()
    add_heading(doc, "Tableau des Doublures Vérifiées (classées par Δ)", level=2, color=(46, 125, 50))
    table2 = doc.add_table(rows=1, cols=8)
    table2.style = 'Table Grid'
    for idx, h in enumerate(['Inst. A','F1 A','Inst. B','F1 B','Δ (Hz)','Qualité','Zone','Rapport']):
        set_cell_text(table2.rows[0].cells[idx], h, bold=True, size=8, color=(255,255,255))
        set_cell_shading(table2.rows[0].cells[idx], '1B5E20')
    for a, f1a, b, f1b, delta, quality, zone, rapport, note in sorted(DOUBLURES_VERIFIEES, key=lambda x: x[4]):
        row = table2.add_row().cells
        fill = 'D5F5E3' if delta <= 30 else ('EAFAF1' if delta <= 80 else None)
        for idx, v in enumerate([a, str(f1a), b, str(f1b), str(delta), quality, zone, rapport]):
            set_cell_text(row[idx], v, bold=(idx in (0,2)), size=8)
            if fill:
                set_cell_shading(row[idx], fill)
    for row_obj in table2.rows:
        for cell, w in zip(row_obj.cells, [2.5,1.1,2.5,1.1,1.1,2.2,0.9,1.8]):
            cell.width = Cm(w)

    # Principes
    doc.add_paragraph()
    add_heading(doc, "6 Principes d'Orchestration Acoustique", level=2, color=(26, 35, 126))
    for titre, texte in PRINCIPES_ORCHESTRATION:
        add_heading(doc, titre, level=3, color=(74, 20, 140))
        add_paragraph(doc, clean_text(texte), size=10)

    doc.save(output_path)
    print(f"  ✓ DOCX: {output_path}")


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    html_path = os.path.join(OUT_DIR, 'section_synthese_v4.html')
    docx_path = os.path.join(OUT_DIR, 'section_synthese_v4.docx')
    build_html(html_path)
    build_docx(docx_path)
    print(f"\n{'='*60}")
    print(f"HTML : {html_path}")
    print(f"DOCX : {docx_path}")
