import re

import pandas as pd

from config import COLUMN_ALIASES, CONTENT_TYPE_MAP, PLATFORM_MAP, REQUIRED_COLUMNS


def standardize_columns(df):
    normalized = df.copy()
    normalized.columns = [str(col).strip().lower().replace(" ", "_") for col in normalized.columns]
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            alias_key = alias.lower().replace(" ", "_")
            if alias_key in normalized.columns and canonical not in normalized.columns:
                normalized[canonical] = normalized[alias_key]
    return normalized


def clean_social_media_data(df, source_name="unknown"):
    report = {
        "source_name": source_name,
        "before_rows": len(df),
        "after_rows": 0,
        "operations": [],
        "missing_columns": [],
    }

    original = df.copy()
    df = standardize_columns(df)
    required = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if required:
        report["missing_columns"] = required
        raise ValueError(f"Missing required columns: {required}")

    df = df.copy()
    df = df.drop_duplicates()
    report["operations"].append({"step": "duplicate_removal", "rows_affected": len(original) - len(df), "reason": "Removed duplicate rows"})

    for column in ["platform", "content_type", "campaign", "caption"]:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")
            df[column] = df[column].astype(str).str.strip()

    if "post_id" in df.columns:
        df["post_id"] = df["post_id"].fillna(pd.Series(range(1, len(df) + 1)).astype(str).map(lambda x: f"post_{x}"))
    else:
        df["post_id"] = [f"post_{idx}" for idx in range(1, len(df) + 1)]

    if "platform" in df.columns:
        df["platform"] = df["platform"].str.lower().map(lambda x: PLATFORM_MAP.get(str(x).strip().lower(), str(x).title()))

    if "content_type" in df.columns:
        df["content_type"] = df["content_type"].fillna("Unspecified")
        df["content_type"] = df["content_type"].astype(str).str.strip().str.lower().map(lambda x: CONTENT_TYPE_MAP.get(str(x).strip(), str(x).title()))
    else:
        df["content_type"] = "Unspecified"

    if "campaign" in df.columns:
        df["campaign"] = df["campaign"].fillna("Unspecified").astype(str).str.strip()
    else:
        df["campaign"] = "Unspecified"

    if "post_date" in df.columns:
        df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
        invalid_dates = int(df["post_date"].isna().sum())
        if invalid_dates:
            report["operations"].append({"step": "date_parsing", "rows_affected": invalid_dates, "reason": "Converted textual dates to datetime and invalid dates set to NaT"})

    if "post_time" in df.columns:
        df["post_time"] = df["post_time"].astype(str).str.strip()
        parsed_times = pd.to_datetime(df["post_time"], format="%H:%M:%S", errors="coerce")
        df["post_time"] = parsed_times
        report["operations"].append({"step": "time_parsing", "rows_affected": int(df["post_time"].isna().sum()), "reason": "Normalized time values to datetime objects"})
    elif "time" in df.columns:
        df["post_time"] = pd.to_datetime(df["time"], format="%H:%M:%S", errors="coerce")
        report["operations"].append({"step": "time_parsing", "rows_affected": int(df["post_time"].isna().sum()), "reason": "Normalized time values to datetime objects"})
    else:
        df["post_time"] = pd.NaT

    numeric_cols = ["likes", "comments", "shares", "clicks", "impressions", "reach"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            report["operations"].append({"step": f"numeric_validation:{col}", "rows_affected": int(df[col].isna().sum()), "reason": f"Converted {col} to numeric and flagged invalid values"})

    if "caption" in df.columns:
        df["caption"] = df["caption"].fillna("No caption").astype(str)
        df["caption"] = df["caption"].apply(lambda x: re.sub(r"\s+", " ", x).strip())
    else:
        df["caption"] = "No caption"

    if "hashtags" in df.columns:
        df["hashtags"] = df["hashtags"].fillna("No hashtags").astype(str)
    else:
        df["hashtags"] = "No hashtags"

    if "post_date" in df.columns and "post_time" in df.columns:
        combined = df["post_date"].dt.strftime("%Y-%m-%d").fillna("1900-01-01") + " " + df["post_time"].dt.strftime("%H:%M:%S").fillna("00:00:00")
        df["post_datetime"] = pd.to_datetime(combined, errors="coerce")
        df["post_day_of_week"] = df["post_datetime"].dt.day_name()
        df["post_hour"] = df["post_datetime"].dt.hour
        df["month_name"] = df["post_datetime"].dt.strftime("%b %Y")

    df = df.reset_index(drop=True)
    report["after_rows"] = len(df)
    report["operations"].append({"step": "final_validation", "rows_affected": len(df) - report["before_rows"], "reason": "Final row count validation after cleaning"})
    return df, report
