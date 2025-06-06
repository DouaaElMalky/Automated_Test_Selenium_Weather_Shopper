# Weather Shopper - Automatisation de Tests Selenium

Ce projet vise à automatiser les tests fonctionnels d’un site e-commerce fictif : [Weather Shopper](https://weathershopper.pythonanywhere.com), qui recommande des produits en fonction de la température extérieure.

---

## Objectif du projet

Automatiser le parcours utilisateur principal avec **Selenium WebDriver** en Python :
Le test suit un scénario conditionnel basé sur la température affichée sur la page d’accueil.

### Déroulé logique du test :

- Accéder à la page d’accueil du site et lire la **température ambiante** affichée en haut de la page.

- En fonction de cette température :
  - Si la température est **inférieure à 19°C**, le test redirige automatiquement vers la boutique de **moisturizers** :
    - Il identifie tous les produits contenant "**aloe**" et "**almond**" dans leur nom.
    - Il sélectionne **le moins cher de chaque type** et les ajoute au panier.
  - Si la température est **supérieure à 34°C**, le test redirige vers la boutique de **sunscreens** :
    - Il recherche les produits contenant "**SPF-30**" et "**SPF-50**".
    - Il sélectionne **le moins cher de chaque type** et les ajoute au panier.
  - Si la température est comprise entre **19°C et 34°C inclus**, le test **s’interrompt volontairement** sans effectuer d'achat, car aucune recommandation n’est nécessaire dans cette plage de confort.

- Une fois les produits ajoutés au panier, le test :
  - Accède au panier.
  - Vérifie que les bons articles ont bien été ajoutés.
  - Lance une **simulation de paiement** via une iframe Stripe intégrée.
  - Remplit les champs requis (email, numéro de carte fictif, date d’expiration, CVC, code postal).
  - Soumet le formulaire de paiement.

- À la fin du test, un **rapport HTML** est automatiquement généré avec `pytest-html`, contenant le statut d'exécution et les détails du test.

---

## Technologies & Librairies

| Outil              | Utilité                                     |
|--------------------|----------------------------------------------|
| Python 3           | Langage principal                            |
| Selenium           | Automatisation de navigateur                 |
| webdriver-manager  | Gestion automatique de ChromeDriver          |
| pytest             | Cadre de test                                |
| pytest-html        | Génération du rapport HTML                   |
| Chrome             | Navigateur requis pour les tests             |

---

## Instructions d’exécution

### 1. Cloner le projet

```bash
git clone https://github.com/Asmaa-rahhali/Automated_Test_Selenium_Weather
cd selenium
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate       
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer le test avec génération du rapport

```bash
pytest --html=rapport_test.html
```

---

## Résultat attendu

- Le navigateur s’ouvre automatiquement.
- Le produit recommandé est sélectionné et ajouté au panier.
- Le paiement est simulé via Stripe.
- Un fichier `rapport_test.html` est généré et peut être ouvert dans un navigateur.

### Réalisé par

- **EL MALKY Douaa**
- **RAHHALI Asmaa**