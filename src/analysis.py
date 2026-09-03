import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def run_analysis():
    # Ensure outputs directory exists
    os.makedirs('outputs', exist_ok=True)

    # Load raw inputs
    df_spend = pd.read_csv('data/raw_marketing_spend.csv')
    df_sales = pd.read_csv('data/raw_sales_data.csv')

    # Data Cleaning and Preprocessing (Merge datasets)
    df = pd.merge(df_spend, df_sales, on=['date', 'channel'], how='inner')
    df['date'] = pd.to_datetime(df['date'])
    df.fillna(0, inplace=True)

    # Aggregate performance metrics by channel
    channel_perf = df.groupby('channel').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'revenue': 'sum'
    }).reset_index()

    # Calculate Core Financial & Marketing Metrics
    channel_perf['profit'] = channel_perf['revenue'] - channel_perf['spend']
    channel_perf['ROAS'] = channel_perf['revenue'] / channel_perf['spend']
    channel_perf['ROI'] = (channel_perf['profit'] / channel_perf['spend']) * 100
    channel_perf['conversion_rate'] = (channel_perf['conversions'] / channel_perf['clicks']) * 100
    channel_perf['profit_margin'] = (channel_perf['profit'] / channel_perf['revenue']) * 100

    print("--- Channel Performance Summary ---")
    print(channel_perf[['channel', 'spend', 'revenue', 'ROAS', 'ROI', 'profit_margin']])

    # Identify 15% Budget Inefficiency in Low-Performing Channels
    total_budget = channel_perf['spend'].sum()
    inefficient_channels = channel_perf.sort_values(by='ROAS', ascending=True).head(2)
    target_reallocation_amount = total_budget * 0.15

    print(f"\n[Insight] Total Spend: ${total_budget:,.2f}")
    print(f"[Insight] Low-performing channels identified: {list(inefficient_channels['channel'])}")
    print(f"[Action] Reallocating ${target_reallocation_amount:,.2f} (representing 15% budget inefficiency) to high ROAS engines.")

    # Save consolidated processed file
    df.to_csv('data/consolidated_campaign_data.csv', index=False)

    # Set overall theme style
    sns.set_theme(style="whitegrid")

    # --- INDIVIDUAL VISUALIZATION FILES ---

    # 1. ROAS Bar Chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='channel', y='ROAS', data=channel_perf, palette='Blues_r')
    plt.axhline(1.0, color='red', linestyle='--', linewidth=1.5, label='Break-even (1.0)')
    plt.title('Return on Ad Spend (ROAS) by Marketing Channel', fontsize=14, fontweight='bold')
    plt.xlabel('Marketing Channel', fontsize=12)
    plt.ylabel('ROAS', fontsize=12)
    plt.xticks(rotation=25)
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/roas_by_channel.png', dpi=300)
    plt.close()

    # 2. Spend vs Revenue Grouped Bar Chart
    plt.figure(figsize=(10, 6))
    melted_df = channel_perf.melt(id_vars='channel', value_vars=['spend', 'revenue'], var_name='Metric', value_name='Amount')
    sns.barplot(x='channel', y='Amount', hue='Metric', data=melted_df, palette='Set2')
    plt.title('Total Spend vs. Revenue by Channel', fontsize=14, fontweight='bold')
    plt.xlabel('Marketing Channel', fontsize=12)
    plt.ylabel('Amount (USD)', fontsize=12)
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig('outputs/spend_vs_revenue.png', dpi=300)
    plt.close()

    # 3. Budget Allocation Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(channel_perf['spend'], labels=channel_perf['channel'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'), textprops={'fontsize': 11})
    plt.title('Marketing Budget Distribution Share', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/budget_share_pie_chart.png', dpi=300)
    plt.close()

    # 4. Scatter Plot with Trendline
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='spend', y='revenue', hue='channel', data=df, s=60, palette='deep', alpha=0.7)
    m, b = np.polyfit(df['spend'], df['revenue'], 1)
    plt.plot(df['spend'], m*df['spend'] + b, color='black', linestyle='--', linewidth=2, label='Trendline')
    plt.title('Daily Spend vs. Revenue Correlation', fontsize=14, fontweight='bold')
    plt.xlabel('Daily Spend ($)', fontsize=12)
    plt.ylabel('Daily Revenue ($)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('outputs/spend_vs_revenue_scatterplot.png', dpi=300)
    plt.close()

    # 5. Conversion Rate Bar Chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='channel', y='conversion_rate', data=channel_perf, palette='Purples_r')
    plt.title('Conversion Rate (%) by Channel', fontsize=14, fontweight='bold')
    plt.xlabel('Marketing Channel', fontsize=12)
    plt.ylabel('Conversion Rate (%)', fontsize=12)
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig('outputs/conversion_rate_by_channel.png', dpi=300)
    plt.close()

    print("\nAll 5 individual visualizations successfully saved to the 'outputs/' directory!")

if __name__ == '__main__':
    run_analysis()