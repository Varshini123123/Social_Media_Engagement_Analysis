import pandas as pd


def compute_kpis(df):
    metrics = {
        "total_posts": int(len(df)),
        "total_likes": int(df["likes"].sum()) if "likes" in df.columns else 0,
        "total_comments": int(df["comments"].sum()) if "comments" in df.columns else 0,
        "total_shares": int(df["shares"].sum()) if "shares" in df.columns else 0,
        "total_clicks": int(df["clicks"].sum()) if "clicks" in df.columns else 0,
        "total_engagements": int(df["total_engagements"].sum()) if "total_engagements" in df.columns else 0,
    }
    if metrics["total_posts"]:
        metrics["avg_engagements_per_post"] = metrics["total_engagements"] / metrics["total_posts"]
    else:
        metrics["avg_engagements_per_post"] = 0.0

    impressions = df["impressions"].sum() if "impressions" in df.columns else 0
    reach = df["reach"].sum() if "reach" in df.columns else 0
    if impressions > 0:
        metrics["engagement_rate"] = (metrics["total_engagements"] / impressions) * 100
        metrics["engagement_rate_basis"] = "Total engagements / total impressions"
    elif reach > 0:
        metrics["engagement_rate"] = (metrics["total_engagements"] / reach) * 100
        metrics["engagement_rate_basis"] = "Total engagements / total reach"
    else:
        metrics["engagement_rate"] = None
        metrics["engagement_rate_basis"] = "Impressions and reach unavailable; avg engagements per post is shown instead"

    if impressions > 0:
        metrics["avg_impressions_per_post"] = impressions / metrics["total_posts"]
    elif reach > 0:
        metrics["avg_impressions_per_post"] = reach / metrics["total_posts"]
    else:
        metrics["avg_impressions_per_post"] = None

    if "platform" in df.columns and not df.empty:
        metrics["platform_ranking"] = df.groupby("platform", dropna=False)["total_engagements"].mean().sort_values(ascending=False).to_dict()
    else:
        metrics["platform_ranking"] = {}

    if "content_type" in df.columns and not df.empty:
        metrics["best_content_category"] = df.groupby("content_type")["total_engagements"].mean().idxmax()
    else:
        metrics["best_content_category"] = None

    if "post_day_of_week" in df.columns and not df.empty:
        metrics["best_posting_day"] = df.groupby("post_day_of_week")["total_engagements"].mean().idxmax()
    else:
        metrics["best_posting_day"] = None

    if "post_hour" in df.columns and not df.empty:
        metrics["best_posting_hour"] = df.groupby("post_hour")["total_engagements"].mean().idxmax()
    else:
        metrics["best_posting_hour"] = None

    if "post_date" in df.columns and not df.empty:
        monthly = df.groupby(df["post_date"].dt.to_period("M"))["total_engagements"].sum().sort_index()
        if len(monthly) > 1:
            current = monthly.iloc[-1]
            previous = monthly.iloc[-2]
            metrics["month_over_month_change"] = None if previous == 0 else ((current - previous) / previous) * 100
        else:
            metrics["month_over_month_change"] = None
    else:
        metrics["month_over_month_change"] = None

    return metrics
