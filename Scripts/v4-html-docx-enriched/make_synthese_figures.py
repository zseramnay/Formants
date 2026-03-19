#!/usr/bin/env python3
"""
make_synthese_figures.py — Fig 1/2/3 synthèse, données CSV v22
"""
import os, sys, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT_IMG, BASE
os.makedirs(OUT_IMG, exist_ok=True)

DATA = {}
for path in [os.path.join(BASE,'Resultats','formants_all_techniques.csv'),
             os.path.join(BASE,'Resultats','formants_yan_adds.csv')]:
    with open(path) as f:
        for r in csv.DictReader(f):
            if r['technique'] in ('ordinario','non-vibrato'):
                k = (r['instrument'],r['technique'])
                if k not in DATA: DATA[k]=r

FP = {'Piccolo':None,'Flute':1535,'Bass_Flute':1338,'Contrabass_Flute':1092,
      'Oboe':1485,'English_Horn':1135,'Clarinet_Eb':1266,'Clarinet_Bb':1412,
      'Bass_Clarinet_Bb':1204,'Contrabass_Clarinet_Bb':1090,'Bassoon':1079,
      'Contrabassoon':1279,'Sax_Alto':1440,'Horn':738,'Trumpet_C':1046,
      'Trombone':1218,'Bass_Trombone':1335,'Bass_Tuba':1239,'Contrabass_Tuba':1182,
      'Violin':893,'Viola':None,'Violoncello':None,'Contrabass':None,
      'Violin_Ensemble':None,'Viola_Ensemble':None,
      'Violoncello_Ensemble':None,'Contrabass_Ensemble':None}

DISPLAY = {'Piccolo':'Petite flûte','Flute':'Flûte','Bass_Flute':'Flûte basse',
           'Contrabass_Flute':'Fl. CB','Oboe':'Hautbois','English_Horn':'Cor anglais',
           'Clarinet_Eb':'Cl. Mib','Clarinet_Bb':'Cl. Sib',
           'Bass_Clarinet_Bb':'Cl. basse','Contrabass_Clarinet_Bb':'Cl. CB',
           'Bassoon':'Basson','Contrabassoon':'Contrebasson','Sax_Alto':'Sax alto',
           'Horn':'Cor','Trumpet_C':'Trompette','Trombone':'Trombone',
           'Bass_Trombone':'Trb. basse','Bass_Tuba':'Tuba basse','Contrabass_Tuba':'Tuba CB',
           'Violin':'Violon','Viola':'Alto','Violoncello':'Violoncelle',
           'Contrabass':'Contrebasse','Violin_Ensemble':'Ens. Violons',
           'Viola_Ensemble':'Ens. Altos','Violoncello_Ensemble':'Ens. Vcl.',
           'Contrabass_Ensemble':'Ens. CB'}

FAMILLE = {'Piccolo':'Bois','Flute':'Bois','Bass_Flute':'Bois','Contrabass_Flute':'Bois',
           'Oboe':'Bois','English_Horn':'Bois','Clarinet_Eb':'Bois','Clarinet_Bb':'Bois',
           'Bass_Clarinet_Bb':'Bois','Contrabass_Clarinet_Bb':'Bois',
           'Bassoon':'Bois','Contrabassoon':'Bois','Sax_Alto':'Saxophones',
           'Horn':'Cuivres','Trumpet_C':'Cuivres','Trombone':'Cuivres',
           'Bass_Trombone':'Cuivres','Bass_Tuba':'Cuivres','Contrabass_Tuba':'Cuivres',
           'Violin':'Cordes sol.','Viola':'Cordes sol.','Violoncello':'Cordes sol.',
           'Contrabass':'Cordes sol.','Violin_Ensemble':'Cordes ens.',
           'Viola_Ensemble':'Cordes ens.','Violoncello_Ensemble':'Cordes ens.',
           'Contrabass_Ensemble':'Cordes ens.'}

FAM_COLORS = {'Bois':'#2E7D32','Saxophones':'#AD1457','Cuivres':'#B71C1C',
              'Cordes sol.':'#1565C0','Cordes ens.':'#0D47A1'}

