# Data Dictionary

The project is designed to work with a real Kaggle social media engagement dataset, and it includes a sample fallback for local testing. The real dataset must contain at least the fields described below; if actual Kaggle columns differ, the configuration file maps the real names to the project schema.

| Column | Data type | Business meaning | Example value | Missing value count | Role |
| --- | --- | --- | --- | --- | --- |
| post_id | String | Unique identifier for each post | post_001 | tracked during cleaning | Key |
| platform | String | Social media platform | Instagram | tracked during cleaning | Dimension |
| content_type | String | Type of content used | Video | tracked during cleaning | Dimension |
| campaign | String | Campaign or initiative label, if available | Spring Launch | tracked during cleaning | Dimension |
| post_date | Date | Date the post was published | 2024-01-05 | tracked during cleaning | Metric dimension |
| post_time | Time | Time of publication | 18:30:00 | tracked during cleaning | Metric dimension |
| caption | Text | Post text or description | New collection is live | tracked during cleaning | Text |
| likes | Integer | Number of likes received | 231 | tracked during cleaning | Engagement metric |
| comments | Integer | Number of comments received | 52 | tracked during cleaning | Engagement metric |
| shares | Integer | Number of shares received | 18 | tracked during cleaning | Engagement metric |
| clicks | Integer | Number of profile or link clicks, if available | 11 | tracked during cleaning | Engagement metric |
| impressions | Integer | Total impressions or views | 11200 | tracked during cleaning | Reach metric |
| reach | Integer | Unique reach or views | 9740 | tracked during cleaning | Reach metric |
| hashtags | String | Associated hashtags | #summer #sale | tracked during cleaning | Text |
| total_engagements | Integer | Combined likes + comments + shares + clicks | 302 | derived | KPI |
| engagement_rate | Float | Total engagements divided by impressions or reach | 2.7% | derived | KPI |
| post_day_of_week | String | Day on which the post was published | Monday | derived | Derived feature |
| post_hour | Integer | Hour of publication | 18 | derived | Derived feature |

Dataset limitations: some public Kaggle files do not include campaign names, hashtags, or time stamps. In such cases, the project handles those fields as optional and continues with available metrics.
