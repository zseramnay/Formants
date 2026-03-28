<i>
Je voudrais travailler sur l'homogénéité des mélanges de timbres tels que décris par Koechlin dans son Traité de l'orchestration et surtout tel que commenté par les articles de Sources/Chiasson_Conference_OICCM_2008.pdf, Sources/DuchesneauChiasson_Koechlin.pdf, Sources/Koechlin-compositeur-humaniste-ebauche.pdf que tu trouveras ici : https://github.com/zseramnay/Formants.git
Les instruments avec un "volume" et une intensité similaires vont se fondre en un plan homogène. Calculons donc le "volume" des instruments, c'est à dire la place qu'ils semblent occuper dans l'espace, leur épaisseur en quelque sorte.
J'imagine que pour comprendre quel paramètre peut être relié au volume des instruments, il va nous falloir faire de nouvelles analyses. En plus des specenv, des moments et des specpeaks que tu connais déjà, j'ai à ma disposition le spectres et les mmfc. Quel descripteur utiliser pour cette description Sepctral sperad ? un autre ou une combinaison d'autres ?
Ne crée aucun fichier, juste un premiere réponse ici.
</i>

---

Je vais d'abord lire les trois articles pour ancrer la réponse dans la terminologie exacte de Koechlin/Chiasson, puis examiner les données disponibles.Maintenant, examinons les données disponibles pour déterminer le meilleur descripteur.Voici ma synthèse après lecture des trois articles.

---

