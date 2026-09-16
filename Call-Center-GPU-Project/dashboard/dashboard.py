import pandas as pd
import altair as alt
import streamlit as st

CSV_FILE = "Call-Center-GPU-Project/data/analysis_data.csv"

st.set_page_config(
    page_title="Call Center GPU Dashboard",
    layout="wide"
)

st.title("Call Center GPU Dashboard")
st.caption("GPU price and availability data collected from U.S. retailers")

# Load data
df = pd.read_csv(CSV_FILE)

# Basic metrics
total_gpu_records = len(df)
total_retailers = df["Retail_ID"].nunique()
average_price = df["Price"].mean()

# Top metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total GPU Records", total_gpu_records)
col2.metric("Retailers / Stores", total_retailers)
col3.metric("Average Price", f"${average_price:,.2f}")

st.divider()

# Availability
st.subheader("Availability")

availability_counts = df["Availability"].value_counts()

st.bar_chart(availability_counts)

st.divider()

# GPU model analysis
st.subheader("Most Reported GPU Models")

# Calculate number of reports and average price per GPU model
model_summary = (
    df.dropna(subset=["GPU model"])
    .groupby("GPU model", as_index=False)
    .agg(
        Reports=("GPU model", "size"),
        Average_Price=("Price", "mean")
    )
    .sort_values("Reports", ascending=False)
    .head(10)
)

# Create interactive chart
chart = (
    alt.Chart(model_summary)
    .mark_bar()
    .encode(
        x=alt.X(
            "Reports:Q",
            title="Number of Reports"
        ),
        y=alt.Y(
            "GPU model:N",
            sort="-x",
            title="GPU Model"
        ),
        tooltip=[
            alt.Tooltip(
                "GPU model:N",
                title="GPU Model"
            ),
            alt.Tooltip(
                "Reports:Q",
                title="Reports"
            ),
            alt.Tooltip(
                "Average_Price:Q",
                title="Average Price",
                format="$,.2f"
            )
        ]
    )
    .properties(
        height=400
    )
)

st.altair_chart(
    chart,
    use_container_width=True
)

st.divider()

# Data preview
st.subheader("Data Preview")

st.dataframe(
    df,
    use_container_width=True
)

