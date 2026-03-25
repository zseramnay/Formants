# Résumé de session — v8 (25 mars 2026)

## Contexte

Repo: `https://github.com/zseramnay/Formants` (user: zseramnay)
Document en ligne: `https://zseramnay.github.io/Formants/Versions-html-and-docx/REFERENCE_FORMANTIQUE_COMPLETE.html`
PAT: nécessite scope `workflow` pour modifier `.github/workflows/`

## Historique rapide (v5–v7)

- **v5** : Points A–F (terminologie, clause sustained, CSV v3 39 col., fenêtrage Hann, axes Bark, σ(Fp))
- **v6** : Bandwidths -3dB, graphiques gaussiens, Fp dynamique tous instruments, anti-collision labels, note sourdines
- **v7** : dB recalculés depuis enveloppe moyenne, 47 enveloppes individuelles (toutes sourdines), bridge hill/table d'harmonie cordes, GitHub Action

## Nouveautés v8

### 1. Amplitudes dB recalculées depuis enveloppe spectrale moyenne

**Problème résolu** : les anciennes amplitudes (médiane par échantillon) donnaient F5 > F1 au violon à cause du biais tessiture (261 notes aiguës vs 9 graves). Corrigé : dB lus sur l'enveloppe **moyenne** à la fréquence de chaque formant. 468/533 profils mis à jour.

**Limitation identifiée** : sur l'enveloppe moyenne globale, F1 < F2 en dB pour certains instruments à grande tessiture (trombone, flûte, clarinette) — physiquement correct mais ne représente pas une note spécifique.

### 2. Étude pilote clarinette — analyse par registre

Étude sur Clarinette Sib (126 éch., D3–G6, ~3.5 octaves) montrant que F1 passe de 183 Hz (oct.3) à 1174 Hz (oct.6), tandis que Fp reste stable (1357–1596 Hz).

**Conclusions** :
- L'analyse par octave résout le problème F1 < F2
- L'enveloppe cepstrale (troncature ord.20 depuis spectre FFT) converge bien avec specenv Orchidea
- Le LPC classique ne fonctionne pas sur des spectres moyennés (il faudrait les .wav originaux)
- Le Fp est la mesure la plus robuste tous registres confondus

### 3. Nouvelle représentation : « Carte spectrale vocalique »

Enveloppe specenv + zones vocaliques superposées, échelle logarithmique, marqueurs F1–F6 + Fp, anti-collision v7 (au-dessus ET en dessous de la courbe), cepstrale normalisée en violet fin. Images individuelles par octave à 51% largeur.

CSS : `img[src*="carte_"] { max-width: 51%; }`

### 4. Scripts v6-html-docx — analyse par octave pour 16 instruments

Nouveau répertoire `Scripts/v6-html-docx/` (copie de v5 + extensions). Pour 16 instruments clés :

**Bois** : Flûte, Hautbois, Clarinette Sib, Basson
**Cuivres** : Cor, Trompette, Trombone, Tuba basse
**Cordes solo** : Violon, Alto, Violoncelle, Contrebasse
**Cordes ensemble** : Ens. violons, Ens. altos, Ens. violoncelles, Ens. contrebasses

Pour chaque instrument :
1. **Profil formantique moyen** (courbes de cloche) — titre mis à jour
2. **Tableau par octave** F1–F7 Hz/dB côte à côte + Fp
3. **Cartes spectrales vocaliques** individuelles par octave

Fonctions ajoutées dans `common.py` (+430 lignes) :
- `load_specenv_by_octave()`, `load_spectrum_by_octave()` (avec fallback Yan_Adds)
- `cepstral_envelope()` (troncature cepstrale ord.20)
- `make_carte_spectrale()` (v7 anti-collision above+below)
- `compute_octave_profiles()`, `make_octave_table_html()`, `generate_per_octave_html()`

### 5. Figure Bark F1×F2 (espace vocalique perceptif)

`make_fig2_bark()` ajouté dans `build_synthese_html_docx.py` et `make_synthese_figures.py` :
- Échelle Bark (Traunmüller) sur les deux axes
- Petits marqueurs (s=40) + adjustText pour anti-collision labels avec flèches
- Ticks Hz + Bark en double
- Référencée comme "Figure 2b" dans HTML et DOCX

### 6. Corrections IRCAM → Orchidea

specenv vient d'**Orchidea** (https://github.com/CarmineCella/orchidea), pas d'IRCAM.
Toutes les références corrigées dans les scripts v6 (SuperVP/AudioSculpt supprimés).

