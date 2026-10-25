CREATE TABLE IF NOT EXISTS platforms (
    platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT NOT NULL,
    campaign_category TEXT
);

CREATE TABLE IF NOT EXISTS posts (
    post_id TEXT PRIMARY KEY,
    platform_id INTEGER,
    content_type TEXT,
    caption TEXT,
    post_date TEXT,
    post_time TEXT,
    campaign_id INTEGER,
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
);

CREATE TABLE IF NOT EXISTS engagements (
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
);

CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform_id);
CREATE INDEX IF NOT EXISTS idx_posts_date ON posts(post_date);
CREATE INDEX IF NOT EXISTS idx_posts_campaign ON posts(campaign_id);
CREATE INDEX IF NOT EXISTS idx_engagements_post ON engagements(post_id);
