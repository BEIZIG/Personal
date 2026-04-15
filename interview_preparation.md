# Plan de Préparation — Entretien Chef de Projet Lutte contre la Fraude Bancaire | La Banque Postale

---

## 1. PITCH DE PRÉSENTATION (2-3 min)

> *Script recommandé :*

**"Bonjour, je suis Ibtihel Ben Khedher. Je suis actuellement Business Operations Analyst chez Accenture, au sein de la practice Risk & Compliance. En 4 ans, j'ai piloté des projets de bout en bout — du cadrage au déploiement — sur des outils de gestion des risques pour des acteurs bancaires, assurantiels et institutionnels.**

**Ce qui me distingue, c'est ma double casquette : je comprends les enjeux métiers du risque ET je suis capable de structurer techniquement les solutions. J'ai d'ailleurs conçu un robot de tests automatisés en Python qui détecte les anomalies de paramétrage — c'est cette capacité à industrialiser et sécuriser les livrables qui, je pense, est directement transférable à un rôle de chef de projet en lutte contre la fraude."**

---

## 2. MOTS-CLÉS "FIT" À PLACER NATURELLEMENT

| Compétence Chef de Projet Fraude | Mot-clé à utiliser | Lien avec ton expérience |
|---|---|---|
| Pilotage de projet | **Cadrage, planning, jalons, RACI** | Le Conservateur : pilotage bout en bout |
| Coordination multi-acteurs | **Animation de workshops, interface métier/IT** | Coordination BlackRock + équipes internes |
| Suivi d'avancement | **Comités de pilotage, reporting hebdomadaire, KPIs** | Points d'avancement réguliers, Jira |
| Gestion des risques projet | **Identification des risques, dépendances, plans de mitigation** | Analyse d'impacts sur processus existants |
| Recette / Qualification | **Cahier de recette, UAT, cas de test, Gherkin** | Tests fonctionnels, black box testing |
| Suivi budgétaire | **Suivi budgétaire, charge/capacité, arbitrage** | "J'ai bien compris l'enjeu du suivi budgétaire, Élodie m'a précisé que cela se ferait avec vos outils internes" |
| Fraude bancaire | **Scoring, détection d'anomalies, règles métier, seuils d'alerte** | Modèle ML anti-fraude automobile (MAE) |
| Conduite du changement | **Formation, adoption utilisateur, support post-déploiement** | 6 phases Le Conservateur |
| Industrialisation | **Automatisation, RPA, scalabilité** | Robot de tests automatisés |

---

## 3. MAPPING EXPÉRIENCES → POSTE CHEF DE PROJET FRAUDE

| Phase Projet | Ton expérience concrète | Comment le formuler |
|---|---|---|
| **Cadrage** | Workshops métier Le Conservateur, structuration EPICs/features | *"J'ai l'habitude de cadrer un projet : périmètre, acteurs, risques, planning"* |
| **Conception** | Spécifications FR/EN, data model, mapping SQL | *"Je rédige des spécifications exploitables par le métier ET par l'IT"* |
| **Coordination** | Interface BlackRock ↔ métier, workshops développeurs | *"Mon rôle était de faire le lien entre les équipes — c'est exactement ce qu'un chef de projet fraude doit faire entre les cellules fraude, l'IT et la conformité"* |
| **Recette** | Plan de test, Gherkin, jeux de données, UAT | *"J'ai conçu et exécuté des cahiers de recette complets — c'est critique pour valider les règles de détection de fraude"* |
| **Suivi anomalies** | Jira, analyse cause racine, suivi correctifs | *"Je suis rigoureuse dans la gestion des anomalies — traçabilité, priorisation, résolution"* |
| **Déploiement** | Formation, accompagnement, support post-prod | *"J'assure la continuité après la livraison — l'adoption utilisateur est clé"* |
| **Fraude** | Modèle ML anti-fraude automobile (scoring, seuils) | *"J'ai déjà travaillé sur de la détection de fraude avec du scoring probabiliste — le principe est le même pour la fraude bancaire"* |

---

## 4. CONNAISSANCES FRAUDE BANCAIRE À MAÎTRISER

### Types de fraude à évoquer :
- **Vol de chéquier** : interception postale, falsification de signature, encaissement frauduleux
- **Vol de carte bancaire** : skimming, utilisation sans contact, fraude CNP (Card Not Present = en ligne)
- **Phishing** : usurpation d'identité par email/SMS, récupération d'identifiants bancaires, virement frauduleux
- **Fraude au virement** : faux RIB, arnaque au président (FOVI)
- **SIM swapping** : prise de contrôle du numéro de téléphone pour valider des opérations

