# CST383-30_2254_PROJECT

# Predicting Satellite Mission Type from Orbital & Physical Features
**Team:** Jess Hammond, Gary Kuepper, Keshab Neupane  
**Course:** CST 383 — Final Project  
**Video (≤5 min):** <link>

## Introduction
We predict a satellite’s **Mission/Purpose** (e.g., Communications, Navigation, Science) from orbital and physical attributes. This matters for quick cataloging/triage and to understand how design/orbit correlate with mission needs.

## Selection of Data
- **Source:** Union of Concerned Scientists (UCS) Satellite Database — https://www.ucsusa.org/resources/satellite-database  
- **Downloaded:** 10/23/2025 
- **Files used in this repo:** `UCS-Satellite-Database-Officialname_5-1-2023.xlsx`, `merged_clean_data.csv` (cleaned), `merged_data.csv` (raw merge).  
- **Cleaning & Features:** standardized column names, consolidated purpose labels to super-classes, dropped `Unknown/None` for supervised training, imputed numerics, scaled numerics, one-hot for `OrbitClass/OrbitType`. Engineered: period/inclination buckets, launch year.

## Methods
- **Split:** stratified train/test with fixed `random_state`.  
- **Pipeline:** numeric imputation → scaling; categorical one-hot; **Logistic Regression (multinomial)** baseline with class weights.  
- **Why LR first:** interpretable baseline, handles imbalance; non-linear models considered for future work.

## Results
- **Test accuracy:** **~0.768** on held-out set.  
- High recall for **Communications** and **Navigation**; weaker recall on minority **Science/Technology** classes due to class imbalance and overlapping features.

### Key Figures
![Confusion Matrix](figures/confusion_matrix.png)  
*(optional)* ![Class Counts](figures/class_counts.png)

## Discussion
- **Implications:** Orbital/physical attributes capture strong signals for comms/navigation missions (e.g., GEO, power/mass).  
- **Limitations:** Missing payload descriptors (sensor band/transponder/bus), constellation membership, and program metadata.  
- **Improvements:** Class weighting/SMOTE, richer domain features, tree ensembles/CatBoost, and a hierarchical classifier (coarse group → subtype).

## Summary
- Achieved ~**0.768** accuracy; strong for **Communications/Navigation**, weaker for minority **Science/Tech** categories.  
- Features provide useful coarse separation; nuanced research missions need richer features.  
- Next: rebalance data, add payload/domain features, try non-linear models, consider hierarchical labels.

## Repro
```bash
pip install -r requirements.txt
# open and Run All the notebook
satellite_project.ipynb
