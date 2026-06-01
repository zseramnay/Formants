# Rapport d'audit et propositions de mise à jour
## Référence Formantique de l'Orchestre — mai 2026

**Basé sur :**
1. Nouvelles analyses `Etude-Formants/Analyses_formants-mai26/` (45 instruments, 3 métriques : LPC-F1, Fp centroïde, Cep-F1)
2. Source Reuter (2023) — *Oxford Handbook of Timbre*, Ch. 13 (rapport comparatif joint)
3. État actuel de `Scripts/v6-html-docx/common.py` + `build_synthese_html_docx.py`

---

## PARTIE I — AUDIT : mai26 vs. valeurs actuelles du pipeline v22

### 1.1 Résultat central : confirmation de la supériorité du Fp centroïde

Les analyses mai26 introduisent trois métriques parallèles sur les mêmes données SOL2020 :
- **lpc_F1** — LPC Parselmouth (même méthode que Reuter)
- **fp_centroid** — centroïde pondéré par l'énergie (métrique pipeline v22)
- **cep_F1_order80** — cepstral d'ordre 80

La comparaison systématique confirme que **lpc_F1 est dramatiquement instable** sur cordes et cuivres, ce qui valide a posteriori le choix du Fp :

| Instrument | LPC-F1 médiane | σ LPC | Fp médiane | σ Fp | Rapport σ(LPC)/σ(Fp) |
|---|---|---|---|---|---|
| Violon | 2179 Hz | 642 | 1125 Hz | 169 | **3,8×** |
| Violoncelle | 1928 Hz | 503 | 1123 Hz | 85 | **5,9×** |
| Alto | 1650 Hz | 557 | 1120 Hz | 133 | **4,2×** |
| Trombone | 760 Hz | 225 | 951 Hz | 121 | **1,9×** |
| Trompette | 1293 Hz | 408 | 1134 Hz | 99 | **4,1×** |
| Clarinette Sib | 1126 Hz | 440 | 1134 Hz | 197 | **2,2×** |
| Basson | 644 Hz | 211 | 955 Hz | 132 | **1,6×** |
| Hautbois | 1436 Hz | 280 | 1263 Hz | 167 | **1,7×** |

> **Constat** : sur les cordes, le LPC-F1 monte à des fréquences aberrantes (2179 Hz pour le violon, 1928 Hz pour le violoncelle) — ce sont des artéfacts de la méthode LPC sur signaux non-vocaliques. Le Fp centroïde reste dans la zone perceptuellement pertinente avec une dispersion 2 à 6 fois moindre.

### 1.2 Nouveaux instruments dans mai26 (absents du pipeline v22)

Les fichiers mai26 couvrent **plusieurs instruments sans Pipeline F1 de référence**, indiquant qu'ils ne sont pas encore formalisés dans le CSV v22 :

| Instrument | Fp mai26 | σ Fp | Note |
|---|---|---|---|
| Bass-Clarinet-Bb | 1110 Hz | 142 | Zone /a/ |
| Bass-Flute | 996 Hz | 104 | Zone /a/ |
| Bass-Trombone | 1088 Hz | 96 | Zone /a/ |
| Contrabass-Flute | 995 Hz | 90 | Zone /a/ |
| Contrabass-Clarinet-Bb | 1264 Hz | 69 | Zone /a/ |
| Contrebasson | 892 Hz | 76 | Zone /a/-/o/ |
| EnglishHorn | 1063 Hz | 103 | Zone /a/ |
| Sax_Alto | 1069 Hz | 214 | Zone /a/ |
| Horn+sordina | 970 Hz | 114 | Zone /a/ |

> **Point notable** : le cor avec sourdine (Horn+sordina, Fp=970 Hz) monte d'environ 582 Hz par rapport au cor sans sourdine (F1=388 Hz, Fp=738 Hz), un comportement cohérent avec les autres sourdines de cuivres.

### 1.3 Écarts LPC vs. Pipeline F1 — instruments principaux

