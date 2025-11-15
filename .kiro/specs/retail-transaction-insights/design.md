# Design Document

## Overview

This design outlines a Python-based retail transaction analysis system that processes large CSV datasets to extract business insights. The solution uses pandas for data manipulation, matplotlib/seaborn for visualizations, and follows a modular architecture with separate modules for data loading, analysis, visualization, and reporting.

The system will be implemented as a Jupyter notebook for interactive analysis and easy PDF export, with supporting Python modules for reusable functions.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Main Analysis Notebook                 │
│                  (retail_analysis.ipynb)                 │
└─────────────────────────────────────────────────────────┘
                            │
                            ├─────────────────────────────┐
                            │                             │
                            ▼                             ▼
┌──────────────────────────────────┐    ┌──────────────────────────────┐
│     Data Processing Module        │    │    Visualization Module       │
│    (data_processor.py)            │    │    (visualizations.py)        │
│                                   │    │                               │
│  - load_data()                    │    │  - plot_top_products()        │
│  - clean_data()                   │    │  - plot_sales_trends()        │
│  - extract_date_features()        │    │  - plot_customer_segments()   │
│  - handle_missing_values()        │    │  - plot_discount_analysis()   │
└──────────────────────────────────┘    └──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────┐
│      Analysis Module              │
│    (analysis.py)                  │
│                                   │
│  - descriptive_stats()            │
│  - customer_analysis()            │
│  - promotion_analysis()           │
│  - seasonal_analysis()            │
└──────────────────────────────────┘
```

### Technology Stack

- **Python 3.8+**: Core programming language
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Basic plotting
- **seaborn**: Statistical visualizations
- **jupyter notebook**: Interactive analysis environment
- **nbconvert**: PDF export functionality

## Components and Interfaces

### 1. Data Processing Module (`data_processor.py`)

**Purpose**: Handle all data loading, cleaning, and preprocessing operations.

**Key Functions**:

```python
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data with appropriate dtypes and error handling.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with loaded data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.ParserError: If CSV is malformed
    """
    pass

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data by handling missing values, duplicates, and outliers.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame with quality report printed
    """
    pass

def extract_date_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Extract temporal features from date column.
    
    Args:
        df: DataFrame with date column
        date_column: Name of the date column
        
    Returns:
        DataFrame with additional date features (year, month, day, day_of_week, quarter)
    """
    pass

def handle_missing_values(df: pd.DataFrame, strategy: dict) -> pd.DataFrame:
    """
    Handle missing values based on column-specific strategies.
    
    Args:
        df: DataFrame with missing values
        strategy: Dict mapping column names to strategies ('drop', 'mean', 'median', 'mode', 'ffill')
        
    Returns:
        DataFrame with missing values handled
    """
    pass
```

### 2. Analysis Module (`analysis.py`)

**Purpose**: Perform all analytical computations and generate insights.

**Key Functions**:

```python
def descriptive_statistics(df: pd.DataFrame) -> dict:
    """
    Generate comprehensive descriptive statistics.
    
    Returns:
        Dictionary containing summary statistics for numerical and categorical columns
    """
    pass

def top_products_analysis(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identify top products by sales volume and revenue.
    
    Args:
        df: Transaction DataFrame
        top_n: Number of top products to return
        
    Returns:
        DataFrame with top products ranked by multiple metrics
    """
    pass

