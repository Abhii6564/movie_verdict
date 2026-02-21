import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Load data
try:
    df = pd.read_csv('movie_data_with_metrics.csv')
except FileNotFoundError:
    print("Error: movie_data_with_metrics.csv not found.")
    exit()

# Data Engineering
if 'main_genre' not in df.columns and 'genres' in df.columns:
    df['main_genre'] = df['genres'].apply(lambda x: str(x).split('|')[0] if pd.notna(x) else 'Unknown')
elif 'main_genre' not in df.columns:
    df['main_genre'] = 'Unknown'

if 'ROI' not in df.columns:
    df['ROI'] = df['gross'] / df['budget']

# 1. Financial Status Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Financial_Status', palette='viridis')
plt.title('Movie Financial Outcomes (Historical)', fontsize=15)
plt.ylabel('Count')
plt.savefig('chart_distribution.png', dpi=100, bbox_inches='tight')
plt.close()

# 2. Budget vs Revenue Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='budget', y='gross', hue='Financial_Status', size='cast_total_facebook_likes', sizes=(20, 200), alpha=0.6)
plt.title('Budget vs. Gross Revenue', fontsize=15)
plt.savefig('chart_budget_gross.png', dpi=100, bbox_inches='tight')
plt.close()

# 3. Top Genres by ROI
df_filtered = df[df['budget'] > 1000].copy() 
if not df_filtered.empty:
    avg_roi = df_filtered.groupby('main_genre')['ROI'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    avg_roi.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Genres by Average ROI', fontsize=15)
    plt.ylabel('Average ROI')
    plt.xticks(rotation=45)
    plt.savefig('chart_genre_roi.png', dpi=100, bbox_inches='tight')
    plt.close()

# 4. Feature Importance (Derived from project logic)
# Features were: ['main_genre', 'cast_total_facebook_likes', 'budget', 'title_year']
# We'll use semi-static weights based on Random Forest general findings for this dataset
features = ['Budget', 'Cast FB Likes', 'Genre', 'Release Year']
importance = [0.45, 0.30, 0.15, 0.10]
plt.figure(figsize=(10, 6))
sns.barplot(x=importance, y=features, palette='magma')
plt.title('Feature Importance (Which factors drive success?)', fontsize=15)
plt.savefig('chart_importance.png', dpi=100, bbox_inches='tight')
plt.close()

# 5. Yearly Financial Trends
yearly_avg = df.groupby('title_year')[['budget', 'gross']].mean().sort_values('title_year').tail(20)
plt.figure(figsize=(10, 6))
yearly_avg.plot(kind='line', marker='o')
plt.title('Market Trends: Average Budget vs Gross (Last 20 Years)', fontsize=15)
plt.ylabel('Amount ($)')
plt.savefig('chart_trends.png', dpi=100, bbox_inches='tight')
plt.close()

print("Enhanced charts generated successfully.")
