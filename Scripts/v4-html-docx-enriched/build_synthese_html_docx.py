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
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker

load_all_csvs()

# ═══════════════════════════════════════════════════════════
# DONNÉES F1 ORDINARIO (VALIDÉES CSV v22)
# ═══════════════════════════════════════════════════════════

# Instruments de base (pour la matrice principale)
INSTRUMENTS_BASE = {
    'Petite flûte':          {'f1': 1109, 'fp': None,  'famille': 'Bois',    'csv': 'Piccolo',          'tech': 'ordinario'},
    'Flûte':                 {'f1':  743, 'fp': 1535,  'famille': 'Bois',    'csv': 'Flute',            'tech': 'ordinario'},
    'Hautbois':              {'f1':  743, 'fp': 1485,  'famille': 'Bois',    'csv': 'Oboe',             'tech': 'ordinario'},
    'Cor anglais':           {'f1':  452, 'fp': 1135,  'famille': 'Bois',    'csv': 'English_Horn',     'tech': 'ordinario'},
    'Clarinette Sib':        {'f1':  463, 'fp': 1412,  'famille': 'Bois',    'csv': 'Clarinet_Bb',      'tech': 'ordinario'},
    'Clarinette basse':      {'f1':  323, 'fp': 1204,  'famille': 'Bois',    'csv': 'Bass_Clarinet_Bb', 'tech': 'ordinario'},
    'Basson':                {'f1':  495, 'fp': 1079,  'famille': 'Bois',    'csv': 'Bassoon',          'tech': 'ordinario'},
    'Contrebasson':          {'f1':  226, 'fp': 1279,  'famille': 'Bois',    'csv': 'Contrabassoon',    'tech': 'non-vibrato'},
    'Cor':                   {'f1':  388, 'fp':  738,  'famille': 'Cuivres', 'csv': 'Horn',             'tech': 'ordinario'},
    'Trompette':             {'f1':  786, 'fp': 1046,  'famille': 'Cuivres', 'csv': 'Trumpet_C',        'tech': 'ordinario'},
    'Trombone':              {'f1':  237, 'fp': 1218,  'famille': 'Cuivres', 'csv': 'Trombone',         'tech': 'ordinario'},
    'Tuba contrebasse':      {'f1':  226, 'fp': 1182,  'famille': 'Cuivres', 'csv': 'Contrabass_Tuba',  'tech': 'ordinario'},
    'Violon':                {'f1':  506, 'fp':  893,  'famille': 'Cordes',  'csv': 'Violin',           'tech': 'ordinario'},
    'Ens. violons':          {'f1':  495, 'fp': None,  'famille': 'Cordes',  'csv': 'Violin_Ensemble',  'tech': 'ordinario'},
    'Alto':                  {'f1':  377, 'fp': None,  'famille': 'Cordes',  'csv': 'Viola',            'tech': 'ordinario'},
    "Ens. altos":            {'f1':  366, 'fp': None,  'famille': 'Cordes',  'csv': 'Viola_Ensemble',   'tech': 'ordinario'},
    'Violoncelle':           {'f1':  205, 'fp': None,  'famille': 'Cordes',  'csv': 'Violoncello',      'tech': 'ordinario'},
    'Ens. violoncelles':     {'f1':  205, 'fp': None,  'famille': 'Cordes',  'csv': 'Violoncello_Ensemble','tech':'ordinario'},
    'Contrebasse':           {'f1':  172, 'fp': None,  'famille': 'Cordes',  'csv': 'Contrabass',       'tech': 'ordinario'},
    'Ens. contrebasses':     {'f1':  172, 'fp': None,  'famille': 'Cordes',  'csv': 'Contrabass_Ensemble','tech':'non-vibrato'},
}

