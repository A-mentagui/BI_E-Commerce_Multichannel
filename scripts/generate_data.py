"""
Synthetic E-commerce Data Generator
Generates realistic multi-channel e-commerce data for BI project
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

fake = Faker('fr_FR')  # French locale
random.seed(42)
np.random.seed(42)

# Configuration
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 2, 15)
NUM_CUSTOMERS = 10000
NUM_PRODUCTS = 500
NUM_ORDERS = 50000
CHANNELS = ['Web', 'Mobile', 'Pop-Up', 'Réseaux Sociaux']
CATEGORIES = [
    'Électronique', 'Mode & Vêtements', 'Beauté & Santé', 'Sports & Loisirs',
    'Maison & Jardin', 'Livres & Médias', 'Jouets & Enfants', 'Alimentation',
    'Chaussures', 'Accessoires', 'Informatique', 'Téléphonie', 'Montres',
    'Bijoux', 'Chaussettes & Lingerie', 'Sacs & Bagages', 'Art & Crafts',
    'Auto & Moto', 'Pet Care', 'Gaming'
]
REGIONS = [
    'Île-de-France', 'Provence-Alpes-Côte d\'Azur', 'Auvergne-Rhône-Alpes',
    'Nouvelle-Aquitaine', 'Occitanie', 'Bourgogne-Franche-Comté', 'Bretagne',
    'Normandie', 'Hauts-de-France', 'Pays de la Loire', 'Centre-Val de Loire',
    'Grand Est', 'Corse'
]
DELIVERY_METHODS = ['Standard (5-7 jours)', 'Express (2-3 jours)', 'Urgent (24h)', 'Retrait en point']
RETURN_REASONS = [
    'Produit défectueux', 'Mauvaise taille', 'Produit différent', 
    'Délai de livraison trop long', 'Insatisfait de la qualité', 'Changement d\'avis'
]


def generate_customers(num_customers):
    """Generate customer dimension"""
    print(f"[1/7] Generating {num_customers} customers...")
    
    customers = []
    segments = ['Nouveau', 'Régulier', 'Fidèle']
    
    for i in range(num_customers):
        customer_id = f"CUST{i:06d}"
        segment = np.random.choice(segments, p=[0.25, 0.50, 0.25])
        registration_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        
        customers.append({
            'CustomerID': customer_id,
            'CustomerName': fake.name(),
            'Email': fake.email(),
            'Segment': segment,
            'RegistrationDate': registration_date,
            'Country': 'France',
            'City': fake.city(),
            'PostalCode': fake.postcode()
        })
    
    return pd.DataFrame(customers)


def generate_products(num_products):
    """Generate product dimension"""
    print(f"[2/7] Generating {num_products} products...")
    
    products = []
    product_id = 0
    
    for category in CATEGORIES:
        num_cat_products = num_products // len(CATEGORIES)
        for _ in range(num_cat_products):
            product_id += 1
            products.append({
                'ProductID': f"PROD{product_id:06d}",
                'ProductName': fake.word() + ' ' + category.lower(),
                'Category': category,
                'SubCategory': fake.word(),
                'Price': round(np.random.lognormal(mean=4, sigma=0.8), 2),  # Realistic price distribution
                'Supplier': fake.company(),
                'Stock': np.random.randint(0, 500)
            })
    
    return pd.DataFrame(products)


def generate_channels():
    """Generate channel dimension"""
    print("[3/7] Generating channels...")
    
    channels = []
    for i, channel in enumerate(CHANNELS):
        channels.append({
            'ChannelID': f"CHAN{i:02d}",
            'ChannelName': channel,
            'ChannelType': 'Digital' if channel != 'Pop-Up' else 'Physical'
        })
    
    return pd.DataFrame(channels)


def generate_regions():
    """Generate region dimension"""
    print("[4/7] Generating regions...")
    
    regions = []
    for i, region in enumerate(REGIONS):
        regions.append({
            'RegionID': f"REG{i:02d}",
            'RegionName': region,
            'Country': 'France',
            'Population': np.random.randint(500000, 12000000)
        })
    
    return pd.DataFrame(regions)


def generate_orders(num_orders, customers_df, products_df, channels_df, regions_df):
    """Generate orders (fact table)"""
    print(f"[5/7] Generating {num_orders} orders...")
    
    orders = []
    
    # Channel distribution and pricing rules
    channel_dist = {'Web': 0.50, 'Mobile': 0.35, 'Pop-Up': 0.10, 'Réseaux Sociaux': 0.05}
    channel_basket = {
        'Web': (75, 150),
        'Mobile': (50, 100),
        'Pop-Up': (100, 250),
        'Réseaux Sociaux': (30, 80)
    }
    
    for i in range(num_orders):
        order_id = f"ORD{i:08d}"
        
        # Select random dimensions
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        channel = np.random.choice(list(channel_dist.keys()), p=list(channel_dist.values()))
        channel_id = channels_df[channels_df['ChannelName'] == channel].iloc[0]['ChannelID']
        region = regions_df.sample(1).iloc[0]
        
        # Generate order details
        order_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        quantity = np.random.randint(1, 5)
        
        # Price influenced by channel
        base_price = product['Price']
        min_basket, max_basket = channel_basket[channel]
        basket_value = np.random.uniform(min_basket, max_basket)
        revenue = round(basket_value, 2)
        
        # Apply discount (10% chance)
        discount = round(revenue * 0.1, 2) if random.random() < 0.1 else 0
        revenue -= discount
        
        # Delivery method
        delivery_method = np.random.choice(DELIVERY_METHODS, p=[0.40, 0.35, 0.15, 0.10])
        
        orders.append({
            'OrderID': order_id,
            'CustomerID': customer['CustomerID'],
            'ProductID': product['ProductID'],
            'ChannelID': channel_id,
            'ChannelName': channel,
            'RegionID': region['RegionID'],
            'RegionName': region['RegionName'],
            'OrderDate': order_date,
            'Quantity': quantity,
            'UnitPrice': round(base_price, 2),
            'Revenue': revenue,
            'Discount': discount,
            'DeliveryMethod': delivery_method,
            'OrderStatus': np.random.choice(['Complété', 'Livré', 'En cours', 'Annulé'], p=[0.70, 0.20, 0.05, 0.05])
        })
    
    return pd.DataFrame(orders)


def generate_returns(orders_df):
    """Generate returns based on orders"""
    print("[6/7] Generating returns...")
    
    returns = []
    
    # Return rates vary by channel
    return_rates = {'Web': 0.08, 'Mobile': 0.06, 'Pop-Up': 0.12, 'Réseaux Sociaux': 0.15}
    
    for _, order in orders_df.iterrows():
        channel = order['ChannelName']
        return_rate = return_rates.get(channel, 0.08)
        
        if random.random() < return_rate and order['OrderStatus'] == 'Livré':
            return_id = f"RET{len(returns):08d}"
            return_date = order['OrderDate'] + timedelta(days=np.random.randint(1, 30))
            
            returns.append({
                'ReturnID': return_id,
                'OrderID': order['OrderID'],
                'ReturnDate': return_date,
                'ReturnReason': np.random.choice(RETURN_REASONS),
                'RefundAmount': order['Revenue']
            })
    
    return pd.DataFrame(returns)


def generate_feedback(orders_df, returns_df):
    """Generate customer feedback/satisfaction"""
    print("[7/7] Generating feedback...")
    
    feedback = []
    
    # Satisfaction inversely correlated with delivery delays
    for idx, order in orders_df.iterrows():
        if random.random() < 0.70:  # 70% of customers provide feedback
            feedback_id = f"FB{idx:08d}"
            
            # Check if product was returned
            is_returned = order['OrderID'] in returns_df['OrderID'].values
            
            # Satisfaction based on delivery and returns
            if is_returned:
                satisfaction = np.random.randint(1, 4)  # Low satisfaction
            elif 'Express' in order['DeliveryMethod'] or 'Urgent' in order['DeliveryMethod']:
                satisfaction = np.random.randint(4, 6)  # High satisfaction
            else:
                satisfaction = np.random.randint(2, 5)  # Medium satisfaction
            
            feedback.append({
                'FeedbackID': feedback_id,
                'OrderID': order['OrderID'],
                'Satisfaction': satisfaction,
                'Comment': fake.sentence(nb_words=10) if random.random() < 0.5 else None,
                'FeedbackDate': order['OrderDate'] + timedelta(days=np.random.randint(3, 15))
            })
    
    return pd.DataFrame(feedback)


def main():
    """Main data generation function"""
    print("\n" + "="*60)
    print("E-COMMERCE SYNTHETIC DATA GENERATOR")
    print("="*60 + "\n")
    
    # Create data directory
    data_dir = 'data/raw'
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate all tables
    customers_df = generate_customers(NUM_CUSTOMERS)
    products_df = generate_products(NUM_PRODUCTS)
    channels_df = generate_channels()
    regions_df = generate_regions()
    orders_df = generate_orders(NUM_ORDERS, customers_df, products_df, channels_df, regions_df)
    returns_df = generate_returns(orders_df)
    feedback_df = generate_feedback(orders_df, returns_df)
    
    # Save to CSV
    print("\n" + "="*60)
    print("SAVING DATA TO CSV FILES")
    print("="*60 + "\n")
    
    customers_df.to_csv(f'{data_dir}/customers.csv', index=False)
    print(f"✓ customers.csv ({len(customers_df)} rows)")
    
    products_df.to_csv(f'{data_dir}/products.csv', index=False)
    print(f"✓ products.csv ({len(products_df)} rows)")
    
    channels_df.to_csv(f'{data_dir}/channels.csv', index=False)
    print(f"✓ channels.csv ({len(channels_df)} rows)")
    
    regions_df.to_csv(f'{data_dir}/regions.csv', index=False)
    print(f"✓ regions.csv ({len(regions_df)} rows)")
    
    orders_df.to_csv(f'{data_dir}/orders.csv', index=False)
    print(f"✓ orders.csv ({len(orders_df)} rows)")
    
    returns_df.to_csv(f'{data_dir}/returns.csv', index=False)
    print(f"✓ returns.csv ({len(returns_df)} rows)")
    
    feedback_df.to_csv(f'{data_dir}/feedback.csv', index=False)
    print(f"✓ feedback.csv ({len(feedback_df)} rows)")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    print(f"\n📊 Customers: {len(customers_df)}")
    print(f"📊 Products: {len(products_df)}")
    print(f"📊 Channels: {len(channels_df)}")
    print(f"📊 Regions: {len(regions_df)}")
    print(f"📊 Orders: {len(orders_df)}")
    print(f"📊 Returns: {len(returns_df)} ({len(returns_df)/len(orders_df)*100:.2f}%)")
    print(f"📊 Feedback: {len(feedback_df)}")
    
    print(f"\n💰 Total Revenue: €{orders_df['Revenue'].sum():,.2f}")
    print(f"📈 Average Basket: €{orders_df['Revenue'].mean():,.2f}")
    print(f"📈 Total Quantity Sold: {orders_df['Quantity'].sum()}")
    
    print(f"\n📅 Period: {START_DATE.date()} to {END_DATE.date()}")
    print(f"✓ All files saved in '{data_dir}/' folder")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
