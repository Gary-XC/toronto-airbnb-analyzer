# Toronto Airbnb Investment Analyzer

![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)

### [Launch Interactive Live Dashboard](https://toronto-airbnb-analyzer.streamlit.app/)

---

## 1. Executive Summary
With Toronto's high real estate costs and saturated short-term rental market, independent investors struggle to identify which neighborhoods and property types yield the highest return on investment. By analyzing a recent snapshot of Toronto's Airbnb market, this project reveals that mid-tier, high-density neighborhoods (like the Bay Street Corridor) outperform prime downtown luxury districts in total estimated annual revenue due to higher sustained occupancy. This interactive dashboard allows stakeholders to filter market parameters, identify high-yield "cash cow" zones, and drill down into granular property data to inform acquisition strategies.

## 2. Business Impact & Recommendations
Based on the data analysis, the following strategic actions are recommended for property investors:
* **Target the "Cash Cows" over the "Unicorns":** Do not over-index on the highest nightly rates in prime downtown cores (e.g., Waterfront). Neighborhoods like *Kensington-Markham* and *Bay Street Corridor* offer a lower median ADR but drive significantly higher total estimated annual revenue due to volume.
* **Capitalize on the "Entire Home" Premium:** The price premium for Entire Homes vs. Private Rooms is statistically significant (p < 0.001). Investors should prioritize acquiring entire condos over renting out spare rooms to maximize top-line revenue, provided the acquisition cost justifies the yield.
* **Budget Using the Median, Not the Mean:** The city-wide mean price is heavily skewed by luxury outliers. Investors should underwrite deals using the median nightly rate (~$140-$160) to avoid severe budget overruns.

## 3. Interactive Live Demo
*Click the image below to launch the live Streamlit dashboard.*

[![Toronto Airbnb Dashboard](https://img.shields.io/badge/Live_Demo-Click_Here-brightgreen?style=for-the-badge&logo=streamlit)](https://toronto-airbnb-analyzer.streamlit.app/)

## 4. Methodology & Tool Justifications
* **Why Median over Mean for Pricing?** Toronto's Airbnb market is heavily right-skewed by multi-million dollar luxury penthouses. Using the mean would artificially inflate the expected ADR. The median and Interquartile Range (IQR) provide a statistically robust baseline for the "typical" property.
* **Why Mann-Whitney U over a T-Test?** To prove the "Entire Home" price premium, we avoided the standard independent T-test because our price data violates the assumption of normal distribution. Utilized the non-parametric Mann-Whitney U test to rigorously compare the medians of the two groups without assuming normality.
* **Why Streamlit over Tableau/PowerBI?** While BI tools are great, Streamlit allows the entire application to be written in Python, version-controlled in Git, and deployed via CI/CD. It demonstrates full-stack software engineering capabilities alongside data analysis.
* **Why Pytest & GitHub Actions?** Data pipelines break silently. Implemented automated data quality assertions (e.g., ensuring no negative prices, unique IDs) triggered on every Pull Request to guarantee the dashboard never serves corrupted data.

## 5. Data Limitations & Caveats
Intellectual honesty is critical in data science. Stakeholders should be aware of the following limitations:
* **The Revenue Proxy Heuristic:** InsideAirbnb does not expose exact booking data. Annual revenue were estimated using an industry-standard heuristic: `(reviews_per_month * 12) / 0.30`. This assumes a 30% review-leave rate. Actual revenue may vary based on seasonal cancellation rates.
* **Regulatory & Bylaw Risks (Crucial Context):** The City of Toronto enforces strict Short-Term Rental bylaws, requiring hosts to register and limiting short-term rentals to a **principal residence**. This dataset includes all active listings and *does not* filter out potentially illegal, unregistered secondary suites. Investors must factor legal compliance and registration fees into their ROI models.
* **Point-in-Time Snapshot:** This data represents a single snapshot in time. It does not capture intra-year seasonality (e.g., peak summer tourism vs. winter dips). A longitudinal analysis using the `calendar.csv` file is recommended for underwriting.

---
*Project built by Gary Chen | [LinkedIn Profile](https://www.linkedin.com/in/garychenx/) *