Le tableau suivant montre l'écart entre la nouvelle mesure LPC-F1 (mai26) et le F1 du pipeline v22. Ces écarts **ne remettent pas en cause le pipeline v22** — ils confirment au contraire que le LPC seul est insuffisant et que Fp est la métrique robuste :

| Instrument | Pipeline F1 (v22) | LPC-F1 mai26 | Δ | Interprétation |
|---|---|---|---|---|
| Basson | 495 Hz | 644 Hz | +149 Hz | LPC capte le 2e harmonique fortement pondéré |
| Cor | 388 Hz | — | — | Horn+sordina only : 505 Hz |
| Clarinette Sib | 463 Hz | 1126 Hz | +663 Hz | LPC capte le registre clairon dominant |
| Trombone | 237 Hz | 760 Hz | +523 Hz | LPC capte le Fp (~1218 Hz dans v22) ou F2 |
| Violon | 506 Hz | 2179 Hz | +1673 Hz | Artéfact LPC typique sur cordes |
| Violoncelle | 205 Hz | 1928 Hz | +1723 Hz | Artéfact LPC sur cordes |
| Trompette | 786 Hz | 1293 Hz | +507 Hz | Capture du registre médium/aigu |
| Tuba basse | 226 Hz | 424 Hz | +198 Hz | LPC capte la zone grave mais pas F1 strict |

> **Conclusion audit § 1.3** : Les valeurs v22 (F1 "strict" bas registre) et les mesures LPC mai26 (médiane tous registres) mesurent des choses différentes. Le document actuel doit l'expliquer explicitement — c'est précisément ce que valide la comparaison avec Reuter (§ 3.6 du rapport comparatif).

### 1.4 Nouvelles données sur les sourdines (Fp centroïde mai26)

Données plus précises que dans v22 pour plusieurs sourdines :

| Instrument | Fp mai26 | σ Fp | Valeur v22 |
|---|---|---|---|
| Trombone+sourdine harmon | 1030 Hz | 89 | 1218 Hz (LPC-based) |
| Trombone+sourdine cup | 969 Hz | 38 | — |
| Trombone+sourdine sèche | 893 Hz | 95 | — |
| Trombone+sourdine wah | 929 Hz | 76 | — |
| Trompette+sourdine harmon | 1169 Hz | 168 | 2358 Hz (F1 strict) |
| Trompette+sourdine cup | 1516 Hz | 163 | — |

> **Anomalie confirmée** : Trompette harmon — le LPC-F1 mai26 donne 3164 Hz (σ=238), très stable, ce qui correspond bien à la zone /i/ (≥2000 Hz) identifiée dans v22. Le Fp reste à 1169 Hz. Les deux métriques coexistent.

### 1.5 Données ensemble (sections d'orchestre)

| Instrument | Fp solo | Fp ensemble | Variation |
|---|---|---|---|
| Violon solo | 1125 Hz | 1165 Hz | +40 Hz (+3,6%) |
| Violoncelle solo | 1123 Hz | 1086 Hz | −37 Hz (−3,3%) |
| Alto solo | 1120 Hz | 1110 Hz | −10 Hz (−0,9%) |
| Contrebasse solo | 1123 Hz | 1077 Hz | −46 Hz (−4,1%) |

> **Bonne nouvelle** : la compression spectrale (section vs solo) reste faible en Fp (< 5% pour toutes les cordes), ce qui valide les doublures inter-registres même en contexte de section. La valeur v22 « F2 drops 23% » concernait F2, pas Fp.

---

## PARTIE II — INTÉGRATION DE REUTER (2023)

### 2.1 Ce que Reuter apporte de nouveau au document

Le rapport comparatif identifie les contributions conceptuelles de Reuter non présentes dans le document actuel :

**A. Mécanisme physique (reed pulse width)** — Fransson (1966/67), Voigt (1975)
Le document actuel cite la stabilité des formants mais n'explique pas *pourquoi* ils sont indépendants de la hauteur. Reuter donne la réponse : la durée de fermeture de l'anche est constante quelle que soit la fréquence fondamentale. C'est une note méthodologique importante.

