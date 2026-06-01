# Résumé de session — v8 (26 mars 2026)

## Contexte

Repo: `https://github.com/zseramnay/Formants` (user: zseramnay)
Document: `https://zseramnay.github.io/Formants/Versions-html-and-docx/REFERENCE_FORMANTIQUE_COMPLETE.html`

## Scripts actifs: `Scripts/v6-html-docx/`

11 fichiers Python. `common.py` ~1600 lignes. Build via GitHub Action (`workflow_dispatch`).

## CSV v3

- `formants_all_techniques_v3.csv` — 487 lignes, 39 colonnes, dB depuis enveloppe moyenne
- `formants_yan_adds_v3.csv` — 46 lignes
- `bandwidths_3db.csv` — 533 profils BW -3dB

## Ce qui a été fait (v5–v8)

### Données et pipeline
- dB recalculés depuis enveloppe spectrale moyenne (468/533 profils)
- CSV v3 avec 39 colonnes (F1-F6 Hz/dB, BW, σ, Fp, n)
- Audit global 16/16 instruments reproduced à Δ=0 Hz
- IRCAM → Orchidea corrigé partout

### Représentations graphiques
- **Profil formantique moyen** (courbes de cloche gaussiennes, BW -3dB)
- **Carte spectrale vocalique** (enveloppe specenv + zones vocaliques, échelle log, anti-collision pixel-based label-vs-courbe, cepstrale ord.30, labels fontsize 7)
- **47 enveloppes spectrales individuelles** (13 bois + 16 cuivres sourdines + 18 cordes)
- **Figure 2b — Espace vocalique F1/F2 en Bark** (Traunmüller, adjustText, style aligné sur Fig 2)
- **Encadré méthodologique** profil formantique vs carte spectrale vocalique

### Analyse par registre (16+1 instruments)
Source: `registres.md`. Notes frontières dans les deux registres adjacents.
- Flûte, Hautbois, Clarinette Sib, **Clarinette basse**, Basson (bois)
- Cor, Trompette, Trombone, Tuba basse (cuivres)
- Violon, Alto, Violoncelle, Contrebasse (cordes solo)
- 4 ensembles (cordes)

Pour chaque instrument: tableau par registre (F1-F7 Hz/dB + Fp) + cartes spectrales vocaliques individuelles. **Présent dans HTML et DOCX.**

### Synthèse
- **9 principes d'orchestration acoustique** (était 6) :
  - P7: convergences spécifiques au registre
  - P8: super-cluster médium 323 Hz (flûte+cor+trompette+alto)
  - P9: stabilité Fp comme signature structurelle
- **Doublures par registre** — tableaux Δ=0 et Δ=11 Hz avec signification orchestrale
- **Seuils de fusion en Bark** : ≤0,3 Bark quasi-parfaite, 0,3–0,7 efficace, ≥1,5 complémentaire
- **Tableau Fp_ref centralisé** — 12 instruments : bande, σ(Fp), contexte solo/ens/sourdine, N
- **Commentaires par registre** pour les 16 instruments clés (convergences, doublures)

### Corrections audit Copilot (v8c)
1. Violon Fp: solo=893, ens.=970, sourdine=variable — documenté dans Fp_ref et ANALYSIS
2. Clarinette Sib: Fp_ref=1412 Hz (réf.), variante 1296 Hz en note
3. Seuils en Bark ajoutés aux principes et matrices
4. Tableau Fp_ref centralisé (HTML + DOCX)
5. F1 terminologie: note terminologique déjà en place dans intro

### Corrections visuelles
- Sidebar: trompette sourdines avant trombone sourdines
- Cartes spectrales: anti-collision pixel-based (label-vs-courbe + label-vs-label), fig 9×5, lw=2, cepstrale ord.30 lw=0.9, labels fontsize 7
- Fig2b Bark: style aligné sur Fig 2 (figsize, scatter size, fontweight, arrowstyle, grid)

## Consignes

- **Prototype avant images, aval avant push, pas de build local**
- specenv vient d'**Orchidea** (pas IRCAM)
- Notes frontières dans les **deux** registres adjacents
- `registres.md` = source des registres instrumentaux

## Workflow git

```bash
git clone https://github.com/zseramnay/Formants.git
cd Formants && git config user.name "Claude" && git config user.email "claude@anthropic.com"
git remote set-url origin https://[PAT]@github.com/zseramnay/Formants.git
# ... work ...
git push origin main
git remote set-url origin https://github.com/zseramnay/Formants.git
```

## Sur l'horizon

- LPC nécessiterait accès aux .wav originaux SOL2020
- Extension répertoire spectral contemporain (Grisey, Murail, Saariaho, Haas, Radulescu)
- Nuage F1×Fp (Bark) de synthèse (suggestion audit)