def top_cities_analysis(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identify top cities by transaction volume and revenue.
    
    Args:
        df: Transaction DataFrame
        top_n: Number of top cities to return
        
    Returns:
        DataFrame with top cities ranked by multiple metrics
    """
    pass

def customer_spending_analysis(df: pd.DataFrame) -> dict:
    """
    Analyze customer spending patterns and segmentation.
    
    Returns:
        Dictionary containing:
        - avg_transaction_value
        - customer_segments (high/medium/low value)
        - spending_distribution
        - repeat_purchase_rate
    """
    pass

def store_type_preference_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze customer preferences across store types.
    
    Returns:
        DataFrame with metrics by store type
    """
    pass

def promotion_effectiveness_analysis(df: pd.DataFrame) -> dict:
    """
    Evaluate promotion and discount effectiveness.
    
    Returns:
        Dictionary containing:
        - discount_vs_non_discount_metrics
        - promotion_roi
        - optimal_discount_levels
    """
    pass

def seasonal_trends_analysis(df: pd.DataFrame) -> dict:
    """
    Identify seasonal patterns and trends.
    
    Returns:
        Dictionary containing:
        - monthly_trends
        - quarterly_trends
        - day_of_week_patterns
        - seasonal_product_preferences
    """
    pass
```

### 3. Visualization Module (`visualizations.py`)

**Purpose**: Create all charts and visualizations with consistent styling.

**Key Functions**:

```python
def setup_plot_style():
    """Configure matplotlib/seaborn style for consistent, professional plots."""
    pass

def plot_top_products(data: pd.DataFrame, metric: str = 'revenue', top_n: int = 10):
    """Create horizontal bar chart for top products."""
    pass

def plot_sales_trends(df: pd.DataFrame, time_period: str = 'monthly'):
    """Create line chart showing sales trends over time."""
    pass

def plot_customer_segments(segments_data: dict):
    """Create pie chart or bar chart showing customer segmentation."""
    pass

def plot_discount_analysis(discount_data: dict):
    """Create comparison charts for discount vs non-discount transactions."""
    pass

def plot_seasonal_heatmap(df: pd.DataFrame):
    """Create heatmap showing sales patterns by month and day of week."""
    pass

def plot_store_type_comparison(store_data: pd.DataFrame):
    """Create grouped bar chart comparing metrics across store types."""
    pass
```

### 4. Main Analysis Notebook (`retail_analysis.ipynb`)

**Structure**:

1. **Setup and Imports**
   - Import all required libraries
   - Set configuration parameters
   - Define file paths

2. **Data Loading and Preparation** (Requirement 1)
   - Load dataset
   - Display data info and sample
   - Clean data
   - Extract date features
   - Show data quality report

3. **Exploratory Data Analysis** (Requirement 2)
   - Descriptive statistics
   - Top products analysis with visualization
   - Top cities analysis with visualization
   - Category and store type distribution

4. **Customer Insights** (Requirement 3)
   - Spending pattern analysis
   - Customer segmentation
   - Store type preferences
   - Purchase frequency analysis
   - Visualizations for each insight

5. **Promotion Analysis** (Requirement 4)
   - Discount vs non-discount comparison
   - Promotion effectiveness metrics
   - Discount level optimization
   - Visualizations showing promotion impact

6. **Seasonal Analysis** (Requirement 5)
   - Monthly and quarterly trends
   - Day of week patterns
   - Seasonal product preferences
   - Heatmaps and trend visualizations

7. **Summary and Recommendations** (Requirement 8)
   - Key findings summary
   - Actionable recommendations
   - Assumptions and limitations
   - Design choices documentation

## Data Models

### Input Data Schema (Expected CSV Structure)

```python
{
    'TransactionID': 'object',          # Unique transaction identifier
    'Date': 'datetime64[ns]',           # Transaction date
    'CustomerID': 'object',             # Customer identifier
    'ProductID': 'object',              # Product identifier
    'ProductName': 'object',            # Product name
    'Category': 'object',               # Product category
    'Quantity': 'int64',                # Quantity purchased
    'Price': 'float64',                 # Unit price
    'TotalAmount': 'float64',           # Total transaction amount
    'Discount': 'float64',              # Discount percentage (0-100)
    'StoreType': 'object',              # Type of store
    'City': 'object',                   # City location
    'PaymentMethod': 'object',          # Payment method used
}
```

### Derived Features

```python
{
    'Year': 'int64',                    # Extracted from Date
    'Month': 'int64',                   # Extracted from Date
    'Day': 'int64',                     # Extracted from Date
    'DayOfWeek': 'object',              # Extracted from Date (Monday, Tuesday, etc.)
    'Quarter': 'int64',                 # Extracted from Date (1-4)
    'HasDiscount': 'bool',              # True if Discount > 0
    'DiscountAmount': 'float64',        # Calculated discount amount
    'NetAmount': 'float64',             # Amount after discount
}
```

### Analysis Output Models

**Customer Segment Model**:
```python
{
    'segment': str,                     # 'High', 'Medium', 'Low'
    'customer_count': int,
    'avg_transaction_value': float,
    'total_revenue': float,
    'transaction_count': int,
}
```

**Product Performance Model**:
```python
{
    'product_id': str,
    'product_name': str,
    'total_quantity': int,
    'total_revenue': float,
    'avg_price': float,
    'transaction_count': int,
}
```

## Error Handling

### Data Loading Errors
- **FileNotFoundError**: Provide clear message with expected file location
- **ParserError**: Log problematic rows and attempt to continue with valid data
- **MemoryError**: Implement chunked reading for large files

### Data Quality Issues
- **Missing Values**: Log percentage of missing values per column, apply appropriate strategy
- **Outliers**: Flag but don't automatically remove; document in report
- **Invalid Data Types**: Attempt conversion, log failures, handle gracefully

### Visualization Errors
- **Empty Data**: Check for empty DataFrames before plotting, show warning message
- **Invalid Parameters**: Validate inputs before creating plots
- **Memory Issues**: Limit data points in plots if necessary

### General Error Handling Pattern
```python
try:
    # Operation
    result = perform_analysis(data)
except SpecificError as e:
    logger.error(f"Error in analysis: {e}")
    # Provide fallback or skip gracefully
    result = None
finally:
    # Cleanup if needed
    pass
```

## Testing Strategy

### Unit Testing Approach

**Data Processing Tests**:
- Test `load_data()` with valid and invalid file paths
- Test `clean_data()` with datasets containing various data quality issues
- Test `extract_date_features()` with different date formats
- Test `handle_missing_values()` with different strategies

**Analysis Tests**:
- Test each analysis function with sample datasets
- Verify calculations are mathematically correct
- Test edge cases (empty data, single row, all nulls)
- Validate output data structures

**Visualization Tests**:
- Test that plots are generated without errors
- Verify plots contain expected elements (title, labels, legend)
- Test with edge cases (empty data, single data point)

### Integration Testing

- Test complete workflow from data loading to report generation
- Verify all modules work together correctly
- Test with sample dataset that mimics production data structure

### Data Validation Tests

- Verify data types after loading
- Check for expected columns
- Validate date ranges are reasonable
- Ensure numerical values are within expected ranges

### Test Data

Create small sample CSV files for testing:
- `test_data_valid.csv`: Clean, well-formed data
- `test_data_missing.csv`: Data with missing values
- `test_data_outliers.csv`: Data with outliers
- `test_data_duplicates.csv`: Data with duplicate records

## Performance Considerations

### Memory Optimization
- Use `dtype` specification when loading CSV to reduce memory footprint
- Use categorical dtype for columns with limited unique values
- Consider chunked processing for very large files (>1GB)

### Computation Optimization
- Use vectorized pandas operations instead of loops
- Cache intermediate results that are reused
- Use `groupby` efficiently with appropriate aggregation functions

### Visualization Optimization
- Limit data points in scatter plots (sample if necessary)
- Use appropriate figure sizes to balance quality and memory
- Close figures after saving to free memory

## Assumptions and Design Decisions

### Assumptions
1. CSV file follows expected schema (columns may vary but core fields exist)
2. Date column is parseable to datetime format
3. Numerical columns (Price, Quantity, TotalAmount) contain valid numbers
4. CustomerID and ProductID are consistent identifiers
5. Discount is represented as percentage (0-100) or amount
6. Dataset fits in memory (or can be processed in chunks)

### Design Decisions

**Why Jupyter Notebook?**
- Interactive analysis allows for exploration and iteration
- Easy to export to PDF for submission
- Combines code, visualizations, and narrative in one document
- Familiar to data analysts and reviewers

**Why Modular Functions?**
- Reusability across different analyses
- Easier to test individual components
- Better code organization and maintainability
- Follows DRY (Don't Repeat Yourself) principle

**Why pandas over other tools?**
- Industry standard for data analysis in Python
- Rich functionality for data manipulation
- Excellent integration with visualization libraries
- Good performance for datasets up to several GB

**Visualization Library Choice**:
- matplotlib for basic plots and fine control
- seaborn for statistical visualizations and better aesthetics
- Both are well-documented and widely used

**Customer Segmentation Approach**:
- Use RFM-like analysis (Recency, Frequency, Monetary) if data supports it
- Otherwise, use quantile-based segmentation on total spending
- Three segments (High, Medium, Low) for simplicity

**Promotion Effectiveness Metrics**:
- Compare average transaction value with/without discount
- Calculate lift in sales volume during promotional periods
- Analyze discount percentage vs sales volume relationship

## Deliverables

1. **Python Modules**:
   - `data_processor.py`
   - `analysis.py`
   - `visualizations.py`

2. **Jupyter Notebook**:
   - `retail_analysis.ipynb` with complete analysis

3. **PDF Report**:
   - Generated from notebook using nbconvert
   - Well-structured with clear sections
   - All visualizations included
   - Summary and recommendations

4. **Documentation**:
   - README.md with setup instructions
   - Requirements.txt with dependencies
   - Assumptions and design choices documented in notebook
