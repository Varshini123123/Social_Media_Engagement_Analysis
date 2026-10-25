from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_FILE = DATA_DIR / "sample" / "social_media_engagement_sample.csv"
DATABASE_PATH = PROCESSED_DATA_DIR / "social_media.db"

REQUIRED_COLUMNS = ["post_id", "platform", "post_date", "likes", "comments", "shares"]

COLUMN_ALIASES = {
    "post_id": ["post_id", "id", "postid", "social_post_id"],
    "platform": ["platform", "social_platform", "network", "source_platform"],
    "post_date": ["post_date", "date", "posted_at", "publish_date", "created_at"],
    "post_time": ["post_time", "time", "posted_time", "publish_time"],
    "content_type": ["content_type", "post_type", "format", "content_format"],
    "caption": ["caption", "post_text", "text", "description", "content"],
    "campaign": ["campaign", "campaign_name", "campaign_id", "initiative"],
    "likes": ["likes", "like_count", "num_likes"],
    "comments": ["comments", "comment_count", "num_comments"],
    "shares": ["shares", "share_count", "num_shares"],
    "clicks": ["clicks", "click_count", "num_clicks"],
    "impressions": ["impressions", "reach_impressions", "views"],
    "reach": ["reach", "unique_reach", "unique_views"],
    "hashtags": ["hashtags", "tags", "hash_tags"],
}

PLATFORM_MAP = {
    "instagram": "Instagram",
    "facebook": "Facebook",
    "twitter": "X",
    "x": "X",
    "linkedin": "LinkedIn",
    "youtube": "YouTube",
    "tiktok": "TikTok",
    "snapchat": "Snapchat",
    "threads": "Threads",
    "unknown": "Unknown",
}

CONTENT_TYPE_MAP = {
    "image": "Image",
    "photo": "Image",
    "video": "Video",
    "reel": "Video",
    "text": "Text",
    "carousel": "Carousel",
    "story": "Story",
    "live": "Live",
    "instagram story": "Story",
}

KAGGLE_SEARCH_TERMS = [
    "social media engagement",
    "social media analytics",
    "social media posts and interactions",
    "social media performance metrics",
]
