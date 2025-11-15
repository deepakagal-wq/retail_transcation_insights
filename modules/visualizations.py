"""
Visualization module for retail transaction analysis.
Provides functions to create professional, consistent charts and plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Union
import warnings


def _validate_dataframe(df: pd.DataFrame, required_columns: list = None, 
                       function_name: str = "function") -> bool:
    """
    Validate DataFrame input for visualization functions.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        function_name: Name of calling function for error messages
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        ValueError: If validation fails with specific error message
    """
    if df is None:
        raise ValueError(f"{function_name}: DataFrame cannot be None")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"{function_name}: Expected pandas DataFrame, got {type(df)}")
    
    if df.empty:
        warnings.warn(f"{function_name}: Empty DataFrame provided. No plot will be generated.")
        return False
    
    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"{function_name}: Missing required columns: {missing_cols}")
    
    return True


def _validate_save_path(save_path: Optional[str], function_name: str = "function") -> None:
    """
    Validate save path for figure export.
    
    Args:
        save_path: Path to save figure
        function_name: Name of calling function for error messages
        
    Raises:
        ValueError: If save path is invalid
    """
    if save_path is not None:
        if not isinstance(save_path, str):
            raise TypeError(f"{function_name}: save_path must be a string")
        
        # Check for valid file extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf', '.svg']
        if not any(save_path.lower().endswith(ext) for ext in valid_extensions):
            warnings.warn(f"{function_name}: save_path should have a valid image extension "
                        f"({', '.join(valid_extensions)}). Using default format.")


def _safe_save_figure(fig, save_path: str, function_name: str = "function") -> None:
    """
    Safely save figure with error handling.
    
    Args:
        fig: Matplotlib figure object
        save_path: Path to save figure
        function_name: Name of calling function for error messages
    """
    try:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved successfully to: {save_path}")
    except Exception as e:
        warnings.warn(f"{function_name}: Failed to save figure to {save_path}. Error: {str(e)}")


def setup_plot_style():
    """
    Configure matplotlib/seaborn style for consistent, professional appearance.
    
    Sets up:
    - Color palette
    - Figure sizes
    - Font sizes
    - Grid and axis styling
    """
    # Set seaborn style
    sns.set_style("whitegrid")
    
    # Set color palette - professional and accessible
    sns.set_palette("husl")
    
    # Configure matplotlib parameters
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300  # High resolution for exports
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 16
    
    # Grid styling
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    
    # Axis styling
    plt.rcParams['axes.grid'] = True
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False



def plot_top_products(data: pd.DataFrame, metric: str = 'revenue', top_n: int = 10, 
                      figsize: tuple = (12, 8), save_path: Optional[str] = None):
    """
    Create horizontal bar chart for top products.
    
    Args:
        data: DataFrame with product data (must have 'ProductName' and metric column)
        metric: Column name to rank by (e.g., 'revenue', 'quantity', 'transaction_count')
        top_n: Number of top products to display
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate inputs
        if not _validate_dataframe(data, ['ProductName', metric], 'plot_top_products'):
            return None
        
        _validate_save_path(save_path, 'plot_top_products')
        
        # Validate top_n parameter
        if not isinstance(top_n, int) or top_n <= 0:
            raise ValueError(f"top_n must be a positive integer, got {top_n}")
        
        # Get top N products
        top_data = data.nlargest(min(top_n, len(data)), metric)
        
        if top_data.empty:
            warnings.warn("No data available after filtering")
            return None
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create horizontal bar chart
        bars = ax.barh(range(len(top_data)), top_data[metric], 
                      color=sns.color_palette("viridis", len(top_data)))
        
        # Set labels
        ax.set_yticks(range(len(top_data)))
        ax.set_yticklabels(top_data['ProductName'])
        ax.set_xlabel(metric.replace('_', ' ').title())
        ax.set_ylabel('Product')
        ax.set_title(f'Top {len(top_data)} Products by {metric.replace("_", " ").title()}')
        
        # Add value labels on bars
        for i, (idx, row) in enumerate(top_data.iterrows()):
            ax.text(row[metric], i, f' {row[metric]:,.0f}', va='center', fontsize=9)
        
        # Invert y-axis so highest value is on top
        ax.invert_yaxis()
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_top_products')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_top_products: {str(e)}")
        return None


