import pandas as pd
import numpy as np

np.random.seed(42)

def generate_datasets():
    channels = ['Google Ads', 'Meta Ads', 'LinkedIn Ads', 'Email Marketing', 'Affiliate Partners']
    dates = pd.date_range(start='2025-01-01', end='2025-06-30', freq='D')
    
    # 1. Marketing Spend Data
    spend_records = []
    for date in dates:
        for channel in channels:
            base_spend = {'Google Ads': 1500, 'Meta Ads': 1200, 'LinkedIn Ads': 800, 'Email Marketing': 300, 'Affiliate Partners': 600}[channel]
            spend = max(100, np.random.normal(base_spend, base_spend * 0.2))
            impressions = int(spend * np.random.uniform(50, 120))
            clicks = int(impressions * np.random.uniform(0.02, 0.08))
            spend_records.append([date, channel, round(spend, 2), impressions, clicks])
            
    df_spend = pd.DataFrame(spend_records, columns=['date', 'channel', 'spend', 'impressions', 'clicks'])
    df_spend.to_csv('data/raw_marketing_spend.csv', index=False)

    # 2. Sales / Conversion Data
    sales_records = []
    for _, row in df_spend.iterrows():
        # Conversion rate variance per channel
        conv_multiplier = {'Google Ads': 0.05, 'Meta Ads': 0.04, 'LinkedIn Ads': 0.025, 'Email Marketing': 0.08, 'Affiliate Partners': 0.06}[row['channel']]
        conversions = int(row['clicks'] * np.random.normal(conv_multiplier, 0.005))
        conversions = max(0, conversions)
        
        # Revenue per conversion
        avg_order_value = {'Google Ads': 120, 'Meta Ads': 90, 'LinkedIn Ads': 250, 'Email Marketing': 70, 'Affiliate Partners': 80}[row['channel']]
        revenue = conversions * max(20, np.random.normal(avg_order_value, 15))
        
        sales_records.append([row['date'], row['channel'], conversions, round(revenue, 2)])
        
    df_sales = pd.DataFrame(sales_records, columns=['date', 'channel', 'conversions', 'revenue'])
    df_sales.to_csv('data/raw_sales_data.csv', index=False)
    print("Datasets successfully generated inside the 'data/' directory.")

if __name__ == '__main__':
    generate_datasets()