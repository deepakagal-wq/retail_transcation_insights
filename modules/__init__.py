"""
Retail Transaction Analysis Modules

This package provides comprehensive tools for analyzing retail transaction data:
- data_processor: Data loading, cleaning, and preprocessing
- analysis: Statistical analysis and insights generation
- visualizations: Professional charts and visualizations
"""

from .data_processor import (
    load_data,
    clean_data,
    extract_date_features,
    handle_missing_values,
    detect_outliers
)

from .analysis import (
    descriptive_statistics,
    top_products_analysis,
    top_cities_analysis,
    customer_spending_analysis,
    store_type_preference_analysis,
    product_preference_by_segment,
    promotion_effectiveness_analysis,
    seasonal_trends_analysis
)

from .visualizations import (
    setup_plot_style,
    plot_top_products,
    plot_top_cities,
    plot_customer_segments,
    plot_spending_distribution,
    plot_store_type_comparison,
    plot_discount_analysis,
    plot_discount_vs_sales,
    plot_sales_trends,
    plot_seasonal_heatmap,
    plot_day_of_week_patterns
)

__version__ = '1.0.0'

__all__ = [
    # Data processing functions
    'load_data',
    'clean_data',
    'extract_date_features',
    'handle_missing_values',
    'detect_outliers',
    # Analysis functions
    'descriptive_statistics',
    'top_products_analysis',
    'top_cities_analysis',
    'customer_spending_analysis',
    'store_type_preference_analysis',
    'product_preference_by_segment',
    'promotion_effectiveness_analysis',
    'seasonal_trends_analysis',
    # Visualization functions
    'setup_plot_style',
    'plot_top_products',
    'plot_top_cities',
    'plot_customer_segments',
    'plot_spending_distribution',
    'plot_store_type_comparison',
    'plot_discount_analysis',
    'plot_discount_vs_sales',
    'plot_sales_trends',
    'plot_seasonal_heatmap',
    'plot_day_of_week_patterns',
]