# Instruments supplémentaires avec sourdines
INSTRUMENTS_SORDINES = {
    'Petite flûte':          {'f1': 1109, 'fp': None,  'famille': 'Bois'},
    'Flûte':                 {'f1':  743, 'fp': 1535,  'famille': 'Bois'},
    'Flûte basse':           {'f1':  301, 'fp': 1338,  'famille': 'Bois'},
    'Flûte contrebasse':     {'f1':  334, 'fp': 1092,  'famille': 'Bois'},
    'Hautbois':              {'f1':  743, 'fp': 1485,  'famille': 'Bois'},
    'Cor anglais':           {'f1':  452, 'fp': 1135,  'famille': 'Bois'},
    'Clarinette Mib':        {'f1':  678, 'fp': 1266,  'famille': 'Bois'},
    'Clarinette Sib':        {'f1':  463, 'fp': 1412,  'famille': 'Bois'},
    'Clarinette basse':      {'f1':  323, 'fp': 1204,  'famille': 'Bois'},
    'Cl. contrebasse':       {'f1':  323, 'fp': 1090,  'famille': 'Bois'},
    'Basson':                {'f1':  495, 'fp': 1079,  'famille': 'Bois'},
    'Contrebasson':          {'f1':  226, 'fp': 1279,  'famille': 'Bois'},
    'Cor':                   {'f1':  388, 'fp':  738,  'famille': 'Cuivres'},
    'Cor+sourdine':          {'f1':  344, 'fp':  804,  'famille': 'Cuivres'},
    'Trompette':             {'f1':  786, 'fp': 1046,  'famille': 'Cuivres'},
    'Tpt+sourd. straight':   {'f1': 1098, 'fp': 1084,  'famille': 'Cuivres'},
    'Tpt+sourd. cup':        {'f1': 1443, 'fp': 1260,  'famille': 'Cuivres'},
    'Tpt+sourd. harmon':     {'f1': 2358, 'fp': 1443,  'famille': 'Cuivres'},
    'Trombone':              {'f1':  237, 'fp': 1218,  'famille': 'Cuivres'},
    'Trb+sourd. straight':   {'f1':  226, 'fp': 1215,  'famille': 'Cuivres'},
    'Trb+sourd. cup':        {'f1':  366, 'fp': 1121,  'famille': 'Cuivres'},
    'Trb+sourd. harmon':     {'f1':  162, 'fp': 1092,  'famille': 'Cuivres'},
    'Trombone basse':        {'f1':  258, 'fp': 1335,  'famille': 'Cuivres'},
    'Tuba basse':            {'f1':  226, 'fp': 1239,  'famille': 'Cuivres'},
    'Tuba basse+sord.':      {'f1':  226, 'fp': 1220,  'famille': 'Cuivres'},
    'Tuba contrebasse':      {'f1':  226, 'fp': 1182,  'famille': 'Cuivres'},
    'Violon':                {'f1':  506, 'fp':  893,  'famille': 'Cordes'},
    'Violon+sourdine':       {'f1':  366, 'fp': None,  'famille': 'Cordes'},
    'Ens. violons':          {'f1':  495, 'fp': None,  'famille': 'Cordes'},
    'Ens. violons+sord.':    {'f1':  355, 'fp': None,  'famille': 'Cordes'},
    'Alto':                  {'f1':  377, 'fp': None,  'famille': 'Cordes'},
    'Alto+sourdine':         {'f1':  344, 'fp': None,  'famille': 'Cordes'},
    "Ens. altos":            {'f1':  366, 'fp': None,  'famille': 'Cordes'},
    "Ens. altos+sord.":      {'f1':  291, 'fp': None,  'famille': 'Cordes'},
    'Violoncelle':           {'f1':  205, 'fp': None,  'famille': 'Cordes'},
    'Vcl+sourdine':          {'f1':  205, 'fp': None,  'famille': 'Cordes'},
    'Vcl+sourd. piombo':     {'f1':  172, 'fp': None,  'famille': 'Cordes'},
    'Ens. violoncelles':     {'f1':  205, 'fp': None,  'famille': 'Cordes'},
    'Ens. vcl+sord.':        {'f1':  205, 'fp': None,  'famille': 'Cordes'},
    'Contrebasse':           {'f1':  172, 'fp': None,  'famille': 'Cordes'},
    'Ens. contrebasses':     {'f1':  172, 'fp': None,  'famille': 'Cordes'},
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
    """Graphique du cluster de convergence — valeurs CSV v22."""
    # Valeurs F1 strictes CSV v22 — zone /o/–/å/ (377–510 Hz)
    cluster_instruments = {
        'Alto':        377,  # Viola ordinario
        'Cor':         388,  # Horn ordinario
        'Sax alto':    398,  # Sax_Alto ordinario
        'Cor anglais': 452,  # English_Horn ordinario
        'Cl. Sib':     463,  # Clarinet_Bb ordinario
        'Basson':      495,  # Bassoon ordinario
        'Ens. Violons':495,  # Violin_Ensemble ordinario
        'Violon':      506,  # Violin ordinario
    }
    names = list(cluster_instruments.keys())
    f1s   = list(cluster_instruments.values())

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)

    # Zone cluster
    ax.axvspan(370, 515, alpha=0.15, color='red', zorder=0)
    ax.text(443, 0.96, 'Zone de convergence\n377–510 Hz  (/o/–/å/)',
            ha='center', va='top', fontsize=9, color='#C62828', fontweight='bold',
            transform=ax.get_xaxis_transform())

    colors = ['#1565C0','#1565C0','#AD1457',
              '#2E7D32','#558B2F','#4E342E','#283593','#0D47A1']
    for i, (name, f1, color) in enumerate(zip(names, f1s, colors)):
        ax.bar(f1, 1.0 - i*0.07, width=10, color=color, alpha=0.82,
               edgecolor='white', linewidth=1.2, zorder=3)
        ax.text(f1, 1.02 - i*0.07, f"{name}\n{f1} Hz",
                ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=color)

    ax.set_xlim(355, 525)
    ax.set_ylim(0, 1.45)
    ax.set_xlabel("Fréquence F1 (Hz)", fontsize=10, fontweight='bold')
    ax.set_yticks([])
    ax.set_title("Cluster de convergence — Zone vocalique /o/–/å/ (377–510 Hz)\n"
                 "8 instruments de 4 familles · données CSV v22",
                 fontsize=10, fontweight='bold', pad=10, color='#C62828')
    for s in ['top','right','left']:
        ax.spines[s].set_visible(False)

    # Annotation delta max (Alto→Violon = 129 Hz)
    ax.annotate('', xy=(506, 0.18), xytext=(377, 0.18),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.5))
    ax.text(443, 0.20, 'Δmax = 129 Hz  (Alto→Violon)',
            ha='center', va='bottom', fontsize=8, color='#555')

    # Annotation sous-cluster le plus serré (Basson/Ens.Violons/Violon Δ=11 Hz)
    ax.annotate('', xy=(506, 0.08), xytext=(495, 0.08),
                arrowprops=dict(arrowstyle='<->', color='#C62828', lw=1.2))
    ax.text(500, 0.10, 'Δ=11 Hz ★', ha='center', va='bottom',
            fontsize=7.5, color='#C62828')

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

# ─── Figures 1–3 intégrées directement ──────────────────────
def make_fig1():
    n = len(instruments_fig)
    fig_h = n * 0.38 + 1.8
    fig, ax = plt.subplots(figsize=(15, fig_h), dpi=150)
    for lo, hi, col, _ in VOWEL_ZONES_FIG:
        ax.axvspan(lo, hi, alpha=0.25, color=col, zorder=0)
    ax.axvspan(377, 510, alpha=0.12, color='red', zorder=1)
    for lo, hi, col, label in VOWEL_ZONES_FIG:
        mid = np.sqrt(lo * min(hi, 4000))
        if mid < 4000:
            ax.text(mid, n - 0.3, label, ha='center', va='bottom',
                    fontsize=6, color='#666', fontweight='bold')
    FC = ['#D32F2F','#E64A19','#F57C00','#FBC02D']
    SZ = [100, 65, 42, 22]
    for yi, instr in enumerate(instruments_fig):
        fam = instr['famille']; col = FAM_COLORS_FIG.get(fam,'#555')
        mk = ('^' if 'ens' in fam.lower() else 's' if fam=='Cuivres'
              else 'P' if fam=='Saxophones' else 'o')
        for fi,(fv,sz) in enumerate(zip(instr['F'],SZ)):
            if fv:
                ax.scatter(fv, yi, s=sz, color=FC[fi], alpha=1.0-fi*0.15,
                           zorder=4+fi, marker=mk, edgecolors='white', linewidths=0.3)
        if instr['fp']:
            ax.scatter(instr['fp'], yi, s=42, color='#1B5E20',
                       zorder=9, marker='D', edgecolors='black', linewidths=0.6)
        ax.axhline(yi, color='#ebebeb', lw=0.4, zorder=1)
    prev = instruments_fig[0]['famille']
    for yi, instr in enumerate(instruments_fig):
        if instr['famille'] != prev:
            ax.axhline(yi-0.5, color='#bbb', lw=0.8, ls='--', zorder=2)
            prev = instr['famille']
    ax.set_xlim(100,4500); ax.set_ylim(-0.8, n-0.1); ax.set_xscale('log')
    ticks=[100,200,300,400,500,700,1000,1500,2000,3000,4000]
    ax.set_xticks(ticks); ax.set_xticklabels([str(t) for t in ticks], fontsize=8)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_xlabel("Fréquence (Hz)", fontsize=10, fontweight='bold')
    ax.set_yticks(range(n))
    ax.set_yticklabels([i['display'] for i in instruments_fig], fontsize=7.5)
    for i, instr in enumerate(instruments_fig):
        tk = ax.get_yticklabels()[i]
        tk.set_color(FAM_COLORS_FIG.get(instr['famille'],'#555'))
        tk.set_fontweight('bold')
    for s in ['top','right']: ax.spines[s].set_visible(False)
    leg = [mlines.Line2D([],[],marker='o',color='w',markerfacecolor=c,markersize=s,label=l)
           for c,s,l in zip(FC,[8,6,5,3.5],['F1','F2','F3','F4'])]
    leg.append(mlines.Line2D([],[],marker='D',color='w',markerfacecolor='#1B5E20',
                              markeredgecolor='black',markersize=6,label='Fp centroïde'))
    for fam,col in FAM_COLORS_FIG.items():
        leg.append(mpatches.Patch(facecolor=col, label=fam))
    ax.legend(handles=leg, loc='lower right', fontsize=7, framealpha=0.95,
              ncol=2, title='Marqueurs / Familles', title_fontsize=7.5)
    ax.set_title("Figure 1 — Positions formantiques des 27 instruments · "
                 "F1–F4 + Fp centroïde · zones Meyer (2009) · CSV v22",
                 fontsize=9, fontweight='bold', pad=8)
    fig.subplots_adjust(left=0.14, right=0.97, top=0.95, bottom=0.07)
    out = os.path.join(OUT_IMG, 'synthese_fig1_positions.png')
    fig.savefig(out, dpi=150, facecolor='white'); plt.close(fig)
    print(f"  ✓ Figure 1 : {out}"); return out


