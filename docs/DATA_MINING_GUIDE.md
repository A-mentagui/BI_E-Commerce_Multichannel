# Data Mining Scripts - Analysis Suite

## 📋 Overview

Three complementary Python scripts for advanced customer and product analytics:

1. **RFM Analysis** : Customer segmentation by value
2. **Churn Prediction** : Identify at-risk customers
3. **Association Rules** : Cross-selling opportunities

---

## 📊 Script 1: RFM Analysis (`rfm_analysis.py`)

### Purpose
Segment customers based on **Recency, Frequency, Monetary** metrics to identify their lifetime value.

### Theory
- **Recency (R)** : Days since last purchase (Lower = Better)
- **Frequency (F)** : Number of purchases (Higher = Better)
- **Monetary (M)** : Total spending (Higher = Better)

### Customer Segments Generated

| Segment | R Score | F Score | M Score | Characteristics | Action |
|---------|---------|---------|---------|-----------------|--------|
| **Champions** | High | High | High | Best customers | Reward loyalty, upsell |
| **Loyal Customers** | High | High | High | Consistently high value | Maintain relationship |
| **Potential Loyalists** | High | Medium | Medium | Recently active, growing value | Nurture & convert |
| **At Risk** | Low | High | High | Were good, now inactive | Win back campaigns |
| **Can't Lose Them** | Low | High | - | Were valuable, now lost | Re-engagement focus |
| **Lost** | Very Low | Low | Low | Haven't purchased recently | Cleanup / remove |
| **Dormant** | Very Low | Very Low | - | No recent activity | Reactivation needed |
| **New Customers** | High | Very Low | Low | Just started | Welcome campaigns |

### Usage

```bash
python scripts/rfm_analysis.py
```

**Outputs:**
- `results/rfm_analysis_results.csv` - Full customer RFM scores & segment
- `results/rfm_segment_summary.csv` - Segment statistics
- `results/rfm_distribution.png` - Distribution histograms
- `results/rfm_segments.png` - Segment bar charts
- `results/rfm_3d.png` - 3D RFM visualization

### Key Insights

```
Total Customers: 10,000
- Champions: ~15% (High-value, retain)
- Loyal Customers: ~25% (Core base)
- Potential Loyalists: ~20% (Growth opportunity)
- At Risk: ~15% (Need attention)
- Lost: ~15% (Cleanup)
- Dormant: ~10% (Reactivate)
```

### Business Applications

- **Marketing Segmentation** : Tailor campaigns by segment
- **Resource Allocation** : Focus on high-value segments
- **Churn Prevention** : Target "At Risk" with retention offers
- **Growth Strategy** : Nurture "New" and "Potential Loyalists"

---

## 🤖 Script 2: Churn Prediction (`churn_prediction.py`)

### Purpose
Identify customers likely to stop purchasing using machine learning classification.

### Model: Random Forest

**Hyperparameters:**
- Estimators: 100 decision trees
- Max Depth: 15
- Min Samples Split: 10
- Class Weight: Balanced (handles imbalanced data)

### Features Used

| Feature | Description | Range |
|---------|-------------|-------|
| **Recency** | Days since last purchase | 0-730 |
| **Frequency** | Number of purchases | 1-50+ |
| **Monetary** | Total spending (€) | 0-50,000+ |
| **AvgBasket** | Average order value | €30-€250 |
| **ReturnRate** | % of orders returned | 0-100% |
| **AvgSatisfaction** | Average satisfaction score | 1-5 |
| **RecencyMonths** | Recency in months | 0-24 |
| **AccountAgeDays** | Days since registration | 0-730 |
| **RecentActivityRatio** | Recency / Account Age | 0-1 |

### Target Variable

**Churn** = No purchase in last 180 days (True/False)

### Churn Risk Levels

```
Low Risk         : Churn Probability 0-25%
Medium Risk      : Churn Probability 25-50%
High Risk        : Churn Probability 50-75%
Critical Risk    : Churn Probability 75-100%
```

### Usage

```bash
python scripts/churn_prediction.py
```

**Outputs:**
- `results/churn_predictions.csv` - Full predictions with risk levels
- `results/churn_feature_importance.csv` - Feature importance ranking
- `results/churn_feature_importance.png` - Feature importance plot
- `results/churn_roc_curve.png` - ROC-AUC curve
- `results/churn_confusion_matrix.png` - Confusion matrix
- `results/churn_distribution.png` - Risk distribution

