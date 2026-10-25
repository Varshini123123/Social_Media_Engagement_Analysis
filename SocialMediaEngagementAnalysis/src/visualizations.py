import pandas as pd
import plotly.express as px


def plot_platform_performance(df):
    grouped = df.groupby("platform", dropna=False)["total_engagements"].mean().reset_index(name="avg_engagements")
    return px.bar(grouped, x="platform", y="avg_engagements", title="Average engagement by platform")


def plot_content_performance(df):
    grouped = df.groupby("content_type", dropna=False)["total_engagements"].mean().reset_index(name="avg_engagements")
    return px.bar(grouped, x="content_type", y="avg_engagements", title="Average engagement by content type")


def plot_daily_engagement(df):
    if "post_day_of_week" not in df.columns:
        return px.bar(title="Daily engagement not available")
    grouped = df.groupby("post_day_of_week")["total_engagements"].mean().reset_index(name="avg_engagements")
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grouped["post_day_of_week"] = pd.Categorical(grouped["post_day_of_week"], categories=ordered_days, ordered=True)
    grouped = grouped.sort_values("post_day_of_week")
    return px.line(grouped, x="post_day_of_week", y="avg_engagements", title="Average engagement by day of week")


def plot_hourly_engagement(df):
    if "post_hour" not in df.columns:
        return px.bar(title="Hourly engagement not available")
    grouped = df.groupby("post_hour")["total_engagements"].mean().reset_index(name="avg_engagements")
    return px.line(grouped, x="post_hour", y="avg_engagements", title="Average engagement by hour")


def plot_top_posts(df):
    top_df = df.sort_values("total_engagements", ascending=False).head(10)
    return px.bar(top_df, x="post_id", y="total_engagements", title="Top 10 posts by total engagement")
