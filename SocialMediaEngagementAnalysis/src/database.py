import sqlite3
from pathlib import Path


def pd_notnull(value):
    return value is not None and value != ""


def initialize_database(df, database_path):
    db_path = Path(database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS engagements")
    cursor.execute("DROP TABLE IF EXISTS posts")
    cursor.execute("DROP TABLE IF EXISTS campaigns")
    cursor.execute("DROP TABLE IF EXISTS platforms")

    cursor.execute(
        """
        CREATE TABLE platforms (
            platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_name TEXT NOT NULL UNIQUE
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE campaigns (
            campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT NOT NULL,
            campaign_category TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE posts (
            post_id TEXT PRIMARY KEY,
            platform_id INTEGER,
            content_type TEXT,
            caption TEXT,
            post_date TEXT,
            post_time TEXT,
            campaign_id INTEGER,
            FOREIGN KEY (platform_id) REFERENCES platforms(platform_id),
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE engagements (
            engagement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            clicks INTEGER,
            impressions INTEGER,
            reach INTEGER,
            total_engagements INTEGER,
            engagement_rate REAL,
            FOREIGN KEY (post_id) REFERENCES posts(post_id)
        )
        """
    )

    platform_ids = {}
    for platform in df["platform"].dropna().unique():
        cursor.execute("INSERT INTO platforms (platform_name) VALUES (?)", (platform,))
        platform_ids[platform] = cursor.execute("SELECT platform_id FROM platforms WHERE platform_name = ?", (platform,)).fetchone()[0]

    campaign_ids = {}
    for campaign in df["campaign"].fillna("Unspecified").dropna().unique():
        cursor.execute("INSERT INTO campaigns (campaign_name, campaign_category) VALUES (?, ?)", (campaign, "General"))
        campaign_ids[campaign] = cursor.execute("SELECT campaign_id FROM campaigns WHERE campaign_name = ?", (campaign,)).fetchone()[0]

    for _, row in df.iterrows():
        platform_id = platform_ids.get(row["platform"], 1)
        campaign_id = campaign_ids.get(row.get("campaign", "Unspecified"), 1)
        date_value = row.get("post_date")
        time_value = row.get("post_time")
        cursor.execute(
            "INSERT INTO posts (post_id, platform_id, content_type, caption, post_date, post_time, campaign_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                row["post_id"],
                platform_id,
                row.get("content_type", "Unspecified"),
                row.get("caption", "No caption"),
                date_value.strftime("%Y-%m-%d") if pd_notnull(date_value) else None,
                time_value.strftime("%H:%M:%S") if pd_notnull(time_value) else None,
                campaign_id,
            ),
        )
        cursor.execute(
            "INSERT INTO engagements (post_id, likes, comments, shares, clicks, impressions, reach, total_engagements, engagement_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                row["post_id"],
                int(row.get("likes", 0) or 0),
                int(row.get("comments", 0) or 0),
                int(row.get("shares", 0) or 0),
                int(row.get("clicks", 0) or 0),
                int(row.get("impressions", 0) or 0),
                int(row.get("reach", 0) or 0),
                int(row.get("total_engagements", 0) or 0),
                float(row.get("engagement_rate", 0) or 0),
            ),
        )

    connection.commit()
    connection.close()
