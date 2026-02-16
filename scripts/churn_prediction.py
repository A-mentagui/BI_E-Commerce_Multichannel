"""
Churn Prediction - Predict which customers are likely to stop purchasing
Uses Random Forest classification model
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (classification_report, confusion_matrix, 
                             roc_auc_score, roc_curve, auc)
import warnings

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class ChurnPredictor:
    """Predicts customer churn risk using machine learning"""
    
    def __init__(self, orders_df, returns_df, feedback_df, current_date='2024-02-15'):
        """
        Initialize Churn Predictor
        
        Parameters:
        -----------
        orders_df : pd.DataFrame
            Orders data
        returns_df : pd.DataFrame
            Returns data
        feedback_df : pd.DataFrame
            Feedback/satisfaction data
        current_date : str
            Reference date for analysis
        """
        self.orders = orders_df.copy()
        self.returns = returns_df.copy()
        self.feedback = feedback_df.copy()
        self.current_date = pd.to_datetime(current_date)
        self.features = None
        self.model = None
        self.predictions = None
    
    def create_features(self, churn_threshold_days=180):
        """
        Create features for churn prediction
        
        Definition of Churn: No purchase in last 'churn_threshold_days' days
        """
        
        print(f"🔧 Creating features (churn threshold: {churn_threshold_days} days)...")
        
        # Convert dates
        self.orders['OrderDate'] = pd.to_datetime(self.orders['OrderDate'])
        if len(self.returns) > 0:
            self.returns['ReturnDate'] = pd.to_datetime(self.returns['ReturnDate'])
        if len(self.feedback) > 0 and 'FeedbackDate' in self.feedback.columns:
            self.feedback['FeedbackDate'] = pd.to_datetime(self.feedback['FeedbackDate'])
        
        # Get unique customers from orders
        customers = self.orders['CustomerID'].unique()
        features = pd.DataFrame({'CustomerID': customers})
        
        # Feature 1: Recency (Days since last purchase)
        recency = self.orders.groupby('CustomerID')['OrderDate'].max().reset_index()
        recency.columns = ['CustomerID', 'LastPurchase']
        recency['Recency'] = (self.current_date - recency['LastPurchase']).dt.days
        features = features.merge(recency[['CustomerID', 'Recency']], on='CustomerID', how='left')
        
        # Feature 2: Frequency (Number of purchases)
        frequency = self.orders.groupby('CustomerID').size().reset_index(name='Frequency')
        features = features.merge(frequency, on='CustomerID', how='left')
        
        # Feature 3: Monetary (Total spending)
        monetary = self.orders.groupby('CustomerID')['Revenue'].sum().reset_index(name='Monetary')
        features = features.merge(monetary, on='CustomerID', how='left')
        
        # Feature 4: Average Basket
        avg_basket = self.orders.groupby('CustomerID')['Revenue'].mean().reset_index(name='AvgBasket')
        features = features.merge(avg_basket, on='CustomerID', how='left')
        
        # Feature 5: Return Rate
        orders_count = self.orders.groupby('CustomerID').size().reset_index(name='TotalOrders')
        features = features.merge(orders_count, on='CustomerID', how='left')
        if len(self.returns) > 0:
            returns_count = self.returns.groupby(self.returns['OrderID'].map(
                self.orders.set_index('OrderID')['CustomerID']
            )).size().reset_index(name='ReturnCount')
            returns_count.columns = ['CustomerID', 'ReturnCount']
            features = features.merge(returns_count, on='CustomerID', how='left')
            features['ReturnRate'] = (features['ReturnCount'].fillna(0) / features['TotalOrders'] * 100).round(2)
        else:
            features['ReturnRate'] = 0
        
        # Feature 6: Average Satisfaction
        if len(self.feedback) > 0 and 'Satisfaction' in self.feedback.columns:
            satisfaction = self.feedback.groupby(self.feedback['OrderID'].map(
                self.orders.set_index('OrderID')['CustomerID']
            ))['Satisfaction'].mean().reset_index(name='AvgSatisfaction')
            satisfaction.columns = ['CustomerID', 'AvgSatisfaction']
            features = features.merge(satisfaction, on='CustomerID', how='left')
        else:
            features['AvgSatisfaction'] = 0
        
        # Feature 7: Purchase Recency in Months
        features['RecencyMonths'] = np.ceil(features['Recency'] / 30).astype(int)
        
        # Feature 8: Days since First Purchase (Account Age)
        first_purchase = self.orders.groupby('CustomerID')['OrderDate'].min().reset_index(name='FirstPurchase')
        first_purchase['AccountAgeDays'] = (self.current_date - first_purchase['FirstPurchase']).dt.days
        features = features.merge(first_purchase[['CustomerID', 'AccountAgeDays']], on='CustomerID', how='left')
        
        # Feature 9: Time since Last Purchase Ratio (Recent activity measure)
        features['RecentActivityRatio'] = np.where(
            features['AccountAgeDays'] > 0,
            features['Recency'] / features['AccountAgeDays'],
            0
        )
        
        # Create Target Variable
        #  Churn = 1 if no purchase in last churn_threshold_days, else 0
        features['Churn'] = (features['Recency'] > churn_threshold_days).astype(int)
        
        # Handle missing values
        features = features.fillna(0)
        
        self.features = features
        
        print(f"✓ Features created for {len(features)} customers")
        print(f"  - Churn cases: {(features['Churn'] == 1).sum()} ({(features['Churn'] == 1).sum()/len(features)*100:.1f}%)")
        print(f"  - Active cases: {(features['Churn'] == 0).sum()} ({(features['Churn'] == 0).sum()/len(features)*100:.1f}%)")
        
        return features
    
    def train_model(self, test_size=0.2, random_state=42):
        """Train Random Forest model"""
        
        print("\n🤖 Training Random Forest model...")
        
        # Select features (exclude CustomerID and target)
        feature_cols = [col for col in self.features.columns 
                       if col not in ['CustomerID', 'Churn', 'LastPurchase', 'FirstPurchase']]
        X = self.features[feature_cols]
        y = self.features['Churn']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=random_state,
            n_jobs=-1,
            class_weight='balanced'  # Handle imbalanced classes
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"✓ Model trained")
        print(f"  - Train Accuracy: {train_score:.4f}")
        print(f"  - Test Accuracy: {test_score:.4f}")
        
        # Get predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Classification report
        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['Active', 'Churn']))
        
        # ROC-AUC
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        print(f"ROC-AUC Score: {roc_auc:.4f}")
        
        # Store test data for visualization
        self.X_test = X_test
        self.y_test = y_test
        self.y_pred = y_pred
        self.y_pred_proba = y_pred_proba
        self.feature_cols = feature_cols
        
        return self.model
    
    def predict_churn(self):
        """Predict churn probability for all customers"""
        
        print("\n🔮 Predicting churn risk for all customers...")
        
        X = self.features[self.feature_cols]
        churn_proba = self.model.predict_proba(X)[:, 1]
        
        self.features['ChurnProbability'] = churn_proba
        self.features['ChurnRisk'] = pd.cut(
            churn_proba,
            bins=[0, 0.25, 0.50, 0.75, 1.0],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        self.predictions = self.features.copy()
        
        # Summary
        print(f"✓ Predictions complete")
        print("\nChurn Risk Distribution:")
        print(self.predictions['ChurnRisk'].value_counts().sort_index())
        
        return self.predictions
    
    def get_high_risk_customers(self, threshold=0.5):
        """Get customers with high churn risk"""
        
        high_risk = self.predictions[self.predictions['ChurnProbability'] >= threshold].sort_values(
            'ChurnProbability', ascending=False
        )
        
        return high_risk[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'ChurnProbability', 'ChurnRisk']]
    
    def feature_importance(self):
        """Get feature importance"""
        
        importance_df = pd.DataFrame({
            'Feature': self.feature_cols,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        return importance_df
    
    def plot_feature_importance(self):
        """Visualize feature importance"""
        
        importance_df = self.feature_importance()
        
        plt.figure(figsize=(10, 6))
        plt.barh(importance_df['Feature'], importance_df['Importance'], color='steelblue', edgecolor='black')
        plt.xlabel('Importance', fontsize=12)
        plt.title('Feature Importance - Churn Prediction', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('results/churn_feature_importance.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/churn_feature_importance.png")
        plt.close()
    
    def plot_roc_curve(self):
        """Plot ROC curve"""
        
        fpr, tpr, _ = roc_curve(self.y_test, self.y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title('ROC Curve - Churn Prediction', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right", fontsize=11)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('results/churn_roc_curve.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/churn_roc_curve.png")
        plt.close()
    
    def plot_confusion_matrix(self):
        """Plot confusion matrix"""
        
        cm = confusion_matrix(self.y_test, self.y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Active', 'Churn'],
                   yticklabels=['Active', 'Churn'])
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.title('Confusion Matrix - Churn Prediction', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('results/churn_confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/churn_confusion_matrix.png")
        plt.close()
    
    def plot_churn_distribution(self):
        """Plot churn probability distribution"""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(self.predictions['ChurnProbability'], bins=50, 
                    color='steelblue', edgecolor='black', alpha=0.7)
        axes[0].axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='Decision Threshold (0.5)')
        axes[0].set_xlabel('Churn Probability', fontsize=12)
        axes[0].set_ylabel('Count', fontsize=12)
        axes[0].set_title('Distribution of Churn Probability', fontsize=12, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Risk categories
        risk_counts = self.predictions['ChurnRisk'].value_counts()
        colors = ['green', 'yellow', 'orange', 'red']
        axes[1].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
        axes[1].set_title('Churn Risk Categories', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/churn_distribution.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: results/churn_distribution.png")
        plt.close()
    
    def export_results(self, filename='results/churn_predictions.csv'):
        """Export predictions"""
        
        export_df = self.predictions[[
            'CustomerID', 'Recency', 'Frequency', 'Monetary', 'AvgSatisfaction',
            'ReturnRate', 'ChurnProbability', 'ChurnRisk'
        ]].sort_values('ChurnProbability', ascending=False)
        
        export_df.to_csv(filename, index=False)
        print(f"💾 Exported: {filename}")
        
        # Also export feature importance
        self.feature_importance().to_csv('results/churn_feature_importance.csv', index=False)
        print(f"💾 Exported: results/churn_feature_importance.csv")
        
        return export_df


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("CHURN PREDICTION - CUSTOMER RETENTION")
    print("="*60 + "\n")
    
    # Load data
    print("📂 Loading data...")
    orders_df = pd.read_csv('data/raw/orders.csv')
    returns_df = pd.read_csv('data/raw/returns.csv')
    feedback_df = pd.read_csv('data/raw/feedback.csv')
    print("✓ Data loaded")
    
    # Initialize predictor
    predictor = ChurnPredictor(orders_df, returns_df, feedback_df)
    
    # Create features
    features_df = predictor.create_features(churn_threshold_days=180)
    
    # Train model
    predictor.train_model()
    
    # Predict churn
    predictions_df = predictor.predict_churn()
    
    # Get high-risk customers
    print("\n" + "="*60)
    print("HIGH-RISK CUSTOMERS (Churn Probability > 50%)")
    print("="*60)
    high_risk = predictor.get_high_risk_customers(threshold=0.5)
    print(high_risk.head(20))
    print(f"\nTotal High-Risk Customers: {len(high_risk)}")
    
    # Feature importance
    print("\n" + "="*60)
    print("FEATURE IMPORTANCE")
    print("="*60)
    print(predictor.feature_importance().head(10))
    
    # Visualizations
    print("\n📊 Creating visualizations...")
    predictor.plot_feature_importance()
    predictor.plot_roc_curve()
    predictor.plot_confusion_matrix()
    predictor.plot_churn_distribution()
    
    # Export results
    print("\n💾 Exporting results...")
    predictor.export_results()
    
    print("\n✅ Churn Prediction Complete!")


if __name__ == "__main__":
    main()