def plot_top_cities(data: pd.DataFrame, metric: str = 'revenue', top_n: int = 10,
                    figsize: tuple = (12, 6), save_path: Optional[str] = None):
    """
    Create bar chart for top cities.
    
    Args:
        data: DataFrame with city data (must have 'City' and metric column)
        metric: Column name to rank by (e.g., 'revenue', 'transaction_count')
        top_n: Number of top cities to display
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate inputs
        if not _validate_dataframe(data, ['City', metric], 'plot_top_cities'):
            return None
        
        _validate_save_path(save_path, 'plot_top_cities')
        
        # Validate top_n parameter
        if not isinstance(top_n, int) or top_n <= 0:
            raise ValueError(f"top_n must be a positive integer, got {top_n}")
        
        # Get top N cities
        top_data = data.nlargest(min(top_n, len(data)), metric)
        
        if top_data.empty:
            warnings.warn("No data available after filtering")
            return None
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create bar chart
        bars = ax.bar(range(len(top_data)), top_data[metric], 
                     color=sns.color_palette("mako", len(top_data)))
        
        # Set labels
        ax.set_xticks(range(len(top_data)))
        ax.set_xticklabels(top_data['City'], rotation=45, ha='right')
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.set_xlabel('City')
        ax.set_title(f'Top {len(top_data)} Cities by {metric.replace("_", " ").title()}')
        
        # Add value labels on bars
        for i, (idx, row) in enumerate(top_data.iterrows()):
            ax.text(i, row[metric], f'{row[metric]:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_top_cities')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_top_cities: {str(e)}")
        return None



def plot_customer_segments(segments_data: Union[pd.DataFrame, dict], 
                           figsize: tuple = (10, 6), save_path: Optional[str] = None):
    """
    Create pie or bar chart showing customer segmentation.
    
    Args:
        segments_data: DataFrame or dict with segment information
                      Expected columns/keys: 'segment', 'customer_count'
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Convert dict to DataFrame if needed
        if isinstance(segments_data, dict):
            if 'segments' in segments_data:
                df = pd.DataFrame(segments_data['segments'])
            else:
                df = pd.DataFrame([segments_data])
        else:
            df = segments_data
        
        # Validate DataFrame
        if not _validate_dataframe(df, ['segment', 'customer_count'], 'plot_customer_segments'):
            return None
        
        _validate_save_path(save_path, 'plot_customer_segments')
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Pie chart
        colors = sns.color_palette("pastel")
        ax1.pie(df['customer_count'], labels=df['segment'], autopct='%1.1f%%', 
                startangle=90, colors=colors)
        ax1.set_title('Customer Distribution by Segment')
        
        # Bar chart
        bars = ax2.bar(df['segment'], df['customer_count'], color=colors)
        ax2.set_xlabel('Segment')
        ax2.set_ylabel('Number of Customers')
        ax2.set_title('Customer Count by Segment')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_customer_segments')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_customer_segments: {str(e)}")
        return None


