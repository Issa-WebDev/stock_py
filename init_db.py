#!/usr/bin/env python3
"""
Script d'initialisation de la base de données avec des données de test
"""

from app import create_app, db
from app.models import User, Product, Sale
from datetime import datetime, timedelta
import random

def init_database():
    """Initialiser la base de données avec des données de test"""
    app = create_app()
    
    with app.app_context():
        # Supprimer toutes les tables existantes et les recréer
        print("Suppression des tables existantes...")
        db.drop_all()
        
        print("Création des nouvelles tables...")
        db.create_all()
        
        # Créer un utilisateur administrateur
        print("Création de l'utilisateur administrateur...")
        admin = User(
            username='admin',
            email='admin@stockmanager.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Créer un utilisateur normal
        user = User(
            username='vendeur',
            email='vendeur@stockmanager.com'
        )
        user.set_password('vendeur123')
        db.session.add(user)
        
        db.session.commit()
        
        # Créer des produits de test
        print("Création des produits de test...")
        products_data = [
            # Électronique
            {'name': 'iPhone 15 Pro', 'reference': 'IP15P-128', 'price': 1229.00, 'quantity': 15, 'category': 'Électronique', 'description': 'Smartphone Apple iPhone 15 Pro 128GB'},
            {'name': 'Samsung Galaxy S24', 'reference': 'SGS24-256', 'price': 899.00, 'quantity': 8, 'category': 'Électronique', 'description': 'Smartphone Samsung Galaxy S24 256GB'},
            {'name': 'MacBook Air M2', 'reference': 'MBA-M2-256', 'price': 1499.00, 'quantity': 5, 'category': 'Électronique', 'description': 'Ordinateur portable Apple MacBook Air M2 256GB'},
            {'name': 'AirPods Pro 2', 'reference': 'APP2-USB', 'price': 279.00, 'quantity': 25, 'category': 'Électronique', 'description': 'Écouteurs sans fil Apple AirPods Pro 2ème génération'},
            {'name': 'iPad Air 5', 'reference': 'IPA5-64', 'price': 669.00, 'quantity': 3, 'category': 'Électronique', 'description': 'Tablette Apple iPad Air 5ème génération 64GB'},
            
            # Vêtements
            {'name': 'T-shirt Nike Dri-FIT', 'reference': 'NK-DFIT-M', 'price': 35.00, 'quantity': 50, 'category': 'Vêtements', 'description': 'T-shirt de sport Nike Dri-FIT taille M'},
            {'name': 'Jean Levi\'s 501', 'reference': 'LV501-32', 'price': 89.00, 'quantity': 20, 'category': 'Vêtements', 'description': 'Jean Levi\'s 501 Original taille 32'},
            {'name': 'Sneakers Adidas Stan Smith', 'reference': 'AD-SS-42', 'price': 99.00, 'quantity': 12, 'category': 'Vêtements', 'description': 'Baskets Adidas Stan Smith pointure 42'},
            {'name': 'Veste Zara', 'reference': 'ZR-VES-L', 'price': 59.00, 'quantity': 4, 'category': 'Vêtements', 'description': 'Veste casual Zara taille L'},
            
            # Alimentation
            {'name': 'Café Nespresso Vertuo', 'reference': 'NES-VER-10', 'price': 4.50, 'quantity': 100, 'category': 'Alimentation', 'description': 'Capsules café Nespresso Vertuo x10'},
            {'name': 'Chocolat Lindt Excellence', 'reference': 'LDT-EXC-100', 'price': 3.20, 'quantity': 45, 'category': 'Alimentation', 'description': 'Chocolat noir Lindt Excellence 100g'},
            {'name': 'Thé Earl Grey Twinings', 'reference': 'TWN-EG-25', 'price': 5.90, 'quantity': 30, 'category': 'Alimentation', 'description': 'Thé Earl Grey Twinings boîte 25 sachets'},
            {'name': 'Miel de Provence', 'reference': 'PRV-MIL-250', 'price': 8.50, 'quantity': 2, 'category': 'Alimentation', 'description': 'Miel de Provence 250g'},
            
            # Maison
            {'name': 'Aspirateur Dyson V15', 'reference': 'DYS-V15-DET', 'price': 599.00, 'quantity': 6, 'category': 'Maison', 'description': 'Aspirateur sans fil Dyson V15 Detect'},
            {'name': 'Cafetière Nespresso', 'reference': 'NES-CAF-ESS', 'price': 89.00, 'quantity': 15, 'category': 'Maison', 'description': 'Cafetière Nespresso Essenza Mini'},
            {'name': 'Bougie parfumée Diptyque', 'reference': 'DIP-BOU-190', 'price': 68.00, 'quantity': 8, 'category': 'Maison', 'description': 'Bougie parfumée Diptyque Baies 190g'},
            {'name': 'Plaid en cachemire', 'reference': 'CSH-PLD-150', 'price': 129.00, 'quantity': 1, 'category': 'Maison', 'description': 'Plaid en cachemire 150x200cm'},
            
            # Sport
            {'name': 'Raquette tennis Wilson', 'reference': 'WIL-RAQ-PRO', 'price': 199.00, 'quantity': 7, 'category': 'Sport', 'description': 'Raquette de tennis Wilson Pro Staff'},
            {'name': 'Ballon football Nike', 'reference': 'NK-BAL-5', 'price': 29.00, 'quantity': 18, 'category': 'Sport', 'description': 'Ballon de football Nike taille 5'},
            {'name': 'Tapis de yoga', 'reference': 'YOG-TAP-6MM', 'price': 45.00, 'quantity': 22, 'category': 'Sport', 'description': 'Tapis de yoga antidérapant 6mm'},
            
            # Livres
            {'name': 'Python pour les Nuls', 'reference': 'PYT-NUL-2024', 'price': 24.90, 'quantity': 12, 'category': 'Livres', 'description': 'Livre Python pour les Nuls édition 2024'},
            {'name': 'Le Petit Prince', 'reference': 'PPR-CLA-FR', 'price': 8.90, 'quantity': 35, 'category': 'Livres', 'description': 'Le Petit Prince - Antoine de Saint-Exupéry'},
            {'name': 'Guide du Routard Paris', 'reference': 'RTD-PAR-2024', 'price': 15.90, 'quantity': 0, 'category': 'Livres', 'description': 'Guide du Routard Paris 2024'},
        ]
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            products.append(product)
            db.session.add(product)
        
        db.session.commit()
        
        # Créer des ventes de test
        print("Création des ventes de test...")
        
        # Générer des ventes sur les 30 derniers jours
        for i in range(50):  # 50 ventes de test
            # Sélectionner un produit aléatoire qui a du stock
            available_products = [p for p in products if p.quantity > 0]
            if not available_products:
                break
                
            product = random.choice(available_products)
            user_to_use = random.choice([admin, user])
            
            # Quantité vendue (1 à min(5, stock_disponible))
            max_quantity = min(5, product.quantity)
            if max_quantity <= 0:
                continue
                
            quantity_sold = random.randint(1, max_quantity)
            
            # Date de vente aléatoire dans les 30 derniers jours
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            sale_date = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # Créer la vente
            sale = Sale(
                product_id=product.id,
                user_id=user_to_use.id,
                quantity_sold=quantity_sold,
                unit_price=product.price,
                total_price=product.price * quantity_sold,
                sale_date=sale_date
            )
            
            # Réduire le stock
            product.quantity -= quantity_sold
            
            db.session.add(sale)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Base de données initialisée avec succès !")
        print("="*50)
        print(f"Utilisateurs créés: {User.query.count()}")
        print(f"Produits créés: {Product.query.count()}")
        print(f"Ventes créées: {Sale.query.count()}")
        print("\nComptes utilisateur:")
        print("- Admin: admin / admin123")
        print("- Vendeur: vendeur / vendeur123")
        print("="*50)

if __name__ == '__main__':
    init_database()