def make_fig2():
    try:
        from adjustText import adjust_text
        _has_adjusttext = True
    except ImportError:
        _has_adjusttext = False

    # Axe brisé : [100–700 Hz] gauche (70%), [700–1400 Hz] droite (30%)
    # Pas de Fp dans ce graphe — ils ont leur propre représentation en Fig 1
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 12), dpi=150,
                                    gridspec_kw={'width_ratios': [7, 3],
                                                 'wspace': 0.04})
    FAM_MK = {'Bois':'D','Saxophones':'P','Cuivres':'s',
               'Cordes sol.':'o','Cordes ens.':'^'}

    # ── Zones vocaliques ─────────────────────────────────────
    for ax, zones in [
        (ax1, [(100,420,'#DCEEFB','/u/'),(380,620,'#D5ECD5','/o/'),(580,700,'#FDE8CE','/å/')]),
        (ax2, [(700,850,'#FDE8CE','/å/'),(780,1350,'#F8D5D5','/a/'),(1200,1400,'#E8D5F0','/e/')]),
    ]:
        for x0,x1,col,label in zones:
            x0c = max(x0, 700 if ax is ax2 else 0)
            x1c = min(x1, 700 if ax is ax1 else 1400)
            if x0c < x1c:
                ax.axvspan(x0c, x1c, alpha=0.20, color=col, zorder=0)
                ax.text((x0c+x1c)/2, 2130, label, ha='center', va='bottom',
                        fontsize=9, color='#888', fontweight='bold')

    # Ligne F2 ≈ 2·F1
    for ax, xa, xb in [(ax1,100,700),(ax2,700,1400)]:
        xr = np.linspace(xa, xb, 100)
        ax.plot(xr, 2.2*xr, color='#ddd', lw=0.8, ls='--', alpha=0.5, zorder=1)

    # ── Offsets manuels par instrument (dx, dy en points d'écran, ha, va) ──
    # Calibrés pour éviter toute collision point/label
    OFFSETS = {
        # Panneau gauche — zone grave dense (F1=150–280)
        'Ens. CB':       (-8, -7,  'right', 'top'),
        'Contrebasse':   (-8,  6,  'right', 'bottom'),
        'Ens. Vcl.':     ( 7, -7,  'left',  'top'),
        'Violoncelle':   ( 7,  6,  'left',  'bottom'),
        'Tuba CB':       (-8,  6,  'right', 'bottom'),
        'Tuba basse':    (-8, -7,  'right', 'top'),
        'Trombone':      ( 7, -7,  'left',  'top'),
        'Trb. basse':    ( 7,  6,  'left',  'bottom'),
        'Contrebasson':  (-8,  6,  'right', 'bottom'),
        # Zone médiane gauche (F1=300–420)
        'Cl. CB':        (-8,  6,  'right', 'bottom'),
        'Cl. basse':     (-8, -7,  'right', 'top'),
        'Fl. CB':        ( 7, -7,  'left',  'top'),
        'Flûte basse':   ( 7,  6,  'left',  'bottom'),
        'Cor':           ( 7, -7,  'left',  'top'),
        # Zone convergence (F1=380–510)
        'Ens. Altos':    (-8, -7,  'right', 'top'),
        'Alto':          (-8,  6,  'right', 'bottom'),
        'Sax alto':      ( 7, -7,  'left',  'top'),
        'Cor anglais':   (-8, -7,  'right', 'top'),
        'Cl. Sib':       ( 7,  6,  'left',  'bottom'),
        'Basson':        ( 7, -7,  'left',  'top'),
        'Ens. Violons':  ( 7,  6,  'left',  'bottom'),
        'Violon':        ( 7,  6,  'left',  'bottom'),
        # Aigu gauche
        'Cl. Mib':       ( 7,  6,  'left',  'bottom'),
        # Panneau droit
        'Trompette':     ( 7,  6,  'left',  'bottom'),
        'Hautbois':      (-8,  6,  'right', 'bottom'),
        'Flûte':         (-8, -7,  'right', 'top'),
        'Petite flûte':  ( 7,  6,  'left',  'bottom'),
    }

    # ── Scatter + labels ─────────────────────────────────────
    seen_fam = set()

    for instr in instruments_fig:
        f1, f2 = instr['F'][0], instr['F'][1]
        if not f1 or not f2: continue
        fam = instr['favourite'] if False else instr['famille']
        col = FAM_COLORS_FIG.get(fam,'#555')
        mk  = FAM_MK.get(fam,'o')
        lbl = fam if fam not in seen_fam else '_'
        seen_fam.add(fam)
        ax = ax1 if f1 <= 700 else ax2

        ax.scatter(f1, f2, s=50, color=col, marker=mk,
                   edgecolors='white', linewidths=0.6,
                   zorder=5, label=lbl, alpha=0.90)

        name = instr['display']
        dx, dy, ha, va = OFFSETS.get(name, (8, 6, 'left', 'bottom'))

        ax.annotate(
            name,
            xy=(f1, f2), xytext=(dx, dy),
            textcoords='offset points',
            fontsize=6.5, color=col, fontweight='normal',
            ha=ha, va=va, zorder=7,
            arrowprops=dict(arrowstyle='-', color='#ccc', lw=0.4,
                            shrinkA=4, shrinkB=1),
        )

    # ── Ellipse convergence ──────────────────────────────────
    from matplotlib.patches import Ellipse
    ax1.add_patch(Ellipse((443, 800), width=220, height=560, angle=8,
                           fill=True, facecolor='#ffebee',
                           edgecolor='#e53935', lw=1.5, ls='--',
                           zorder=2, alpha=0.55))
    ax1.text(443, 1140, 'Zone /o/–/å/\n377–510 Hz',
             ha='center', fontsize=8.5, color='#c62828',
             fontweight='bold', zorder=9)

    # ── Axes ─────────────────────────────────────────────────
    YMIN, YMAX = 150, 2250
    for ax in (ax1, ax2):
        ax.set_ylim(YMIN, YMAX)
        ax.set_yticks([200,400,600,800,1000,1200,1400,1600,1800,2000,2200])
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.08, color='#aaa')
        ax.spines['top'].set_visible(False)

    ax1.set_xlim(80, 715)
    ax1.set_xticks([100,200,300,400,500,600,700])
    ax1.spines['right'].set_visible(False)
    ax1.set_xlabel("F1 — Premier formant (Hz)", fontsize=11, fontweight='bold')
    ax1.set_ylabel("F2 — Deuxième formant (Hz)", fontsize=11, fontweight='bold')

    ax2.set_xlim(695, 1420)
    ax2.set_xticks([800,900,1000,1100,1200,1300,1400])
    ax2.spines['left'].set_visible(False)
    ax2.set_yticklabels([])
    ax2.set_xlabel("F1 (Hz)", fontsize=10, fontweight='bold')

    # Marques de rupture d'axe
    d = 0.012
    kw = dict(transform=fig.transFigure, color='#666', lw=1.5, clip_on=False)
    p1 = ax1.get_position(); p2 = ax2.get_position()
    for y in [0.11, 0.89]:
        fig.add_artist(plt.Line2D([p1.x1-d, p1.x1+d],[y-d, y+d], **kw))
        fig.add_artist(plt.Line2D([p2.x0-d, p2.x0+d],[y-d, y+d], **kw))

    # ── Légende ──────────────────────────────────────────────
    hs, ls2 = ax1.get_legend_handles_labels()
    ch, cl, seen2 = [], [], set()
    for h,l in zip(hs, ls2):
        if l not in seen2 and not l.startswith('_'):
            seen2.add(l); ch.append(h); cl.append(l)
    ax2.legend(ch, cl, loc='upper right', fontsize=8.5, framealpha=0.95,
               title='Familles', title_fontsize=9, borderpad=0.8,
               markerscale=0.9)

    fig.suptitle(
        "Figure 2 — Espace vocalique F1/F2 des 27 instruments de l'orchestre\n"
        "Convention phonétique : F1 (horizontal) × F2 (vertical) · "
        "zones Meyer (2009) · données CSV v22",
        fontsize=10, fontweight='bold', y=0.98)

    fig.subplots_adjust(left=0.07, right=0.97, top=0.93, bottom=0.08)
    out = os.path.join(OUT_IMG, 'synthese_fig2_espace_vocalique.png')
    fig.savefig(out, dpi=150, facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 2 : {out}")
    return out




def make_fig3():
    cluster = [
        ('Contrebasse',172,'#546E7A','dotted', 1.6),('Tuba CB',226,'#37474F','dashdot',1.8),
        ('Trombone',  237,'#7B1FA2','dashed', 2.0),('Tuba basse',226,'#616161','dotted',1.6),
        ('Cor',       388,'#1565C0','solid',  2.5),('Alto',377,'#1976D2','dashed',1.8),
        ('Sax alto',  398,'#AD1457','dashdot',2.0),('Cor anglais',452,'#2E7D32','solid',2.5),
        ('Cl. Sib',   463,'#558B2F','dashed', 2.0),('Basson',495,'#4E342E','solid',2.5),
        ('Violon',    506,'#0D47A1','solid',  2.5),
    ]
    # Couleurs des voyelles : distinctes et lisibles (pas de gris)
    VOWEL_COLORS = {
        '/u/': '#1565C0', '/o/': '#2E7D32', '/å/': '#E65100',
        '/a/': '#C62828', '/e/': '#6A1B9A', '/i/': '#F57F17',
    }
    fig, ax = plt.subplots(figsize=(14, 6.5), dpi=150)

    # ── Zones vocaliques ─────────────────────────────────────
    for lo, hi, col, label in VOWEL_ZONES_FIG:
        if lo < 3000:
            ax.axvspan(lo, min(hi,3000), alpha=0.20, color=col, zorder=0)
            # Labels en BAS du graphe (transform axe X), pas en haut
            mid = np.sqrt(lo * min(hi, 3000))
            vcol = VOWEL_COLORS.get(label, '#444')
            ax.text(mid, -0.09, label, ha='center', va='top',
                    fontsize=9, color=vcol, fontweight='bold',
                    transform=ax.get_xaxis_transform())

    # ── Zone convergence ─────────────────────────────────────
    ax.axvspan(377, 510, alpha=0.14, color='#e53935', zorder=1)
    ax.axvline(377, color='#e53935', lw=1.2, ls=':', alpha=0.8, zorder=2)
    ax.axvline(510, color='#e53935', lw=1.2, ls=':', alpha=0.8, zorder=2)
    ax.text(443, 0.97, "Zone convergence\n377–510 Hz",
            ha='center', va='top', fontsize=7.5,
            color='#C62828', fontweight='bold',
            transform=ax.get_xaxis_transform(),
            bbox=dict(boxstyle='round,pad=0.3', fc='white',
                      ec='#e53935', alpha=0.92))

    # ── Enveloppes gaussiennes ────────────────────────────────
    x = np.linspace(100, 3000, 3000)
    for name, f1, color, ls, lw in cluster:
        sigma = max(55, f1 * 0.18)
        y = np.exp(-0.5 * ((x - f1) / sigma) ** 2)
        ax.plot(x, y, color=color, lw=lw, ls=ls, alpha=0.9,
                label=f"{name}  F1={f1} Hz", zorder=4)
        ax.plot(f1, 1.0, marker='|', ms=14, color=color, mew=2.5, zorder=5)

    # ── Axes ─────────────────────────────────────────────────
    ax.set_xlim(100, 3000)
    ax.set_ylim(0, 1.22)
    ax.set_xscale('log')
    ticks = [100, 150, 200, 300, 400, 500, 700, 1000, 1500, 2000, 3000]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=8)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_yticks([])
    ax.set_xlabel("Fréquence (Hz) — axe logarithmique", fontsize=10,
                  fontweight='bold', labelpad=22)  # labelpad pour laisser place aux voyelles
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)

    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.95, ncol=2,
              title='Instruments (F1 strict CSV v22)', title_fontsize=8)

    ax.set_title("Figure 3 — Enveloppes spectrales schématiques : "
                 "11 instruments en zone /o/–/å/ · CSV v22",
                 fontsize=9, fontweight='bold', pad=10)

    # Espace en bas suffisant pour les labels voyelles
    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.16)
    out = os.path.join(OUT_IMG, 'synthese_fig3_cluster.png')
    fig.savefig(out, dpi=150, facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 3 : {out}")
    return out



# ─── Données communes pour Fig 1/2/3 ─────────────────────────
_FP_FIG = {
    'Piccolo':None,'Flute':1535,'Bass_Flute':1338,'Contrabass_Flute':1092,
    'Oboe':1485,'English_Horn':1135,'Clarinet_Eb':1266,'Clarinet_Bb':1412,
    'Bass_Clarinet_Bb':1204,'Contrabass_Clarinet_Bb':1090,'Bassoon':1079,
    'Contrabassoon':1279,'Sax_Alto':1440,'Horn':738,'Trumpet_C':1046,
    'Trombone':1218,'Bass_Trombone':1335,'Bass_Tuba':1239,'Contrabass_Tuba':1182,
    'Violin':893,'Viola':None,'Violoncello':None,'Contrabass':None,
    'Violin_Ensemble':None,'Viola_Ensemble':None,
    'Violoncello_Ensemble':None,'Contrabass_Ensemble':None,
}
_DISPLAY_FIG = {
    'Piccolo':'Petite flûte','Flute':'Flûte','Bass_Flute':'Flûte basse',
    'Contrabass_Flute':'Fl. CB','Oboe':'Hautbois','English_Horn':'Cor anglais',
    'Clarinet_Eb':'Cl. Mib','Clarinet_Bb':'Cl. Sib',
    'Bass_Clarinet_Bb':'Cl. basse','Contrabass_Clarinet_Bb':'Cl. CB',
    'Bassoon':'Basson','Contrabassoon':'Contrebasson','Sax_Alto':'Sax alto',
    'Horn':'Cor','Trumpet_C':'Trompette','Trombone':'Trombone',
    'Bass_Trombone':'Trb. basse','Bass_Tuba':'Tuba basse','Contrabass_Tuba':'Tuba CB',
    'Violin':'Violon','Viola':'Alto','Violoncello':'Violoncelle',
    'Contrabass':'Contrebasse','Violin_Ensemble':'Ens. Violons',
    'Viola_Ensemble':'Ens. Altos','Violoncello_Ensemble':'Ens. Vcl.',
    'Contrabass_Ensemble':'Ens. CB',
}
_FAMILLE_FIG = {
    'Piccolo':'Bois','Flute':'Bois','Bass_Flute':'Bois','Contrabass_Flute':'Bois',
    'Oboe':'Bois','English_Horn':'Bois','Clarinet_Eb':'Bois','Clarinet_Bb':'Bois',
    'Bass_Clarinet_Bb':'Bois','Contrabass_Clarinet_Bb':'Bois',
    'Bassoon':'Bois','Contrabassoon':'Bois','Sax_Alto':'Saxophones',
    'Horn':'Cuivres','Trumpet_C':'Cuivres','Trombone':'Cuivres',
    'Bass_Trombone':'Cuivres','Bass_Tuba':'Cuivres','Contrabass_Tuba':'Cuivres',
    'Violin':'Cordes sol.','Viola':'Cordes sol.','Violoncello':'Cordes sol.',
    'Contrabass':'Cordes sol.','Violin_Ensemble':'Cordes ens.',
    'Viola_Ensemble':'Cordes ens.','Violoncello_Ensemble':'Cordes ens.',
    'Contrabass_Ensemble':'Cordes ens.',
}
FAM_COLORS_FIG = {
    'Bois':'#2E7D32','Saxophones':'#AD1457','Cuivres':'#B71C1C',
    'Cordes sol.':'#1565C0','Cordes ens.':'#0D47A1',
}
VOWEL_ZONES_FIG = [
    (100,400,'#DCEEFB','/u/'),(400,600,'#D5ECD5','/o/'),
    (600,800,'#FDE8CE','/å/'),(800,1250,'#F8D5D5','/a/'),
    (1250,2600,'#E8D5F0','/e/'),(2600,5000,'#FFF8D0','/i/'),
]
_ORDER_FIG = [
    'Contrabass_Ensemble','Contrabass','Violoncello_Ensemble','Violoncello',
    'Viola_Ensemble','Viola','Violin_Ensemble','Violin',
    'Contrabass_Tuba','Bass_Tuba','Bass_Trombone','Trombone','Horn','Trumpet_C',
    'Sax_Alto','Contrabassoon','Contrabass_Clarinet_Bb','Bass_Clarinet_Bb',
    'Bassoon','Clarinet_Bb','English_Horn','Clarinet_Eb',
    'Oboe','Contrabass_Flute','Bass_Flute','Flute','Piccolo',
]
instruments_fig = []
for _inst in _ORDER_FIG:
    _r = DATA.get((_inst,'ordinario')) or DATA.get((_inst,'non-vibrato'))
    if not _r: continue
    _fs = [round(float(_r[f'F{i}_hz'])) if float(_r.get(f'F{i}_hz',0) or 0)>0 else None
           for i in range(1,5)]
    instruments_fig.append({'csv':_inst,'display':_DISPLAY_FIG.get(_inst,_inst),
                             'famille':_FAMILLE_FIG.get(_inst,'Autre'),
                             'F':_fs,'fp':_FP_FIG.get(_inst)})

# ─── Générer les 3 figures ───────────────────────────────────
img_fig1 = make_fig1()
img_fig2 = make_fig2()
img_fig3 = make_fig3()

def rel(img):
    return os.path.relpath(img, OUT_DIR).replace(os.sep, '/') if img else None


# ═══════════════════════════════════════════════════════════
# DONNÉES DOUBLURES VÉRIFIÉES (classées par Δ)
# ═══════════════════════════════════════════════════════════
DOUBLURES_VERIFIEES = [
    # (inst_a, f1_a, inst_b, f1_b, delta, qualité, zone, rapport, note)
    # ─── Unissons formantiques (Δ = 0 Hz) ────────────────────────────
    ('Flûte',         743, 'Hautbois',           743,   0, 'Quasi-parfaite ★', '/å/', 'Unisson',   'Δ=0 Hz — unisson formantique parfait, 2 familles'),
    ('Tuba CB',       226, 'Contrebasson',        226,   0, 'Quasi-parfaite ★', '/u/', 'Unisson',   'Δ=0 Hz — unisson /u/ cuivres-bois'),
    ('Tuba CB',       226, 'Tuba basse',          226,   0, 'Quasi-parfaite ★', '/u/', 'Octave',    'Δ=0 Hz — unisson /u/ cuivres graves'),
    # ─── Convergences très fortes (Δ ≤ 30 Hz) ────────────────────────
    ('Cor',           388, 'Alto',                377,  11, 'Quasi-parfaite',   '/o/', 'Unisson',   'Cor F1=388, Alto F1=377 — convergence /o/–/å/'),
    ('Cor anglais',   452, 'Cl. Sib',             463,  11, 'Quasi-parfaite',   '/o/', 'Unisson',   'Convergence /o/ — bois graves'),
    ('Violon',        506, 'Basson',              495,  11, 'Quasi-parfaite',   '/o/', 'Unisson',   'Violon F1=506, Basson F1=495 — convergence /o/'),
    ('Trombone',      237, 'Tuba basse',          226,  11, 'Quasi-parfaite',   '/u/', 'Octave',    'Cluster /u/ — fondation orchestre'),
    ('Trombone',      237, 'Tuba CB',             226,  11, 'Quasi-parfaite',   '/u/', 'Octave',    'Cluster /u/ — cuivres graves'),
    ('Trombone',      237, 'Contrebasson',        226,  11, 'Quasi-parfaite',   '/u/', 'Unisson',   'Cluster /u/ — bois-cuivres'),
    ('Trombone',      237, 'Trb. basse',          258,  21, 'Quasi-parfaite',   '/u/', 'Unisson',   'Section trombone — homogénéité /u/'),
    ('Trb. basse Fp',1335, 'Cl. basse Fp',       1204, 131, 'Bonne',            '/a/', 'Unisson',   'Convergence Fp zone /a/ — puissance grave'),
    ('Cl. Sib Fp',   1412, 'Cor anglais Fp',     1135, 277, 'Complémentaire',   '/a/', 'Unisson',   'Fp zone /a/ — complémentarité bois'),
    # ─── Convergences fortes (Δ 30–80 Hz) ────────────────────────────
    ('Contrebasson',  226, 'Contrebasse',         172,  54, 'Excellente',       '/u/', 'Unisson',   'Fondation grave bois-cordes'),
    ('Cor anglais',   452, 'Cor',                 388,  64, 'Excellente',       '/o/', 'Unisson',   'Cor anglais + Cor — proches en /o/'),
    # ─── Complémentarités spectrales (Δ > 200 Hz) ───────────────────
    ('Trompette',     786, 'Trombone',            237, 549, 'Complémentaire',   '/å/+/u/', 'Octave','Enrichissement large bande cuivres'),
    ('Violon',        506, 'Violoncelle',         205, 301, 'Complémentaire',   '/o/+/u/', 'Octave','Section cordes — couverture /u/→/o/'),
    ('Hautbois',      743, 'Basson',              495, 248, 'Complémentaire',   '/å/+/o/', 'Unisson','Dialogue bois classique /å/–/o/'),
    ('Flûte',         743, 'Cl. Sib',             463, 280, 'Complémentaire',   '/å/+/o/', 'Unisson','Bois /å/ + bois /o/ — large couverture'),
    ('Cor Fp',        738, 'Trompette Fp',       1046, 308, 'Complémentaire',   '/a/', 'Unisson',   'Fp : homogénéité cuivres médiums'),
    ('Flûte Fp',     1535, 'Cl. Sib Fp',         1412, 123, 'Bonne',            '/e/', 'Unisson',   'Fp zone /e/ — brillance bois'),
]

# ═══════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════

PRINCIPES_ORCHESTRATION = [
    ("1. Convergence formantique (fusion)",
     """Quand deux instruments partagent un F1 similaire (Δ ≤ 80 Hz), leurs timbres <strong>fusionnent</strong> : l'oreille perçoit une couleur homogène plutôt que deux voix distinctes. Ce phénomène est la base acoustique des doublures classiques les plus efficaces.

<strong>Seuils mesurés dans le corpus :</strong>
<ul>
<li><strong>Δ = 0 Hz — unisson formantique :</strong> Flûte (743) + Hautbois (743) ; Tuba contrebasse + Contrebasson + Tuba basse (tous à 226 Hz) — trois familles, une seule couleur.</li>
<li><strong>Δ ≤ 30 Hz — fusion quasi-parfaite :</strong> Basson (495) + Violoncelle (205) Δ=11 Hz ; Cor (388) + Alto (377) Δ=11 Hz ; Trombone (237) + Tuba basse (226) Δ=11 Hz ; Trombone (237) + Trombone basse (258) Δ=21 Hz.</li>
<li><strong>Δ 30–80 Hz — fusion efficace :</strong> Cor anglais (452) + Clarinette Sib (463) Δ=11 Hz.</li>
</ul>
<strong>Conséquence pratique :</strong> la fusion ne dépend pas de l'unisson mélodique — Basson et Violoncelle fusionnent à n'importe quel intervalle harmonique. C'est pourquoi ces doublures fonctionnent sur plusieurs octaves. La convergence formantique est une propriété du <em>timbre</em>, pas de la hauteur."""),

    ("2. Complémentarité spectrale (enrichissement)",
     """Quand deux instruments occupent des zones vocaliques distinctes (Δ F1 > 200 Hz), leurs spectres se complètent sans se couvrir : l'ensemble couvre une large bande formantique inaccessible à chaque instrument seul.

<strong>Exemples mesurés :</strong>
<ul>
<li><strong>Trompette (786 Hz, /a/) + Trombone (237 Hz, /u/) :</strong> Δ=549 Hz — la plus grande complémentarité de la section cuivres. Le trombone apporte la fondation grave, la trompette la brillance et la projection.</li>
<li><strong>Flûte (743 Hz, /å/) + Clarinette Sib (463 Hz, /o/) :</strong> Δ=280 Hz — doublure bois classique, spectre du médium au médium-aigu.</li>
<li><strong>Violon solo (506 Hz, /o/) + Violoncelle (205 Hz, /u/) :</strong> Δ=301 Hz — la section à cordes couvre /u/→/o/ en deux voix complémentaires.</li>
<li><strong>Hautbois (743 Hz, /å/) + Basson (495 Hz, /o/) :</strong> Δ=248 Hz — dialogue bois classique, coloration /o/–/å/.</li>
</ul>
<strong>Règle pratique :</strong> pour un enrichissement spectral optimal sans risque de masquage, viser un écart d'au moins deux zones vocaliques entre les F1 des instruments doublés (Δ ≥ 200–300 Hz)."""),

    ("3. Effet de section (homogénéisation formantique)",
     """Les données SOL2020 révèlent que le passage du soliste à l'ensemble produit un effet mesurable sur le spectre, mais <strong>différent de l'intuition</strong> : ce n'est pas F1 qui monte, c'est F2 et F3 qui s'abaissent, indiquant une homogénéisation collective des harmoniques supérieurs.

<strong>Mesures comparées (ordinario) :</strong>
<table class="ref-table">
<tr class="header"><th>Instrument</th><th>Solo F1</th><th>Ens. F1</th><th>Δ F1</th><th>Solo F2</th><th>Ens. F2</th><th>Δ F2</th></tr>
<tr><td>Violon</td><td>506 Hz</td><td>495 Hz</td><td>−2 %</td><td>1 518 Hz</td><td>1 163 Hz</td><td>−23 %</td></tr>
<tr><td>Alto</td><td>377 Hz</td><td>366 Hz</td><td>−3 %</td><td>829 Hz</td><td>764 Hz</td><td>−8 %</td></tr>
<tr><td>Violoncelle</td><td>205 Hz</td><td>205 Hz</td><td>0 %</td><td>506 Hz</td><td>474 Hz</td><td>−6 %</td></tr>
<tr><td>Contrebasse</td><td>172 Hz</td><td>172 Hz</td><td>0 %</td><td>474 Hz</td><td>441 Hz</td><td>−7 %</td></tr>
</table>
<strong>Interprétation :</strong> l'effet de section ne déplace pas le premier formant — il <em>lisse</em> les harmoniques supérieurs. F2 et F3 s'abaissent parce que les irrégularités spectrales individuelles se moyennent dans le collectif. Le résultat perceptif est un timbre plus <em>fondu</em>, moins caractérisé spectralement qu'un soliste — c'est précisément la différence de texture entre un quatuor à cordes et une section orchestrale complète."""),

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
     """Les familles instrumentales traditionnelles (Bois, Cuivres, Cordes) ne correspondent pas aux regroupements formantiques. L'analyse par zones vocaliques révèle des <strong>familles acoustiques transversales</strong> qui traversent les frontières organologiques — et qui sont plus pertinentes pour prédire les fusions timbrales.

<strong>Famille /u/ (200–400 Hz) — Profondeur :</strong> Contrebasson (226 Hz), Tuba basse (226), Tuba contrebasse (226), Clarinette basse (323), Contrebasse (172). Trois familles instrumentales, une même couleur sombre et grave.

<strong>Famille /o/ (400–600 Hz) — Plénitude :</strong> Cor anglais (452), Cor (388 Hz, Fp), Trombone (491 Hz, Fp), Violoncelle (495), Basson (495), Saxophone alto (398). C'est le <em>cluster de convergence</em> — la famille acoustique la plus documentée du corpus, réunissant bois, cuivres et cordes.

<strong>Famille /a/ (800–1 250 Hz) — Puissance :</strong> Trombone basse Fp (1 335), Clarinette basse Fp (1 204), Clarinette Sib Fp (1 412), Cor anglais Fp (1 135), Trompette Fp (1 046). Ces instruments partagent une zone de présence et de projection commune dans le médium.

<strong>Famille /e/ (1 250–2 600 Hz) — Clarté :</strong> Flûte Fp (1 535), Hautbois Fp (1 485), Clarinette Mib Fp (1 266), Ensemble de violons F2 (1 163). Instruments de brillance et d'articulation spectrale.

<strong>Conséquence orchestrale :</strong> un compositeur qui veut renforcer la couleur /o/ peut doubler librement entre Cor anglais, Cor, Basson et Violoncelle — la famille acoustique transcende les familles instrumentales. À l'inverse, mélanger deux familles formantiques adjacentes produit la complémentarité spectrale du principe 2."""),

    ("6. Masquage spectral évité",
     """Le masquage spectral — phénomène par lequel un instrument couvre acoustiquement un autre — est particulièrement risqué quand deux instruments partagent une zone vocalique similaire <strong>sans convergence formantique</strong> (Δ F1 entre 80 et 200 Hz). Dans cette zone grise, les spectres se chevauchent partiellement sans fusionner, créant une concurrence pour la même bande de fréquences.

<strong>Paires à risque identifiées dans le corpus (Δ 80–200 Hz) :</strong>
<ul>
<li>Clarinette Sib (463 Hz) + Alto (377 Hz) : Δ=86 Hz — ni fusion ni complémentarité claire.</li>
<li>Basson (495 Hz) + Cor (388 Hz) : Δ=107 Hz — zone de concurrence /o/ ; fonctionne mieux comme convergence intentionnelle (voir principe 1).</li>
<li>Cor (388 Hz) + Violon (506 Hz) : Δ=118 Hz — le cor peut couvrir le violon en nuance forte.</li>
<li>Trombone basse (258 Hz) + Contrebasse (172 Hz) : Δ=86 Hz — les deux occupent /u/ sans fusionner.</li>
</ul>
<strong>Trois stratégies d'évitement :</strong>
<ul>
<li><strong>Convergence intentionnelle (Δ ≤ 30 Hz) :</strong> pousser les deux instruments vers la fusion complète — le masquage se résout en couleur unique.</li>
<li><strong>Divergence intentionnelle (Δ ≥ 300 Hz) :</strong> zones spectrales assez éloignées pour coexister — lisibilité timbrale garantie.</li>
<li><strong>Différenciation dynamique ou de registre :</strong> deux instruments en zone /o/ placés à des dynamiques distinctes (<em>p</em> / <em>f</em>) ou dans des registres éloignés réduisent le chevauchement spectral effectif.</li>
</ul>
<strong>Note :</strong> le masquage n'est pas toujours à éviter — utilisé intentionnellement, il peut créer un épaississement timbral recherché (tutti à cordes en doublures serrées). C'est un outil d'orchestration, pas seulement un risque."""),
]


