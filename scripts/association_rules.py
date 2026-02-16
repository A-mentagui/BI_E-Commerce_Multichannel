"""
Association Rules Analysis - Market Basket Analysis
Identify products frequently purchased together using Apriori algorithm
"""

import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class AssociationAnalyzer:
    """Performs market basket analysis using association rules"""
    
    def __init__(self, orders_df, products_df):
        """
        Initialize Association Analyzer
        
        Parameters:
        -----------
        orders_df : pd.DataFrame
            Orders data with OrderID, CustomerID, ProductID
        products_df : pd.DataFrame
            Products data with ProductID, ProductName, Category
        """
        self.orders = orders_df.copy()
        self.products = products_df.copy()
        self.transaction_db = None
        self.rules = None
        self.item_support = None
    
    def create_transaction_db(self):
        """Create transaction database (items per order)"""
        
        print("📊 Creating transaction database...")
        
        # Group products by order
        transactions = self.orders.groupby('OrderID')['ProductID'].apply(list).reset_index()
        transactions.columns = ['OrderID', 'Items']
        
        # Get product names for readability
        self.transaction_db = transactions.copy()
        
        print(f"✓ Transaction DB created")
        print(f"  - Total Transactions: {len(transactions)}")
        print(f"  - Avg Items per Transaction: {np.mean([len(items) for items in transactions['Items']]):.2f}")
        print(f"  - Max Items in Transaction: {max([len(items) for items in transactions['Items']])}")
        
        return self.transaction_db
    
    def calculate_support(self, min_support=0.001):
        """Calculate support for all itemsets"""
        
        print(f"\n📉 Calculating support (min_support: {min_support})...")
        
        total_transactions = len(self.transaction_db)
        all_items = set()
        
        # Get all unique items
        for items in self.transaction_db['Items']:
            all_items.update(items)
        
        all_items = sorted(list(all_items))
        
        # Calculate support for single items
        item_support = {}
        item_count = {}
        
        for item in all_items:
            count = sum([1 for items in self.transaction_db['Items'] if item in items])
            support = count / total_transactions
            item_count[item] = count
            item_support[item] = support
        
        # Filter by min_support
        frequent_items = {k: v for k, v in item_support.items() if v >= min_support}
        
        # Create dataframe  - handle empty case
        if len(frequent_items) == 0:
            print(f"⚠ No frequent items found with min_support={min_support}, lowering threshold...")
            min_support = min(item_support.values()) * 0.1
            frequent_items = {k: v for k, v in item_support.items() if v >= min_support}
        
        self.item_support = pd.DataFrame([
            {'Item': item, 'Support': support, 'Count': item_count[item]} 
            for item, support in frequent_items.items()
        ])
        
        if len(self.item_support) > 0:
            self.item_support = self.item_support.sort_values('Support', ascending=False)
        
        print(f"✓ Support calculated for {len(self.item_support)} frequent items")
        
        return self.item_support
    
    def find_itemsets(self, min_support=0.01):
        """Find frequent itemsets using Apriori"""
        
        print(f"\n🔍 Finding frequent itemsets (min_support: {min_support})...")
        
        total_transactions = len(self.transaction_db)
        
        # Get frequent 1-itemsets
        frequent_itemsets = {
            frozenset([item]): support 
            for item, support in self.item_support.set_index('Item')['Support'].items()
        }
        
        # Generate k-itemsets
        k = 2
        while True:
            candidates = gen_candidates(frequent_itemsets, k)
            if not candidates:
                break
            
            # Count support for candidates
            candidate_support = {}
            for candidate in candidates:
                count = 0
                for items in self.transaction_db['Items']:
                    if candidate.issubset(set(items)):
                        count += 1
                support = count / total_transactions
                if support >= min_support:
                    candidate_support[candidate] = support
            
            if not candidate_support:
                break
            
            frequent_itemsets.update(candidate_support)
            k += 1
        
        self.frequent_itemsets = frequent_itemsets
        
        print(f"✓ Found {len(frequent_itemsets)} frequent itemsets")
        
        # Filter itemsets with 2+ items for rules
        multi_item_sets = {
            itemset: support 
            for itemset, support in frequent_itemsets.items() 
            if len(itemset) > 1
        }
        print(f"  - Itemsets with 2+ items: {len(multi_item_sets)}")
        
        return frequent_itemsets
    
    def generate_rules(self, min_confidence=0.3, min_lift=1.0):
        """Generate association rules from frequent itemsets"""
        
        print(f"\n⚙️ Generating rules (min_confidence: {min_confidence}, min_lift: {min_lift})...")
        
        rules = []
        
        # Get itemsets with 2+ items
        multi_item_sets = {
            itemset: support 
            for itemset, support in self.frequent_itemsets.items() 
            if len(itemset) > 1
        }
        
        for itemset, support in multi_item_sets.items():
            itemset_list = list(itemset)
            
            # Generate all possible rules from itemset
            for i in range(1, len(itemset_list)):
                for antecedent in combinations(itemset_list, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    
                    # Calculate confidence
                    antecedent_support = self.frequent_itemsets.get(antecedent, 0)
                    if antecedent_support == 0:
                        continue
                    
                    confidence = support / antecedent_support
                    if confidence < min_confidence:
                        continue
                    
                    # Calculate lift
                    consequent_support = self.frequent_itemsets.get(consequent, 0)
                    if consequent_support == 0:
                        continue
                    
                    lift = confidence / consequent_support
                    if lift < min_lift:
                        continue
                    
                    # Get product names
                    antecedent_names = ', '.join([
                        self.products[self.products['ProductID'] == pid]['ProductName'].values[0]
                        if pid in self.products['ProductID'].values else pid
                        for pid in antecedent
                    ])
                    
                    consequent_names = ', '.join([
                        self.products[self.products['ProductID'] == pid]['ProductName'].values[0]
                        if pid in self.products['ProductID'].values else pid
                        for pid in consequent
                    ])
                    
                    rules.append({
                        'Antecedent': antecedent_names,
                        'Consequent': consequent_names,
                        'Support': support,
                        'Confidence': confidence,
                        'Lift': lift,
                        'Count': int(support * len(self.transaction_db))
                    })
        
        self.rules = pd.DataFrame(rules).sort_values('Lift', ascending=False)
        
        print(f"✓ Generated {len(self.rules)} association rules")
        
        return self.rules
    
    def get_top_rules(self, n=20, metric='Lift'):
        """Get top N rules by specified metric"""
        
        return self.rules.nlargest(n, metric)
    
    def cross_selling_opportunities(self, n=10):
        """Get cross-selling opportunities"""
        
        opportunities = self.rules[
            (self.rules['Confidence'] >= 0.3) & 
            (self.rules['Lift'] > 1.2) &
            (self.rules['Count'] >= 5)  # At least 5 co-purchases
        ].sort_values('Lift', ascending=False).head(n)
        
        return opportunities[['Antecedent', 'Consequent', 'Confidence', 'Lift', 'Count']]
    
    def product_pairs_analysis(self, n=20):
        """Analyze top product pairs"""
        
        # Filter rules with high confidence and lift
        high_quality_rules = self.rules[
            (self.rules['Confidence'] >= 0.4) & 
            (self.rules['Lift'] > 1.5)
        ].head(n)
        
        return high_quality_rules[['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift']]
    
    def plot_support_distribution(self):
        """Plot support distribution"""
        
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(self.item_support)), self.item_support['Support'].values, 
               color='steelblue', edgecolor='black', alpha=0.7)
        plt.xlabel('Product (Ranked by Support)', fontsize=12)
        plt.ylabel('Support', fontsize=12)
        plt.title('Item Support Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('results/association_support.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/association_support.png")
        plt.close()
    
    def plot_rules_metrics(self):
        """Plot rules by confidence and lift"""
        
        if len(self.rules) == 0:
            print("⚠️ No rules to plot")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Confidence distribution
        axes[0].hist(self.rules['Confidence'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('Confidence', fontsize=12)
        axes[0].set_ylabel('Count', fontsize=12)
        axes[0].set_title('Distribution of Rule Confidence', fontsize=12, fontweight='bold')
        axes[0].axvline(x=0.3, color='red', linestyle='--', label='Min Threshold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Lift distribution
        axes[1].hist(self.rules['Lift'], bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('Lift', fontsize=12)
        axes[1].set_ylabel('Count', fontsize=12)
        axes[1].set_title('Distribution of Rule Lift', fontsize=12, fontweight='bold')
        axes[1].axvline(x=1.0, color='red', linestyle='--', label='No Association')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/association_rules_metrics.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/association_rules_metrics.png")
        plt.close()
    
    def plot_scatter_confidence_lift(self):
        """Plot rules scatter: Confidence vs Lift"""
        
        if len(self.rules) == 0:
            print("⚠️ No rules to plot")
            return
        
        plt.figure(figsize=(10, 8))
        
        # Size by support (scaled)
        sizes = self.rules['Support'] * 1000
        
        scatter = plt.scatter(
            self.rules['Confidence'], 
            self.rules['Lift'],
            s=sizes,
            alpha=0.6,
            c=self.rules['Count'],
            cmap='viridis',
            edgecolor='black',
            linewidth=0.5
        )
        
        plt.xlabel('Confidence', fontsize=12)
        plt.ylabel('Lift', fontsize=12)
        plt.title('Association Rules: Confidence vs Lift', fontsize=14, fontweight='bold')
        plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='No Association (Lift=1)')
        plt.grid(alpha=0.3)
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Co-purchase Count', fontsize=11)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('results/association_confidence_lift.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/association_confidence_lift.png")
        plt.close()
    
    def export_results(self):
        """Export analysis results"""
        
        # Export item support
        self.item_support.to_csv('results/association_item_support.csv', index=False)
        print("💾 Exported: results/association_item_support.csv")
        
        # Export rules
        if len(self.rules) > 0:
            self.rules.to_csv('results/association_rules.csv', index=False)
            print("💾 Exported: results/association_rules.csv")
            
            # Export cross-selling opportunities
            cross_sell = self.cross_selling_opportunities(n=50)
            cross_sell.to_csv('results/cross_selling_opportunities.csv', index=False)
            print("💾 Exported: results/cross_selling_opportunities.csv")


def gen_candidates(frequent_itemsets, k):
    """Generate k-itemset candidates from frequent (k-1)-itemsets"""
    
    frequent_items = [itemset for itemset in frequent_itemsets.keys() if len(itemset) == k - 1]
    
    candidates = set()
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate = frequent_items[i] | frequent_items[j]
            if len(candidate) == k:
                candidates.add(candidate)
    
    return candidates


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("ASSOCIATION RULES - MARKET BASKET ANALYSIS")
    print("="*60 + "\n")
    
    # Load data
    print("📂 Loading data...")
    orders_df = pd.read_csv('data/raw/orders.csv')
    products_df = pd.read_csv('data/raw/products.csv')
    print("✓ Data loaded")
    
    # Initialize analyzer
    analyzer = AssociationAnalyzer(orders_df, products_df)
    
    # Create transaction database
    analyzer.create_transaction_db()
    
    # Calculate support
    analyzer.calculate_support(min_support=0.01)
    
    # Find itemsets
    analyzer.find_itemsets(min_support=0.01)
    
    # Generate rules
    analyzer.generate_rules(min_confidence=0.2, min_lift=1.1)
    
    # Display results
    print("\n" + "="*60)
    print("TOP 10 ASSOCIATION RULES (by Lift)")
    print("="*60)
    print(analyzer.get_top_rules(n=10))
    
    print("\n" + "="*60)
    print("CROSS-SELLING OPPORTUNITIES")
    print("="*60)
    print(analyzer.cross_selling_opportunities(n=15))
    
    print("\n" + "="*60)
    print("TOP 15 PRODUCT PAIRS")
    print("="*60)
    print(analyzer.product_pairs_analysis(n=15))
    
    # Visualizations
    print("\n📊 Creating visualizations...")
    analyzer.plot_support_distribution()
    analyzer.plot_rules_metrics()
    analyzer.plot_scatter_confidence_lift()
    
    # Export results
    print("\n💾 Exporting results...")
    analyzer.export_results()
    
    print("\n✅ Association Rules Analysis Complete!")
    print(f"\nSummary:")
    print(f"- Total Rules Generated: {len(analyzer.rules)}")
    print(f"- Frequent Items: {len(analyzer.item_support)}")
    print(f"- Strong Rules (Lift > 1.5): {len(analyzer.rules[analyzer.rules['Lift'] > 1.5])}")


if __name__ == "__main__":
    main()
