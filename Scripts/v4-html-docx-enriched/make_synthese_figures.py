#!/usr/bin/env python3
"""
make_synthese_figures.py
Génère les 3 figures manquantes de la synthèse :
  Fig. 1 — Positions formantiques (F1–F4 + Fp) des 27 instruments
  Fig. 2 — Espace vocalique F1/F2
  Fig. 3 — Cluster de convergence 450–502 Hz (enveloppes schématiques)

Toutes les valeurs proviennent des CSV v22.
"""
import os, sys, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.colors import to_rgba

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT_IMG, BASE

os.makedirs(OUT_IMG, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# DONNÉES
# ═══════════════════════════════════════════════════════════

DATA = {}
for path in [
    os.path.join(BASE,'Resultats','formants_all_techniques.csv'),
    os.path.join(BASE,'Resultats','formants_yan_adds.csv'),
]:
    with open(path) as f:
        for r in csv.DictReader(f):
            if r['technique'] in ('ordinario','non-vibrato'):
                k = (r['instrument'], r['technique'])
                if k not in DATA:
                    DATA[k] = r

FP = {
    'Piccolo':None,'Flute':1535,'Bass_Flute':1338,'Contrabass_Flute':1092,
    'Oboe':1485,'English_Horn':1135,'Clarinet_Eb':1266,'Clarinet_Bb':1412,
    'Bass_Clarinet_Bb':1204,'Contrabass_Clarinet_Bb':1090,
    'Bassoon':1079,'Contrabassoon':1279,'Sax_Alto':1440,
    'Horn':738,'Trumpet_C':1046,'Trombone':1218,'Bass_Trombone':1335,
    'Bass_Tuba':1239,'Contrabass_Tuba':1182,
    'Violin':893,'Viola':None,'Violoncello':None,'Contrabass':None,
    'Violin_Ensemble':None,'Viola_Ensemble':None,
    'Violoncello_Ensemble':None,'Contrabass_Ensemble':None,
}

DISPLAY = {
    'Piccolo':'Petite flûte','Flute':'Flûte','Bass_Flute':'Flûte basse',
    'Contrabass_Flute':'Fl. contrebasse','Oboe':'Hautbois',
    'English_Horn':'Cor anglais','Clarinet_Eb':'Cl. Mib','Clarinet_Bb':'Cl. Sib',
    'Bass_Clarinet_Bb':'Cl. basse','Contrabass_Clarinet_Bb':'Cl. CB',
    'Bassoon':'Basson','Contrabassoon':'Contrebasson','Sax_Alto':'Sax alto',
    'Horn':'Cor','Trumpet_C':'Trompette','Trombone':'Trombone',
    'Bass_Trombone':'Trb. basse','Bass_Tuba':'Tuba basse',
    'Contrabass_Tuba':'Tuba CB',
    'Violin':'Violon','Viola':'Alto','Violoncello':'Violoncelle',
    'Contrabass':'Contrebasse',
    'Violin_Ensemble':'Ens. Violons','Viola_Ensemble':'Ens. Altos',
    'Violoncello_Ensemble':'Ens. Vcl.','Contrabass_Ensemble':'Ens. CB',
}

FAMILLE = {
    'Piccolo':'Bois','Flute':'Bois','Bass_Flute':'Bois','Contrabass_Flute':'Bois',
    'Oboe':'Bois','English_Horn':'Bois','Clarinet_Eb':'Bois','Clarinet_Bb':'Bois',
    'Bass_Clarinet_Bb':'Bois','Contrabass_Clarinet_Bb':'Bois',
    'Bassoon':'Bois','Contrabassoon':'Bois','Sax_Alto':'Saxophones',
    'Horn':'Cuivres','Trumpet_C':'Cuivres','Trombone':'Cuivres',
    'Bass_Trombone':'Cuivres','Bass_Tuba':'Cuivres','Contrabass_Tuba':'Cuivres',
    'Violin':'Cordes sol.','Viola':'Cordes sol.','Violoncello':'Cordes sol.',
    'Contrabass':'Cordes sol.',
    'Violin_Ensemble':'Cordes ens.','Viola_Ensemble':'Cordes ens.',
    'Violoncello_Ensemble':'Cordes ens.','Contrabass_Ensemble':'Cordes ens.',
}

FAM_COLORS = {
    'Bois':'#2E7D32','Saxophones':'#AD1457','Cuivres':'#B71C1C',
    'Cordes sol.':'#1565C0','Cordes ens.':'#0D47A1',
}

ORDER = [
    'Contrabass_Ensemble','Contrabass','Violoncello_Ensemble','Violoncello',
    'Viola_Ensemble','Viola','Violin_Ensemble','Violin',
    'Contrabass_Tuba','Bass_Tuba','Bass_Trombone','Trombone','Trumpet_C','Horn',
    'Sax_Alto',
    'Contrabassoon','Contrabass_Clarinet_Bb','Bass_Clarinet_Bb',
    'Bassoon','Clarinet_Bb','English_Horn','Clarinet_Eb',
    'Oboe','Contrabass_Flute','Bass_Flute','Flute','Piccolo',
]

instruments = []
for inst in ORDER:
    r = DATA.get((inst,'ordinario')) or DATA.get((inst,'non-vibrato'))
    if not r:
        continue
    fs = [round(float(r[f'F{i}_hz'])) if float(r.get(f'F{i}_hz',0) or 0)>0 else None
          for i in range(1,5)]
    instruments.append({
        'csv':inst, 'display':DISPLAY.get(inst,inst),
        'famille':FAMILLE.get(inst,'Autre'),
        'F':fs, 'fp':FP.get(inst),
    })

# ═══════════════════════════════════════════════════════════
# ZONES VOCALIQUES (Meyer 2009)
# ═══════════════════════════════════════════════════════════
VOWEL_ZONES = [
    (100,  400,  '#DCEEFB', '/u/ (oo)\nProfondeur'),
    (400,  600,  '#D5ECD5', '/o/ (oh)\nPlénitude'),
    (600,  800,  '#FDE8CE', '/å/ (aw)\nTransition'),
    (800,  1250, '#F8D5D5', '/a/ (ah)\nPuissance'),
    (1250, 2600, '#E8D5F0', '/e/ (eh)\nClarté'),
    (2600, 6000, '#FFF8D0', '/i/ (ee)\nBrillance'),
]


# ═══════════════════════════════════════════════════════════
# FIGURE 1 — POSITIONS FORMANTIQUES F1–F4 + Fp
# ═══════════════════════════════════════════════════════════
def make_fig1():
    n = len(instruments)
    fig, ax = plt.subplots(figsize=(14, n * 0.42 + 2), dpi=180)

    # Zones vocaliques (fond)
    for lo, hi, col, label in VOWEL_ZONES:
        if lo < 5000:
            ax.axvspan(lo, min(hi, 5000), alpha=0.28, color=col, zorder=0)
            mid = (lo + min(hi, 5000)) / 2
            ax.text(mid, n + 0.2, label, ha='center', va='bottom',
                    fontsize=6.5, color='#777', fontweight='bold',
                    transform=ax.get_xaxis_transform())

    # Cluster /o/
    ax.axvspan(400, 600, alpha=0.12, color='red', zorder=1)

    FC_COLORS = ['#D32F2F','#E64A19','#F57C00','#FBC02D']
    FC_SIZES  = [120, 80, 50, 30]
    FC_ALPHA  = [1.0, 0.85, 0.7, 0.55]

    for yi, instr in enumerate(instruments):
        fam = instr['famille']
        col = FAM_COLORS.get(fam, '#555')

        # F1–F4
        for fi, (fval, fsize, falpha) in enumerate(zip(instr['F'], FC_SIZES, FC_ALPHA)):
            if fval:
                marker = 'D' if fam in ('Cordes ens.',) else ('s' if fam=='Cuivres' else 'o')
                ax.scatter(fval, yi, s=fsize, color=FC_COLORS[fi],
                           alpha=falpha, zorder=4+fi, marker=marker,
                           edgecolors='#333', linewidths=0.5)

        # Fp (centroïde) — losange vert
        if instr['fp']:
            ax.scatter(instr['fp'], yi, s=55, color='#1B5E20', alpha=0.9,
                       zorder=9, marker='D', edgecolors='black', linewidths=0.8)

        # Ligne horizontale légère
        ax.axhline(yi, color='#e0e0e0', linewidth=0.5, zorder=1)

        # Label instrument
        ax.text(90, yi, instr['display'], ha='right', va='center',
                fontsize=7.5, color=col, fontweight='bold')

        # Ligne famille à gauche
        ax.plot([80, 83], [yi, yi], color=col, linewidth=3, zorder=3)

    ax.set_xlim(90, 5000)
    ax.set_ylim(-0.8, n - 0.2)
    ax.set_xscale('log')
    ticks = [100,150,200,300,400,500,600,800,1000,1500,2000,3000,4000,5000]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=7)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_yticks([])
    ax.set_xlabel("Fréquence (Hz)", fontsize=10, fontweight='bold')

    for s in ['top','right','left']:
        ax.spines[s].set_visible(False)

    # Séparateurs de familles
    boundaries = []
    prev = instruments[0]['famille']
    for yi, instr in enumerate(instruments):
        if instr['famille'] != prev:
            boundaries.append(yi - 0.5)
            prev = instr['famille']
    for b in boundaries:
        ax.axhline(b, color='#bbb', linewidth=1.0, linestyle='--', zorder=2)

    # Légende marqueurs
    legend_elements = [
        mlines.Line2D([],[],marker='o',color='w',markerfacecolor=FC_COLORS[0],
                      markersize=9,markeredgecolor='#333',label='F1'),
        mlines.Line2D([],[],marker='o',color='w',markerfacecolor=FC_COLORS[1],
                      markersize=7,markeredgecolor='#333',label='F2'),
        mlines.Line2D([],[],marker='o',color='w',markerfacecolor=FC_COLORS[2],
                      markersize=5.5,markeredgecolor='#333',label='F3'),
        mlines.Line2D([],[],marker='o',color='w',markerfacecolor=FC_COLORS[3],
                      markersize=4,markeredgecolor='#333',label='F4'),
        mlines.Line2D([],[],marker='D',color='w',markerfacecolor='#1B5E20',
                      markersize=7,markeredgecolor='black',label='Fp centroïde'),
    ]
    for fam, col in FAM_COLORS.items():
        legend_elements.append(mpatches.Patch(facecolor=col, label=fam))

    ax.legend(handles=legend_elements, loc='lower right', fontsize=7,
              framealpha=0.95, ncol=2, title='Marqueurs & Familles',
              title_fontsize=7.5)

    ax.set_title(
        "Figure 1 — Positions formantiques des 27 instruments de l'orchestre\n"
        "F1–F4 (cercles/losanges, taille décroissante) + Fp centroïde (◆ vert) · "
        "zones vocaliques Meyer (2009) · données CSV v22",
        fontsize=9, fontweight='bold', pad=12)

    plt.tight_layout()
    out = os.path.join(OUT_IMG, 'synthese_fig1_positions.png')
    fig.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 1 : {out}")
    return out


