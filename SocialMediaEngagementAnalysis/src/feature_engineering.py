import pandas as pd


def add_engagement_features(df):
    out = df.copy()
    metric_columns = [col for col in ["likes", "comments", "shares", "clicks"] if col in out.columns]
    for col in metric_columns:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)

    engagement_components = ["likes", "comments", "shares"]
    present = [col for col in engagement_components if col in out.columns]
    if present:
        out["total_engagements"] = out[present].sum(axis=1)
    else:
        out["total_engagements"] = 0

    if "clicks" in out.columns:
        out["total_engagements"] = out["total_engagements"] + out["clicks"].fillna(0)

    if "impressions" in out.columns:
        out["engagement_rate"] = (out["total_engagements"] / out["impressions"].replace(0, pd.NA)) * 100
    elif "reach" in out.columns:
        out["engagement_rate"] = (out["total_engagements"] / out["reach"].replace(0, pd.NA)) * 100
    else:
        out["engagement_rate"] = pd.NA

    if "post_date" in out.columns:
        out["post_date"] = pd.to_datetime(out["post_date"], errors="coerce")
        out["post_day_of_week"] = out["post_date"].dt.day_name()
        out["month_name"] = out["post_date"].dt.strftime("%b %Y")
    if "post_datetime" in out.columns:
        out["post_hour"] = out["post_datetime"].dt.hour
    return out