ORDER = ['Contrabass_Ensemble','Contrabass','Violoncello_Ensemble','Violoncello',
         'Viola_Ensemble','Viola','Violin_Ensemble','Violin',
         'Contrabass_Tuba','Bass_Tuba','Bass_Trombone','Trombone','Horn','Trumpet_C',
         'Sax_Alto','Contrabassoon','Contrabass_Clarinet_Bb','Bass_Clarinet_Bb',
         'Bassoon','Clarinet_Bb','English_Horn','Clarinet_Eb',
         'Oboe','Contrabass_Flute','Bass_Flute','Flute','Piccolo']

instruments = []
for inst in ORDER:
    r = DATA.get((inst,'ordinario')) or DATA.get((inst,'non-vibrato'))
    if not r: continue
    fs = [round(float(r[f'F{i}_hz'])) if float(r.get(f'F{i}_hz',0) or 0)>0 else None
          for i in range(1,5)]
    instruments.append({'csv':inst,'display':DISPLAY.get(inst,inst),
                        'famille':FAMILLE.get(inst,'Autre'),'F':fs,'fp':FP.get(inst)})

VOWEL_ZONES = [(100,400,'#DCEEFB','/u/'),(400,600,'#D5ECD5','/o/'),
               (600,800,'#FDE8CE','/å/'),(800,1250,'#F8D5D5','/a/'),
               (1250,2600,'#E8D5F0','/e/'),(2600,5000,'#FFF8D0','/i/')]