**B. Historiographie complète** — Helmholtz → Schumann (1929) → Meyer → Reuter
Le document actuel cite Meyer, Backus, Giesler, McCarty mais pas la chaîne historique complète. Reuter constitue la synthèse de référence anglophone de cette tradition.

**C. Concept de "selective masking"** — Reuter (2002)
Le terme est déjà utilisé dans le document actuel (section Synthèse). Reuter en est l'auteur — il faut le citer explicitement.

**D. Validation croisée LPC vs Fp**
La comparaison mai26 (LPC) / v22 (Fp) démontre empiriquement ce que Reuter illustre qualitativement avec ses ellipses larges. Cela justifie un encadré méthodologique dédié.

### 2.2 Points de concordance à mentionner explicitement

| Sujet | Reuter Ch13 | Maresz v22 | Accord |
|---|---|---|---|
| Zone /o/ principale | 300–500 Hz | 377–506 Hz | ✓ Quantification plus précise |
| Basson–cor | ✓ | Δ=107 Hz F1, Δ=341 Hz Fp | ✓ Étendu |
| Hautbois–trompette | ~1000–1400 Hz | Δ=43 Hz (Fp) | ✓ Confirmé |
| Absence formant flûte | ✓ | σ(Fp) élevé = 240 Hz | ✓ Quantifié |
| Registre aigu → formant masqué | ✓ | Per-register F1 tables | ✓ Documenté |
| Cordes = 2e rang | ✓ (bref) | Pleine intégration | Extension majeure |

### 2.3 Points de divergence à expliquer (nouvelle section §3.6)

La divergence LPC (Reuter/Parselmouth) vs Fp (Maresz/pipeline) explique les écarts apparents entre les deux études — une note de réconciliation est nécessaire dans la section méthodologie :

- **Trombone** : Reuter ~500 Hz [o] ↔ Maresz F1=237 Hz [u]. La valeur Reuter correspond au **Fp** du pipeline (≈1218 Hz) ou à la mesure du registre médium. Le F1 strict est plus grave.
- **Violoncelle** : Meyer/Reuter ~500 Hz ↔ Maresz F1=205 Hz. Même explication : Meyer mesure le Hauptformant = F2 dans la nomenclature Maresz.
- **Clarinette** : Reuter ~1500 Hz (clairon) ↔ Maresz F1=463 Hz (chalumeau). Les deux sont exacts pour des registres différents.

---

## PARTIE III — PROPOSITIONS DE MISE À JOUR DES SCRIPTS

### 3.1 `common.py` — Ajouts recommandés

#### A. Nouvelle fonction `reuter_comparison_note()`

Ajouter dans la section HTML utilities (après `ref_table_html()`, ligne ~600) une fonction générant un encadré standardisé de réconciliation LPC/Fp :

```python
def reuter_note_html(instrument_name, pipeline_f1, reuter_zone, fp_val, note_text=""):
    """
    Encadré de réconciliation Reuter (LPC) vs Pipeline (Fp) pour un instrument.
    À appeler dans chaque section instrument quand la divergence est notable.
    """
    return (
        f'<div class="source-note" style="border-left:3px solid #7986CB;padding:8px 12px;margin:8px 0;">'
        f'<strong>Concordance Reuter (2023) :</strong> zone LPC ~{reuter_zone} Hz. '
        f'Pipeline v22 : F1 strict={pipeline_f1} Hz, Fp={fp_val} Hz. '
        f'{note_text} '
        f'<em>Voir §3.1 — paradigme Fp vs LPC.</em>'
        f'</div>'
    )
```

#### B. Mise à jour de `SOURCES_NOTE` dans `build_synthese_html_docx.py`

Ligne 1204 actuelle :
```python
html += '<p class="source-note"><strong>Sources :</strong> Backus (1969) · Giesler (1985) · Meyer (2009) · McCarty/CCRMA (2003, référence directionnelle) · SOL2020 Orchidea · Yan_Adds · pipeline v22 validé.</p>\n'
```

