"""
Analysis Module for Retail Transaction Analysis

This module performs all analytical computations and generates insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple


def descriptive_statistics(df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive descriptive statistics.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        Dictionary containing summary statistics for numerical and categorical columns
    """
    print("\n" + "="*60)
    print("DESCRIPTIVE STATISTICS")
    print("="*60)
    
    stats = {}
    
    # Numerical columns statistics
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    print("\n1. NUMERICAL COLUMNS")
    print("-" * 60)
    
    numerical_stats = {}
    for col in numerical_cols:
        col_stats = {
            'count': int(df[col].count()),
            'mean': float(df[col].mean()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'q25': float(df[col].quantile(0.25)),
            'median': float(df[col].median()),
            'q75': float(df[col].quantile(0.75)),
            'max': float(df[col].max()),
        }
        numerical_stats[col] = col_stats
        
        print(f"\n{col}:")
        print(f"  Count: {col_stats['count']:,}")
        print(f"  Mean: {col_stats['mean']:.2f}")
        print(f"  Std: {col_stats['std']:.2f}")
        print(f"  Min: {col_stats['min']:.2f}")
        print(f"  25%: {col_stats['q25']:.2f}")
        print(f"  Median: {col_stats['median']:.2f}")
        print(f"  75%: {col_stats['q75']:.2f}")
        print(f"  Max: {col_stats['max']:.2f}")
    
    stats['numerical'] = numerical_stats
    
    # Categorical columns statistics
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    print("\n2. CATEGORICAL COLUMNS")
    print("-" * 60)
    
    categorical_stats = {}
    for col in categorical_cols:
        unique_count = df[col].nunique()
        value_counts = df[col].value_counts().head(10).to_dict()
        
        col_stats = {
            'count': int(df[col].count()),
            'unique': int(unique_count),
            'top_values': value_counts,
            'most_common': df[col].mode()[0] if not df[col].mode().empty else None,
        }
        categorical_stats[col] = col_stats
        
        print(f"\n{col}:")
        print(f"  Count: {col_stats['count']:,}")
        print(f"  Unique values: {col_stats['unique']:,}")
        print(f"  Most common: {col_stats['most_common']}")
        print(f"  Top 5 values:")
        for value, count in list(value_counts.items())[:5]:
            percentage = (count / len(df)) * 100
            print(f"    {value}: {count:,} ({percentage:.1f}%)")
    
    stats['categorical'] = categorical_stats
    
    # Overall dataset statistics
    print("\n3. DATASET OVERVIEW")
    print("-" * 60)
    
    overview = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'numerical_columns': len(numerical_cols),
        'categorical_columns': len(categorical_cols),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
    }
    
    stats['overview'] = overview
    
    print(f"  Total rows: {overview['total_rows']:,}")
    print(f"  Total columns: {overview['total_columns']}")
    print(f"  Numerical columns: {overview['numerical_columns']}")
    print(f"  Categorical columns: {overview['categorical_columns']}")
    print(f"  Memory usage: {overview['memory_usage_mb']:.2f} MB")
    
    print("\n" + "="*60)
    
    return stats



