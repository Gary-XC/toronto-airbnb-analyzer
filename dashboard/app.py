import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Toronto Airbnb Investment Analyzer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- DATA LOADING (CACHED FOR PERFORMANCE) ---
@st.cache_data
def load_data():
    # Resolve the absolute path to the project root, regardless of where the script is called from
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / "data" / "processed" / "listings_clean.csv"

    # Safety check for cloud deployment
    if not data_path.exists():
        st.error(
            f"Data file not found at {data_path}. Please ensure the processed data is committed to the repository."
        )
        st.stop()

    df = pd.read_csv(data_path)

    # Ensure numeric types just in case
    df["price"] = pd.to_numeric(df["price"])
    df["estimated_annual_revenue"] = pd.to_numeric(df["estimated_annual_revenue"])
    return df


df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Market Parameters")

# 1. Borough Filter
boroughs = st.sidebar.multiselect(
    "Select Boroughs:",
    options=df["neighbourhood_group"].unique(),
    default=df["neighbourhood_group"].unique(),
)

# 2. Room Type Filter
room_types = st.sidebar.multiselect(
    "Select Property Types:",
    options=df["room_type"].unique(),
    default=df["room_type"].unique(),
)

# 3. Price Range Slider
min_price = int(df["price"].min())
max_price = int(df["price"].max())
price_range = st.sidebar.slider(
    "Nightly Price Range ($):",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, 1000),  # Default to a realistic investor range
)

# --- APPLY FILTERS ---
filtered_df = df[
    (df["neighbourhood_group"].isin(boroughs))
    & (df["room_type"].isin(room_types))
    & (df["price"].between(price_range[0], price_range[1]))
]

# --- F-PATTERN LAYOUT ---

# HEADER
st.title("Toronto Airbnb Investment Analyzer")
st.markdown(
    "*Identify high-yield neighborhoods and optimize property acquisition strategies.*"
)
st.divider()

# ROW 1: BIG-ASS NUMBERS (BANs) - The Immediate Pulse
col1, col2, col3, col4 = st.columns(4)

total_listings = len(filtered_df)
median_price = filtered_df["price"].median()
total_est_revenue = filtered_df["estimated_annual_revenue"].sum()
avg_min_nights = filtered_df["minimum_nights"].mean()

col1.metric("Total Active Listings", f"{total_listings:,}")
col2.metric("Median Nightly Rate (ADR)", f"${median_price:,.0f}")
col3.metric("Est. Total Annual Revenue", f"${total_est_revenue:,.0f}")
col4.metric("Avg. Minimum Night Stay", f"{avg_min_nights:.1f} Nights")

st.divider()

# ROW 2: STRATEGIC VISUALIZATIONS - The Yield Matrix
st.subheader("The Neighborhood Yield Matrix")
st.markdown(
    "*Bubble size represents total listing volume. Target the top-right quadrant for maximum market dominance.*"
)

# Aggregate for the scatter plot
neighborhood_metrics = (
    filtered_df.groupby(["neighbourhood", "neighbourhood_group"])
    .agg(
        median_price=("price", "median"),
        total_est_revenue=("estimated_annual_revenue", "sum"),
        listing_count=("id", "count"),
    )
    .reset_index()
)

# Filter out tiny neighborhoods for the chart to reduce noise
neighborhood_metrics = neighborhood_metrics[neighborhood_metrics["listing_count"] >= 5]

fig_scatter = px.scatter(
    neighborhood_metrics,
    x="median_price",
    y="total_est_revenue",
    size="listing_count",
    color="neighbourhood_group",
    hover_name="neighbourhood",
    labels={
        "median_price": "Median Nightly Price ($)",
        "total_est_revenue": "Total Est. Annual Revenue ($)",
        "listing_count": "Listing Volume",
    },
    template="plotly_white",
    height=500,
)
fig_scatter.update_layout(showlegend=False)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ROW 3: GRANULAR DATA TABLE - Deal Hunting
st.subheader("Granular Property Explorer")
st.markdown(
    "*Sort by Estimated Annual Revenue to find the highest yielding individual properties in your filtered criteria.*"
)

# Select specific columns for the table to keep it clean
table_cols = [
    "neighbourhood",
    "room_type",
    "price",
    "minimum_nights",
    "estimated_annual_revenue",
]
st.dataframe(
    filtered_df[table_cols].sort_values(by="estimated_annual_revenue", ascending=False),
    use_container_width=True,
    height=400,
    column_config={
        "price": st.column_config.NumberColumn("Nightly Price ($)", format="$%d"),
        "estimated_annual_revenue": st.column_config.NumberColumn(
            "Est. Annual Rev ($)", format="$%d"
        ),
        "minimum_nights": st.column_config.NumberColumn("Min Nights", format="%d"),
    },
)