def plot_spending_distribution(spending_data: pd.Series, bins: int = 30,
                               figsize: tuple = (12, 6), save_path: Optional[str] = None):
    """
    Create histogram of customer spending distribution.
    
    Args:
        spending_data: Series with customer spending values
        bins: Number of bins for histogram
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate inputs
        if not isinstance(spending_data, pd.Series):
            raise TypeError(f"Expected pandas Series, got {type(spending_data)}")
        
        if spending_data.empty:
            warnings.warn("Empty Series provided to plot_spending_distribution")
            return None
        
        _validate_save_path(save_path, 'plot_spending_distribution')
        
        # Validate bins parameter
        if not isinstance(bins, int) or bins <= 0:
            raise ValueError(f"bins must be a positive integer, got {bins}")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create histogram
        n, bins_edges, patches = ax.hist(spending_data, bins=bins, color='skyblue', 
                                         edgecolor='black', alpha=0.7)
        
        # Add mean and median lines
        mean_val = spending_data.mean()
        median_val = spending_data.median()
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                  label=f'Mean: ${mean_val:,.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, 
                  label=f'Median: ${median_val:,.2f}')
        
        # Set labels
        ax.set_xlabel('Total Spending ($)')
        ax.set_ylabel('Number of Customers')
        ax.set_title('Customer Spending Distribution')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_spending_distribution')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_spending_distribution: {str(e)}")
        return None


def plot_store_type_comparison(store_data: pd.DataFrame, metrics: list = None,
                               figsize: tuple = (14, 6), save_path: Optional[str] = None):
    """
    Create grouped bar chart comparing metrics across store types.
    
    Args:
        store_data: DataFrame with store type data
                   Expected columns: 'StoreType' and metric columns
        metrics: List of metric column names to compare
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate DataFrame
        if not _validate_dataframe(store_data, ['StoreType'], 'plot_store_type_comparison'):
            return None
        
        _validate_save_path(save_path, 'plot_store_type_comparison')
        
        # Default metrics if not provided
        if metrics is None:
            metrics = [col for col in store_data.columns if col != 'StoreType']
        
        if not metrics:
            raise ValueError("No metrics available to plot")
        
        # Validate all metrics exist
        missing_metrics = [m for m in metrics if m not in store_data.columns]
        if missing_metrics:
            raise ValueError(f"Missing metric columns: {missing_metrics}")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set up bar positions
        x = np.arange(len(store_data))
        width = 0.8 / len(metrics)
        
        # Create bars for each metric
        for i, metric in enumerate(metrics):
            offset = width * i - (width * len(metrics) / 2) + width / 2
            bars = ax.bar(x + offset, store_data[metric], width, 
                         label=metric.replace('_', ' ').title())
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:,.0f}', ha='center', va='bottom', fontsize=8)
        
        # Set labels
        ax.set_xlabel('Store Type')
        ax.set_ylabel('Value')
        ax.set_title('Store Type Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(store_data['StoreType'])
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_store_type_comparison')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_store_type_comparison: {str(e)}")
        return None



def plot_discount_analysis(discount_data: dict, figsize: tuple = (14, 6), 
                           save_path: Optional[str] = None):
    """
    Create comparison charts for discount vs non-discount transactions.
    
    Args:
        discount_data: Dictionary with discount analysis results
                      Expected keys: 'with_discount', 'without_discount' with metrics
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate inputs
        if not discount_data or not isinstance(discount_data, dict):
            warnings.warn("Empty or invalid data provided to plot_discount_analysis")
            return None
        
        _validate_save_path(save_path, 'plot_discount_analysis')
        
        # Extract data
        with_disc = discount_data.get('with_discount', {})
        without_disc = discount_data.get('without_discount', {})
        
        if not with_disc and not without_disc:
            warnings.warn("No discount data available in the provided dictionary")
            return None
        
        # Metrics to compare
        metrics = ['transaction_count', 'total_revenue', 'avg_transaction_value']
        metric_labels = ['Transaction Count', 'Total Revenue ($)', 'Avg Transaction Value ($)']
        
        # Create figure with subplots
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            ax = axes[i]
            
            # Get values
            with_val = with_disc.get(metric, 0)
            without_val = without_disc.get(metric, 0)
            
            # Create bar chart
            bars = ax.bar(['With Discount', 'Without Discount'], 
                          [with_val, without_val],
                          color=['#FF6B6B', '#4ECDC4'])
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            ax.set_ylabel(label)
            ax.set_title(label)
        
        fig.suptitle('Discount vs Non-Discount Transaction Comparison', fontsize=16, y=1.02)
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_discount_analysis')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_discount_analysis: {str(e)}")
        return None


def plot_discount_vs_sales(df: pd.DataFrame, figsize: tuple = (12, 6),
                           save_path: Optional[str] = None):
    """
    Create scatter plot showing discount percentage vs sales volume with trend line.
    
    Args:
        df: DataFrame with 'Discount' and sales metric columns
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate DataFrame
        required_cols = ['Discount', 'Quantity', 'TotalAmount', 'TransactionID']
        if not _validate_dataframe(df, required_cols, 'plot_discount_vs_sales'):
            return None
        
        _validate_save_path(save_path, 'plot_discount_vs_sales')
        
        # Filter to only discounted transactions
        df_disc = df[df['Discount'] > 0].copy()
        
        if df_disc.empty:
            warnings.warn("No discounted transactions found in the data")
            return None
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Aggregate by discount level
        discount_agg = df_disc.groupby('Discount').agg({
            'Quantity': 'sum',
            'TotalAmount': 'sum',
            'TransactionID': 'count'
        }).reset_index()
        discount_agg.columns = ['Discount', 'TotalQuantity', 'TotalRevenue', 'TransactionCount']
        
        # Create scatter plot
        scatter = ax.scatter(discount_agg['Discount'], discount_agg['TotalQuantity'],
                            s=discount_agg['TransactionCount']*2, alpha=0.6,
                            c=discount_agg['TotalRevenue'], cmap='viridis')
        
        # Add trend line
        if len(discount_agg) > 1:
            z = np.polyfit(discount_agg['Discount'], discount_agg['TotalQuantity'], 1)
            p = np.poly1d(z)
            ax.plot(discount_agg['Discount'], p(discount_agg['Discount']), 
                   "r--", alpha=0.8, linewidth=2, label='Trend Line')
        
        # Set labels
        ax.set_xlabel('Discount Percentage (%)')
        ax.set_ylabel('Total Quantity Sold')
        ax.set_title('Discount Percentage vs Sales Volume')
        ax.legend()
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Total Revenue ($)')
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_discount_vs_sales')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_discount_vs_sales: {str(e)}")
        return None



def plot_sales_trends(df: pd.DataFrame, time_period: str = 'monthly',
                     figsize: tuple = (14, 6), save_path: Optional[str] = None):
    """
    Create line chart showing sales trends over time (monthly/quarterly).
    
    Args:
        df: DataFrame with date features and sales metrics
        time_period: 'monthly' or 'quarterly'
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate time_period parameter
        if time_period not in ['monthly', 'quarterly']:
            raise ValueError(f"time_period must be 'monthly' or 'quarterly', got '{time_period}'")
        
        # Validate DataFrame
        required_cols = ['TotalAmount', 'TransactionID']
        if not _validate_dataframe(df, required_cols, 'plot_sales_trends'):
            return None
        
        _validate_save_path(save_path, 'plot_sales_trends')
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
        
        if time_period == 'monthly':
            # Group by year and month
            if 'Year' not in df.columns or 'Month' not in df.columns:
                raise ValueError("Year and Month columns required for monthly trends")
            
            time_group = df.groupby(['Year', 'Month']).agg({
                'TotalAmount': 'sum',
                'TransactionID': 'count'
            }).reset_index()
            time_group['Period'] = time_group['Year'].astype(str) + '-' + time_group['Month'].astype(str).str.zfill(2)
        else:  # quarterly
            if 'Year' not in df.columns or 'Quarter' not in df.columns:
                raise ValueError("Year and Quarter columns required for quarterly trends")
            
            time_group = df.groupby(['Year', 'Quarter']).agg({
                'TotalAmount': 'sum',
                'TransactionID': 'count'
            }).reset_index()
            time_group['Period'] = time_group['Year'].astype(str) + '-Q' + time_group['Quarter'].astype(str)
        
        if time_group.empty:
            warnings.warn("No data available after grouping")
            return None
        
        # Plot revenue trend
        ax1.plot(range(len(time_group)), time_group['TotalAmount'], 
                marker='o', linewidth=2, markersize=6, color='#2E86AB')
        ax1.set_ylabel('Total Revenue ($)')
        ax1.set_title(f'{time_period.title()} Revenue Trend')
        ax1.set_xticks(range(len(time_group)))
        ax1.set_xticklabels(time_group['Period'], rotation=45, ha='right')
        ax1.grid(True, alpha=0.3)
        
        # Plot transaction count trend
        ax2.plot(range(len(time_group)), time_group['TransactionID'], 
                marker='s', linewidth=2, markersize=6, color='#A23B72')
        ax2.set_ylabel('Transaction Count')
        ax2.set_xlabel('Period')
        ax2.set_title(f'{time_period.title()} Transaction Count Trend')
        ax2.set_xticks(range(len(time_group)))
        ax2.set_xticklabels(time_group['Period'], rotation=45, ha='right')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_sales_trends')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_sales_trends: {str(e)}")
        return None


def plot_seasonal_heatmap(df: pd.DataFrame, figsize: tuple = (12, 8),
                          save_path: Optional[str] = None):
    """
    Create heatmap showing sales patterns by month and day of week.
    
    Args:
        df: DataFrame with 'Month', 'DayOfWeek', and sales metrics
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate DataFrame
        required_cols = ['Month', 'DayOfWeek', 'TotalAmount']
        if not _validate_dataframe(df, required_cols, 'plot_seasonal_heatmap'):
            return None
        
        _validate_save_path(save_path, 'plot_seasonal_heatmap')
        
        # Create pivot table
        heatmap_data = df.pivot_table(
            values='TotalAmount',
            index='DayOfWeek',
            columns='Month',
            aggfunc='sum',
            fill_value=0
        )
        
        if heatmap_data.empty:
            warnings.warn("No data available after pivot")
            return None
        
        # Reorder days of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex([day for day in day_order if day in heatmap_data.index])
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create heatmap
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Total Revenue ($)'}, ax=ax)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Day of Week')
        ax.set_title('Sales Heatmap: Revenue by Month and Day of Week')
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_seasonal_heatmap')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_seasonal_heatmap: {str(e)}")
        return None