def top_products_analysis(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identify top products by sales volume and revenue.
    
    Args:
        df: Transaction DataFrame
        top_n: Number of top products to return (default: 10)
        
    Returns:
        DataFrame with top products ranked by multiple metrics
    """
    print("\n" + "="*60)
    print(f"TOP {top_n} PRODUCTS ANALYSIS")
    print("="*60)
    
    # Group by product
    product_metrics = df.groupby(['ProductID', 'ProductName']).agg({
        'Quantity': 'sum',
        'TotalAmount': 'sum',
        'TransactionID': 'count',
        'Price': 'mean'
    }).reset_index()
    
    # Rename columns for clarity
    product_metrics.columns = ['ProductID', 'ProductName', 'TotalQuantity', 
                                'TotalRevenue', 'TransactionCount', 'AvgPrice']
    
    # Sort by revenue (primary metric)
    product_metrics = product_metrics.sort_values('TotalRevenue', ascending=False)
    
    # Get top N
    top_products = product_metrics.head(top_n).copy()
    
    # Add ranking
    top_products['RevenueRank'] = range(1, len(top_products) + 1)
    
    # Calculate percentage of total
    total_revenue = df['TotalAmount'].sum()
    top_products['RevenuePercentage'] = (top_products['TotalRevenue'] / total_revenue) * 100
    
    print(f"\nTop {top_n} Products by Revenue:")
    print("-" * 60)
    for idx, row in top_products.iterrows():
        print(f"\n{row['RevenueRank']}. {row['ProductName']}")
        print(f"   Product ID: {row['ProductID']}")
        print(f"   Total Revenue: ${row['TotalRevenue']:,.2f} ({row['RevenuePercentage']:.1f}% of total)")
        print(f"   Total Quantity Sold: {row['TotalQuantity']:,.0f}")
        print(f"   Transaction Count: {row['TransactionCount']:,}")
        print(f"   Average Price: ${row['AvgPrice']:.2f}")
    
    print("\n" + "="*60)
    
    return top_products


def top_cities_analysis(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identify top cities by transaction volume and revenue.
    
    Args:
        df: Transaction DataFrame
        top_n: Number of top cities to return (default: 10)
        
    Returns:
        DataFrame with top cities ranked by multiple metrics
    """
    print("\n" + "="*60)
    print(f"TOP {top_n} CITIES ANALYSIS")
    print("="*60)
    
    # Group by city
    city_metrics = df.groupby('City').agg({
        'TransactionID': 'count',
        'TotalAmount': 'sum',
        'Quantity': 'sum',
        'CustomerID': 'nunique'
    }).reset_index()
    
    # Rename columns for clarity
    city_metrics.columns = ['City', 'TransactionCount', 'TotalRevenue', 
                            'TotalQuantity', 'UniqueCustomers']
    
    # Calculate average transaction value
    city_metrics['AvgTransactionValue'] = city_metrics['TotalRevenue'] / city_metrics['TransactionCount']
    
    # Sort by revenue (primary metric)
    city_metrics = city_metrics.sort_values('TotalRevenue', ascending=False)
    
    # Get top N
    top_cities = city_metrics.head(top_n).copy()
    
    # Add ranking
    top_cities['RevenueRank'] = range(1, len(top_cities) + 1)
    
    # Calculate percentage of total
    total_revenue = df['TotalAmount'].sum()
    top_cities['RevenuePercentage'] = (top_cities['TotalRevenue'] / total_revenue) * 100
    
    print(f"\nTop {top_n} Cities by Revenue:")
    print("-" * 60)
    for idx, row in top_cities.iterrows():
        print(f"\n{row['RevenueRank']}. {row['City']}")
        print(f"   Total Revenue: ${row['TotalRevenue']:,.2f} ({row['RevenuePercentage']:.1f}% of total)")
        print(f"   Transaction Count: {row['TransactionCount']:,}")
        print(f"   Unique Customers: {row['UniqueCustomers']:,}")
        print(f"   Total Quantity: {row['TotalQuantity']:,.0f}")
        print(f"   Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
    
    print("\n" + "="*60)
    
    return top_cities



def customer_spending_analysis(df: pd.DataFrame) -> Dict:
    """
    Analyze customer spending patterns and segmentation.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        Dictionary containing:
        - avg_transaction_value: Overall average transaction value
        - customer_segments: DataFrame with customer segmentation (high/medium/low value)
        - spending_distribution: Statistics about spending distribution
        - repeat_purchase_rate: Percentage of customers with multiple purchases
        - visit_frequency: Average visits per customer
    """
    print("\n" + "="*60)
    print("CUSTOMER SPENDING ANALYSIS")
    print("="*60)
    
    # Calculate customer-level metrics
    customer_metrics = df.groupby('CustomerID').agg({
        'TotalAmount': ['sum', 'mean', 'count'],
        'TransactionID': 'count',
        'Date': ['min', 'max']
    }).reset_index()
    
    # Flatten column names
    customer_metrics.columns = ['CustomerID', 'TotalSpending', 'AvgTransactionValue', 
                                 'TransactionCount', 'TransactionCount2', 'FirstPurchase', 'LastPurchase']
    customer_metrics = customer_metrics.drop('TransactionCount2', axis=1)
    
    # Overall metrics
    avg_transaction_value = df['TotalAmount'].mean()
    total_customers = df['CustomerID'].nunique()
    total_transactions = len(df)
    
    print("\n1. OVERALL METRICS")
    print("-" * 60)
    print(f"  Total Customers: {total_customers:,}")
    print(f"  Total Transactions: {total_transactions:,}")
    print(f"  Average Transaction Value: ${avg_transaction_value:.2f}")
    print(f"  Average Transactions per Customer: {total_transactions / total_customers:.2f}")
    
    # Customer segmentation based on spending quantiles
    print("\n2. CUSTOMER SEGMENTATION")
    print("-" * 60)
    
    # Define segments based on total spending
    q33 = customer_metrics['TotalSpending'].quantile(0.33)
    q67 = customer_metrics['TotalSpending'].quantile(0.67)
    
    def assign_segment(spending):
        if spending >= q67:
            return 'High Value'
        elif spending >= q33:
            return 'Medium Value'
        else:
            return 'Low Value'
    
    customer_metrics['Segment'] = customer_metrics['TotalSpending'].apply(assign_segment)
    
    # Segment statistics
    segment_stats = customer_metrics.groupby('Segment').agg({
        'CustomerID': 'count',
        'TotalSpending': ['sum', 'mean'],
        'AvgTransactionValue': 'mean',
        'TransactionCount': 'mean'
    }).reset_index()
    
    segment_stats.columns = ['Segment', 'CustomerCount', 'TotalRevenue', 
                             'AvgSpendingPerCustomer', 'AvgTransactionValue', 'AvgTransactionCount']
    
    # Calculate percentages
    segment_stats['CustomerPercentage'] = (segment_stats['CustomerCount'] / total_customers) * 100
    segment_stats['RevenuePercentage'] = (segment_stats['TotalRevenue'] / df['TotalAmount'].sum()) * 100
    
    # Sort by segment value
    segment_order = {'High Value': 0, 'Medium Value': 1, 'Low Value': 2}
    segment_stats['SortOrder'] = segment_stats['Segment'].map(segment_order)
    segment_stats = segment_stats.sort_values('SortOrder').drop('SortOrder', axis=1)
    
    print("\nCustomer Segments:")
    for idx, row in segment_stats.iterrows():
        print(f"\n{row['Segment']}:")
        print(f"  Customers: {row['CustomerCount']:,} ({row['CustomerPercentage']:.1f}%)")
        print(f"  Total Revenue: ${row['TotalRevenue']:,.2f} ({row['RevenuePercentage']:.1f}%)")
        print(f"  Avg Spending per Customer: ${row['AvgSpendingPerCustomer']:.2f}")
        print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
        print(f"  Avg Transactions: {row['AvgTransactionCount']:.1f}")
    
    # Spending distribution
    print("\n3. SPENDING DISTRIBUTION")
    print("-" * 60)
    
    spending_distribution = {
        'min': float(customer_metrics['TotalSpending'].min()),
        'q25': float(customer_metrics['TotalSpending'].quantile(0.25)),
        'median': float(customer_metrics['TotalSpending'].median()),
        'q75': float(customer_metrics['TotalSpending'].quantile(0.75)),
        'max': float(customer_metrics['TotalSpending'].max()),
        'mean': float(customer_metrics['TotalSpending'].mean()),
        'std': float(customer_metrics['TotalSpending'].std()),
    }
    
    print(f"  Min Spending: ${spending_distribution['min']:.2f}")
    print(f"  25th Percentile: ${spending_distribution['q25']:.2f}")
    print(f"  Median Spending: ${spending_distribution['median']:.2f}")
    print(f"  75th Percentile: ${spending_distribution['q75']:.2f}")
    print(f"  Max Spending: ${spending_distribution['max']:.2f}")
    print(f"  Mean Spending: ${spending_distribution['mean']:.2f}")
    print(f"  Std Deviation: ${spending_distribution['std']:.2f}")
    
    # Repeat purchase analysis
    print("\n4. PURCHASE FREQUENCY")
    print("-" * 60)
    
    repeat_customers = (customer_metrics['TransactionCount'] > 1).sum()
    repeat_purchase_rate = (repeat_customers / total_customers) * 100
    avg_visit_frequency = customer_metrics['TransactionCount'].mean()
    
    print(f"  Customers with Multiple Purchases: {repeat_customers:,} ({repeat_purchase_rate:.1f}%)")
    print(f"  One-time Customers: {total_customers - repeat_customers:,} ({100 - repeat_purchase_rate:.1f}%)")
    print(f"  Average Visits per Customer: {avg_visit_frequency:.2f}")
    print(f"  Max Visits by Single Customer: {customer_metrics['TransactionCount'].max():.0f}")
    
    # Transaction frequency distribution
    freq_distribution = customer_metrics['TransactionCount'].value_counts().sort_index().head(10)
    print(f"\n  Transaction Frequency Distribution (Top 10):")
    for transactions, count in freq_distribution.items():
        percentage = (count / total_customers) * 100
        print(f"    {transactions} transaction(s): {count:,} customers ({percentage:.1f}%)")
    
    print("\n" + "="*60)
    
    return {
        'avg_transaction_value': avg_transaction_value,
        'customer_segments': segment_stats,
        'customer_metrics': customer_metrics,
        'spending_distribution': spending_distribution,
        'repeat_purchase_rate': repeat_purchase_rate,
        'visit_frequency': avg_visit_frequency,
        'total_customers': total_customers,
    }



def store_type_preference_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze customer preferences across store types.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        DataFrame with metrics by store type
    """
    print("\n" + "="*60)
    print("STORE TYPE PREFERENCE ANALYSIS")
    print("="*60)
    
    # Group by store type
    store_metrics = df.groupby('StoreType').agg({
        'TransactionID': 'count',
        'TotalAmount': ['sum', 'mean'],
        'Quantity': 'sum',
        'CustomerID': 'nunique',
        'ProductID': 'nunique'
    }).reset_index()
    
    # Flatten column names
    store_metrics.columns = ['StoreType', 'TransactionCount', 'TotalRevenue', 
                             'AvgTransactionValue', 'TotalQuantity', 'UniqueCustomers', 'UniqueProducts']
    
    # Calculate percentages
    total_revenue = df['TotalAmount'].sum()
    total_transactions = len(df)
    
    store_metrics['RevenuePercentage'] = (store_metrics['TotalRevenue'] / total_revenue) * 100
    store_metrics['TransactionPercentage'] = (store_metrics['TransactionCount'] / total_transactions) * 100
    
    # Calculate revenue per customer
    store_metrics['RevenuePerCustomer'] = store_metrics['TotalRevenue'] / store_metrics['UniqueCustomers']
    
    # Sort by revenue
    store_metrics = store_metrics.sort_values('TotalRevenue', ascending=False)
    
    print("\nStore Type Performance:")
    print("-" * 60)
    for idx, row in store_metrics.iterrows():
        print(f"\n{row['StoreType']}:")
        print(f"  Total Revenue: ${row['TotalRevenue']:,.2f} ({row['RevenuePercentage']:.1f}%)")
        print(f"  Transaction Count: {row['TransactionCount']:,} ({row['TransactionPercentage']:.1f}%)")
        print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
        print(f"  Unique Customers: {row['UniqueCustomers']:,}")
        print(f"  Revenue per Customer: ${row['RevenuePerCustomer']:.2f}")
        print(f"  Total Quantity Sold: {row['TotalQuantity']:,.0f}")
        print(f"  Unique Products: {row['UniqueProducts']:,}")
    
    print("\n" + "="*60)
    
    return store_metrics


def product_preference_by_segment(df: pd.DataFrame, customer_segments: pd.DataFrame) -> Dict:
    """
    Analyze product preferences by customer segment.
    
    Args:
        df: Transaction DataFrame
        customer_segments: DataFrame with customer segmentation from customer_spending_analysis
        
    Returns:
        Dictionary with product preferences by segment
    """
    print("\n" + "="*60)
    print("PRODUCT PREFERENCE BY CUSTOMER SEGMENT")
    print("="*60)
    
    # Merge customer segments with transactions
    df_with_segments = df.merge(
        customer_segments[['CustomerID', 'Segment']], 
        on='CustomerID', 
        how='left'
    )
    
    segment_preferences = {}
    
    for segment in ['High Value', 'Medium Value', 'Low Value']:
        segment_data = df_with_segments[df_with_segments['Segment'] == segment]
        
        if len(segment_data) == 0:
            continue
        
        print(f"\n{segment} Customers:")
        print("-" * 60)
        
        # Top categories
        category_sales = segment_data.groupby('Category').agg({
            'TotalAmount': 'sum',
            'TransactionID': 'count'
        }).sort_values('TotalAmount', ascending=False).head(5)
        
        print(f"  Top 5 Categories:")
        for category, row in category_sales.iterrows():
            revenue_pct = (row['TotalAmount'] / segment_data['TotalAmount'].sum()) * 100
            print(f"    {category}: ${row['TotalAmount']:,.2f} ({revenue_pct:.1f}%)")
        
        # Top products
        product_sales = segment_data.groupby(['ProductID', 'ProductName']).agg({
            'TotalAmount': 'sum',
            'Quantity': 'sum'
        }).sort_values('TotalAmount', ascending=False).head(5)
        
        print(f"  Top 5 Products:")
        for (prod_id, prod_name), row in product_sales.iterrows():
            print(f"    {prod_name}: ${row['TotalAmount']:,.2f} (Qty: {row['Quantity']:.0f})")
        
        segment_preferences[segment] = {
            'top_categories': category_sales.to_dict(),
            'top_products': product_sales.to_dict()
        }
    
    print("\n" + "="*60)
    
    return segment_preferences



def promotion_effectiveness_analysis(df: pd.DataFrame) -> Dict:
    """
    Evaluate promotion and discount effectiveness.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        Dictionary containing:
        - discount_vs_non_discount_metrics: Comparison of transactions with/without discounts
        - promotion_roi: Return on investment metrics
        - discount_level_analysis: Analysis by discount percentage ranges
        - top_discounted_products: Products that benefit most from discounts
    """
    print("\n" + "="*60)
    print("PROMOTION EFFECTIVENESS ANALYSIS")
    print("="*60)
    
    # Create discount flag
    df['HasDiscount'] = df['Discount'] > 0
    
    # 1. Discount vs Non-Discount Comparison
    print("\n1. DISCOUNT VS NON-DISCOUNT COMPARISON")
    print("-" * 60)
    
    discount_comparison = df.groupby('HasDiscount').agg({
        'TransactionID': 'count',
        'TotalAmount': ['sum', 'mean'],
        'Quantity': ['sum', 'mean'],
        'CustomerID': 'nunique'
    }).reset_index()
    
    discount_comparison.columns = ['HasDiscount', 'TransactionCount', 'TotalRevenue', 
                                   'AvgTransactionValue', 'TotalQuantity', 'AvgQuantity', 'UniqueCustomers']
    
    # Calculate percentages
    total_revenue = df['TotalAmount'].sum()
    total_transactions = len(df)
    
    for idx, row in discount_comparison.iterrows():
        discount_status = "With Discount" if row['HasDiscount'] else "Without Discount"
        revenue_pct = (row['TotalRevenue'] / total_revenue) * 100
        transaction_pct = (row['TransactionCount'] / total_transactions) * 100
        
        print(f"\n{discount_status}:")
        print(f"  Transaction Count: {row['TransactionCount']:,} ({transaction_pct:.1f}%)")
        print(f"  Total Revenue: ${row['TotalRevenue']:,.2f} ({revenue_pct:.1f}%)")
        print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
        print(f"  Total Quantity: {row['TotalQuantity']:,.0f}")
        print(f"  Avg Quantity per Transaction: {row['AvgQuantity']:.2f}")
        print(f"  Unique Customers: {row['UniqueCustomers']:,}")
    
    # Calculate lift
    if len(discount_comparison) == 2:
        with_discount = discount_comparison[discount_comparison['HasDiscount'] == True].iloc[0]
        without_discount = discount_comparison[discount_comparison['HasDiscount'] == False].iloc[0]
        
        quantity_lift = ((with_discount['AvgQuantity'] - without_discount['AvgQuantity']) / 
                        without_discount['AvgQuantity'] * 100)
        
        print(f"\nPromotion Lift Metrics:")
        print(f"  Average Quantity Lift: {quantity_lift:+.1f}%")
    
    # 2. Discount Level Analysis
    print("\n2. DISCOUNT LEVEL ANALYSIS")
    print("-" * 60)
    
    # Filter only discounted transactions
    discounted_df = df[df['HasDiscount']].copy()
    
    if len(discounted_df) > 0:
        # Create discount ranges
        discounted_df['DiscountRange'] = pd.cut(
            discounted_df['Discount'], 
            bins=[0, 10, 20, 30, 50, 100],
            labels=['1-10%', '11-20%', '21-30%', '31-50%', '51-100%']
        )
        
        discount_level_metrics = discounted_df.groupby('DiscountRange', observed=True).agg({
            'TransactionID': 'count',
            'TotalAmount': ['sum', 'mean'],
            'Quantity': ['sum', 'mean']
        }).reset_index()
        
        discount_level_metrics.columns = ['DiscountRange', 'TransactionCount', 'TotalRevenue', 
                                          'AvgTransactionValue', 'TotalQuantity', 'AvgQuantity']
        
        print("\nSales by Discount Level:")
        for idx, row in discount_level_metrics.iterrows():
            print(f"\n{row['DiscountRange']} Discount:")
            print(f"  Transactions: {row['TransactionCount']:,}")
            print(f"  Total Revenue: ${row['TotalRevenue']:,.2f}")
            print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
            print(f"  Avg Quantity: {row['AvgQuantity']:.2f}")
    else:
        discount_level_metrics = pd.DataFrame()
        print("  No discounted transactions found.")
    
    # 3. Calculate Promotion ROI
    print("\n3. PROMOTION ROI ANALYSIS")
    print("-" * 60)
    
    if len(discounted_df) > 0:
        # Calculate discount amount (assuming TotalAmount is after discount)
        # Discount amount = TotalAmount * (Discount / (100 - Discount))
        discounted_df['DiscountAmount'] = discounted_df['TotalAmount'] * (
            discounted_df['Discount'] / (100 - discounted_df['Discount'])
        )
        
        total_discount_given = discounted_df['DiscountAmount'].sum()
        revenue_from_discounts = discounted_df['TotalAmount'].sum()
        
        # Simple ROI calculation
        promotion_roi = ((revenue_from_discounts - total_discount_given) / total_discount_given) * 100
        
        print(f"  Total Discount Amount Given: ${total_discount_given:,.2f}")
        print(f"  Revenue from Discounted Transactions: ${revenue_from_discounts:,.2f}")
        print(f"  Promotion ROI: {promotion_roi:.1f}%")
        
        # Average discount percentage
        avg_discount_pct = discounted_df['Discount'].mean()
        print(f"  Average Discount Percentage: {avg_discount_pct:.1f}%")
    else:
        promotion_roi = 0
        total_discount_given = 0
    
    # 4. Products that benefit most from discounts
    print("\n4. TOP PRODUCTS WITH DISCOUNTS")
    print("-" * 60)
    
    if len(discounted_df) > 0:
        product_discount_analysis = discounted_df.groupby(['ProductID', 'ProductName']).agg({
            'TransactionID': 'count',
            'TotalAmount': 'sum',
            'Quantity': 'sum',
            'Discount': 'mean'
        }).sort_values('TotalAmount', ascending=False).head(10)
        
        product_discount_analysis.columns = ['TransactionCount', 'TotalRevenue', 
                                             'TotalQuantity', 'AvgDiscount']
        
        print("\nTop 10 Products by Revenue (with discounts):")
        rank = 1
        for (prod_id, prod_name), row in product_discount_analysis.iterrows():
            print(f"\n{rank}. {prod_name}")
            print(f"   Revenue: ${row['TotalRevenue']:,.2f}")
            print(f"   Quantity Sold: {row['TotalQuantity']:.0f}")
            print(f"   Transactions: {row['TransactionCount']:,}")
            print(f"   Avg Discount: {row['AvgDiscount']:.1f}%")
            rank += 1
    else:
        product_discount_analysis = pd.DataFrame()
        print("  No discounted products found.")
    
    print("\n" + "="*60)
    
    return {
        'discount_comparison': discount_comparison,
        'discount_level_metrics': discount_level_metrics,
        'promotion_roi': promotion_roi,
        'total_discount_given': total_discount_given,
        'top_discounted_products': product_discount_analysis,
    }



def seasonal_trends_analysis(df: pd.DataFrame) -> Dict:
    """
    Identify seasonal patterns and trends.
    
    Args:
        df: Transaction DataFrame (must have date features extracted)
        
    Returns:
        Dictionary containing:
        - monthly_trends: Sales trends by month
        - quarterly_trends: Sales trends by quarter
        - day_of_week_patterns: Patterns by day of week
        - seasonal_product_preferences: Popular products by season
        - year_over_year: Year-over-year comparison if applicable
    """
    print("\n" + "="*60)
    print("SEASONAL TRENDS ANALYSIS")
    print("="*60)
    
    # Ensure date features exist
    required_cols = ['Year', 'Month', 'Quarter', 'DayOfWeek']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required date features: {missing_cols}. Run extract_date_features() first.")
    
    # 1. Monthly Trends
    print("\n1. MONTHLY TRENDS")
    print("-" * 60)
    
    monthly_trends = df.groupby('Month').agg({
        'TransactionID': 'count',
        'TotalAmount': ['sum', 'mean'],
        'Quantity': 'sum',
        'CustomerID': 'nunique'
    }).reset_index()
    
    monthly_trends.columns = ['Month', 'TransactionCount', 'TotalRevenue', 
                              'AvgTransactionValue', 'TotalQuantity', 'UniqueCustomers']
    
    # Add month names
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 
                   5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    monthly_trends['MonthName'] = monthly_trends['Month'].map(month_names)
    
    print("\nSales by Month:")
    for idx, row in monthly_trends.iterrows():
        print(f"\n{row['MonthName']}:")
        print(f"  Transactions: {row['TransactionCount']:,}")
        print(f"  Revenue: ${row['TotalRevenue']:,.2f}")
        print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
        print(f"  Unique Customers: {row['UniqueCustomers']:,}")
    
    # Identify peak month
    peak_month = monthly_trends.loc[monthly_trends['TotalRevenue'].idxmax()]
    print(f"\nPeak Month: {peak_month['MonthName']} (${peak_month['TotalRevenue']:,.2f})")
    
    # 2. Quarterly Trends
    print("\n2. QUARTERLY TRENDS")
    print("-" * 60)
    
    quarterly_trends = df.groupby('Quarter').agg({
        'TransactionID': 'count',
        'TotalAmount': ['sum', 'mean'],
        'Quantity': 'sum',
        'CustomerID': 'nunique'
    }).reset_index()
    
    quarterly_trends.columns = ['Quarter', 'TransactionCount', 'TotalRevenue', 
                                'AvgTransactionValue', 'TotalQuantity', 'UniqueCustomers']
    
    print("\nSales by Quarter:")
    for idx, row in quarterly_trends.iterrows():
        print(f"\nQ{row['Quarter']}:")
        print(f"  Transactions: {row['TransactionCount']:,}")
        print(f"  Revenue: ${row['TotalRevenue']:,.2f}")
        print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
        print(f"  Unique Customers: {row['UniqueCustomers']:,}")
    
    # 3. Day of Week Patterns
    print("\n3. DAY OF WEEK PATTERNS")
    print("-" * 60)
    
    # Define day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    dow_trends = df.groupby('DayOfWeek').agg({
        'TransactionID': 'count',
        'TotalAmount': ['sum', 'mean'],
        'Quantity': 'sum'
    }).reset_index()
    
    dow_trends.columns = ['DayOfWeek', 'TransactionCount', 'TotalRevenue', 
                          'AvgTransactionValue', 'TotalQuantity']
    
    # Sort by day order
    dow_trends['DayOrder'] = dow_trends['DayOfWeek'].apply(
        lambda x: day_order.index(x) if x in day_order else 999
    )
    dow_trends = dow_trends.sort_values('DayOrder').drop('DayOrder', axis=1)
    
    print("\nSales by Day of Week:")
    for idx, row in dow_trends.iterrows():
        print(f"\n{row['DayOfWeek']}:")
        print(f"  Transactions: {row['TransactionCount']:,}")
        print(f"  Revenue: ${row['TotalRevenue']:,.2f}")
        print(f"  Avg Transaction Value: ${row['AvgTransactionValue']:.2f}")
    
    # Identify busiest day
    busiest_day = dow_trends.loc[dow_trends['TransactionCount'].idxmax()]
    print(f"\nBusiest Day: {busiest_day['DayOfWeek']} ({busiest_day['TransactionCount']:,} transactions)")
    
    # 4. Seasonal Product Preferences
    print("\n4. SEASONAL PRODUCT PREFERENCES")
    print("-" * 60)
    
    # Define seasons based on quarters
    season_map = {1: 'Winter (Q1)', 2: 'Spring (Q2)', 3: 'Summer (Q3)', 4: 'Fall (Q4)'}
    df['Season'] = df['Quarter'].map(season_map)
    
    seasonal_products = {}
    
    for season in season_map.values():
        season_data = df[df['Season'] == season]
        
        if len(season_data) == 0:
            continue
        
        top_products = season_data.groupby(['ProductName', 'Category']).agg({
            'TotalAmount': 'sum',
            'Quantity': 'sum'
        }).sort_values('TotalAmount', ascending=False).head(5)
        
        print(f"\n{season} - Top 5 Products:")
        rank = 1
        for (prod_name, category), row in top_products.iterrows():
            print(f"  {rank}. {prod_name} ({category}): ${row['TotalAmount']:,.2f}")
            rank += 1
        
        seasonal_products[season] = top_products
    
    # 5. Year-over-Year Trends (if multiple years exist)
    print("\n5. YEAR-OVER-YEAR TRENDS")
    print("-" * 60)
    
    unique_years = sorted(df['Year'].unique())
    
    if len(unique_years) > 1:
        yoy_trends = df.groupby('Year').agg({
            'TransactionID': 'count',
            'TotalAmount': 'sum',
            'CustomerID': 'nunique'
        }).reset_index()
        
        yoy_trends.columns = ['Year', 'TransactionCount', 'TotalRevenue', 'UniqueCustomers']
        
        print("\nYear-over-Year Comparison:")
        for idx, row in yoy_trends.iterrows():
            print(f"\n{int(row['Year'])}:")
            print(f"  Transactions: {row['TransactionCount']:,}")
            print(f"  Revenue: ${row['TotalRevenue']:,.2f}")
            print(f"  Unique Customers: {row['UniqueCustomers']:,}")
        
        # Calculate growth rates
        if len(yoy_trends) >= 2:
            print("\nGrowth Rates:")
            for i in range(1, len(yoy_trends)):
                prev_year = yoy_trends.iloc[i-1]
                curr_year = yoy_trends.iloc[i]
                
                revenue_growth = ((curr_year['TotalRevenue'] - prev_year['TotalRevenue']) / 
                                 prev_year['TotalRevenue'] * 100)
                transaction_growth = ((curr_year['TransactionCount'] - prev_year['TransactionCount']) / 
                                     prev_year['TransactionCount'] * 100)
                
                print(f"  {int(prev_year['Year'])} → {int(curr_year['Year'])}:")
                print(f"    Revenue Growth: {revenue_growth:+.1f}%")
                print(f"    Transaction Growth: {transaction_growth:+.1f}%")
    else:
        yoy_trends = pd.DataFrame()
        print(f"  Only one year of data available ({unique_years[0]}). Year-over-year comparison not applicable.")
    
    print("\n" + "="*60)
    
    return {
        'monthly_trends': monthly_trends,
        'quarterly_trends': quarterly_trends,
        'day_of_week_patterns': dow_trends,
        'seasonal_products': seasonal_products,
        'year_over_year': yoy_trends,
    }
