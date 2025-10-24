# CST383 Final Project — Predicting Satellite Mission Type from Orbital & Physical Features

**Team:** Jess Hammond, Gary Kuepper, Keshab Neupane  
**Course:** CST 383 — Data Science  
**Video (≤5 min):** *link*  

---

## Introduction 

This project explores whether a satellite’s **mission type** (e.g., *Communications*, *Navigation*, *Science*, *Technology Demonstration*, *Surveillance*) can be predicted using only its **orbital and physical parameters**.

### Motivation
1. **Rapid Cataloging:** Public and private organizations manage thousands of satellites. A predictive model could accelerate cataloging and assist in identifying unknown satellites.
2. **Scientific Insight:** Understanding relationships between orbit design and mission type reveals trends in satellite engineering (e.g., *Geostationary* orbits for communications vs. *Sun-synchronous* for science missions).

### Research Question
Can we accurately predict a satellite’s **mission category** using publicly available **orbital and physical features** from the UCS Satellite Database?

---

## Selection of Data 

**Source:**  
- [Union of Concerned Scientists (UCS) Satellite Database](https://www.ucsusa.org/resources/satellite-database) Accessed: 2025-10-10  
- [Celestrak SatCat](https://celestrak.org/pub/satcat.csv)   Accessed: 2025-10-20

**Data Characteristics:**
- ~7,560 merged entries (UCS + SatCat)
- Key features:  
  `OrbitClass`, `OrbitType`, `Apogee`, `Perigee`, `Eccentricity`, `Inclination`, `Period`, `LaunchMass`, `LaunchYear`
- **Target:** `Purpose` (grouped into 6 super-classes)  
  | Category | Count |
  |-----------|------:|
  | Communications | 5503 |
  | Science | 1093 |
  | Tech Demo | 453 |
  | Navigation | 345 |
  | Surveillance | 156 |
  | Other | 10 |

### Data Cleaning & Feature Engineering
- Dropped redundant *Unnamed* columns; merged fragmented *Source* fields.  
- Normalized categorical labels (e.g., merged “Gov”, “Govt” → “Government”).  
- Parsed and extracted `LaunchYear` from `LaunchDate`.  
- Imputed missing numeric values with medians.  
- Encoded categoricals with one-hot encoding.  
- Created engineered features:
  - `LaunchYear` (numerical)
  - Period/Inclination “buckets” for visualization
  - `PurposeSuperAudit`: manually curated high-level categories (Communications, Science, etc.)

---

## Methods 

**Libraries:** `pandas`, `NumPy`, `scikit-learn`, `matplotlib`, `seaborn`

**Preprocessing Pipeline**
1. **Numerical Features:** imputed with median → standardized (`StandardScaler`)  
2. **Categorical Features:** one-hot encoded (`OneHotEncoder(handle_unknown='ignore')`)  
3. **Split:** stratified 80 / 20 train–test split (preserving class balance)

**Model Choice**
- **Logistic Regression (multinomial, solver='lbfgs', max_iter=600)**  
  - Serves as an **interpretable baseline** to evaluate how orbital and physical variables drive classification.
  - Chosen for simplicity and transparency before exploring non-linear models (RandomForest, CatBoost).

---

## Results 

| Metric | Value |
|--------|-------:|
| Accuracy | **0.944** |
| Weighted F1 | **0.94** |
| Macro F1 | **0.71** |

### Per-Class Performance
| Class | Precision | Recall | F1 |
|-------|-----------:|-------:|--:|
| Communications | 0.99 | 0.99 | 0.99 |
| Navigation | 0.98 | 0.88 | 0.93 |
| Science | 0.81 | 0.88 | 0.85 |
| Tech Demo | 0.73 | 0.64 | 0.68 |
| Surveillance | 0.89 | 0.77 | 0.83 |

### Interpretation
- Model achieves **excellent performance** for dominant categories (*Communications*, *Navigation*).  
- Misclassifications mostly between *Science* and *Tech Demo*, reflecting overlapping orbital patterns.  
- “Other” category too small for meaningful learning.

### Visualization Highlights
- **Confusion Matrix:** Strong diagonal dominance; limited confusion between science-related classes.  
- **Pairplots & Countplots:** Clear separability in `OrbitClass`, `Inclination`, and `Apogee`.

---

## Discussion 

### Implications
- Orbital and physical parameters are powerful proxies for mission classification.  
- Clear pattern: *Communications* satellites occupy **GEO**, while *Science* and *Tech Demo* prefer **LEO / Sun-synchronous**.  

### Limitations
- Missing payload descriptors (sensor type, transponder details).  
- Severe **class imbalance**—Communications dominates dataset.  
- Dataset is static, omitting temporal behavior (orbital decay, end-of-life status).

### Future Work
1. Integrate **payload and bus data** from open orbital catalogs.   
2. Experiment with **tree ensembles** or **gradient boosting** for non-linear interactions.
3. Explore **hierarchical classification** (broad mission → sub-type).
4. Add time-series analysis (launch trends by year, orbit drift).

---

## Summary 

- Built a supervised ML model predicting satellite mission from orbital/physical data.  
- Achieved **94% accuracy** using multinomial Logistic Regression.  
- Demonstrated that simple linear models already capture strong mission–orbit relationships.  
- Future work: rebalance classes, add richer features, and explore non-linear models for higher-granularity prediction.

---

##  Reproducibility

```bash
pip install -r requirements.txt
jupyter notebook satellite_project.ipynb
# or:
python satellite_project.py