def plot_day_of_week_patterns(df: pd.DataFrame, figsize: tuple = (12, 6),
                              save_path: Optional[str] = None):
    """
    Create bar chart of sales by day of week.
    
    Args:
        df: DataFrame with 'DayOfWeek' and sales metrics
        figsize: Figure size as (width, height)
        save_path: Optional path to save the figure
        
    Returns:
        matplotlib figure object or None if validation fails
    """
    try:
        # Validate DataFrame
        required_cols = ['DayOfWeek', 'TotalAmount', 'TransactionID', 'Quantity']
        if not _validate_dataframe(df, required_cols, 'plot_day_of_week_patterns'):
            return None
        
        _validate_save_path(save_path, 'plot_day_of_week_patterns')
        
        # Aggregate by day of week
        day_agg = df.groupby('DayOfWeek').agg({
            'TotalAmount': 'sum',
            'TransactionID': 'count',
            'Quantity': 'sum'
        }).reset_index()
        
        if day_agg.empty:
            warnings.warn("No data available after aggregation")
            return None
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_agg['DayOfWeek'] = pd.Categorical(day_agg['DayOfWeek'], categories=day_order, ordered=True)
        day_agg = day_agg.sort_values('DayOfWeek')
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Revenue by day
        bars1 = ax1.bar(day_agg['DayOfWeek'], day_agg['TotalAmount'], 
                       color=sns.color_palette("rocket", len(day_agg)))
        ax1.set_xlabel('Day of Week')
        ax1.set_ylabel('Total Revenue ($)')
        ax1.set_title('Revenue by Day of Week')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        # Transaction count by day
        bars2 = ax2.bar(day_agg['DayOfWeek'], day_agg['TransactionID'],
                       color=sns.color_palette("mako", len(day_agg)))
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Transaction Count')
        ax2.set_title('Transaction Count by Day of Week')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            _safe_save_figure(fig, save_path, 'plot_day_of_week_patterns')
        
        return fig
        
    except Exception as e:
        warnings.warn(f"Error in plot_day_of_week_patterns: {str(e)}")
        return None