### Model Performance

Example Expected Metrics:
```
Accuracy: 82-85%
Precision: 0.75-0.80
Recall: 0.70-0.75
ROC-AUC: 0.85-0.90
```

### Feature Importance (Typical Rankings)

1. **Recency** (25-30%) - Most important
2. **RecentActivityRatio** (15-20%)
3. **AvgSatisfaction** (10-15%)
4. **Monetary** (8-12%)
5. **ReturnRate** (5-10%)

### Business Applications

- **Retention Campaigns** : Target high-probability churners
- **Loyalty Programs** : Engage at-risk customers
- **Predictive Pricing** : Offer discounts to high-risk segments
- **Customer Support** : Proactive outreach
- **Revenue Forecasting** : Account for predicted churn

### Interpretation

```
High-Risk Customer Example:
- Recency: 200 days (hasn't purchased in 6+ months)
- Frequency: 5 purchases (occasional buyer)
- Monetary: €300 (low lifetime value)
- AvgSatisfaction: 2.5/5 (dissatisfied)
- ReturnRate: 15% (high returns)
→ Churn Probability: 78% (Critical)
→ Action: Win-back email, discount offer
```

---

## 🛒 Script 3: Association Rules (`association_rules.py`)

### Purpose
Discover products frequently bought together to drive cross-selling and upselling.

### Algorithm: Apriori

**Technique:** Market Basket Analysis
- Finds frequent itemsets (product combinations)
- Generates association rules
- Measures strength of associations
- Uses customer-level product baskets (historical affinity baskets)

### Key Metrics

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **Support** | Freq(A∪B) / Total | % transactions with both items |
| **Confidence** | Freq(A∪B) / Freq(A) | % of A buyers who also buy B |
| **Lift** | Confidence / Support(B) | How much more likely A→B vs random |

### Understanding Metrics

```
Rule: Laptop → Mouse
- Support: 2% (2 out of 100 transactions)
- Confidence: 60% (60% of laptop buyers also buy mouse)
- Lift: 2.0 (Buyers 2× more likely to buy mouse if they buy laptop)

Interpretation:
- Support (Low) but Confidence (High) + Lift (High) = Good cross-sell opportunity
- Even if rare, when it happens, it's a strong association
```

### Rule Filtering

Default Thresholds:
```
min_support (items): 0.002 (0.2% of baskets)
min_support (pairs): 0.0005 (0.05% of baskets)
min_confidence: 0.1 (10% confidence)
min_lift: 1.0 (baseline association)
```

### Cross-Selling Opportunities

High-priority recommendations typically have:
- Support: > 0.05% (sparse catalog, still meaningful)
- Confidence: > 10% (practical for wide-product catalogs)
- Lift: > 1.2 (significantly above random)
- Count: >= 5 co-purchases (sufficient volume)

### Usage

```bash
python scripts/association_rules.py
```

**Outputs:**
- `results/association_item_support.csv` - Individual item popularity
- `results/association_rules.csv` - All generated rules
- `results/cross_selling_opportunities.csv` - High-value recommendations
- `results/association_support.png` - Item support chart
- `results/association_rules_metrics.png` - Confidence & lift distributions
- `results/association_confidence_lift.png` - Scatter plot

### Example Output

```
Antecedent              | Consequent         | Support | Confidence | Lift
-----------            | ----------         | ------- | ---------- | ----
Laptop                 | Mouse              | 2.1%    | 62%        | 2.8
iPhone Case            | iPhone             | 8.5%    | 45%        | 2.2
Running Shoes          | Sports Socks       | 5.2%    | 71%        | 3.1
Headphones             | Phone              | 12.3%   | 58%        | 2.1
Winter Coat            | Winter Boots       | 3.7%    | 68%        | 1.9
```

### Business Applications

- **Product Bundling** : Create recommended packages ("Frequently Bought Together")
- **Upselling** : Suggest complementary products at checkout
- **Inventory Management** : Stock related items near each other
- **Marketing** : Joint promotions and cross-sell campaigns
- **Recommendation Engine** : Power product suggestions

### Implementation Strategy

```
1. Identify top rules (Lift > 1.5, Confidence > 40%)
2. Create product bundles or recommendations
3. Place suggested items near primary products
4. Test A/B variations on website
5. Monitor lift in basket size and AOV (Average Order Value)
6. Refine thresholds based on campaign results
```

