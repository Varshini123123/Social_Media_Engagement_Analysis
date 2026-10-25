def generate_insights(df):
    observations = []
    recommendations = []

    if df.empty:
        return {"observations": ["No data available for insight generation."], "recommendations": ["Add more posts to evaluate performance."]}

    top_platform = df.groupby("platform")["total_engagements"].mean().idxmax()
    top_platform_avg = df.groupby("platform")["total_engagements"].mean().max()
    observations.append(f"The strongest-performing platform is {top_platform}, averaging {top_platform_avg:.1f} engagements per post.")
    recommendations.append(f"Increase investment in {top_platform} content themes that align with the top-performing posts and maintain frequency there.")

    if "content_type" in df.columns:
        best_content = df.groupby("content_type")["total_engagements"].mean().idxmax()
        best_content_avg = df.groupby("content_type")["total_engagements"].mean().max()
        observations.append(f"Content type with the highest average engagement is {best_content} at {best_content_avg:.1f} engagements per post.")
        recommendations.append(f"Prioritize {best_content} content when planning campaigns and test variations of it across different audiences.")

    if "post_day_of_week" in df.columns:
        best_day = df.groupby("post_day_of_week")["total_engagements"].mean().idxmax()
        observations.append(f"The strongest posting day in the historical data is {best_day}.")
        recommendations.append(f"Schedule more posts on {best_day} and test similar post timings around that day to strengthen reach and engagement.")

    if "post_hour" in df.columns:
        best_hour = df.groupby("post_hour")["total_engagements"].mean().idxmax()
        observations.append(f"The most effective posting hour in the dataset is {best_hour}:00.")
        recommendations.append(f"Aim to publish high-priority campaigns around {best_hour}:00 to match observed audience behavior.")

    top_post = df.sort_values("total_engagements", ascending=False).head(1).iloc[0]
    observations.append(f"The leading post, {top_post['post_id']}, generated {top_post['total_engagements']} engagements and provides a benchmark for future creative testing.")
    recommendations.append("Use the top-performing post as a benchmark for copy, creative treatment, and CTA design in future campaigns.")

    return {"observations": observations, "recommendations": recommendations}