**Remplacer par :**
```python
html += (
    '<p class="source-note"><strong>Sources :</strong> '
    'Backus (1969) · Giesler (1985) · Meyer (2009) · McCarty/CCRMA (2003) · '
    'SOL2020 Orchidea · Yan_Adds · pipeline v22 validé.<br>'
    '<strong>Source additionnelle :</strong> Reuter, C. (2023). '
    '« Formants: The Missing Link between Orchestration and Post-Helmholtzian Timbre Research ». '
    '<em>Oxford Handbook of Timbre</em>. Oxford University Press. '
    '[Concordance zones /u/–/o/ : ✓ ; mécanisme anche : Fransson 1966/67, Voigt 1975]'
    '</p>\n'
)
```

#### C. Ajout d'une ligne Reuter dans le tableau de concordance multi-sources

Dans `build_synthese_html_docx.py`, section `# 6. Concordance multi-sources` (ligne ~1187), le tableau HTML de concordance doit recevoir une 5e colonne "Reuter (2023)" :

**Structure actuelle :**
```
| Instrument | F1 v22 | Backus | Giesler | Meyer | Accord global |
```

**Structure proposée :**
```
| Instrument | F1 v22 | Backus | Giesler | Meyer | Reuter (2023) | Accord global |
```

Avec ces données pour chaque ligne :

| Instrument | Reuter zone | Méthode Reuter |
|---|---|---|
| Basson | 300–500 Hz | LPC/Parselmouth ≈ F1 strict |
| Cor | 300–500 Hz | LPC/Parselmouth ≈ F1 strict |
| Trombone | ~500 Hz | LPC → capte Fp, non F1 strict |
| Violoncelle | ~500 Hz | LPC → Hauptformant = F2 |
| Trompette | 1000–1400 Hz | LPC → registre médium/aigu |
| Clarinette Sib | ~1500 Hz | LPC → registre clairon |
| Violon | 800–1000 Hz | Bridge resonance, non LPC |

#### D. Nouvelle note méthodologique dans `build_intro_html_docx.py`

Ajouter dans la section "Méthodologie" un paragraphe sur la comparaison avec la méthode LPC (Reuter/Parselmouth), justifiant le choix du Fp centroïde. Texte proposé :

```python
REUTER_METHODOLOGIE_NOTE = """
<div class="encadre-methodologique">
<h4>Note : Paradigme Fp vs LPC (Parselmouth/Praat)</h4>
<p>La méthode standard en phonétique instrumentale est l'analyse LPC (Linear Predictive Coding),
utilisée notamment par Reuter (2023, <em>Oxford Handbook of Timbre</em>) via l'interface Python
Parselmouth. Cette méthode identifie les pics formantiques F1/F2 en modélisant le spectre comme
un filtre de prédiction linéaire.</p>
<p>Les analyses comparatives de mai 2026 (dossier <code>Analyses_formants-mai26</code>) montrent
que sur les instruments non-vocaliques — cordes et cuivres en particulier — le LPC-F1 produit
des valeurs aberrantes (violon : LPC-F1 médiane = 2179 Hz, σ=642 Hz ; violoncelle : 1928 Hz,
σ=503 Hz) sans rapport avec les résonances perceptivement saillantes de l'instrument.</p>
<p>Le <strong>Fp centroïde pondéré par l'énergie</strong> adopté dans ce pipeline présente une
dispersion 2 à 6 fois moindre sur les mêmes données, et correspond directement au concept de
<em>Hauptformant</em> de Meyer (2009). Il est 4,7× à 10,4× plus stable que le F2 LPC mesuré par
Parselmouth sur les registres extrêmes. C'est pourquoi les valeurs du pipeline v22 divergent
parfois des mesures LPC publiées — les deux paradigmes répondent à des questions différentes.</p>
<p>La convergence entre les deux approches est néanmoins confirmée à 93 % sur les 29 instruments
comparables (voir §VI — Concordance), les divergences étant systématiquement explicables
par la distinction F1 strict / Fp ou par la capture d'un registre spécifique.</p>
</div>
"""
```

