-- 1. Total posts and total recorded engagements
SELECT COUNT(*) AS total_posts, SUM(total_engagements) AS total_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id;

-- 2. Platform-wise performance comparison
SELECT pl.platform_name,
       COUNT(*) AS total_posts,
       ROUND(AVG(e.total_engagements), 2) AS avg_engagements_per_post,
       SUM(e.total_engagements) AS total_engagements
FROM posts p
JOIN platforms pl ON pl.platform_id = p.platform_id
JOIN engagements e ON e.post_id = p.post_id
GROUP BY pl.platform_name
ORDER BY total_engagements DESC;

-- 3. Top-performing post
SELECT p.post_id, pl.platform_name, p.content_type, e.total_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id
JOIN platforms pl ON pl.platform_id = p.platform_id
ORDER BY e.total_engagements DESC
LIMIT 10;

-- 4. Lowest-performing post
SELECT p.post_id, pl.platform_name, p.content_type, e.total_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id
JOIN platforms pl ON pl.platform_id = p.platform_id
ORDER BY e.total_engagements ASC
LIMIT 10;

-- 5. Engagement by content type
SELECT p.content_type, COUNT(*) AS total_posts,
       ROUND(AVG(e.total_engagements), 2) AS avg_engagements,
       SUM(e.total_engagements) AS total_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id
GROUP BY p.content_type
ORDER BY total_engagements DESC;

-- 6. Best performing posting day
SELECT CASE CAST(strftime('%w', p.post_date) AS INTEGER)
    WHEN 0 THEN 'Sunday'
    WHEN 1 THEN 'Monday'
    WHEN 2 THEN 'Tuesday'
    WHEN 3 THEN 'Wednesday'
    WHEN 4 THEN 'Thursday'
    WHEN 5 THEN 'Friday'
    WHEN 6 THEN 'Saturday'
END AS post_day,
COUNT(*) AS total_posts,
ROUND(AVG(e.total_engagements), 2) AS avg_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id
GROUP BY post_day
ORDER BY avg_engagements DESC;

-- 7. Best performing posting hour
SELECT CAST(strftime('%H', p.post_time) AS INTEGER) AS post_hour,
       COUNT(*) AS total_posts,
       ROUND(AVG(e.total_engagements), 2) AS avg_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id
GROUP BY post_hour
ORDER BY avg_engagements DESC;

-- 8. Monthly engagement trend
SELECT strftime('%Y-%m', p.post_date) AS month,
       SUM(e.total_engagements) AS total_engagements,
       ROUND(AVG(e.total_engagements), 2) AS avg_engagements
FROM posts p
JOIN engagements e ON e.post_id = p.post_id
GROUP BY month
ORDER BY month;

-- 9. Campaign analysis
SELECT c.campaign_name,
       COUNT(*) AS total_posts,
       ROUND(AVG(e.total_engagements), 2) AS avg_engagements,
       SUM(e.total_engagements) AS total_engagements
FROM posts p
JOIN campaigns c ON c.campaign_id = p.campaign_id
JOIN engagements e ON e.post_id = p.post_id
GROUP BY c.campaign_name
ORDER BY total_engagements DESC;

-- 10. Posts with no engagement
SELECT p.post_id, pl.platform_name, p.content_type, p.post_date
FROM posts p
JOIN platforms pl ON pl.platform_id = p.platform_id
LEFT JOIN engagements e ON e.post_id = p.post_id
WHERE COALESCE(e.total_engagements, 0) = 0
ORDER BY p.post_date;

-- 11. Engagement rate overview using impressions when available
SELECT pl.platform_name,
       SUM(e.impressions) AS total_impressions,
       SUM(e.total_engagements) AS total_engagements,
       ROUND((SUM(e.total_engagements) * 100.0) / NULLIF(SUM(e.impressions), 0), 2) AS engagement_rate_pct
FROM posts p
JOIN platforms pl ON pl.platform_id = p.platform_id
JOIN engagements e ON e.post_id = p.post_id
GROUP BY pl.platform_name
ORDER BY engagement_rate_pct DESC;

-- 12. Date range summary
SELECT MIN(p.post_date) AS earliest_post_date,
       MAX(p.post_date) AS latest_post_date,
       COUNT(*) AS total_posts
FROM posts p;