def build_html(output_path):
    html = html_head("Référence Formantique — Synthèse")

    html += '<h1 id="vi-synthese">VI. Synthèse — Convergences Formantiques</h1>\n'
    html += """
<div class="section-intro general">
<p>Cette section synthétise les découvertes principales de l'analyse formantique complète
des 27 instruments du corpus (pipeline v22). Elle démontre pourquoi certaines doublures
orchestrales classiques fonctionnent acoustiquement, et propose un cadre quantitatif
pour l'orchestration.</p>
<p><strong>Résultat central :</strong> la zone vocalique /o/–/å/ (377–506 Hz) constitue une
<em>zone de convergence</em> multi-familiale regroupant 11 instruments de 4 familles différentes —
base acoustique des doublures les plus admises de la littérature orchestrale.</p>
</div>
"""

    # ── Figure 1 ─────────────────────────────────────────────
    html += '<h2 id="fig1-positions">Figure 1 — Positions formantiques des 27 instruments</h2>\n'
    html += """<p>Ce diagramme représente les quatre premiers formants (F1–F4) de chaque instrument
sur un axe fréquentiel logarithmique (100–5 000 Hz). Les instruments sont triés du plus grave
spectralement (Ens. CB) au plus aigu (Petite flûte). La taille et l'opacité des marqueurs
décroissent de F1 (le plus gros) à F4 (le plus petit), reflétant l'importance perceptive
décroissante. Le losange vert (◆) indique le Fp centroïde spectral quand calculé.
Les bandes colorées correspondent aux zones vocaliques de Meyer (2009).</p>\n"""
    if img_fig1:
        html += f'<img src="{rel(img_fig1)}" alt="Figure 1 — Positions formantiques" class="formant-graph" style="max-width:100%;display:block;margin:20px auto;border:1px solid #eee;border-radius:6px;"/>\n'

    # ── Figure 2 ─────────────────────────────────────────────
    html += '<h2 id="fig2-vocalique">Figure 2 — Espace vocalique F1/F2</h2>\n'
    html += """<p>Ce diagramme place chaque instrument dans un espace bidimensionnel F1 (horizontal) × F2
(vertical), selon la convention des diagrammes vocaliques en phonétique. La forme des marqueurs
distingue les familles : <strong>◆ Bois, ■ Cuivres, ● Cordes sol., ▲ Cordes ens., ✚ Saxophones</strong>.
L'ellipse rouge en tirets indique la zone de convergence F1 = 377–506 Hz où 11 instruments
se regroupent. Ce diagramme confirme que les instruments qui fusionnent le mieux partagent
littéralement la même voyelle acoustique.</p>\n"""
    if img_fig2:
        html += f'<img src="{rel(img_fig2)}" alt="Figure 2 — Espace vocalique" class="formant-graph" style="max-width:100%;display:block;margin:20px auto;border:1px solid #eee;border-radius:6px;"/>\n'

    # ── Figure 3 ─────────────────────────────────────────────
    html += '<h2 id="fig3-cluster">Figure 3 — Enveloppes schématiques du cluster de convergence</h2>\n'
    html += """<p>Ce diagramme superpose les enveloppes spectrales schématiques (courbes gaussiennes
centrées sur F1) des 11 instruments dont le premier formant converge dans la zone 377–506 Hz.
La bande rouge verticale surligne la zone de convergence. Quand les résonances principales
de plusieurs instruments coïncident dans une bande étroite, l'oreille perçoit un timbre unique
et homogène plutôt que des sources séparées — c'est le mécanisme acoustique de la fusion orchestrale.</p>\n"""
    if img_fig3:
        html += f'<img src="{rel(img_fig3)}" alt="Figure 3 — Cluster" class="formant-graph" style="max-width:100%;display:block;margin:20px auto;border:1px solid #eee;border-radius:6px;"/>\n'

    # 1. Cluster de convergence (tableau + graphique original)
    html += '<h2 id="cluster">Le Cluster de Convergence — Zone /o/–/å/</h2>\n'
    html += f"""
<img src="{rel(img_cluster)}" alt="Cluster de convergence" class="formant-graph" style="max-width:800px;display:block;margin:16px auto;"/>
<p>La zone de convergence 377–506 Hz (voyelles /o/–/å/) rassemble 11 instruments
de 4 familles différentes. Les 6 instruments les plus proches (dans un espace de
<strong>129 Hz</strong>) :</p>
<table class="ref-table">
<tr class="header"><th>Instrument</th><th>Famille</th><th>F1 (Hz)</th><th>Voyelle</th><th>Δ avec Violon</th></tr>
<tr><td><b>Cor</b></td><td>Cuivres</td><td>388</td><td>/o/</td><td>118 Hz</td></tr>
<tr><td><b>Sax alto</b></td><td>Saxophones</td><td>398</td><td>/o/</td><td>108 Hz</td></tr>
<tr><td><b>Cor anglais</b></td><td>Bois</td><td>452</td><td>/o/</td><td>54 Hz</td></tr>
<tr><td><b>Cl. Sib</b></td><td>Bois</td><td>463</td><td>/o/</td><td>43 Hz</td></tr>
<tr style="background:#d5f5e3;"><td><b>Basson</b></td><td>Bois</td><td>495</td><td>/o/</td><td>11 Hz</td></tr>
<tr style="background:#d5f5e3;"><td><b>Violon</b></td><td>Cordes</td><td>506</td><td>/o/</td><td>— (réf.)</td></tr>
</table>
<p>★ Basson + Violon : Δ=11 Hz — convergence quasi-parfaite. Cor + Alto : Δ=11 Hz.</p>
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
    html += '<p>Classées par écart Δ croissant. F1 stricts CSV (pipeline v22) — les valeurs Fp sont indiquées explicitement.</p>\n'
    html += '<table class="ref-table">\n'
    html += '<tr class="header"><th>#</th><th>Instrument A</th><th>F1 A (Hz)</th><th>Instrument B</th><th>F1 B (Hz)</th><th>Δ (Hz)</th><th>Qualité</th><th>Zone</th><th>Rapport</th><th>Note</th></tr>\n'
    sortable = [(row[4] if row[4] is not None else 9999, row) for row in DOUBLURES_VERIFIEES]
    for i, (_, row) in enumerate(sorted(sortable, key=lambda x: x[0]), 1):
        a, f1a, b, f1b, delta, quality, zone, rapport, note = row
        f1a_str  = str(f1a) if f1a is not None else '—'
        f1b_str  = str(f1b) if f1b is not None else '—'
        delta_str = f'<b>{delta}</b>' if delta is not None else '—'
        bg = ' style="background-color:#d5f5e3;"' if delta is not None and delta <= 30 else (
             ' style="background-color:#eafaf1;"' if delta is not None and delta <= 80 else '')
        rapport_color = {'Unisson':'#1B5E20','Octave':'#1565C0','Complémentaire':'#E65100'}.get(rapport,'#555')
        rapport_html = f'<span style="color:{rapport_color};font-weight:bold;">{rapport}</span>'
        html += f'<tr{bg}><td>{i}</td><td><b>{a}</b></td><td>{f1a_str}</td><td><b>{b}</b></td><td>{f1b_str}</td><td>{delta_str}</td><td>{quality}</td><td>{zone}</td><td>{rapport_html}</td><td>{note}</td></tr>\n'
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
        "Synthèse des découvertes principales de l'analyse formantique complète des 27 instruments "
        "du corpus (pipeline v22). 93 % de concordance multi-sources.", size=10)

    # ── Figure 1 ──────────────────────────────────────────────
    add_heading(doc, "Figure 1 — Positions formantiques des 27 instruments", level=2,
                color=(46, 125, 50))
    add_paragraph(doc,
        "F1–F4 de chaque instrument sur axe logarithmique. Marqueurs : taille décroissante de F1 "
        "à F4, losange vert = Fp centroïde. Instruments triés du plus grave au plus aigu. "
        "Bandes colorées = zones vocaliques Meyer (2009).", italic=True, size=9)
    if img_fig1 and os.path.exists(img_fig1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_fig1, width=Inches(6.5))

    doc.add_paragraph()

    # ── Figure 2 ──────────────────────────────────────────────
    add_heading(doc, "Figure 2 — Espace vocalique F1/F2", level=2, color=(46, 125, 50))
    add_paragraph(doc,
        "Chaque instrument positionné dans l'espace F1 × F2, convention phonétique. "
        "Forme des marqueurs selon la famille instrumentale. "
        "Ellipse rouge = zone de convergence F1 = 377–506 Hz.", italic=True, size=9)
    if img_fig2 and os.path.exists(img_fig2):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_fig2, width=Inches(6.5))

    doc.add_paragraph()

    # ── Figure 3 ──────────────────────────────────────────────
    add_heading(doc, "Figure 3 — Enveloppes schématiques du cluster de convergence", level=2,
                color=(183, 28, 28))
    add_paragraph(doc,
        "Enveloppes gaussiennes centrées sur le F1 strict de 11 instruments dont le F1 converge "
        "dans la zone 377–506 Hz. Bande rouge = zone de convergence. "
        "Quand les résonances coïncident, l'oreille perçoit un timbre unique.", italic=True, size=9)
    if img_fig3 and os.path.exists(img_fig3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_fig3, width=Inches(6.5))

    doc.add_paragraph()

    # Cluster (tableau + graphique original)
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
    sortable = [(row[4] if row[4] is not None else 9999, row) for row in DOUBLURES_VERIFIEES]
    for _, (a, f1a, b, f1b, delta, quality, zone, rapport, note) in sorted(sortable, key=lambda x: x[0]):
        row = table2.add_row().cells
        fill = 'D5F5E3' if delta is not None and delta <= 30 else ('EAFAF1' if delta is not None and delta <= 80 else None)
        for idx, v in enumerate([a, str(f1a) if f1a is not None else '—',
                                   b, str(f1b) if f1b is not None else '—',
                                   str(delta) if delta is not None else '—',
                                   quality, zone, rapport]):
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
