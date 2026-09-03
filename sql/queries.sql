-- Consolidate marketing spend and sales performance metrics using a full JOIN on date and channel
SELECT 
    COALESCE(s.date, rev.date) AS campaign_date,
    COALESCE(s.channel, rev.channel) AS marketing_channel,
    SUM(s.spend) AS total_spend,
    SUM(s.impressions) AS total_impressions,
    SUM(s.clicks) AS total_clicks,
    SUM(rev.conversions) AS total_conversions,
    SUM(rev.revenue) AS total_revenue
FROM marketing_spend s
FULL OUTER JOIN sales_data rev 
    ON s.date = rev.date AND s.channel = rev.channel
GROUP BY campaign_date, marketing_channel
ORDER BY campaign_date DESC, marketing_channel;