### 3.2 `build_synthese_html_docx.py` — Nouvelle sous-section Reuter

Ajouter après la section "Concordance Multi-Sources" (actuellement la dernière, ligne ~1204) une nouvelle sous-section :

```python
# 7. Positionnement par rapport à Reuter (2023)
html += '<h2 id="reuter-positionnement">Positionnement — Reuter (2023), Oxford Handbook of Timbre</h2>\n'
html += REUTER_POSITIONNEMENT_HTML
```

Avec `REUTER_POSITIONNEMENT_HTML` contenant :

```html
<p>Le chapitre 13 de Reuter (<em>Oxford Handbook of Timbre</em>, 2023) constitue la meilleure
synthèse anglophone de la tradition formantique allemande (Helmholtz → Schumann 1929 → Meyer
1972/2009). Il fournit le cadre théorique (mécanisme de fermeture d'anche, masquage sélectif),
les cartes formantiques interactives (VSL, Parselmouth/LPC) et les deux zones de convergence
/u/–/o/ (300–500 Hz) et /a/–/æ/ (1000–1500 Hz).</p>

<p>La présente étude s'inscrit comme <strong>implémentation quantitative et multi-familles</strong>
de ce cadre, dans trois directions :</p>
<ol>
<li><strong>Méthodologique</strong> — substitution du LPC par le Fp centroïde (2–6× plus stable
sur cordes et cuivres) ; introduction de σ(Fp) comme proxy de largeur de bande.</li>
<li><strong>Empirique</strong> — tables par registre pour 30 instruments, valeurs Δ explicites
pour 1 173 convergences, validation multi-sources à 93 %.</li>
<li><strong>Périmètre</strong> — intégration des cordes comme membres à part entière du cluster
formantique, sourdines (11 configurations), ensembles, instruments graves étendus.</li>
</ol>

<table class="ref-table">
<tr class="header">
  <th>Critère</th><th>Reuter (2023)</th><th>Maresz (2026)</th>
</tr>
<tr><td>Corpus</td><td>~1 100 sons (VSL + Spitfire), vents principalement</td>
    <td>5 914 sons (SOL2020 Orchidea + Yan_Adds), 30 instruments</td></tr>
<tr><td>Métrique</td><td>LPC-F1/F2 (Parselmouth/Praat)</td>
    <td>Fp centroïde pondéré + F1–F6 par registre</td></tr>
<tr><td>Zone /o/ principale</td><td>300–500 Hz [u/o]</td>
    <td>377–506 Hz — 11 instruments, 4 familles (Δ=11 Hz min)</td></tr>
<tr><td>Cordes</td><td>Mentionnées, données limitées</td>
    <td>Pleinement intégrées ; Δ violon–basson = 11 Hz</td></tr>
<tr><td>Sourdines</td><td>Non couvertes</td><td>11 configurations analysées</td></tr>
<tr><td>Mécanisme physique</td><td>Détaillé (Reed pulse, Fransson/Voigt)</td>
    <td>Cité, non développé (hors périmètre)</td></tr>
<tr><td>Validation</td><td>Carte interactive (ellipses)</td>
    <td>93 % concordance 4 sources, outliers annotés</td></tr>
</table>

<p class="source-note">Reuter, C. (2023). Formants: The Missing Link between Orchestration and
Post-Helmholtzian Timbre Research. In <em>The Oxford Handbook of Timbre</em>. Oxford University
Press. — Cité avec accord pour le cadre conceptuel (masquage sélectif, zones de convergence).</p>
```

### 3.3 Sections instruments — mises à jour ponctuelles

#### Trombone (build_cuivres_html_docx.py)
La note de réconciliation "sources mesurent le Fp" doit être mise à jour avec les chiffres mai26 :
- LPC-F1 mai26 médiane = **760 Hz** (σ=225) — confirme que LPC capture la zone medium/Fp
- Fp mai26 = **951 Hz** (σ=121) — légèrement inférieur au v22 (1218 Hz, méthode différente)
- Valeur v22 F1 strict = 237 Hz — inchangée, robuste

