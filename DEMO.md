# 🚀 Guide de Démonstration - Stock Manager

## Démarrage Rapide

### 1. Installation et Lancement

```bash
# Cloner le projet (si nécessaire)
cd stock-manager

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
pip install email-validator  # Dépendance supplémentaire

# Initialiser la base de données avec des données de test
python init_db.py

# Lancer l'application
python run.py
```

L'application sera accessible sur : **http://localhost:5000**

### 2. Comptes de Test

#### Administrateur
- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin123`

#### Vendeur
- **Nom d'utilisateur** : `vendeur`
- **Mot de passe** : `vendeur123`

## 🎯 Scénarios de Démonstration

### Scénario 1 : Connexion et Découverte du Dashboard
1. Accédez à http://localhost:5000
2. Connectez-vous avec le compte `admin` / `admin123`
3. Explorez le tableau de bord :
   - **23 produits** en stock
   - Valeur totale du stock
   - **Alertes de stock faible** (plusieurs produits < 5 unités)
   - **50 ventes** déjà enregistrées

### Scénario 2 : Gestion des Produits
1. Allez dans **Produits** > **Liste des produits**
2. Observez les **23 produits** pré-chargés avec différentes catégories
3. Testez le **tri** par nom, catégorie, prix, stock
4. **Ajoutez un nouveau produit** :
   - Nom : "Nouveau Produit Test"
   - Référence : "TEST-001"
   - Prix : 25.99€
   - Quantité : 10
   - Catégorie : Électronique
5. **Modifiez un produit existant** (par exemple, augmenter le stock)
6. Consultez les **détails d'un produit** avec ses statistiques de vente

### Scénario 3 : Alertes de Stock Faible
1. Allez dans **Produits** > **Stock faible**
2. Observez les produits avec moins de 5 unités :
   - iPad Air 5 (3 unités)
   - Veste Zara (4 unités)
   - Miel de Provence (2 unités)
   - Plaid en cachemire (1 unité)
   - Guide du Routard Paris (0 unité - RUPTURE)
3. Cliquez sur **Modifier** pour réapprovisionner un produit

### Scénario 4 : Enregistrement de Ventes
1. Allez dans **Ventes** > **Nouvelle vente**
2. Sélectionnez un produit avec du stock disponible
3. Entrez une quantité à vendre
4. Validez la vente
5. Vérifiez que :
   - Le stock du produit a été réduit automatiquement
   - La vente apparaît dans l'historique
   - Le tableau de bord est mis à jour

### Scénario 5 : Recherche et Filtrage
1. Utilisez la fonction **Recherche**
2. Testez différents critères :
   - Recherche par nom : "iPhone"
   - Recherche par référence : "NK-"
   - Filtrage par catégorie : "Électronique"
3. Observez les résultats filtrés en temps réel

### Scénario 6 : Historique des Ventes
1. Allez dans **Ventes** > **Historique**
2. Consultez les **50 ventes** générées automatiquement
3. Utilisez les **filtres par date** pour affiner les résultats
4. Observez les **statistiques** :
   - Chiffre d'affaires total
   - Nombre d'articles vendus
   - Nombre de transactions

## 📊 Données de Test Incluses

### Produits par Catégorie
- **Électronique** (5 produits) : iPhone, Samsung, MacBook, AirPods, iPad
- **Vêtements** (4 produits) : T-shirt Nike, Jean Levi's, Sneakers Adidas, Veste Zara
- **Alimentation** (4 produits) : Café Nespresso, Chocolat Lindt, Thé Earl Grey, Miel
- **Maison** (4 produits) : Aspirateur Dyson, Cafetière, Bougie Diptyque, Plaid
- **Sport** (3 produits) : Raquette Wilson, Ballon Nike, Tapis de yoga
- **Livres** (3 produits) : Python pour les Nuls, Le Petit Prince, Guide du Routard

### Caractéristiques des Données
- **Prix variés** : de 3,20€ (chocolat) à 1499€ (MacBook)
- **Stocks réalistes** : de 0 à 100 unités selon le type de produit
- **Ventes réparties** sur les 30 derniers jours
- **Plusieurs produits en stock critique** pour tester les alertes

## 🎨 Fonctionnalités à Tester

### Interface Utilisateur
- ✅ **Design moderne** avec Bootstrap 5
- ✅ **Navigation intuitive** avec menu déroulant
- ✅ **Responsive design** (testez sur mobile)
- ✅ **Animations CSS** au survol
- ✅ **Messages flash** pour les actions utilisateur

### Fonctionnalités Avancées
- ✅ **Pagination** automatique des listes
- ✅ **Tri multi-critères** des produits
- ✅ **Validation des formulaires** en temps réel
- ✅ **Calculs automatiques** des totaux de vente
- ✅ **Statistiques en temps réel** sur le dashboard

### Sécurité
- ✅ **Authentification** obligatoire
- ✅ **Sessions sécurisées**
- ✅ **Protection CSRF** sur les formulaires
- ✅ **Validation côté serveur**

## 🔧 Tests Supplémentaires

### Test de Robustesse
1. Essayez de vendre plus que le stock disponible
2. Tentez d'ajouter un produit avec une référence existante
3. Testez les champs obligatoires des formulaires
4. Vérifiez la gestion des erreurs

### Test de Performance
1. Naviguez rapidement entre les pages
2. Effectuez plusieurs recherches consécutives
3. Ajoutez plusieurs produits rapidement
4. Consultez les statistiques après modifications

## 🎉 Points Forts à Démontrer

1. **Interface Professionnelle** : Design moderne et intuitif
2. **Fonctionnalités Complètes** : Toutes les exigences sont implémentées
3. **Données Réalistes** : Produits et ventes crédibles
4. **Alertes Intelligentes** : Gestion proactive du stock
5. **Statistiques Utiles** : Tableaux de bord informatifs
6. **Code Propre** : Architecture modulaire et maintenable

## 📱 Accès Mobile

L'application est entièrement responsive. Testez-la sur :
- **Desktop** : Toutes les fonctionnalités
- **Tablette** : Interface adaptée
- **Mobile** : Navigation optimisée

---

**Durée de démonstration recommandée** : 15-20 minutes pour couvrir tous les scénarios principaux.

**Note** : Toutes les données sont réinitialisables en relançant `python init_db.py`