### Ce qu'un chef de projet fraude fait :
- Piloter les projets d'évolution des **systèmes de détection** (règles, scoring, alertes)
- Coordonner les acteurs : **cellule fraude, conformité, IT, éditeurs de solutions**
- Suivre les **indicateurs** : taux de détection, faux positifs, délai de traitement
- Assurer la **conformité réglementaire** (DSP2, authentification forte)
- Gérer le **cahier de recette** des règles de détection avant mise en production

### Cahier de recette (définition) :
> Document qui liste tous les cas de test à exécuter pour valider qu'un livrable fonctionne conformément aux spécifications. Tu en as déjà fait — c'est exactement tes plans de test en Gherkin + jeux de données. Utilise le terme "cahier de recette" à la place de "test plan" pendant l'entretien.

---

## 5. QUESTIONS ATTENDUES & RÉPONSES SUGGÉRÉES

### Q1. Présentez-vous.
→ Utiliser le pitch de la section 1. Finir par le lien direct avec le poste fraude.

### Q2. Pourquoi ce poste / pourquoi la lutte contre la fraude ?
→ *"J'ai déjà travaillé sur un modèle de détection de fraude en assurance — j'ai vu l'impact concret que ça peut avoir. La lutte contre la fraude bancaire me motive parce que c'est un sujet où la rigueur du pilotage projet a un impact direct sur la protection des clients."*

### Q3. Quelle est votre vision du rôle de chef de projet ?
→ *"Le chef de projet est le garant du cadrage, de la coordination et de la livraison. Concrètement : je structure le projet (périmètre, planning, risques, budget), je coordonne les acteurs, je suis l'avancement semaine par semaine, je remonte les alertes et je sécurise la qualité via la recette avant chaque mise en production."*

### Q4. Racontez un projet que vous avez piloté de bout en bout.
→ Le Conservateur : dérouler les 6 phases en 3 minutes. Insister sur les livrables et la coordination multi-acteurs.

### Q5. Comment gérez-vous les risques projet ?
→ *"Je les identifie dès le cadrage : dépendances techniques, disponibilité des acteurs, complexité des spécifications. Je tiens un registre de risques mis à jour à chaque comité, avec des plans de mitigation. Chez Le Conservateur, j'ai anticipé les impacts de la migration sur les processus existants dès la phase de cadrage."*

### Q6. Avez-vous de l'expérience en suivi budgétaire ?
→ *"Je comprends l'importance du suivi budgétaire dans le pilotage projet. Élodie m'a indiqué que La Banque Postale dispose d'outils dédiés pour cela — je suis tout à fait à l'aise pour m'y former rapidement et assurer ce suivi."* (Honnêteté + volonté d'apprentissage)

### Q7. Qu'est-ce qu'un cahier de recette pour vous ?
→ *"C'est le document qui formalise l'ensemble des cas de test à dérouler pour valider un livrable. J'en ai conçu plusieurs : je rédige les scénarios en Gherkin, je prépare les jeux de données — tests de seuil, valeurs limites, cas extrêmes — et j'exécute en UAT avant la mise en production."*

### Q8. Comment coordonnez-vous les différents acteurs ?
→ *"Par des rituels structurés : workshops de cadrage, points d'avancement hebdomadaires, comités de pilotage. Chez Le Conservateur, je faisais l'interface entre les équipes métier internes et l'éditeur BlackRock — deux mondes différents qu'il faut aligner."*

### Q9. Parlez-nous de votre robot de tests.
→ Dérouler l'histoire : constat (les tests prennent trop de temps) → conception → RPA + Python + Gherkin → résultat (industrialisation, scalabilité). Message = **capacité à identifier un problème et proposer une solution concrète**.

### Q10. Une question piège possible : "Vous n'avez pas d'expérience bancaire directe, qu'est-ce qui vous rend légitime ?"
→ *"Ma valeur ajoutée est justement transversale : je maîtrise le pilotage de projet, la gestion des risques, la coordination multi-acteurs et les tests fonctionnels. Et j'ai une expérience directe en détection de fraude via mon modèle de scoring. Les méthodes de gestion de projet sont les mêmes — c'est la connaissance du domaine bancaire que j'intégrerai rapidement grâce à ma curiosité et ma rigueur."*

---

## 6. CHECKLIST JOUR J

- [ ] Relire les 6 phases du Conservateur (ton meilleur argument)
- [ ] Connaître 4-5 types de fraude bancaire + exemples
- [ ] Maîtriser le vocabulaire : cahier de recette, UAT, comité de pilotage, RACI, registre de risques
- [ ] Préparer 2-3 questions à poser (ex: *"Quels outils utilisez-vous pour le suivi projet ?"*, *"Quelle est la taille de l'équipe fraude ?"*, *"Quels sont les principaux chantiers en cours ?"*)
- [ ] Avoir le pitch de 2-3 min fluide à l'oral
- [ ] Préparer le point budget (formulation honnête + proactive)
