# QUICK REFERENCE SHEET

## 🚀 START HERE (5 Minutes)

### 1️⃣ Generate Data
```bash
python scripts/generate_data.py
```
✅ Creates 7 CSV files in `data/raw/`

### 2️⃣ Create Database
```bash
mysql -u root -p < setup_database.sql
```
✅ Creates `ecommerce_bi` database

### 3️⃣ Run Analysis (Choose Any)
```bash
python scripts/rfm_analysis.py              # Customer segments
python scripts/churn_prediction.py          # At-risk customers
python scripts/association_rules.py         # Cross-selling
```
✅ Generates results in `results/` folder

---

## 📊 PROJECT STRUCTURE

```
BI2/
├── README.md                          ← Start here!
├── PROJECT_INDEX.md                   ← Complete guide
├── PROJECT_COMPLETION_SUMMARY.md      ← Status & deliverables
│
├── docs/
│   ├── BI_Project.md                  Original requirements
│   ├── ETL_DOCUMENTATION.md           ETL details (Pentaho)
│   ├── MDX_QUERIES.md                 17 OLAP queries
│   ├── DATA_MINING_GUIDE.md           Analysis scripts guide
│   └── implementation/
│       ├── PROJECT_IMPLEMENTATION_PLAN.md   Master roadmap
│       └── DATA_MODEL.md              Schema design
│
├── scripts/
│   ├── generate_data.py               Generate 50,000 orders
│   ├── rfm_analysis.py                Customer segments
│   ├── churn_prediction.py            Risk prediction
│   └── association_rules.py           Cross-selling
│
├── setup_database.sql                 Database creation
└── data/, etl/, olap/, results/       (Auto-generated)
```

---

## 🎯 KEY NUMBERS

| Metric | Value |
|--------|-------|
| Customers | 10,000 |
| Products | 500 |
| Orders | 50,000 |
| Regions | 13 |
| Period | 2022-2024 |
| Return Rate | 8.5% |
| Satisfaction | 3.2/5 |
| Channels | 4 (Web, Mobile, Pop-Up, Social) |

---

## 📚 DOCUMENTATION GUIDE

**Read FIRST**: `README.md` (10 min)
**For Planning**: `PROJECT_IMPLEMENTATION_PLAN.md` (15 min)
**For Schema**: `DATA_MODEL.md` (15 min)
**For ETL**: `ETL_DOCUMENTATION.md` (20 min)
**For Analysis**: `OLAP: MDX_QUERIES.md` + `Data Mining: DATA_MINING_GUIDE.md` (30 min)

---

## 🔧 COMMAND QUICK REFERENCE

### Data Generation
```bash
# Generate synthetic dataset (CSV files)
python scripts/generate_data.py              # ~2 min
```

### Database
```bash
# Create dimensional warehouse
mysql -u root -p < setup_database.sql        # ~10 sec
```

### RFM Analysis
```bash
# Segment customers by value (8 segments)
python scripts/rfm_analysis.py               # ~30 sec
# Output: rfm_analysis_results.csv, visualizations
```

### Churn Prediction
```bash
# Predict at-risk customers (Random Forest)
python scripts/churn_prediction.py           # ~1 min
# Output: churn_predictions.csv, ROC curve, feature importance
```

### Association Rules
```bash
# Cross-selling opportunities (Apriori algorithm)
python scripts/association_rules.py          # ~2 min
# Output: association_rules.csv, recommendations
```

---

## 📊 RFM SEGMENTS

| Segment | % | Action |
|---------|---|--------|
| **Champions** | 15% | Reward & upsell |
| **Loyal** | 25% | Maintain relationship |
| **Potential** | 20% | Nurture & convert |
| **At Risk** | 15% | Win back |
| **Lost** | 15% | Remove |
| **Dormant** | 10% | Reactivate |

---

## ⚠️ CHURN PREDICTION

**Definition**: No purchase in 180 days

| Risk Level | Probability | Action |
|-----------|-------------|--------|
| 🟢 Low | 0-25% | Normal engagement |
| 🟡 Medium | 25-50% | Monitor closely |
| 🟠 High | 50-75% | Win-back campaign |
| 🔴 Critical | 75-100% | Urgent retention |

---

## 🛒 ASSOCIATION METRICS

| Metric | Meaning |
|--------|---------|
| **Support** | % of transactions with both items |
| **Confidence** | % of item A buyers who also buy B |
| **Lift** | How much more likely than random |

**Good Rules**: Confidence > 40%, Lift > 1.5

---

## 📋 FILES CREATED

### Documentation (6)
- ✅ README.md (5K words)
- ✅ PROJECT_IMPLEMENTATION_PLAN.md (6.5K words)
- ✅ DATA_MODEL.md (5K words)
- ✅ ETL_DOCUMENTATION.md (6K words)
- ✅ MDX_QUERIES.md (5.5K words)
- ✅ DATA_MINING_GUIDE.md (4.5K words)

### Scripts (5)
- ✅ generate_data.py (500+ lines)
- ✅ setup_database.sql (200+ lines)
- ✅ rfm_analysis.py (400+ lines)
- ✅ churn_prediction.py (600+ lines)
- ✅ association_rules.py (500+ lines)

### Support (3)
- ✅ PROJECT_INDEX.md (Quick reference)
- ✅ PROJECT_COMPLETION_SUMMARY.md (Status report)
- ✅ QUICK_REFERENCE.md (This file!)

---

## 🏆 PROJECT STATUS