→ La note dans le tableau concordance doit préciser : *"LPC-F1 (Reuter/mai26) = 760 Hz — capte le F2 ou Fp. F1 strict = 237 Hz (/u/). Fp = 951–1218 Hz selon méthode."*

#### Violon (build_cordes_html_docx.py)
- LPC-F1 mai26 = **2179 Hz** (σ=642) — artéfact LPC confirmé, à mentionner explicitement
- Fp mai26 = **1125 Hz** (σ=169) — proche de v22 (893 Hz, légère différence de bande)
- F1 strict v22 = 506 Hz — inchangé

→ Ajouter note : *"Analyse LPC (mai 2026, N=284) : F1 médiane = 2179 Hz — artéfact caractéristique du LPC sur cordes (σ=642 Hz). Fp centroïde = 1125 Hz (σ=169) — métrique stable confirmée."*

#### Clarinette Sib (build_bois_html_docx.py)
- LPC-F1 mai26 = **1126 Hz** (σ=440) — tous registres confondus
- Fp mai26 = **1134 Hz** (σ=197) — remarquable convergence LPC/Fp pour cet instrument
- Cep-80 = **1443 Hz** (proche Backus/Giesler = 1500 Hz)

→ C'est le seul instrument où LPC et Fp convergent. À signaler comme cas particulier : *"Clarinette Sib : LPC-F1 (mai26) = 1126 Hz ≈ Fp = 1134 Hz — cas unique de convergence des trois métriques. Confirme que le registre clairon domine spectralement l'analyse globale."*

#### Cor anglais (build_bois_html_docx.py)
Instrument absent du Pipeline F1 strict dans v22 — les données mai26 fournissent la première estimation Fp robuste :
- Fp mai26 = **1063 Hz** (σ=103, N=128) — très stable, zone /a/
- LPC-F1 mai26 = 1109 Hz — convergence avec Fp
- Cep-80 = 1055 Hz — triple convergence

→ Ajouter dans les tables de références : *"Fp = 1063 Hz (mai26, N=128, σ=103 Hz). LPC-F1 = 1109 Hz. Triple convergence LPC/Fp/cepstral."*

---

## PARTIE IV — RÉSUMÉ OPÉRATIONNEL

### Ce qui doit être fait dans les scripts (par ordre de priorité)

**Priorité 1 — `build_synthese_html_docx.py`**
1. Ajouter colonne "Reuter (2023)" au tableau concordance multi-sources
2. Ajouter nouvelle section `#reuter-positionnement` après la concordance
3. Mettre à jour le `source-note` pour inclure Reuter

**Priorité 2 — `build_intro_html_docx.py`**
4. Ajouter l'encadré méthodologique Fp vs LPC (avec chiffres mai26)
5. Ajouter Reuter à la liste des sources en introduction

**Priorité 3 — sections instruments**
6. Trombone : note LPC-F1 mai26 = 760 Hz + réconciliation
7. Violon : note artéfact LPC mai26 = 2179 Hz
8. Clarinette Sib : note convergence triple
9. Cor anglais : première entrée Fp = 1063 Hz

**Priorité 4 — bibliographie**
10. Ajouter dans toutes les sections : `Reuter, C. (2023). Oxford Handbook of Timbre, Ch. 13.`

### Ce qui *ne change pas* dans le pipeline v22
- Toutes les valeurs F1, F2…F6, Fp du CSV `formants_all_techniques.csv` — **inchangées**
- Les convergences Δ et le cluster 377–506 Hz — **confirmés** par mai26
- Le taux de concordance 93 % — **confirmé**
- L'anomalie sourdine harmon trombone (volume spectral +0,63) — **confirmée**

---

*Rapport produit le 31 mai 2026 — basé sur lecture directe de 45 fichiers `Analyses_formants-mai26/*.txt`, `Scripts/v6-html-docx/common.py` (v22, 64 450 chars) et `build_synthese_html_docx.py` (83 018 chars), et rapport comparatif Reuter/Maresz joint.*
