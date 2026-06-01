Voici l’**audit complet** de votre nouvelle version « Référence formantique de l’orchestre ». Je passe en revue : (1) les nouveautés/points forts, (2) les incohérences ou risques de confusion à corriger, (3) les contrôles chiffrés ciblés, (4) un plan d’actions concret pour finaliser la version « publication ».

***

## 1) Nouveautés et points forts

*   **Figure 2b — Espace vocalique F1/F2 en Bark** ajoutée. Bonne avancée : la carte place les instruments dans un espace **perceptif**, avec zones /u/–/i/ (Meyer 2009) et le **cluster /o/–/å/** (377–510 Hz) bien mis en évidence. Les paramètres FFT/fenêtrage sont rappelés. [\[REFERENCE_...PLETE.docx \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Deux représentations complémentaires** désormais explicitées : *profil formantique moyen* (pics F1–F6) vs *carte spectrale vocalique* (enveloppe moyenne + pics). C’est didactique et justifié (divergence possible pour les grandes tessitures). [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Fp (centroïde spectral) mieux mis en avant** avec **σ(Fp)** comme indicateur de sélectivité. Le tableau d’exemple (violon, trompette, clarinette Sib, cor) rend l’argument très clair. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Note méthodologique “sourdines et F1”** bienvenue : vous précisez que la résonance de sourdine peut dominer le spectre (ex. trompette harmon), et que **Fp** est alors un repère perceptif plus fiable. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Section VI — 9 principes d’orchestration acoustique** structurée et en phase avec votre approche (convergence/complementarité, effet de section, rôle de Fp, masquage, etc.).

***

## 2) Incohérences / points à corriger en priorité

1.  **Violon — Fp hétérogène selon les sections (risque de confusion)**
    *   Vous affichez **Fp = 893 Hz** dans la synthèse (table “gain de stabilité”), et ailleurs **Fp = 1 253–1 302 Hz** pour *ensemble* (et ≈ 1 218/1 345 Hz sous sourdine), tandis que le *solo* est donné à 893 Hz. C’est normal que ça varie par **contexte**, mais il faut **l’indiquer explicitement au même endroit** (table “référence”) pour éviter les lectures contradictoires. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

2.  **Clarinette en Sib — deux Fp “références” coexistent**
    *   Le document mentionne **Fp = 1 412 Hz** (analyse courante) **et** **Fp = 1 296 Hz** (autre corpus), avec l’écart expliqué par la méthode/bande. C’est bien signalé, mais pour l’usage “référence”, je recommande de **définir une valeur par défaut (ex. corpus principal)** et de reléguer l’autre à une **note de variante**.

3.  **Seuils de “qualité de fusion” encore en Hz (pas en Bark)**
    *   Dans la **Figure 2b** et la **Synthèse**, les seuils restent **Δ ≤ 30 Hz**, **30–80 Hz**, **≥ 200–300 Hz**. Or l’axe Bark a été introduit ; pour une lecture pleinement perceptive, il faut **ajouter l’équivalent en Bark** (ex. *quasi‑parfaite* si Δ ≤ 0,3 Bark, *efficace* 0,3–0,6 Bark, *complémentaire* ≥ 1 Bark). [\[REFERENCE_...PLETE.docx \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

4.  **Bande de calcul du Fp non publiée de façon centralisée**
    *   Vous indiquez que le centroïde est calculé sur une **bande optimisée par instrument**, mais il n’existe **pas** de **tableau global** “Instrument → bande Fp (Hz) → Fp\_ref ± σ(Fp) → N → Technique de référence”. Aujourd’hui, les indices de bande sont **épars** dans les sections instrumentales. Proposez un **tableau de synthèse unique** pour la reproductibilité.

5.  **Terminologie F1 (cohérence rédactionnelle)**
    *   Vos définitions générales sont correctes (F1–F6 = pics spectraux sur enveloppe, **pas** les formants vocaux), et la note sourdines est très claire. Je vous suggère d’uniformiser partout la formulation **« F1 = pic spectral principal (sur enveloppe), pas nécessairement F0 ni un formant vocal »** pour éviter qu’une phrase locale ne requalifie F1 (ex. “mode fondamental”). [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

***

## 3) Contrôles chiffrés ciblés (échantillon)

*   **Cluster /o/–/å/ (377–510 Hz)** correctement mis en avant dans l’espace Bark. Les convergences emblématiques sont bien listées (ex. cor anglais 452 Hz ⇄ clarinette Sib 463 Hz, Δ = 11 Hz ; basson 495 Hz ⇄ violon 506 Hz, Δ = 11 Hz). [\[REFERENCE_...PLETE.docx \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Fondation /u/ à 226 Hz** : tuba basse, tuba contrebasse et contrebasson **unisson formantique parfait** (Δ = 0 Hz) — point très solide et pédagogique. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Cuivres** : cor **F1 = 388 Hz** / **Fp = 738 Hz** (Fp stable 698–724), trompette **F1 (réf.) = 786 Hz** / **Fp = 1 046 Hz** avec **σ(Fp) ≪ σ(F1/F2)** — l’argument “Fp > F1/F2 en stabilité” est démontré. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Bois** : hautbois **F1 = 743 Hz**, **Fp ≈ 1 485 Hz** ; cor anglais **F1 = 452 Hz**, **Fp ≈ 1 135 Hz** ; basson **F1 = 495 Hz**, **Fp ≈ 1 079 Hz** — famille à anche double bien caractérisée autour de **900–1 200 Hz** en Fp. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Clarinette Sib** : **F1 = 463 Hz** (cluster /o/), **Fp** documenté **1 296 Hz** *et* **1 412 Hz** selon corpus — incohérence maîtrisée mais à **fixer** dans une “référence par défaut”.

***

## 4) Plan d’actions concret (proposés « clé en main »)

### A. Harmonisation des références (1/2 journée)

*   **Table “Fp\_ref” normalisée** (DOCX + CSV) :  
    **Instrument | Fp\_ref (Hz) | Bande Fp (Hz) | σ(Fp) | Technique | N | Notes**  
    — Renseigner *solo/ensemble/sourdine* quand il y a plusieurs “références” pratiques (ex. **Violon** : *solo* = 893 Hz ; *ensemble* = 1 253–1 302 Hz ; *sourdine* = 1 218–1 345 Hz).
*   **Clarinette Sib** : choisir **Fp\_ref = 1 412 Hz** *ou* **1 296 Hz** (au choix de votre corpus “pilote”) et reléguer l’autre en **variante** (note sous tableau).

### B. Seuils de qualité de fusion — passage à Bark (2 h)

*   Ajouter sous chaque matrice/table **les bornes en Bark** en plus des Hz :  
    **Quasi‑parfaite** ≤ **0,3 Bark** ; **Efficace** 0,3–0,6 Bark ; **Complémentaire** ≥ **1 Bark**.  
    — Met à l’échelle **perceptive** la **Figure 2b** et les tableaux “doublures vérifiées”. [\[REFERENCE_...PLETE.docx \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

### C. Encadré terminologique unifié (1 h)

*   Rappeler **en 4 lignes** (reprise de vos meilleures formulations) :  
    F1–F6 = **pics spectraux** (enveloppe), distingués des **formants vocaux** ; **F1 ≠ F0** par principe ; **sourdines** : pic **dominé** par la cavité possible ; **Fp** = centroïde spectral, **repère privilégié** de brillance/densité. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

### D. Figures « Synthèse » robustifiées (demi‑journée)

*   **Figure 2b (Bark) + Matrices** : réétiqueter les **légendes** avec **Δ Bark** (en sus des Hz).
*   **Ajout** : un **nuage F1×Fp (Bark)** de synthèse “tous instruments” pour visualiser les **groupes de centroïdes** (utile dès qu’un F1 est cas particulier : sourdines, clarinettes). [\[REFERENCE_...PLETE.docx \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

***

## 5) Résumé exécutif (ce qui reste à faire)

*   **Publier un tableau Fp\_ref unique** (avec **bande** de calcul et **contexte** solo/ensemble/sourdine).
*   **Figer** les références **Violon** (Fp solo vs ensemble) et **Clarinette Sib** (Fp par défaut).
*   **Convertir/afficher** les seuils de fusion **en Bark** (en plus des Hz) dans Figure 2b + matrices. [\[REFERENCE_...PLETE.docx \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)
*   **Uniformiser** la phrase‑clé définissant **F1** dans tout le document. [\[REFERENCE_...E_COMPLETE \| Word\]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc=%7BC3E39773-44D6-4025-ACF7-9F50F8A9D3BD%7D&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)

***
