import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from wordcloud import WordCloud

# Function to connect to the database and fetch all data
def fetch_all_data():
    conn = sqlite3.connect('FinalDatabase.db')
    cursor = conn.cursor()

    query = '''
    SELECT business_id, name, stars, review_count, categories, city, state, address, attributes
    FROM business
    '''
    
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    # Convert data to a Pandas DataFrame for easier analysis
    df = pd.DataFrame(data, columns=[
        'business_id', 'name', 'stars', 'review_count', 'categories', 'city', 'state', 'address', 'attributes'
    ])
    return df

# Fetch all the data
data_df = fetch_all_data()

# 1. Plot the Distribution of Ratings (Stars)
def plot_star_distribution(df):
    plt.hist(df['stars'], bins=np.arange(0.5, 6, 0.5), edgecolor='black', alpha=0.7)
    plt.xlabel('Stars')
    plt.ylabel('Number of Businesses')
    plt.title('Distribution of Business Ratings')
    plt.show()

# 2. Plot the Distribution of Review Counts
def plot_review_count_distribution(df):
    plt.hist(df['review_count'], bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Review Count')
    plt.ylabel('Number of Businesses')
    plt.title('Distribution of Review Counts')
    plt.show()

# 3. Plot Top Categories by Count
def plot_top_categories(df):
    category_count = {}
    for categories in df['categories']:
        if categories:
            for category in categories.split(','):
                category_count[category.strip()] = category_count.get(category.strip(), 0) + 1
    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:10]
    labels = [cat[0] for cat in top_categories]
    values = [cat[1] for cat in top_categories]
    plt.barh(labels, values, color='skyblue')
    plt.xlabel('Number of Businesses')
    plt.title('Top 10 Business Categories')
    plt.show()

# 4. Plot Heatmap of Businesses by City and Stars
def plot_heatmap_by_city_and_stars(df):
    pivot_table = df.pivot_table(index='city', columns='stars', aggfunc='size', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt='d', cmap="YlGnBu", cbar_kws={'label': 'Number of Businesses'})
    plt.title('Heatmap of Businesses by City and Stars')
    plt.ylabel('City')
    plt.xlabel('Stars')
    plt.show()

# 5. Plot Review Count vs. Stars (Scatter Plot)
def plot_review_count_vs_stars(df):
    plt.scatter(df['review_count'], df['stars'], alpha=0.5, color='purple')
    plt.xlabel('Review Count')
    plt.ylabel('Stars')
    plt.title('Review Count vs. Stars')
    plt.show()

# 6. Plot Businesses by City and State
def plot_businesses_by_city_and_state(df):
    city_state_count = df.groupby(['city', 'state']).size().sort_values(ascending=False)[:10]
    city_state_count.plot(kind='barh', color='lightcoral', figsize=(10, 7))
    plt.xlabel('Number of Businesses')
    plt.ylabel('City, State')
    plt.title('Top 10 Business Cities and States')
    plt.show()

def plot_avg_rating_by_city(df):
    # Group by city and calculate the average rating
    avg_rating = df.groupby('city')['stars'].mean().sort_values(ascending=False).head(10)
    
    # Plot the average rating for the top 10 cities
    avg_rating.plot(kind='barh', color='lightgreen', figsize=(10, 7))
    plt.xlabel('Average Rating')
    plt.ylabel('City')
    plt.title('Top 10 Cities by Average Business Rating')
    plt.show()

def plot_review_count_vs_stars_with_city(df):
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='review_count', y='stars', hue='city', data=df, alpha=0.7, palette='tab20')
    plt.xlabel('Review Count')
    plt.ylabel('Stars')
    plt.title('Review Count vs. Stars (Color by City)')
    plt.legend(title='City', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_boxplot_ratings_by_city(df):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='city', y='stars', data=df)
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.xlabel('City')
    plt.ylabel('Stars')
    plt.title('Business Rating Distribution by City')
    plt.show()

def plot_correlation_heatmap(df):
    correlation_matrix = df[['stars', 'review_count']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap of Stars and Review Count')
    plt.show()

def plot_category_wordcloud(df):
    # Combine all categories into a single string
    all_categories = ' '.join(df['categories'].dropna())
    
    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_categories)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Most Common Business Categories')
    plt.show()

# Run all visualizations
def run_all_visualizations(df):
    #plot_star_distribution(df)
    #plot_review_count_distribution(df)
    #plot_top_categories(df)
    #plot_heatmap_by_city_and_stars(df)
    #plot_review_count_vs_stars(df)
    #plot_businesses_by_city_and_state(df)
    #plot_avg_rating_by_city(df)
    #plot_review_count_vs_stars_with_city(df)
    #plot_boxplot_ratings_by_city(df)
    #plot_correlation_heatmap(df)
    plot_category_wordcloud(df)

# Call the function to generate all visualizations
run_all_visualizations(data_df)