def make_fig1():
    """Fig 1 — Positions formantiques F1-F4 + Fp, axe horizontal."""
    n = len(instruments)
    fig_h = n * 0.38 + 1.8  # hauteur proportionnelle, pas de tight_layout
    fig, ax = plt.subplots(figsize=(15, fig_h), dpi=150)

    for lo, hi, col, _ in VOWEL_ZONES:
        ax.axvspan(lo, hi, alpha=0.25, color=col, zorder=0)
    ax.axvspan(377, 510, alpha=0.12, color='red', zorder=1)

    # Labels zones en haut du graphe
    for lo, hi, col, label in VOWEL_ZONES:
        mid = np.sqrt(lo * min(hi, 4000))
        if mid < 4000:
            ax.text(mid, n - 0.3, label, ha='center', va='bottom',
                    fontsize=6, color='#666', fontweight='bold')

    FC = ['#D32F2F','#E64A19','#F57C00','#FBC02D']
    SZ = [100, 65, 42, 22]

    for yi, instr in enumerate(instruments):
        fam = instr['famille']
        col = FAM_COLORS.get(fam, '#555')
        mk  = ('^' if 'ens' in fam.lower() else
               's' if fam == 'Cuivres' else
               'P' if fam == 'Saxophones' else 'o')
        for fi, (fv, sz) in enumerate(zip(instr['F'], SZ)):
            if fv:
                ax.scatter(fv, yi, s=sz, color=FC[fi],
                           alpha=1.0 - fi*0.15, zorder=4+fi,
                           marker=mk, edgecolors='white', linewidths=0.3)
        if instr['fp']:
            ax.scatter(instr['fp'], yi, s=42, color='#1B5E20',
                       zorder=9, marker='D', edgecolors='black', linewidths=0.6)
        ax.axhline(yi, color='#ebebeb', lw=0.4, zorder=1)

    # Séparateurs familles
    prev = instruments[0]['famille']
    for yi, instr in enumerate(instruments):
        if instr['famille'] != prev:
            ax.axhline(yi - 0.5, color='#bbb', lw=0.8, ls='--', zorder=2)
            prev = instr['famille']

    ax.set_xlim(100, 4500)
    ax.set_ylim(-0.8, n - 0.1)
    ax.set_xscale('log')
    ticks = [100, 200, 300, 400, 500, 700, 1000, 1500, 2000, 3000, 4000]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=8)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_xlabel("Fréquence (Hz)", fontsize=10, fontweight='bold')

    ax.set_yticks(range(n))
    ax.set_yticklabels([i['display'] for i in instruments], fontsize=7.5)
    for i, instr in enumerate(instruments):
        tk = ax.get_yticklabels()[i]
        tk.set_color(FAM_COLORS.get(instr['famille'], '#555'))
        tk.set_fontweight('bold')

    for s in ['top','right']:
        ax.spines[s].set_visible(False)

    leg = [mlines.Line2D([],[],marker='o',color='w',markerfacecolor=c,markersize=s,label=l)
           for c,s,l in zip(FC,[8,6,5,3.5],['F1','F2','F3','F4'])]
    leg.append(mlines.Line2D([],[],marker='D',color='w',markerfacecolor='#1B5E20',
                              markeredgecolor='black',markersize=6,label='Fp centroïde'))
    for fam, col in FAM_COLORS.items():
        leg.append(mpatches.Patch(facecolor=col, label=fam))
    ax.legend(handles=leg, loc='lower right', fontsize=7, framealpha=0.95,
              ncol=2, title='Marqueurs / Familles', title_fontsize=7.5)

    ax.set_title("Figure 1 — Positions formantiques des 27 instruments · "
                 "F1–F4 + Fp centroïde · zones Meyer (2009) · CSV v22",
                 fontsize=9, fontweight='bold', pad=8)

    fig.subplots_adjust(left=0.14, right=0.97, top=0.95, bottom=0.07)
    out = os.path.join(OUT_IMG, 'synthese_fig1_positions.png')
    fig.savefig(out, dpi=150, facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 1 : {out}")
    return out


def make_fig2():
    """Fig 2 — Espace vocalique F1/F2."""
    fig, ax = plt.subplots(figsize=(13, 9), dpi=150)

    for lo, hi, col, label in VOWEL_ZONES:
        if lo < 3000:
            ax.axvspan(lo, min(hi,3000), alpha=0.20, color=col, zorder=0, ymin=0, ymax=1)

    FAM_MK = {'Bois':'D','Saxophones':'P','Cuivres':'s',
               'Cordes sol.':'o','Cordes ens.':'^'}
    seen = set()
    for instr in instruments:
        f1, f2 = instr['F'][0], instr['F'][1]
        if not f1 or not f2: continue
        fam = instr['famille']
        col = FAM_COLORS.get(fam,'#555')
        mk  = FAM_MK.get(fam,'o')
        lbl = fam if fam not in seen else '_'
        seen.add(fam)
        ax.scatter(f1, f2, s=80, color=col, marker=mk,
                   edgecolors='white', linewidths=0.7,
                   zorder=5, label=lbl, alpha=0.9)
        if instr['fp']:
            ax.scatter(instr['fp'], f2, s=32, color='#1B5E20',
                       marker='D', edgecolors='black', lw=0.5, zorder=6, alpha=0.75, label='_')
            ax.plot([f1, instr['fp']], [f2,f2], color='#1B5E20', lw=0.6, alpha=0.3, zorder=3)
        ax.annotate(instr['display'], (f1, f2), xytext=(5,3),
                    textcoords='offset points', fontsize=6,
                    color=col, fontweight='bold', zorder=7)

    # Ellipse convergence
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((443, 820), width=195, height=950, angle=12,
                          fill=False, edgecolor='red', lw=2, ls='--', zorder=8))
    ax.text(443, 1400, 'Zone /o/–/å/\n377–510 Hz',
            ha='center', fontsize=8, color='red', fontweight='bold', zorder=9)

    ax.set_xlim(80, 2800); ax.set_ylim(200, 3800)
    ax.set_xscale('log'); ax.set_yscale('log')
    xt = [100,150,200,300,400,600,800,1200,2000]
    yt = [200,300,500,700,1000,1500,2000,3000]
    ax.set_xticks(xt); ax.set_xticklabels([str(t) for t in xt], fontsize=7.5)
    ax.set_yticks(yt); ax.set_yticklabels([str(t) for t in yt], fontsize=7.5)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xlabel("F1 — Premier formant (Hz)", fontsize=10, fontweight='bold')
    ax.set_ylabel("F2 — Deuxième formant (Hz)", fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.14)
    for s in ['top','right']: ax.spines[s].set_visible(False)

    hs, ls2 = ax.get_legend_handles_labels()
    ch, cl = [], []
    seen2 = set()
    for h, l in zip(hs, ls2):
        if l not in seen2 and not l.startswith('_'):
            seen2.add(l); ch.append(h); cl.append(l)
    ch.append(mlines.Line2D([],[],marker='D',color='w',markerfacecolor='#1B5E20',
                              markeredgecolor='black',markersize=7,label='Fp centroïde'))
    cl.append('Fp centroïde')
    ax.legend(ch, cl, loc='upper left', fontsize=8, framealpha=0.9,
              title='Familles', title_fontsize=8)

    ax.set_title("Figure 2 — Espace vocalique F1/F2 · convention phonétique · "
                 "ellipse = zone de convergence · CSV v22",
                 fontsize=9, fontweight='bold', pad=10)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.09)
    out = os.path.join(OUT_IMG, 'synthese_fig2_espace_vocalique.png')
    fig.savefig(out, dpi=150, facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 2 : {out}")
    return out


def make_fig3():
    """Fig 3 — Enveloppes gaussiennes cluster convergence."""
    cluster = [
        ('Contrebasse', 172,'#546E7A','dotted', 1.6,'Cordes sol.'),
        ('Tuba CB',     226,'#37474F','dashdot',1.8,'Cuivres'),
        ('Trombone',    237,'#7B1FA2','dashed', 2.0,'Cuivres'),
        ('Tuba basse',  226,'#616161','dotted', 1.6,'Cuivres'),
        ('Cor',         388,'#1565C0','solid',  2.5,'Cuivres'),
        ('Alto',        377,'#1976D2','dashed', 1.8,'Cordes sol.'),
        ('Sax alto',    398,'#AD1457','dashdot',2.0,'Saxophones'),
        ('Cor anglais', 452,'#2E7D32','solid',  2.5,'Bois'),
        ('Cl. Sib',     463,'#558B2F','dashed', 2.0,'Bois'),
        ('Basson',      495,'#4E342E','solid',  2.5,'Bois'),
        ('Violon',      506,'#0D47A1','solid',  2.5,'Cordes sol.'),
    ]
    fig, ax = plt.subplots(figsize=(14, 6.5), dpi=150)

    for lo, hi, col, label in VOWEL_ZONES:
        if lo < 3000:
            ax.axvspan(lo, min(hi,3000), alpha=0.20, color=col, zorder=0)
            mid = np.sqrt(lo * min(hi,3000))
            ax.text(mid, 1.01, label, ha='center', va='bottom', fontsize=8,
                    color='#777', fontweight='bold',
                    transform=ax.get_xaxis_transform())

    ax.axvspan(377, 510, alpha=0.14, color='#e53935', zorder=1)
    ax.axvline(377, color='#e53935', lw=1.2, ls=':', alpha=0.8, zorder=2)
    ax.axvline(510, color='#e53935', lw=1.2, ls=':', alpha=0.8, zorder=2)
    ax.text(443, 0.97, "Zone convergence\n377–510 Hz",
            ha='center', va='top', fontsize=7.5, color='#C62828', fontweight='bold',
            transform=ax.get_xaxis_transform(),
            bbox=dict(boxstyle='round,pad=0.3',fc='white',ec='#e53935',alpha=0.92))

    x = np.linspace(100, 3000, 3000)
    for name, f1, color, ls, lw, fam in cluster:
        sigma = max(55, f1 * 0.18)
        y = np.exp(-0.5 * ((x - f1) / sigma) ** 2)
        ax.plot(x, y, color=color, lw=lw, ls=ls, alpha=0.9,
                label=f"{name}  F1={f1} Hz", zorder=4)
        ax.plot(f1, 1.0, marker='|', ms=14, color=color, mew=2.5, zorder=5)

    ax.set_xlim(100, 3000); ax.set_ylim(0, 1.22)
    ax.set_xscale('log')
    ticks = [100,150,200,300,400,500,700,1000,1500,2000,3000]
    ax.set_xticks(ticks); ax.set_xticklabels([str(t) for t in ticks], fontsize=8)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_yticks([])
    ax.set_xlabel("Fréquence (Hz) — axe logarithmique", fontsize=10, fontweight='bold')
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.95,
              ncol=2, title='Instruments (F1 strict CSV v22)', title_fontsize=8)
    ax.set_title("Figure 3 — Enveloppes spectrales schématiques : "
                 "11 instruments en zone /o/–/å/ · CSV v22",
                 fontsize=9, fontweight='bold', pad=10)

    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.10)
    out = os.path.join(OUT_IMG, 'synthese_fig3_cluster.png')
    fig.savefig(out, dpi=150, facecolor='white')
    plt.close(fig)
    print(f"  ✓ Figure 3 : {out}")
    return out


if __name__ == '__main__':
    print("Génération des 3 figures de synthèse...")
    make_fig1()
    make_fig2()
    make_fig3()
    print("Terminé.")
