---
# yaml-language-server: $schema=schemas/page.schema.json
Object type:
    - Page
Backlinks:
    - OrchBook material
Creation date: "2026-03-19T10:31:29Z"
Created by:
    - yanmaresz
id: bafyreihwwpor77tx3ffuluwxxkmeht54zmxqd6p2i3dx3lhbpkjsyx3bzi
---
# Audit Copilot   
Merci — j’ai bien reçu votre « Référence formantique ». Voilà un **audit technique franc et concret** : ce qui est solide, ce qui accroche, et comment corriger vite.   
 --- 
## Ce qui est très bien   
- **Taille et variété du corpus** (5 914 échantillons, 30 instruments), paramètres d’analyse exposés (FFT 4096 à 44,1 kHz, `find\_peaks`, plage 100–3 000 Hz). C’est clair et réplicable. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
- **Idée de Fp (centroïde spectral)** pour stabiliser la caractérisation timbrale quand F1/F2 fluctuent selon le registre/dynamique (ex. violon Fp = 893 Hz, σ = 92 Hz ; trompette Fp = 1 046 Hz, σ = 98 Hz). C’est pertinent et justifié par vos chiffres. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
- **Hypothèse “cluster de convergence /o/–/å/ (377–510 Hz)”** réunissant cor, cor anglais, clarinette Sib, basson, violon, (sax alto quand dispo) : on comprend immédiatement les doublures « qui fusionnent ». [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true), [[archive.org]](https://archive.org/download/dover-books-on-music-arthur-h.-benade-fundamentals-of-musical-acoustics-second-r/%28Dover%20Books%20on%20Music%29%20Arthur%20H.%20Benade%20-%20Fundamentals%20of%20Musical%20Acoustics_%20Second,%20Revised%20Edition-Dover%20Publications%20%281990%29.pdf)   
- **Traitement séparé des sourdines** (effets mesurés et signés : trompette + harmon → F1 ≈ 2 358 Hz). C’est un vrai plus pratique. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
 --- 
   
## Points à corriger (avec propositions “copier–coller”)   
### 1) Contradiction sur l’ensemble de violons   
- Dans la synthèse « Cordes d’ensemble », vous écrivez : *« Exemple le plus marqué : Violon solo F1 = 506 Hz → Ensemble de violons F1 = 1 556 Hz »*. Or, votre propre page « Ensemble de violons » montre **F1 ensemble = 495 Hz**, quasi-identique au solo (−2 %). [[archive.org]](https://archive.org/download/dover-books-on-music-arthur-h.-benade-fundamentals-of-musical-acoustics-second-r/%28Dover%20Books%20on%20Music%29%20Arthur%20H.%20Benade%20-%20Fundamentals%20of%20Musical%20Acoustics_%20Second,%20Revised%20Edition-Dover%20Publications%20%281990%29.pdf)   
- **Correction proposée**   
   
Remplacez la phrase par :   
« Exemple : Violon solo F1 = 506 Hz → Ensemble de violons **F1 = 495 Hz (−2 %)** ; l’effet de section abaisse surtout **F2** (1 518 → 1 163 Hz, −23 %) et **F3** (2 347 → 1 970 Hz, −16 %), d’où un timbre plus fondu. » [[archive.org]](https://archive.org/download/dover-books-on-music-arthur-h.-benade-fundamentals-of-musical-acoustics-second-r/%28Dover%20Books%20on%20Music%29%20Arthur%20H.%20Benade%20-%20Fundamentals%20of%20Musical%20Acoustics_%20Second,%20Revised%20Edition-Dover%20Publications%20%281990%29.pdf)   
### 2) Mélange F1 / Fp dans certains tableaux de « Valeurs de référence »   
- **Tuba contrebasse** : un tableau indique *« Yan\_Adds (Fp) »* avec **F1 = 471 ± 155 Hz** et **F2 = 1 304 ± 576 Hz** — ces chiffres décrivent en réalité **un Fp et/ou des valeurs centrées différentes**, pas le **F1 strict** (qui est 226 Hz partout ailleurs). Le libellé « ( Fp ) » dans la colonne F1 entretient la confusion. [[englishspe...rvices.com]](https://www.englishspeechservices.com/blog/the-vowel-space/)   
- **Cor en Fa** : autre exemple où les lignes « SOL2020 (Fp) » cohabitent avec des colonnes intitulées F1/F2, alors que la valeur 738 Hz est bien un **Fp** (pas un F1). Normaliser l’entête évitera les lectures de travers. [[ccrma.stanford.edu]](https://ccrma.stanford.edu/~jmccarty/formant.htm)   
- **Correction proposée (générique)**   
   
Dans les tableaux « Valeurs de référence », remplacez l’en-tête par : \*\*F1 (Hz) \| F2 (Hz) \| … \| *Fp (centroïde, Hz)* \*\*, et ne placez **jamais** Fp dans les colonnes F1/F2. Ajoutez une note : « Fp=centroïde spectral (défini ci-dessus), différent de F1/F2 (pics). » [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
### 3) Terminologie F1/F2 vs “premiers pics”   
- Vous écrivez que l’algorithme choisit « le pic le plus proéminent (pas premier pic) », puis vous nommez **F1/F2** ces pics. En acoustique, **F1** et **F2** évoquent la **nomenclature vocale** (vrais formants) ; ici, ce sont des **pics spectraux** d’un instrument (souvent pas “des formants” au sens tractus vocal). D’où des malentendus possibles (notamment pour flûtes/clarinettes). [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
- **Correction proposée**   
   
Renommer partout F1/F2 → P1/P2 (premier/deuxième ***pic* spectral)** quand il s’agit de pics extraits par `find\_peaks`. Conserver **Fp** pour le centroïde (mesure perceptive). Ajoutez dans la méthodologie un encadré « **P1/P2 ≠ F1/F2 des voyelles** ». [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
### 4) Clarinette en Sib : “pas de formant fixe” — très juste, mais nuance utile   
- Votre section explique bien que le pic peut suivre la fondamentale (ratio 1.0) ou le 3e harmonique (ratio 3.0), et que la famille (tuyau cylindrique quasi-clos) favorise les impairs ; c’est conforme à la littérature. Ajoutez simplement que **les pairs ne sont pas “mathématiquement absents”** (pavillon, trous, registre aigu → quelques pairs réapparaissent), pour éviter une interprétation trop littérale. [[archive.org]](https://archive.org/details/acousticalfounda0000back), [[ince.publi...onnect.com]](https://ince.publisher.ingentaconnect.com/contentone/ince/ncej/2010/00000058/00000005/art00012)   
   
### 5) Cartes voyelles : 1D par F1 → à déplacer en 2D (F1×F2)   
- Votre tableau « Correspondance voyelles–fréquences (Meyer 2009) » mappe des zones vocaliques via une **seule fréquence** ; or, en phonétique, une **voyelle = (F1,F2)** (au moins). Pour éviter les sur-interprétations, présentez une **carte F1×F2** (échelle Bark/ERB) et placez vos Fp ou P1 sur ce plan. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true), [[books.google.com]](https://books.google.com/books/about/Acoustics_and_the_Performance_of_Music.html?id=Mlkut4PAAiUC)   
- **Sources rapides à citer** (contexte : espace vocalique, cardinal vowels, méthode) : CCRMA / McCarty (vowel space appliqué aux instruments), et un rappel pédagogique sur l’espace vocalique acoustique (F1 vs F2). [[Datasets – Orchidea]](http://www.orch-idea.org/datasets/), [[books.google.com]](https://books.google.com/books/about/Acoustics_and_the_Performance_of_Music.html?id=Mlkut4PAAiUC)   
   
### 6) Cohérence inter-sources (Backus / Meyer / Gieseler / SOL/Orchidea)   
- Votre doc croise correctement Backus, Meyer, Gieseler et SOL ; pour renforcer la traçabilité, liez dès l’Intro les **entrées exactes des ouvrages/datasets** utilisés (pages/chapitres pour Backus/Meyer ; fiches publiques SOL/OrchideaSOL). [[forum.ircam.fr]](https://forum.ircam.fr/collections/detail/sol-instrumental-sounds-datasets/), [[zenodo.org]](https://zenodo.org/records/3686252)   
 --- 
   
## Améliorations méthodologiques (faciles à intégrer)   
1. **Fenêtrage + lissage**   
   
Mentionnez le **fenêtrage Hann** et un lissage (p. ex. médian ou Savitzky‑Golay) avant `find\_peaks` pour stabiliser P1/P2 sur signaux bruités (flûtes, multiphoniques). [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
1. **Critères de pic adaptatifs**   
   
Vos seuils fixes (hauteur 10 %, proéminence 5 %, distance ~50 Hz) sont honnêtes, mais autorisez une règle **adaptée à la dynamique** (pp vs ff) afin d’éviter le faux choix d’un bruit d’air comme P1. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
1. **Statistiques robustes et CIs**   
   
Affichez **médiane + IQR** (pas seulement σ) et **IC95 %** pour Fp et P1 en “ordinario”. Ça crédibilise les comparaisons inter-instruments. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
1. **Échelles perceptives**   
   
Proposez les mêmes graphiques en **Bark/ERB** (en plus des Hz) pour toutes les matrices de convergence — lecture timbrale plus directe. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
1. **Lien formant–jeu réel**   
   
Pour la **clarinette** et la **flûte** (pas de formant fixe au sens strict), assumez une terminologie « **zone d’énergie dominante** (P1/Fp)\*\* » sans employer *formant* isolé. Cela évite le contresens « formant = résonateur fixe ». [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true)   
 --- 
## Deux « patchs » concrets à insérer tels quels   
- **Synthèse / Cordes d’ensemble — remplacement**   
   
> « Ensemble de violons : F1 = 495 Hz (≈ solo 506 Hz, −2 %). L’effet de section n’élève pas F1 ; il lisse F2/F3 (F2 = 1 518 → 1 163 Hz, F3 = 2 347 → 1 970 Hz), d’où un timbre plus homogène. » [archive.org]   

- **Cuivres graves — dédoublage F1/Fp dans le tableau**   
   
> « Tuba contrebasse (ordinario) : F1 = 226 Hz ; Fp (centroïde) = 1 182–1 279 Hz (suivant source/pipeline). Les lignes marquées (Fp) ne doivent pas être placées dans la colonne F1. » [englishspe...rvices.com]   

 --- 
## Pour vos références (ancrages rapides)   
- Backus, ***The Acoustical Foundations of Music*** — source historique, chapitres bois/cuivres. [[forum.ircam.fr]](https://forum.ircam.fr/collections/detail/sol-instrumental-sounds-datasets/)   
- Meyer, ***Acoustics and the Performance of Music* (5ᵉ éd., 2009)** — cartographies instrumentales & couleurs vocaliques.   
- **IRCAM SOL / OrchideaSOL** — description publique des corpus 2020 (techniques étendues, sourdines).   
- **McCarty (CCRMA)** — *Timbral Analysis & Orchestration* (vowel space appliqué aux instruments). [[Datasets – Orchidea]](http://www.orch-idea.org/datasets/)   
- **Benade** — rappel utile sur clarinettes et harmoniques impairs (nuancer « pairs absents »). [[ince.publi...onnect.com]](https://ince.publisher.ingentaconnect.com/contentone/ince/ncej/2010/00000058/00000005/art00012)   
 --- 
   
## Verdict   
Votre **cadre « P1/Fp + convergence Δ »** est puissant et exploitable en orchestration ; en corrigeant les **deux incohérences** ci‑dessus (violons d’ensemble, colonnes F1/Fp) et en **normalisant la terminologie** (P1/P2 vs F1/F2 vocaux, carte voyelles en F1×F2), la référence gagne en rigueur **sans rien perdre** de sa lisibilité pratique. [[REFERENCE\_...PLETE.docx \| Word]](https://cnsmdp-my.sharepoint.com/personal/y_maresz_cnsmdp_fr/_layouts/15/Doc.aspx?sourcedoc={C3E39773-44D6-4025-ACF7-9F50F8A9D3BD}&file=REFERENCE_FORMANTIQUE_COMPLETE.docx&action=default&mobileredirect=true), [[archive.org]](https://archive.org/download/dover-books-on-music-arthur-h.-benade-fundamentals-of-musical-acoustics-second-r/%28Dover%20Books%20on%20Music%29%20Arthur%20H.%20Benade%20-%20Fundamentals%20of%20Musical%20Acoustics_%20Second,%20Revised%20Edition-Dover%20Publications%20%281990%29.pdf)   
Souhaitez‑vous que je vous renvoie **une version annotée** (PDF avec commentaires) ou **un erratum prêt à coller** dans le DOCX ? Je peux aussi générer **une figure F1×F2 (Bark)** plaçant vos P1/Fp des 27 instruments pour la section « Synthèse ».   