---

## 📂 Results Directory Structure

After running all scripts:
```
results/
├── RFM Analysis
│   ├── rfm_analysis_results.csv           Full customer data
│   ├── rfm_segment_summary.csv            Segment statistics
│   ├── rfm_distribution.png               Distribution plots
│   ├── rfm_segments.png                   Segment analysis
│   └── rfm_3d.png                         3D visualization
│
├── Churn Prediction
│   ├── churn_predictions.csv              Predictions for all customers
│   ├── churn_feature_importance.csv       Feature importance
│   ├── churn_feature_importance.png       Feature importance chart
│   ├── churn_roc_curve.png                ROC curve (model performance)
│   ├── churn_confusion_matrix.png         Confusion matrix
│   └── churn_distribution.png             Risk distribution
│
└── Association Rules
    ├── association_item_support.csv       Item popularity
    ├── association_rules.csv              All rules
    ├── cross_selling_opportunities.csv    Top recommendations
    ├── association_support.png            Support chart
    ├── association_rules_metrics.png      Metrics distributions
    └── association_confidence_lift.png    Confidence vs Lift
```

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

### Run All Analysis

```bash
# 1. RFM Analysis
python scripts/rfm_analysis.py

# 2. Churn Prediction
python scripts/churn_prediction.py

# 3. Association Rules
python scripts/association_rules.py
```

Each script runs independently and creates its own results directory.

---

## 🔧 Customization

### Adjust RFM Segments

Edit `rfm_analysis.py` function `assign_segment()` to modify scoring logic.

### Modify Churn Definition

```python
# Current: 180 days threshold
analyzer = ChurnPredictor(..., churn_threshold_days=180)

# Change to 90 days for stricter definition
analyzer = ChurnPredictor(..., churn_threshold_days=90)
```

### Tune Churn Model

```python
# In train_model() method, adjust:
RandomForestClassifier(
    n_estimators=150,      # More trees = more accurate but slower
    max_depth=20,          # Deeper trees = more complex patterns
    min_samples_split=5,   # Lower = more leafy, higher = simpler
)
```

### Filter Association Rules

```python
# In generate_rules() method, adjust thresholds:
analyzer.generate_rules(
    min_confidence=0.4,    # Higher = stricter rules
    min_lift=1.5           # Higher = stronger associations
)
```

---

## 📊 Interpretation Guide

### RFM Scores (1-4 Scale)

**R Score (Recency)**
- 4: Purchased in last 30 days
- 3: Purchased 30-60 days ago
- 2: Purchased 60-90 days ago
- 1: Purchased >90 days ago

**F Score (Frequency)**
- 1: Low frequency (few purchases)
- 2: Medium-low frequency
- 3: Medium-high frequency
- 4: High frequency (many purchases)

**M Score (Monetary)**
- 1: Low spending
- 2: Medium-low spending
- 3: Medium-high spending
- 4: High spending

### Combining Scores

```
RFM Score "444" = Champion (highest priority)
RFM Score "111" = Lost (lowest priority)
```

### Churn Risk Interpretation

```
0.75-1.0 (Critical)  : Immediate retention needed
0.50-0.75 (High)     : Urgent win-back campaign
0.25-0.50 (Medium)   : Monitor closely, nurture
0.00-0.25 (Low)      : Continue normal engagement
```

---

## 📈 KPIs to Monitor

### RFM KPIs
- % of Champions (target: 15-20%)
- % of Lost (target: <10%)
- Segment migration quarter-over-quarter

### Churn KPIs
- Churn Rate (% of high-risk customers who actually churn)
- Retention Rate from win-back campaigns
- Precision of model (% of predicted churners who actually churn)

### Association KPIs
- Average Order Value (AOV) increase from cross-selling
- Conversion rate on recommendations
- Revenue lift from bundled products

---

## 🎯 Next Steps

1. **Segment Customers** → Run RFM analysis
2. **Identify At-Risk** → Run Churn prediction
3. **Create Campaigns** → Target each segment differently
4. **Drive Cross-Sales** → Use Association rules
5. **Monitor Results** → Track KPIs weekly
6. **Refine Models** → Retrain quarterly with new data

---

**End of Data Mining Documentation**
