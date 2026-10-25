import pandas as pd
import streamlit as st

from config import DATABASE_PATH
from src.data_loader import find_dataset_file, load_dataset
from src.data_cleaning import clean_social_media_data
from src.database import initialize_database
from src.feature_engineering import add_engagement_features
from src.insights import generate_insights
from src.metrics import compute_kpis
from src.visualizations import (
    plot_content_performance,
    plot_daily_engagement,
    plot_hourly_engagement,
    plot_platform_performance,
    plot_top_posts,
)

st.set_page_config(page_title="Social Media Engagement Analysis", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(10, 16, 28, 0.72), rgba(10, 16, 28, 0.72)),
            url('https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp > div {
        background: transparent;
    }
    div[data-testid="stSidebar"] {
        background-color: rgba(14, 17, 23, 0.78);
        border-right: 1px solid rgba(255,255,255,0.12);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric, .stDataFrame, .stPlotlyChart, .stDataFrameContainer {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    }
    h1, h2, h3, p, li, label, .stSelectbox label, .stMultiselect label {
        color: #f5f7fb !important;
    }
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #4f46e5, #06b6d4);
        color: white;
        border: none;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_dataset():
    dataset_path = find_dataset_file()
    df = load_dataset(dataset_path)
    cleaned_df, quality_report = clean_social_media_data(df, source_name=dataset_path.name)
    cleaned_df = add_engagement_features(cleaned_df)
    initialize_database(cleaned_df, str(DATABASE_PATH))
    return cleaned_df, quality_report


cleaned_df, quality_report = get_dataset()

st.title("Social Media Engagement Analysis")
st.caption("Evidence-based investigation of post performance, posting times, and content trends")

if "sample" in quality_report.get("source_name", "").lower() or "synthetic" in quality_report.get("source_name", "").lower():
    st.info("Sample or synthetic data is currently being used for local demonstration. Replace the file in data/raw with a real Kaggle export to run the analysis on production data.")

platform_options = sorted(cleaned_df["platform"].dropna().unique().tolist())
content_options = sorted(cleaned_df["content_type"].dropna().fillna("Unspecified").unique().tolist())
campaign_options = sorted(cleaned_df["campaign"].fillna("Unspecified").unique().tolist())

with st.sidebar:
    st.header("Filters")
    selected_platforms = st.multiselect("Platform", platform_options, default=platform_options)
    selected_content = st.multiselect("Content type", content_options, default=content_options)
    selected_campaigns = st.multiselect("Campaign", campaign_options, default=campaign_options)
    start_date = st.date_input("Start date", min_value=cleaned_df["post_date"].min(), max_value=cleaned_df["post_date"].max())
    end_date = st.date_input("End date", min_value=cleaned_df["post_date"].min(), max_value=cleaned_df["post_date"].max(), value=cleaned_df["post_date"].max())

filtered_df = cleaned_df[
    cleaned_df["platform"].isin(selected_platforms)
    & cleaned_df["content_type"].isin(selected_content)
    & cleaned_df["campaign"].isin(selected_campaigns)
    & (cleaned_df["post_date"] >= pd.Timestamp(start_date))
    & (cleaned_df["post_date"] <= pd.Timestamp(end_date))
].copy()

if filtered_df.empty:
    st.warning("No posts match the current filters. Please adjust the filters to view the dashboard.")
    st.stop()

metrics = compute_kpis(filtered_df)
insights = generate_insights(filtered_df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total posts", f"{metrics['total_posts']:,}")
with col2:
    st.metric("Total engagements", f"{metrics['total_engagements']:,}")
with col3:
    st.metric("Avg engagements/post", f"{metrics['avg_engagements_per_post']:.2f}")
with col4:
    engagement_rate_display = "N/A" if metrics["engagement_rate"] is None else f"{metrics['engagement_rate']:.2f}%"
    st.metric("Engagement rate", engagement_rate_display)

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.metric("Likes", f"{metrics['total_likes']:,}")
with col6:
    st.metric("Comments", f"{metrics['total_comments']:,}")
with col7:
    st.metric("Shares", f"{metrics['total_shares']:,}")
with col8:
    avg_imp_display = "N/A" if metrics["avg_impressions_per_post"] is None else f"{metrics['avg_impressions_per_post']:.0f}"
    st.metric("Avg impressions/post", avg_imp_display)

st.subheader("Platform performance")
st.plotly_chart(plot_platform_performance(filtered_df), use_container_width=True)

st.subheader("Content performance")
st.plotly_chart(plot_content_performance(filtered_df), use_container_width=True)

st.subheader("Posting time analysis")
col9, col10 = st.columns(2)
with col9:
    st.plotly_chart(plot_daily_engagement(filtered_df), use_container_width=True)
with col10:
    st.plotly_chart(plot_hourly_engagement(filtered_df), use_container_width=True)

st.subheader("Top performing posts")
st.plotly_chart(plot_top_posts(filtered_df), use_container_width=True)

st.subheader("Observed insights")
for observation in insights["observations"]:
    st.write("- " + observation)

st.subheader("Recommended actions")
for action in insights["recommendations"]:
    st.write("- " + action)

st.subheader("Detailed post-level explorer")
post_table = filtered_df[["post_id", "platform", "content_type", "campaign", "post_date", "post_time", "likes", "comments", "shares", "total_engagements", "engagement_rate"]].copy()
post_table = post_table.sort_values("total_engagements", ascending=False)
st.dataframe(post_table, use_container_width=True)

csv_data = post_table.to_csv(index=False)
st.download_button("Download filtered CSV", csv_data, "filtered_social_media_posts.csv", "text/csv")

st.caption(f"Source file: {quality_report.get('source_name', 'Unknown')}")