# ═══════════════════════════════════════════════════════════
# FIGURE 2 — ESPACE VOCALIQUE F1/F2
# ═══════════════════════════════════════════════════════════
def make_fig2():
    fig, ax = plt.subplots(figsize=(13, 9), dpi=180)

    # Zones vocaliques en fond (F1 = axe X, F2 = axe Y)
    vowel_2d = [
        (100,400,  200,800,   '#DCEEFB', '/u/\n(oo)'),
        (400,600,  500,1200,  '#D5ECD5', '/o/\n(oh)'),
        (600,800,  700,1500,  '#FDE8CE', '/å/\n(aw)'),
        (800,1250, 900,2200,  '#F8D5D5', '/a/\n(ah)'),
        (1250,2600,1100,3200, '#E8D5F0', '/e/\n(eh)'),
        (2600,4000,2000,4000, '#FFF8D0', '/i/\n(ee)'),
    ]
    for x0,x1,y0,y1,col,label in vowel_2d:
        rect = matplotlib.patches.FancyBboxPatch(
            (x0,y0), x1-x0, y1-y0,
            boxstyle='round,pad=0', facecolor=col, edgecolor='#ccc',
            alpha=0.4, zorder=0)
        ax.add_patch(rect)
        ax.text((x0+x1)/2, (y0+y1)/2, label, ha='center', va='center',
                fontsize=8, color='#888', fontweight='bold', alpha=0.8)

    # Cluster /o/ (zone F1=400-600)
    ax.axvspan(400, 600, alpha=0.08, color='red', zorder=1, label='_nolegend_')

    # Marqueurs par famille
    FAM_MARKERS = {
        'Bois': 'D', 'Saxophones': 'P',
        'Cuivres': 's', 'Cordes sol.': 'o', 'Cordes ens.': '^',
    }
    plotted = set()

    for instr in instruments:
        f1 = instr['F'][0]
        f2 = instr['F'][1]
        if not f1 or not f2:
            continue
        fam = instr['famille']
        col = FAM_COLORS.get(fam,'#555')
        marker = FAM_MARKERS.get(fam,'o')

        label_fam = fam if fam not in plotted else '_nolegend_'
        plotted.add(fam)

        ax.scatter(f1, f2, s=85, color=col, marker=marker, zorder=5,
                   edgecolors='white', linewidths=0.8,
                   label=label_fam, alpha=0.9)

        # Fp sur le même graphe (en vert, plus petit)
        if instr['fp']:
            ax.scatter(instr['fp'], f2, s=40, color='#1B5E20', marker='D',
                       zorder=6, edgecolors='black', linewidths=0.5,
                       label='_nolegend_', alpha=0.7)
            # Trait entre F1 et Fp
            ax.plot([f1, instr['fp']], [f2, f2], color='#1B5E20',
                    linewidth=0.6, alpha=0.35, zorder=3)

        # Label
        offset_x = 18
        offset_y = 15
        ax.annotate(instr['display'],
                    (f1, f2), xytext=(f1+offset_x, f2+offset_y),
                    fontsize=6.2, color=col, fontweight='bold',
                    arrowprops=dict(arrowstyle='-', color=col,
                                   lw=0.4, alpha=0.4),
                    zorder=7)

    # Ellipse cluster /o/
    from matplotlib.patches import Ellipse
    e = Ellipse((490, 750), width=220, height=800,
                angle=15, fill=False,
                edgecolor='red', linewidth=2, linestyle='--',
                zorder=8, label='Cluster /o/ (F1=388–506 Hz)')
    ax.add_patch(e)
    ax.text(490, 1200, 'Cluster /o/', ha='center', fontsize=8,
            color='red', fontweight='bold', zorder=9)

    ax.set_xlim(80, 2800)
    ax.set_ylim(200, 3500)
    ax.set_xscale('log')
    ax.set_yscale('log')
    xticks = [100,150,200,300,400,500,600,800,1000,1500,2000]
    yticks = [200,300,400,500,700,1000,1500,2000,3000]
    ax.set_xticks(xticks); ax.set_xticklabels([str(t) for t in xticks], fontsize=7)
    ax.set_yticks(yticks); ax.set_yticklabels([str(t) for t in yticks], fontsize=7)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xlabel("F1 — Premier formant (Hz)", fontsize=10, fontweight='bold')
    ax.set_ylabel("F2 — Deuxième formant (Hz)", fontsize=10, fontweight='bold')

    ax.grid(True, alpha=0.2, zorder=0)
    for s in ['top','right']:
        ax.spines[s].set_visible(False)

    # Légende famille
    handles, labels = ax.get_legend_handles_labels()
    seen = {}
    clean_h, clean_l = [], []
    for h, l in zip(handles, labels):
        if l not in seen and not l.startswith('_'):
            seen[l] = True; clean_h.append(h); clean_l.append(l)
    clean_h.append(mlines.Line2D([],[],marker='D',color='w',
                                  markerfacecolor='#1B5E20',markersize=7,
                                  markeredgecolor='black',label='Fp centroïde'))
    clean_l.append('Fp centroïde')
    ax.legend(clean_h, clean_l, loc='upper left', fontsize=8, framealpha=0.9,
              title='Familles', title_fontsize=8)

    ax.set_title(
        "Figure 2 — Espace vocalique F1/F2 des 27 instruments de l'orchestre\n"
        "Convention phonétique : F1 (horizontal) × F2 (vertical) · "
        "zones Meyer (2009) · données CSV v22",
        fontsize=9, fontweight='bold', pad=12)

    plt.tight_layout()
    out = os.path.join(OUT_IMG, 'synthese_fig2_espace_vocalique.png')
    fig.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 2 : {out}")
    return out