Le « volume » de Koechlin, tel que Chiasson le formalise — la place qu'un son semble occuper dans l'espace sonore, indépendamment de son intensité — est un concept perceptif rare dans la littérature orchestrale. Chiasson lui-même (dans l'article « humaniste ») note que les recherches de Stevens montrent que volume et densité sont des attributs perceptifs distincts, et que l'intensité perçue (loudness) serait le *produit* du volume par la densité. Il cite aussi van Dinther & Patterson (2006) sur la « grosseur auditive » (auditory size) et Fitch (1997) sur la corrélation entre la **dispersion des formants** et la taille corporelle perçue.

**Aucun descripteur unique ne suffit.** Voici mon analyse des candidats avec les données que tu as :

**1. Spectral Spread (moment 2) — candidat principal mais imparfait**

C'est le premier réflexe, et il est justifié : le spread mesure l'écart-type de la distribution spectrale autour du centroïde. Un spread large signifie que l'énergie est étalée sur une large bande de fréquences. Mais le problème est qu'il dépend fortement de la hauteur jouée (un son aigu de flûte aura mécaniquement un spread différent d'un son grave de cor, même s'ils ont le même « volume » koechlinien). Il faut donc le **normaliser** — soit par f0, soit par le centroïde.

**2. Spectral Centroid / f0 (ratio centroïde-fondamentale) — complémentaire essentiel**

Ce ratio capte combien d'harmoniques participent effectivement au son. Un ratio bas (énergie concentrée près de f0) correspond aux sons « gros » de Koechlin : cor, tuba, flûte grave. Un ratio élevé correspond aux sons « minces et denses » : hautbois médium, trompette aiguë. C'est facilement calculable à partir des moments + f0 (déductible du nom de fichier).

**3. Dispersion des formants (Δf moyen entre formants consécutifs) — l'ancrage psychoacoustique**

C'est le descripteur le plus directement relié à la littérature sur la perception de taille des sources sonores. Des formants rapprochés = résonateur perçu comme « grand » = volume koechlinien « gros ». On a déjà les formants dans les CSV — il suffit de calculer (F2−F1), (F3−F2), etc., et d'en prendre la moyenne. Ceci dit, Fp serait peut-être un meilleur point de départ que les formants individuels, pour les mêmes raisons de stabilité qui nous ont conduit à le privilégier.

**4. Proportion d'énergie basse (< 1 kHz ou < 2 kHz) — « poids spectral bas »**

Calculable directement à partir des fichiers spectrum (1024 bins). La proportion d'énergie dans les basses fréquences correspond à l'intuition koechlinienne : le tuba et le cor ont un poids spectral bas massif, le hautbois et le piccolo non.

**Ma recommandation : un indice composite « Volume spectral »**

Plutôt qu'un seul descripteur, je propose de calculer un **indice de volume** combinant trois métriques complémentaires, toutes calculables avec les données existantes :

- **V₁ = Spread / Centroid** (normalisation du spread) — capte la largeur spectrale relative
- **V₂ = Énergie < 1 kHz / Énergie totale** (ratio bas du spectrum) — capte le poids grave
- **V₃ = 1 / (dispersion formantique moyenne)** — inversé pour que gros résonateur = valeur haute

Ces trois composantes couvrent des facettes différentes du « volume » : la largeur spectrale (V₁), la gravité du timbre (V₂), et la taille apparente du résonateur (V₃). On pourrait les combiner par moyenne pondérée (après standardisation z-score) et vérifier si le classement obtenu correspond au tableau de Koechlin (vol. I, p. 288) :

**Gros** → Tubas, Cors, Saxhorns → Trombones → Trompettes, Flûtes grave, Bassons, Saxophones → Clarinettes, Hautbois grave → ... → **Mince**

Quant aux **MFCC** (je présume que « mmfc » était une coquille) : ils seraient intéressants pour capter la *forme globale* de l'enveloppe spectrale (les premiers coefficients décrivent la pente spectrale et la courbure), mais ils ne sont pas directement interprétables en termes de « volume ». Ce serait un outil complémentaire pour une analyse en composantes principales du timbre, pas pour un indice de volume en soi. Et je ne les trouve pas dans le repo — tu les as par ailleurs ?

En résumé : **Spectral Spread seul ne suffit pas** ; l'indice doit combiner spread normalisé + proportion basses fréquences + dispersion formantique. Le tout est calculable avec moments + spectrum + les CSVs formants existants.

---

<i>
vas-y, fais moi une mesure du "volume" par registre pour les instruments présents dans registres.md avec ta recommandation qui propose de calculer un indice de volume combinant trois métriques complémentaires, toutes calculables avec les données existantes :
* V₁ = Spread / Centroid (normalisation du spread) — capte la largeur spectrale relative
* V₂ = Énergie < 1 kHz / Énergie totale (ratio bas du spectrum) — capte le poids grave
* V₃ = 1 / (dispersion formantique moyenne) — inversé pour que gros résonateur = valeur haute

MFCC disponibles dans Data si besoin.
</i>

---

Résultats très cohérents. Comparons à l'échelle de Koechlin. Filtrons aussi par dynamique mf pour un meilleur contrôle :Résultats remarquables : **ρ = −0.855** (p < 0.0001) à dynamique mf. Copions les CSV vers outputs et créons un résumé visuel.## Résultats — Indice de Volume Spectral (Koechlin)

### Méthode
L'indice composite combine trois métriques z-normalisées :
- **V₁ = Spread/Centroid** — largeur spectrale relative
- **V₂ = Énergie < 1 kHz / Énergie totale** — poids grave (depuis les fichiers spectrum, 1024 bins)
- **V₃ = 1 / dispersion formantique moyenne** — taille apparente du résonateur (depuis les CSVs formants)

### Corrélation avec Koechlin (registre médium, mf)
**Spearman ρ = −0.855, p < 0.0001** (n=15 instruments). La corrélation négative est attendue : Volume_index ↑ quand rang Koechlin ↓ (gros=1, mince=7).

Le classement obtenu reproduit presque exactement l'échelle de Koechlin (vol. I, p. 288) :

| Rang | Instrument | Vol_idx (mf) | Koechlin |
|---|---|---|---|
| 1 | Bass Tuba | **1.46** | gros |
| 2 | Contrebasse | **1.20** | gros |
| 3 | Trombone | **0.79** | gros |
| 4 | Cor | **0.72** | gros |
| 5 | Violoncelle ens. | **0.71** | moyen |
| 6 | Basson | **0.56** | moyen |
| 7 | Violoncelle | **0.53** | moyen |
| 8 | Flûte (médium) | **0.35** | moyen |
| 9 | Clarinette | **0.10** | moyen-mince |
| 10 | Cl. basse | **0.03** | moyen-mince |
| 11 | Alto | **−0.24** | mince |
| 12 | Violon ens. | **−0.68** | mince |
| **13** | **Trompette** | **−0.86** | **moyen ← outlier** |
| 14 | Violon | **−0.87** | mince |
| 15 | Hautbois | **−0.95** | mince |

### Deux outliers intéressants

**Trompette** (Koechlin rang 4, notre indice −0.86) : son V₂ est très bas (~0.40) car même à mf, le spectre de la trompette est dominé par les harmoniques aiguës. Koechlin percevait peut-être le « volume » de la trompette à travers sa capacité projective et sa qualité de « remplissage spatial », quelque chose que V₂ (ratio d'énergie basse) ne capte pas. C'est un candidat pour un 4ᵉ composant : la **diffusion spatiale** perçue, possiblement liée aux MFCC ou à la directivité.

**Hautbois** (en bas du classement même au grave) : cohérent avec Koechlin qui le décrit comme « mince et solide » — une « étoile naine de densité considérable ».

### Fichiers produits
- `volume_index_par_registre_all.csv` — 67 lignes, toutes dynamiques
- `volume_index_par_registre_mf.csv` — 60 lignes, mf uniquement
- Script : `Scripts/compute_volume_index_v2.py`

### Prochaines étapes possibles
1. Explorer les **MFCC** (coefficients 1-3) comme proxy de la « forme spectrale globale » pour améliorer la capture du volume de la trompette
2. Calculer un **indice de densité** (inverse du volume × intensité, selon Stevens/Koechlin) pour construire le système complet volume/intensité/transparence/densité
3. Construire une **matrice d'homogénéité** : instruments dont le Volume_index ET le profil formantique sont proches → prédiction des mélanges « fondus » au sens de Koechlin

---

### L'ajout de MFCC₁ (pente spectrale) change la donne

L'intégration de **V₄ = MFCC₁** calculé depuis les fichiers spectrum a un effet notable :

- **Corrélation Koechlin ρ = −0.755** (v3, 4 composantes) vs −0.822 (v2, 3 composantes). Légère baisse car **MFCC₁ favorise la clarinette basse** (pente spectrale très prononcée vers les graves → V₄ élevé = 47.18) qui monte à la 8ᵉ place alors que Koechlin la classe « mince ». C'est un signal intéressant : la clarinette basse a spectralement un profil « gros » (beaucoup d'énergie basse, pente raide) mais perceptivement un volume subjectif plus modeste. Ça pointe vers la distinction Koechlin/Stevens entre volume *spectral* et volume *perceptif*.

- En revanche, le **problème de la trompette** s'améliore légèrement grâce à V₄ : son MFCC₁ médium (32.00) est médiocre, cohérent avec un timbre « étroit et brillant ».

### Matrice d'homogénéité — résultats remarquables

Les **top 5 paires les plus homogènes** au registre médium :

| H | Paire | Commentaire Koechlin/orchestration |
|---|---|---|
| **0.995** | Cor + Trombone | Doublure classique des cuivres |
| **0.989** | Cl. basse + Cor | Mélange typique de l'orchestre français |
| **0.988** | Cl. basse + Trombone | Utilisé par Ravel, Debussy |
| **0.985** | Basson + Cor | Le mélange « fondu » par excellence (Brahms, Wagner) |
| **0.984** | Basson + Trombone | Base du tutti grave |

Et des confirmations remarquables de pratiques orchestrales connues :

- **Trompette + Violon = 0.975** — le doublage orchestral classique du chant aigu
- **Alto + Ensemble de violons = 0.953** — cohérence naturelle des cordes
- **Clarinette + Alto_Ensemble = 0.983** — le fameux mélange « caméléon » de la clarinette
- **Hautbois isolé** (H < 0.70 avec cuivres/graves) — confirme sa nature « dense » et non fusionnelle

### 4 fichiers produits

- `volume_koechlin_v3.csv` — 67 lignes, Volume/Densité/Transparence par registre
- `homogeneite_matrix_v3.csv` — matrice 17×17 
- `mfcc_par_registre.csv` — profils MFCC complets (13 coefficients) par registre
- `compute_volume_index_v3.py` — script reproductible

### Piste pour la suite

Le cœur du système Koechlin est maintenant mesurable. Pour aller plus loin vers les **plans orchestraux** : croiser cette matrice d'homogénéité avec les données de convergence formantique qu'on a déjà (le cluster 450-502 Hz) permettrait de prédire quels instruments forment un **plan fondu** (H élevé + formants convergents) versus un **plan hétérogène** (H faible = instruments qui se distinguent).

---

<i>
croiser cette matrice d'homogénéité avec les données de convergence formantique qu'on a déjà (le cluster 450-502 Hz) permettrait de prédire quels instruments forment un plan fondu (H élevé + formants convergents) versus un plan hétérogène (H faible = instruments qui se distinguent)
</i>

---

## Résultats — Plans orchestraux de Koechlin

Le croisement **Homogénéité (Volume + MFCC) × Convergence formantique (F1 + Fp)** donne des résultats remarquablement cohérents avec la pratique orchestrale.

### Classification des 136 paires (registre médium)

| Catégorie | N | Critère |
|---|---|---|
| ★ **FONDU** | 31 | H ≥ 0.80 ET (ΔF1 ≤ 30 ou ΔFp ≤ 50) |
| ● **SEMI-FONDU** | 58 | H ≥ 0.70 + ΔF1 ≤ 80, ou H ≥ 0.80 seul |
| ○ **HÉTÉROGÈNE** | 47 | reste |

### Plans fondus les plus remarquables

**Cor + Trombone** (H=0.995, ΔF1=21, ΔFp=1) — le score de fusion le plus élevé de tout le corpus. C'est le doublage archétypal de Brahms/Wagner. Les deux instruments ont un volume quasi-identique, un profil MFCC pratiquement superposable, et un Fp qui ne diverge que de **1 Hz**.

**Violoncelle + Violoncelle Ensemble** (H=0.942, ΔF1=0, ΔFp=9) — trivial mais rassurant comme validation.

**Trompette + Alto** (H=0.905, ΔF1=11, ΔFp=11) — un résultat étonnant mais acoustiquement fondé : au registre médium, ces deux instruments partagent un F1 quasi-identique (~322-333 Hz, zone /o/) et un Fp presque superposé (~1306-1317 Hz).

**Clarinette basse + Violoncelle** (H=0.984, ΔF1=10, ΔFp=71) — la doublure classique Debussy/Ravel, confirmée par un H exceptionnel.

### Convergences inter-registres : les trois clusters vocaliques

L'analyse registre×registre (264 paires ΔF1 ≤ 30 Hz) révèle trois zones de convergence :

**Cluster /u/ (≤ 250 Hz) — 126 paires** : le monde grave. Tuba, trombone pédale, contrebasse, violoncelle grave, clarinette chalumeau convergent tous vers 161–236 Hz. C'est la zone de la « plénitude matérielle » de Koechlin — le sous-médium.

**Cluster /o/–/å/ (350–520 Hz) — 60 paires** : le cluster central que notre projet documente depuis le début. Alto, violon médium, cor aigu, basson, flûte médium, trompette grave — tous convergent dans cette bande. La paire **Clarinette gorge + Alto Ensemble grave** (ΔF1=0, H=0.983) est probablement la convergence la plus « fusionnelle » tous critères confondus entre deux familles différentes.

**Autres (>520 Hz) — 78 paires** : inclut les convergences remarquables flûte grave–alto médium (ΔF1=0, H=0.947) et clarinette basse aigu–cor médium (ΔF1=11, H=0.989).

### Le cas fascinant : convergences formantiques sans homogénéité de volume

Certaines paires ont un ΔF1 faible mais un H faible. Ce sont les cas où Koechlin aurait dit que les instruments sont dans la même « zone vocalique » mais de volume trop différent pour former un plan fondu — ils formeraient plutôt des **plans hétérogènes superposés** : audibles séparément mais dans la même couleur harmonique.

### Fichiers produits
- `plans_orchestraux_koechlin.csv` — 136 paires, registre médium, classifiées
- `convergences_par_registre.csv` — toutes les convergences F1 ≤ 30 Hz entre registres croisés
- `compute_plans_orchestraux.py` — script (utilise `common.py` pour les Fp)

---

<i>
merci de refaire tous les cvs de cette étude pour y inclure tous les instruments avec leurs multiples sourdines. Elle deviendrait bien plus interessante si elle dépasse le classicisme Koechlin/Chiasson.
Donc : 
volume_index_par_registre_all.csv
volume_index_par_registre_mf.csv
volume_koechlin_v3.csv
homogeneite_matrix_v3.csv
mfcc_par_registre.csv — profils MFCC complets
plans_orchestraux_koechlin.csv
convergences_par_registre.csv

avant de faire, pour les sourdines de cuivres ne prends que les ordinario, et pour wah les  ord_open et les ord_closed
</i>

---

Les plans ne couvrent que 136 paires car `common.py` ne connaît que 17 instruments de base. Il faut calculer F1/Fp directement depuis les spectres pour inclure les 53. Je corrige :## Résultats — 53 instruments, 193 registres, 5835 échantillons

Le passage de 17 à **53 instruments** (avec les 4 sourdines de trompette, 4 de trombone, cor sourd, tuba sourd, basson sourd, hautbois sourd, cordes avec sourdine et sourdine piombo, ensembles avec sourdine, + piccolo, flûtes basse et contrebasse, cor anglais, clarinette Mib, clarinette contrebasse, contrebasson, trombone basse, tuba contrebasse, sax alto, guitare, harpe, marimba, vibraphone) transforme le paysage :

### Chiffres clés

| | Avant (17 instr.) | Maintenant (53 instr.) |
|---|---|---|
| Matrice d'homogénéité | 17×17 | **53×53** |
| Paires analysées | 136 | **1 378** |
| Plans fondus | 31 | **308** (148 FONDU + 160 FONDU_Fp) |
| Convergences F1 ≤ 30 Hz | 264 | **1 220** |

### Découvertes les plus intéressantes au-delà du classicisme

**Trombone harmon + Violoncelle sordina piombo** (fusion=0.968, ΔFp=12 Hz) — une paire que personne n'aurait devinée empiriquement. La sourdine harmon déplace le spectre du trombone vers une zone qui converge avec le violoncelle étouffé au plomb.

**Cor + Marimba** (ΔF1=0, H=0.96) — la sourdine n'est même pas nécessaire : ces deux instruments partagent un F1 identique au médium. Le cor « chante » dans la même zone vocalique que le marimba.

**Clarinette Mib + Flûte** (ΔF1=0, ΔFp=5 Hz, H=0.95) — convergence quasi-parfaite. Leur tessiture commune au médium produit un mélange remarquablement fondu.

**Flûte basse + Flûte contrebasse** (H=0.99, ΔFp=4 Hz) — famille homogène par excellence, comme attendu.

**Tuba sourd + Basson sourd** (H=1.00, ΔF1=11, ΔFp=30) — la sourdine du tuba le rapproche spectralement du basson sourd, créant une convergence qu'on ne trouve pas entre les versions ouvertes.

**Flûte contrebasse + Alto sourd** (ΔFp=23 Hz, H=0.98) — la sourdine de l'alto réduit son volume et le rapproche de la flûte contrebasse — une doublure d'orchestre contemporain.

---

<i>
dans convergences_par_registre, à quoi correspond la zone "autre" ?
</i>

---

Bonne question. Regardons ce que ça recouvre concrètement :C'est clair : « autre » est un fourre-tout qui masque en réalité **trois zones vocaliques distinctes** :

**70% (359 paires)** sont dans la bande **251–349 Hz**, c'est-à-dire la zone de transition **/å/** entre /u/ et /o/. C'est exactement le cœur du cluster de convergence qu'on documente depuis le début — cor grave, alto grave, cl. basse, contrebasse suraigu, violoncelle aigu. Le fait qu'elles soient classées « autre » est un bug de classification : le seuil /o/ démarrait trop haut à 350 Hz.

Ensuite, trois vraies zones supplémentaires :
- **54 paires en 521–800 Hz** → zone **/a/** (basson aigu, clarinette clairon, flûte grave, hautbois médium)
- **28 paires en 801–1200 Hz** → zone **/e/** (clarinette suraigu, piccolo, trompette harmon)
- **46 paires > 1200 Hz** → zone **/i/** (flûte suraigu, trompette cup suraigu — les sourdines déplacent F1 très haut)

Il faudrait remplacer la classification binaire par les vraies zones vocaliques IPA. Tu veux que je refasse le CSV avec les 5 zones : /u/ ≤ 250, /o/ 251–400, /å/ 401–520, /a/ 521–800, /e/–/i/ > 800 ?

Les 1 220 convergences se répartissent maintenant proprement sur les 5 zones vocaliques :

| Zone | F1 moyen | Paires | Caractère orchestral |
|---|---|---|---|
| **/u/** | ≤ 250 Hz | **544** | Fondation grave — tubas, contrebasses, trombones pédale, violoncelles graves |
| **/o/** | 251–400 Hz | **423** | Le grand cluster de convergence — cor, alto, clarinette basse, basson |
| **/å/** | 401–520 Hz | **125** | Zone charnière — flûte médium, basson, violon grave, trompette grave |
| **/a/** | 521–800 Hz | **54** | Présence/projection — clarinette clairon, hautbois médium, basson aigu |
| **/e/–/i/** | > 800 Hz | **74** | Brillance — piccolo, clarinette suraigu, trompette cup/harmon suraiguë |

Le gros de l'action orchestrale se joue dans les deux premières zones : **/u/** (la plénitude matérielle de Koechlin, le sous-médium) et **/o/** (le cluster de convergence central de notre document). À elles deux, elles concentrent **79%** des convergences formantiques.


