| Phase | Status |
|-------|--------|
| Planning & Analysis | ✅ 100% |
| Design & Modeling | ✅ 100% |
| Documentation | ✅ 100% |
| Scripts Development | ✅ 100% |
| **Overall readiness** | **✅ 100%** |

**→ Ready to execute data generation!**

---

## 💡 TIPS FOR SUCCESS

1. **Start with README.md** (5 min read)
2. **Run generate_data.py** first (creates test data)
3. **Review DATA_MODEL.md** before touching database
4. **Document your changes** in version control
5. **Test on small data** before full load
6. **Monitor Pentaho logs** during ETL runs
7. **Validate data quality** at each step
8. **Archive results** weekly

---

## 🆘 COMMON ISSUES

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: faker` | `pip install faker pandas numpy` |
| `Connection refused` (MySQL) | Start MySQL service, check port 3306 |
| `CSV file not found` | Run `generate_data.py` first |
| `Out of memory` | Reduce `NUM_ORDERS` in script |
| `Slow performance` | Add database indexes, increase buffer pool |

---

## 📈 EXPECTED OUTPUTS

### From `generate_data.py`:
```
✓ customers.csv (10,000 rows)
✓ products.csv (500 rows)
✓ channels.csv (4 rows)
✓ regions.csv (13 rows)
✓ orders.csv (50,000 rows)
✓ returns.csv (~3,500 rows)
✓ feedback.csv (~35,000 rows)
```

### From `rfm_analysis.py`:
```
✓ rfm_analysis_results.csv (customers with segments)
✓ rfm_segment_summary.csv (segment statistics)
✓ 3 visualization PNG files
```

### From `churn_prediction.py`:
```
✓ churn_predictions.csv (all customers + risk)
✓ churn_feature_importance.csv (feature rankings)
✓ 4 visualization PNG files
```

### From `association_rules.py`:
```
✓ association_rules.csv (all rules discovered)
✓ cross_selling_opportunities.csv (top recommendations)
✓ 3 visualization PNG files
```

---

## 🔐 DATA SPECIFICATIONS

### Customers
- **ID Format**: CUST000001 to CUST010000
- **Segments**: Nouveau(25%), Régulier(50%), Fidèle(25%)
- **Period**: 2022-01-01 to 2024-02-15

### Products
- **ID Format**: PROD000001 to PROD000500
- **Price Range**: €10 to €5,000 (Lognormal)
- **Categories**: 20 categories (Electronics, Fashion, etc.)

### Orders
- **ID Format**: ORD00000001 to ORD00050000
- **Channels**: Web(50%), Mobile(35%), Pop-Up(10%), Social(5%)
- **Basket**: €30 to €250 (varies by channel)
- **Discount**: 10% chance of 10% off

### Returns
- **Rate**: 6-15% depending on channel
- **Reason**: Product defect, Size, Quality, etc.

### Feedback
- **Satisfaction**: 1-5 scale
- **Rate**: 70% of orders
- **Inverse correlation**: Higher delivery time → Lower satisfaction

---

## 🎓 LEARNING PATH

### For Business Users
1. README.md
2. PROJECT_IMPLEMENTATION_PLAN.md
3. MDX_QUERIES.md (understand what's possible)

### For Data Engineers
1. DATA_MODEL.md
2. ETL_DOCUMENTATION.md
3. setup_database.sql

### For Analysts
1. MDX_QUERIES.md
2. DATA_MINING_GUIDE.md
3. Run the Python scripts

### For DBAs
1. DATA_MODEL.md
2. setup_database.sql
3. ETL_DOCUMENTATION.md (performance tuning)

---

## 🔗 QUICK LINKS TO IMPORTANT SECTIONS

- **How to Start?** → README.md → Démarrage Rapide
- **What's the Plan?** → PROJECT_IMPLEMENTATION_PLAN.md
- **What's the Schema?** → DATA_MODEL.md → 2. PHASE 1
- **How to Build ETL?** → ETL_DOCUMENTATION.md
- **What Queries to Write?** → MDX_QUERIES.md
- **How to Analyze?** → DATA_MINING_GUIDE.md
- **Full Index?** → PROJECT_INDEX.md

---

## ⏱️ TIME ESTIMATES

| Task | Time | Command |
|------|------|---------|
| Read README | 10 min | - |
| Generate data | 2 min | `python scripts/generate_data.py` |
| Setup database | <1 min | `mysql -u root -p < setup_database.sql` |
| RFM analysis | 1 min | `python scripts/rfm_analysis.py` |
| Churn prediction | 1 min | `python scripts/churn_prediction.py` |
| Association rules | 2 min | `python scripts/association_rules.py` |
| **Total** | **~20 min** | - |

---

## 📞 SUPPORT RESOURCES

| Topic | Document |
|-------|----------|
| Getting Started | README.md |
| Project Overview | PROJECT_INDEX.md |
| Status & Deliverables | PROJECT_COMPLETION_SUMMARY.md |
| Data Details | DATA_MODEL.md |
| ETL Steps | ETL_DOCUMENTATION.md |
| Analytics Queries | MDX_QUERIES.md |
| Analysis Guide | DATA_MINING_GUIDE.md |

---

## ✅ PRE-FLIGHT CHECKLIST

- [ ] ProjectPy installed (3.8+)
- [ ] MySQL/PostgreSQL running
- [ ] faker, pandas, numpy installed
- [ ] All .py scripts downloaded
- [ ] setup_database.sql available
- [ ] README.md reviewed
- [ ] Ready to generate data

**Once checked**: Run `python scripts/generate_data.py`

---

**Last Updated**: February 15, 2026  
**Status**: ✅ Project ready for execution

Quick reference version - Full details in `/docs/` folder
