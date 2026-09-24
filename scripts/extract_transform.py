import pandas as pd
import numpy as np
from pathlib import Path


def clean_toronto_airbnb_data(raw_path: str, processed_path: str) -> pd.DataFrame:
    """
    Cleans and transforms raw Toronto Airbnb listings data.

    Business Logic Justifications:
    1. Price Cleaning: InsideAirbnb stores price as strings (e.g., "$150.00").
       We must convert to float for revenue calculations.
    2. Missing Reviews: New listings have NaN for 'reviews_per_month'. We fill with 0.
       A new listing has 0 historical momentum, which is a risk factor for investors.
    3. Outlier Removal: We filter out properties with price < $10 or > $1,500.
       Sub-$10 is likely a data error or a shared room anomaly; >$1,500 skews the
       median ADR and represents ultra-luxury, which is outside our target investor profile.
    4. Revenue Proxy: Since exact bookings are hidden, we use the industry-standard
       heuristic: (reviews_per_month * 12) / 0.30 = estimated annual bookings
       (assuming a 30% review leave rate). Multiplied by price, this gives a
       relative 'Estimated Annual Revenue' for comparing neighborhoods.
    """

    # 1. Load Data
    print(f"Loading data from {raw_path}...")
    df = pd.read_csv(raw_path)
    initial_shape = df.shape

    # 2. Clean Price Column
    df["price"] = (
        df["price"].astype(str).str.replace(r"[$,]", "", regex=True).astype(float)
    )

    # 3. Handle Missing Values
    # Fill NaN reviews_per_month with 0 (new listings with no review history yet)
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0.0)

    # Fill missing neighbourhood_group with 'Unknown' to preserve row count but flag for analysis
    df["neighbourhood_group"] = df["neighbourhood_group"].fillna("Unknown")

    # 4. Filter Outliers (Business Rules)
    # Remove impossible minimum nights or extreme prices
    df = df[(df["minimum_nights"] >= 1) & (df["minimum_nights"] <= 365)]
    df = df[(df["price"] >= 10) & (df["price"] <= 1500)]

    # 5. Feature Engineering: Estimated Annual Revenue Proxy
    # Assuming 30% of guests leave a review
    REVIEW_LEAVE_RATE = 0.30
    df["estimated_annual_bookings"] = (df["reviews_per_month"] * 12) / REVIEW_LEAVE_RATE
    df["estimated_annual_revenue"] = df["price"] * df["estimated_annual_bookings"]

    # 6. Select Final Columns for Analysis (Reduce memory footprint)
    final_columns = [
        "id",
        "name",
        "neighbourhood_group",
        "neighbourhood",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
        "estimated_annual_revenue",
    ]
    df_clean = df[final_columns].copy()

    # 7. Save Processed Data
    Path(processed_path).parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(processed_path, index=False)
    print(f"Cleaning complete. Saved to {processed_path}")
    print(
        f"Rows dropped: {initial_shape[0] - df_clean.shape[0]} ({((initial_shape[0] - df_clean.shape[0])/initial_shape[0])*100:.1f}%)"
    )

    return df_clean


if __name__ == "__main__":
    # Define paths relative to the script location
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_FILE = BASE_DIR / "data" / "raw" / "listings.csv"
    PROCESSED_FILE = BASE_DIR / "data" / "processed" / "listings_clean.csv"

    clean_toronto_airbnb_data(str(RAW_FILE), str(PROCESSED_FILE))