### 7. Commentaires cordes solo — bridge hill et table d'harmonie

Valeurs CSV v3 vérifiées pour les 4 instruments solistes :
- **Violon** : F1=506 Hz (/o/, caisse, σ=376), bridge hill F3–F5 (2347–3908), Fp=1253, convergence basson Δ=11
- **Alto** : F1=377 Hz (/å/, caisse, σ=202), bridge hill ~F3=1540, Fp=1300 (≈violon Δ=47)
- **Violoncelle** : F1=205 Hz (/u/, table d'harmonie, σ=287), fusion F2 vcl(506)≈F1 basson(495) Δ=11, Fp=1242
- **Contrebasse** : F1=172 Hz (/u/, caisse, σ=36 le plus stable), Fp=1235≈vcl Δ=7

Tableau doublures violon corrigé (Fp=1253, Hautbois Fp=1393, Flûte Fp=1352, Cl.Sib Fp=1296).

### 8. Section VII — 47 enveloppes spectrales individuelles

Images individuelles (au lieu de planches groupées) : 13 Bois + 16 Cuivres (toutes sourdines) + 18 Cordes (solo+sourdine+piombo+ensembles). CSS : `img[src*="specenv_"] { max-width: 60%; }`

### 9. GitHub Action

`.github/workflows/build.yml` : `workflow_dispatch` (manuel).
Installe : numpy, matplotlib, python-docx, docxcompose, adjustText.
Lance : `Scripts/v6-html-docx/build_document_complet.py`
Prérequis : Settings → Actions → General → Workflow permissions = Read and write.

## État du repo

```
Scripts/
  v5-html-docx/                                 ← version stable précédente
  v6-html-docx/                                 ← version active ★
    common.py                                   ← 1438 lignes, per-octave + carte spectrale vocalique
    build_bois_html_docx.py                     ← per-octave : Flûte, Hautbois, Cl.Sib, Basson
    build_cuivres_html_docx.py                  ← per-octave : Cor, Trompette, Trombone, Tuba
    build_cordes_html_docx.py                   ← per-octave : 4 solo + 4 ensembles, bridge hill
    build_sax_html_docx.py
    build_synthese_html_docx.py                 ← Figure 2b Bark
    build_intro_html_docx.py                    ← Orchidea (non IRCAM)
    build_envelopes_by_family_html_docx.py      ← 47 images individuelles
    build_document_complet.py                   ← CSS carte_ 51%, pointe v6
    make_synthese_figures.py                    ← fig2_bark standalone

Resultats/
  formants_all_techniques_v3.csv                ← 487 lignes, dB depuis enveloppe moyenne ★
  formants_yan_adds_v3.csv                      ← 46 lignes, idem ★
  bandwidths_3db.csv                            ← 533 profils BW -3dB

.github/workflows/build.yml                    ← manual trigger, v6, adjustText
```

## Consignes pour la suite

- **Toujours montrer une image prototype avant de régénérer les images**
- **Toujours demander l'aval avant push**
- **Ne pas lancer build_document_complet localement** — fait via GitHub Action
- **Ne rien faire sans demander avant**
- specenv vient d'**Orchidea** (pas IRCAM)
- Fichiers specenv : `Data/FullSOL2020_specenv par instrument/` et `Data/Yan_Adds-Divers_specenv par instrument/`
- Fichiers spectrum (FFT) : `Data/FullSOL2020.spectrum_par_instrument/` et `Data/Yan_Adds-Divers.spectrum_par_instrument/`

## Workflow git

```bash
git clone https://github.com/zseramnay/Formants.git
cd Formants
git config user.name "Claude" && git config user.email "claude@anthropic.com"
git remote set-url origin https://[PAT]@github.com/zseramnay/Formants.git
git push origin main
git remote set-url origin https://github.com/zseramnay/Formants.git
```

## Ce qu'on ne change PAS

- Pas de renommage F1→P1/P2 (note terminologique suffit)
- Pas de transitions formantiques/diphthongaison (hors scope, sustained only)
- Pas de normalisation morphologique (non pertinent pour instruments)

## Sur l'horizon

- **Analyse LPC** nécessiterait accès aux .wav originaux SOL2020
- Extension répertoire spectral contemporain (Grisey, Murail, Saariaho, Haas, Radulescu)
- Méthodologie d'extraction de doublures depuis partitions + analyse spectrale d'enregistrements
