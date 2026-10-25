SELECT 'Total posts' AS check_name, COUNT(*) AS result FROM posts
UNION ALL
SELECT 'Missing post dates', COUNT(*) FROM posts WHERE post_date IS NULL
UNION ALL
SELECT 'Missing platform values', COUNT(*) FROM posts WHERE platform_id IS NULL
UNION ALL
SELECT 'Duplicate post IDs', COUNT(*) FROM (
    SELECT post_id FROM posts GROUP BY post_id HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'Posts without engagement metrics', COUNT(*) FROM posts p
LEFT JOIN engagements e ON e.post_id = p.post_id
WHERE e.post_id IS NULL;