# ═══════════════════════════════════════════════════════════
# FIGURE 3 — CLUSTER DE CONVERGENCE (enveloppes gaussiennes)
# ═══════════════════════════════════════════════════════════
def make_fig3():
    # Instruments du cluster élargi — F1 strict CSV
    cluster_insts = [
        ('Contrebasse',  172, '#455A64', 'solid',   2.5, 'Cordes'),
        ('Trombone',     237, '#7B1FA2', 'dashed',  2.0, 'Cuivres'),
        ('Tuba basse',   226, '#37474F', 'dashed',  2.0, 'Cuivres'),
        ('Cor',          388, '#1565C0', 'solid',   2.5, 'Cuivres'),
        ('Cor anglais',  452, '#2E7D32', 'solid',   2.5, 'Bois'),
        ('Cl. Sib',      463, '#558B2F', 'dashed',  2.0, 'Bois'),
        ('Sax alto',     398, '#AD1457', 'dashdot', 2.0, 'Saxophones'),
        ('Alto',         377, '#1976D2', 'dashed',  2.0, 'Cordes'),
        ('Basson',       495, '#4E342E', 'solid',   2.5, 'Bois'),
        ('Violon',       506, '#0D47A1', 'solid',   2.5, 'Cordes'),
        ('Ens. Violons', 495, '#283593', 'dotted',  1.8, 'Cordes ens.'),
    ]

    fig, ax = plt.subplots(figsize=(14, 7), dpi=180)

    # Zones vocaliques
    for lo, hi, col, label in VOWEL_ZONES:
        if lo < 3500:
            ax.axvspan(lo, min(hi, 3500), alpha=0.22, color=col, zorder=0)
            mid = (lo + min(hi, 3500)) / 2
            ax.text(mid, 1.02, label.split('\n')[0], ha='center', va='bottom',
                    fontsize=8, color='#888', fontweight='bold',
                    transform=ax.get_xaxis_transform())

    # Zone de convergence
    ax.axvspan(377, 506, alpha=0.18, color='#e53935', zorder=1)
    ax.axvline(377, color='#e53935', linewidth=1.2, linestyle=':', alpha=0.7, zorder=2)
    ax.axvline(506, color='#e53935', linewidth=1.2, linestyle=':', alpha=0.7, zorder=2)
    ax.text(440, 0.97, "Zone de\nconvergence\n377–506 Hz",
            ha='center', va='top', fontsize=7.5, color='#C62828',
            fontweight='bold', transform=ax.get_xaxis_transform(),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#e53935', alpha=0.9))

    # Enveloppes gaussiennes centrées sur F1
    x = np.linspace(80, 3500, 2000)
    max_amp = {}

    for name, f1, color, ls, lw, fam in cluster_insts:
        # Largeur proportionnelle au registre : plus large pour les graves
        sigma = max(70, f1 * 0.20)
        y = np.exp(-0.5 * ((x - f1) / sigma) ** 2)
        ax.plot(x, y, color=color, linewidth=lw, linestyle=ls,
                label=f"{name}  F1={f1} Hz", zorder=4, alpha=0.9)
        # Marqueur F1
        ax.plot(f1, 1.0, marker='|', markersize=12, color=color,
                markeredgewidth=2.5, zorder=5)

    ax.set_xlim(80, 3000)
    ax.set_ylim(0, 1.35)
    ax.set_xscale('log')
    ticks = [100,150,200,300,400,500,600,800,1000,1500,2000,3000]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=8)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_yticks([])
    ax.set_xlabel("Fréquence (Hz) — axe logarithmique", fontsize=10, fontweight='bold')
    ax.set_ylabel("Amplitude relative (schématique)", fontsize=10)

    for s in ['top','right','left']:
        ax.spines[s].set_visible(False)

    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.95,
              ncol=2, title='Instruments (F1 strict CSV v22)',
              title_fontsize=8)

    ax.set_title(
        "Figure 3 — Cluster de convergence : enveloppes spectrales schématiques\n"
        "11 instruments dont le F1 converge dans la zone 377–506 Hz (voyelle /o/–/å/) · "
        "données CSV v22",
        fontsize=9, fontweight='bold', pad=14)

    plt.tight_layout()
    out = os.path.join(OUT_IMG, 'synthese_fig3_cluster.png')
    fig.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 3 : {out}")
    return out


if __name__ == '__main__':
    import matplotlib.ticker
    print("Génération des 3 figures de synthèse...")
    fig1 = make_fig1()
    fig2 = make_fig2()
    fig3 = make_fig3()
    print("\nTerminé.")
