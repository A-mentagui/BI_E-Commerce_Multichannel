"""
RFM Analysis - Customer Segmentation based on Recency, Frequency, Monetary
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class RFMAnalyzer:
    """Performs RFM analysis and customer segmentation"""
    
    def __init__(self, orders_df, customers_df, current_date=None):
        """
        Initialize RFM Analyzer
        
        Parameters:
        -----------
        orders_df : pd.DataFrame
            Orders data with CustomerID, OrderDate, Revenue
        customers_df : pd.DataFrame
            Customer data with CustomerID, Segment
        current_date : str
            Reference date for Recency calculation (default: today)
        """
        self.orders = orders_df.copy()
        self.customers = customers_df.copy()
        self.current_date = current_date or datetime.now()
        self.rfm = None
        self.segments = None
    
    def calculate_rfm(self):
        """Calculate RFM metrics for each customer"""
        
        print("📊 Calculating RFM metrics...")
        
        # Convert OrderDate to datetime
        self.orders['OrderDate'] = pd.to_datetime(self.orders['OrderDate'])
        
        # Ensure current_date is datetime
        if isinstance(self.current_date, str):
            reference_date = pd.to_datetime(self.current_date)
        else:
            reference_date = pd.to_datetime(self.current_date)
        
        # Group by customer
        rfm = self.orders.groupby('CustomerID').agg({
            'OrderDate': 'max',  # For Recency
            'OrderID': 'count',   # For Frequency
            'Revenue': 'sum'      # For Monetary
        }).reset_index()
        
        rfm.columns = ['CustomerID', 'LastPurchaseDate', 'Frequency', 'Monetary']
        
        # Calculate Recency (days since last purchase)
        rfm['Recency'] = (reference_date - rfm['LastPurchaseDate']).dt.days
        
        # Ensure positive values
        rfm['Recency'] = rfm['Recency'].clip(lower=0)
        
        self.rfm = rfm[['CustomerID', 'Recency', 'Frequency', 'Monetary']].copy()
        
        # Calculate quartiles for score assignment
        self._assign_rfm_scores()
        
        print(f"✓ RFM calculated for {len(self.rfm)} customers")
        return self.rfm
    
    def _assign_rfm_scores(self):
        """Assign RFM scores on 1-4 scale"""
        
        # Recency: Lower is better (1 = most recent)
        self.rfm['R_Score'] = pd.qcut(self.rfm['Recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
        
        # Frequency: Higher is better (4 = most frequent)
        self.rfm['F_Score'] = pd.qcut(self.rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
        
        # Monetary: Higher is better (4 = highest spending)
        self.rfm['M_Score'] = pd.qcut(self.rfm['Monetary'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
        
        # Convert to numeric
        self.rfm['R_Score'] = self.rfm['R_Score'].astype(int)
        self.rfm['F_Score'] = self.rfm['F_Score'].astype(int)
        self.rfm['M_Score'] = self.rfm['M_Score'].astype(int)
        
        # Calculate RFM Score: Concatenate scores
        self.rfm['RFM_Score'] = (self.rfm['R_Score'].astype(str) + 
                                  self.rfm['F_Score'].astype(str) + 
                                  self.rfm['M_Score'].astype(str))
    
    def segment_customers(self):
        """Segment customers based on RFM scores"""
        
        print("🎯 Segmenting customers...")
        
        def assign_segment(row):
            """Assign segment based on RFM scores logic"""
            
            r = row['R_Score']
            f = row['F_Score']
            m = row['M_Score']
            
            # Champions (Best customers): High R, High F, High M
            if r >= 3 and f >= 3 and m >= 3:
                return 'Champions'
            
            # Loyal Customers: High F, High M
            elif f >= 3 and m >= 3:
                return 'Loyal Customers'
            
            # Potential Loyalists: Recent, Good F, Good M
            elif r >= 3 and f >= 2 and m >= 2:
                return 'Potential Loyalists'
            
            # At Risk: Low R but was good customer
            elif r < 2 and f >= 2 and m >= 2:
                return 'At Risk'
            
            # Can't Lose Them: Was champion, recent inactivity
            elif r < 2 and f >= 3:
                return 'Can\'t Lose Them'
            
            # Lost: Very low R, F, M
            elif r == 1 and f <= 2 and m <= 2:
                return 'Lost'
            
            # Dormant: Low activity
            elif f <= 1:
                return 'Dormant'
            
            # New Customers: High R, Low F, Low M
            elif r >= 3 and f == 1:
                return 'New Customers'
            
            else:
                return 'Need Attention'
        
        self.rfm['Segment'] = self.rfm.apply(assign_segment, axis=1)
        self.segments = self.rfm.copy()
        
        print(f"✓ Customers segmented into {self.segments['Segment'].nunique()} segments")
        return self.segments
    
    def get_segment_summary(self):
        """Get summary statistics by segment"""
        
        summary = self.segments.groupby('Segment').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            'R_Score': 'mean',
            'F_Score': 'mean',
            'M_Score': 'mean'
        }).round(2)
        
        summary.columns = ['Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 
                          'Avg_R_Score', 'Avg_F_Score', 'Avg_M_Score']
        summary['Percent'] = (summary['Count'] / summary['Count'].sum() * 100).round(1)
        
        return summary.sort_values('Avg_Monetary', ascending=False)
    
    def plot_rfm_distribution(self):
        """Visualize RFM distribution"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Recency distribution
        axes[0, 0].hist(self.rfm['Recency'], bins=50, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Recency Distribution (Days)', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Days Since Last Purchase')
        axes[0, 0].set_ylabel('Count')
        
        # Frequency distribution
        axes[0, 1].hist(self.rfm['Frequency'], bins=30, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('Frequency Distribution', fontsize=12, fontweight='bold')
        axes[0, 1].set_xlabel('Number of Purchases')
        axes[0, 1].set_ylabel('Count')
        
        # Monetary distribution
        axes[1, 0].hist(self.rfm['Monetary'], bins=50, color='lightcoral', edgecolor='black')
        axes[1, 0].set_title('Monetary Distribution (€)', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Total Spending (€)')
        axes[1, 0].set_ylabel('Count')
        
        # Segment count
        segment_counts = self.segments['Segment'].value_counts()
        axes[1, 1].barh(segment_counts.index, segment_counts.values, color='mediumpurple', edgecolor='black')
        axes[1, 1].set_title('Customer Count by Segment', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Count')
        
        plt.tight_layout()
        plt.savefig('results/rfm_distribution.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/rfm_distribution.png")
        plt.close()
    
    def plot_segments(self):
        """Visualize segments with different aspects"""
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        segment_data = self.segments.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        
        # Recency by segment
        segment_data['Recency'].sort_values().plot(kind='barh', ax=axes[0], color='skyblue', edgecolor='black')
        axes[0].set_title('Average Recency by Segment', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Days Since Last Purchase')
        
        # Frequency by segment
        segment_data['Frequency'].sort_values().plot(kind='barh', ax=axes[1], color='lightgreen', edgecolor='black')
        axes[1].set_title('Average Frequency by Segment', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Number of Purchases')
        
        # Monetary by segment
        segment_data['Monetary'].sort_values().plot(kind='barh', ax=axes[2], color='lightcoral', edgecolor='black')
        axes[2].set_title('Average Monetary by Segment', fontsize=12, fontweight='bold')
        axes[2].set_xlabel('Total Spending (€)')
        
        plt.tight_layout()
        plt.savefig('results/rfm_segments.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/rfm_segments.png")
        plt.close()
    
    def plot_3d_rfm(self):
        """Create 3D scatter plot of RFM"""
        
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Color by segment
        colors = {'Champions': 'red', 'Loyal Customers': 'orange', 
                 'Potential Loyalists': 'yellow', 'At Risk': 'purple',
                 'Can\'t Lose Them': 'brown', 'Lost': 'black',
                 'Dormant': 'gray', 'New Customers': 'green', 'Need Attention': 'blue'}
        
        for segment in self.segments['Segment'].unique():
            data = self.segments[self.segments['Segment'] == segment]
            ax.scatter(data['Recency'], data['Frequency'], data['Monetary'],
                      label=segment, s=50, alpha=0.6, color=colors.get(segment, 'blue'))
        
        ax.set_xlabel('Recency (days)')
        ax.set_ylabel('Frequency (#)')
        ax.set_zlabel('Monetary (€)')
        ax.set_title('RFM 3D Visualization', fontsize=14, fontweight='bold')
        ax.legend()
        
        plt.savefig('results/rfm_3d.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/rfm_3d.png")
        plt.close()
    
    def export_results(self, filename='results/rfm_analysis_results.csv'):
        """Export RFM analysis results"""
        
        # Merge with customer data
        result = self.segments.merge(self.customers[['CustomerID']], on='CustomerID', how='left')
        result.to_csv(filename, index=False)
        print(f"💾 Exported: {filename}")
        
        # Also export segment summary
        summary = self.get_segment_summary()
        summary.to_csv('results/rfm_segment_summary.csv')
        print(f"💾 Exported: results/rfm_segment_summary.csv")
        
        return result


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("RFM ANALYSIS - CUSTOMER SEGMENTATION")
    print("="*60 + "\n")
    
    # Load data
    print("[*] Loading data...")
    orders_df = pd.read_csv('data/raw/orders.csv')
    customers_df = pd.read_csv('data/raw/customers.csv')
    print("[OK] Data loaded")
    
    # Initialize and run analysis
    analyzer = RFMAnalyzer(orders_df, customers_df, current_date='2024-02-15')
    
    # Calculate RFM
    rfm_df = analyzer.calculate_rfm()
    print("\nRFM Statistics:")
    print(rfm_df.describe())
    
    # Segment customers
    segments_df = analyzer.segment_customers()
    
    # Display summary
    print("\n" + "="*60)
    print("SEGMENT SUMMARY")
    print("="*60)
    summary = analyzer.get_segment_summary()
    print(summary)
    
    # Visualizations
    print("\n[*] Creating visualizations...")
    analyzer.plot_rfm_distribution()
    analyzer.plot_segments()
    analyzer.plot_3d_rfm()
    
    # Export results
    print("\n[*] Exporting results...")
    analyzer.export_results()
    
    print("\n✅ RFM Analysis Complete!")
    print("\nKey Insights:")
    print(f"- Total Customers: {len(segments_df)}")
    print(f"- Champions: {len(segments_df[segments_df['Segment'] == 'Champions'])} ({len(segments_df[segments_df['Segment'] == 'Champions'])/len(segments_df)*100:.1f}%)")
    print(f"- Loyal Customers: {len(segments_df[segments_df['Segment'] == 'Loyal Customers'])} ({len(segments_df[segments_df['Segment'] == 'Loyal Customers'])/len(segments_df)*100:.1f}%)")
    print(f"- At Risk: {len(segments_df[segments_df['Segment'] == 'At Risk'])} ({len(segments_df[segments_df['Segment'] == 'At Risk'])/len(segments_df)*100:.1f}%)")
    print(f"- Lost: {len(segments_df[segments_df['Segment'] == 'Lost'])} ({len(segments_df[segments_df['Segment'] == 'Lost'])/len(segments_df)*100:.1f}%)")


if __name__ == "__main__":
    main()
