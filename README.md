# Population Health Outcomes Intervention Optimization Python Case Study
This project analyzes global population-level health outcomes using life expectancy and economic indicators. Using Python, it performs descriptive, diagnostic, and prescriptive analytics to quantify drivers of health outcomes, identify underperforming populations, segment countries into risk tiers, and simulate intervention scenarios.

The analysis examines how economic resources and temporal trends relate to health outcomes, identifies countries underperforming relative to expectations, segments populations into interpretable risk groups, and simulates how targeted interventions could improve predicted outcomes.

This mirrors real workflows in healthcare analytics, population health management, Medicaid intervention planning, and public-health decision support.

## 📂 Repository Structure

- `data/`
  - `all_data.csv` - Raw population-level dataset containing life expectancy, GDP, country, and year variables
- `python/`
   - `notebooks/`
      - `Population_Health_Outcomes_Analysis.ipynb` - Narrative notebook explaining analytical decisions, visual exploration, and interpretation of results
   - `python code/`
      - `life_exp_gdp_analysis.py` - Python pipeline for feature engineering, modeling, clustering, and exporting dashboard-ready outputs
- `reports/figures/` - Generated from python (Matplotlib & Seaborn)
   - `figures/`
      - `global_life_expectancy_trend.png` - Global average life expectancy trend over time
      - `life_exp_vs_gdp.png` - Relationship between economic capacity (log GDP) and life expectancy
      - `life_expectancy_distribution.png` - Global distribution of life expectancy across countries
      - `outcome_gap_residuals.png` - Residuals showing under/overperformers vs expected outcomes
      - `population_segments_clusters.png` - K-Means clusters used to segment countries into risk tiers
- `README.md/`
## 🎯 Objectives

Describe global variation in life expectancy across countries and time.

Quantify how economic capacity and time trends relate to health outcomes.

Identify underperforming countries using regression outcome gaps (residuals).

Segment populations into interpretable risk tiers using clustering.

Simulate “what-if” scenarios to support intervention planning.


## ❓ Key Questions Answered
Understanding Population Health

* How do life expectancy levels vary globally?

* What is the overall gap between the highest- and lowest-performing populations?

* Which countries show meaningful declines or improvements over time?

Drivers of Health Outcomes

* How strongly is economic capacity (GDP) associated with life expectancy?

* Does log-transforming GDP reveal a more linear relationship?

* How much of life expectancy can be explained using a simple regression model?

Underperforming Populations

* Which countries have significantly lower life expectancy than expected given their economic scale?

* What do regression residuals reveal about outcome gaps?

* Can we identify populations requiring prioritized intervention?

Segmentation & Stratification

* How can clustering group countries into interpretable risk categories?

* What distinguishes “High-Risk,” “Elevated-Risk,” “Moderate-Risk,” and “Low-Risk” population segments?

 Intervention Planning

* If a country increases its economic resources by 10%, how would predicted life expectancy change?

* Which population clusters benefit most from targeted investment?

* How can scenario modeling inform policy or public-health planning?

## 📈 Results
Population Overview (KPIs)

* Life expectancy varies widely across countries, with a ~28-year gap between the highest- and lowest-performing populations.

* Significant inequality persists, even among economically similar groups.

Economic Drivers of Outcomes

* Log-transformed GDP shows a strong, positive, and more linear relationship with life expectancy.

* A simple regression model captures broad trends effectively (R² ≈ 0.8), indicating economic capacity and time trends explain a large share of health-outcome variance.

Underperformers & Outcome Gaps

* Several countries fall well below predicted life expectancy, even after accounting for economic resources.

* These underperformers represent priority candidates for targeted public-health interventions.

Population Segmentation

* K-Means clustering groups populations into four coherent segments:
  
  * **High Risk** – low life expectancy and limited resources  
  * **Elevated Risk** – improving outcomes but still below global averages  
  * **Moderate Risk** – stable mid-range performance  
  * **Low Risk** – highest life expectancy and strongest economic capacity  

* These clusters make intervention prioritization more actionable.
Scenario Simulations

* A 10% increase in economic resources yields measurable improvements in predicted life expectancy, varying by cluster.

* High-risk and underperforming clusters show the largest modeled gains, indicating where investment may maximize population-level impact.

## 🛠️ Tools Used
Python via VSCode (pandas, NumPy, seaborn, matplotlib, scikit-learn (LinearRegression, KMeans, StandardScaler), pathlib, modular scripting structure)

GitHub (Version control, Clean project structure, Documented analytics pipeline)

## 💡 Why This Project Matters

Understanding what drives differences in life expectancy is essential for organizations involved in:

* Population health analytics

* Medicaid and care-management programs

* Public-health planning

* Health-equity initiatives

* Insurance & risk modeling

* Global health policy

This project demonstrates your ability to:

* Transform raw data into meaningful healthcare insights

* Use regression to identify outcome drivers

* Apply segmentation to stratify populations

* Perform prescriptive scenario modeling

* Build dashboards that support strategic decision-making

For employers, this project shows data storytelling, Python analytics, and Tableau visualization skills—directly applicable to healthcare analytics roles.
