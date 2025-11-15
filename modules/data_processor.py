"""
Data Processing Module for Retail Transaction Analysis

This module handles data loading, cleaning, and preprocessing operations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
import warnings


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
    try:
        # Define dtype specifications for memory optimization
        dtype_spec = {
            'TransactionID': 'object',
            'CustomerID': 'object',
            'ProductID': 'object',
            'ProductName': 'object',
            'Category': 'object',
            'Quantity': 'int64',
            'Price': 'float64',
            'TotalAmount': 'float64',
            'Discount': 'float64',
            'StoreType': 'object',
            'City': 'object',
            'PaymentMethod': 'object',
        }
        
        # Load the CSV file
        print(f"Loading data from {file_path}...")
        df = pd.read_csv(file_path, dtype=dtype_spec, parse_dates=['Date'])
        
        print(f"\n✓ Data loaded successfully!")
        print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Display basic info
        print("\n" + "="*60)
        print("DATA PREVIEW")
        print("="*60)
        print(df.head())
        
        print("\n" + "="*60)
        print("DATA INFO")
        print("="*60)
        print(f"\nColumn Data Types:")
        print(df.dtypes)
        
        print(f"\nBasic Statistics:")
        print(df.describe())
        
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: The file '{file_path}' was not found. "
            f"Please check the file path and try again."
        )
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(
            f"Error parsing CSV file: {e}. "
            f"Please check that the file is properly formatted."
        )
    except Exception as e:
        raise Exception(f"Unexpected error loading data: {e}")



def extract_date_features(df: pd.DataFrame, date_column: str = 'Date') -> pd.DataFrame:
    """
    Extract temporal features from date column.
    
    Args:
        df: DataFrame with date column
        date_column: Name of the date column (default: 'Date')
        
    Returns:
        DataFrame with additional date features (Year, Month, Day, DayOfWeek, Quarter)
    """
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Check if date column exists
    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")
    
    # Convert to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        print(f"Converting '{date_column}' to datetime format...")
        try:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        except Exception as e:
            raise ValueError(f"Error parsing dates: {e}")
    
    # Check for invalid dates
    invalid_dates = df[date_column].isna().sum()
    if invalid_dates > 0:
        warnings.warn(f"Found {invalid_dates} invalid dates that were converted to NaT")
    
    # Extract date features
    print(f"\nExtracting date features from '{date_column}'...")
    df['Year'] = df[date_column].dt.year
    df['Month'] = df[date_column].dt.month
    df['Day'] = df[date_column].dt.day
    df['DayOfWeek'] = df[date_column].dt.day_name()
    df['Quarter'] = df[date_column].dt.quarter
    
    # Validate date ranges
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    
    print(f"✓ Date features extracted successfully!")
    print(f"  Date range: {min_date.date()} to {max_date.date()}")
    print(f"  Years covered: {sorted(df['Year'].dropna().unique().astype(int).tolist())}")
    print(f"  New columns added: Year, Month, Day, DayOfWeek, Quarter")
    
    return df



def handle_missing_values(df: pd.DataFrame, strategy: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Handle missing values based on column-specific strategies.
    
    Args:
        df: DataFrame with missing values
        strategy: Dict mapping column names to strategies 
                 ('drop', 'mean', 'median', 'mode', 'ffill')
                 If None, uses default strategies based on data type
        
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    
    if strategy is None:
        # Default strategies based on data type
        strategy = {}
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    strategy[col] = 'median'
                else:
                    strategy[col] = 'mode'
    
    print("\nHandling missing values...")
    for col, method in strategy.items():
        if col not in df.columns:
            continue
            
        missing_count = df[col].isna().sum()
        if missing_count == 0:
            continue
        
        if method == 'drop':
            df = df.dropna(subset=[col])
            print(f"  {col}: Dropped {missing_count} rows")
        elif method == 'mean':
            fill_value = df[col].mean()
            df[col].fillna(fill_value, inplace=True)
            print(f"  {col}: Filled {missing_count} values with mean ({fill_value:.2f})")
        elif method == 'median':
            fill_value = df[col].median()
            df[col].fillna(fill_value, inplace=True)
            print(f"  {col}: Filled {missing_count} values with median ({fill_value:.2f})")
        elif method == 'mode':
            fill_value = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
            df[col].fillna(fill_value, inplace=True)
            print(f"  {col}: Filled {missing_count} values with mode ({fill_value})")
        elif method == 'ffill':
            df[col].fillna(method='ffill', inplace=True)
            print(f"  {col}: Forward filled {missing_count} values")
    
    return df


def detect_outliers(df: pd.DataFrame, columns: Optional[list] = None, method: str = 'iqr') -> pd.DataFrame:
    """
    Detect outliers in numerical columns using IQR method.
    
    Args:
        df: DataFrame to check for outliers
        columns: List of columns to check (if None, checks all numerical columns)
        method: Method to use ('iqr' for Interquartile Range)
        
    Returns:
        DataFrame with outlier flags added as new columns
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    outlier_summary = {}
    
    for col in columns:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            df[f'{col}_outlier'] = outlier_mask
            
            outlier_count = outlier_mask.sum()
            outlier_summary[col] = {
                'count': outlier_count,
                'percentage': (outlier_count / len(df)) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
    
    return df, outlier_summary


def clean_data(df: pd.DataFrame, missing_strategy: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Clean data by handling missing values, duplicates, and outliers.
    
    Args:
        df: Raw DataFrame
        missing_strategy: Optional dict mapping column names to missing value strategies
        
    Returns:
        Cleaned DataFrame with quality report printed
    """
    print("\n" + "="*60)
    print("DATA CLEANING REPORT")
    print("="*60)
    
    initial_rows = len(df)
    initial_cols = len(df.columns)
    
    # 1. Check for duplicates
    print("\n1. DUPLICATE CHECK")
    print("-" * 60)
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"  Found {duplicates} duplicate rows ({duplicates/len(df)*100:.2f}%)")
        df = df.drop_duplicates()
        print(f"  ✓ Removed {duplicates} duplicate rows")
    else:
        print("  ✓ No duplicates found")
    
    # 2. Check for missing values
    print("\n2. MISSING VALUES CHECK")
    print("-" * 60)
    missing_summary = df.isna().sum()
    missing_summary = missing_summary[missing_summary > 0]
    
    if len(missing_summary) > 0:
        print("  Missing values by column:")
        for col, count in missing_summary.items():
            percentage = (count / len(df)) * 100
            print(f"    {col}: {count} ({percentage:.2f}%)")
        
        df = handle_missing_values(df, missing_strategy)
        print(f"  ✓ Missing values handled")
    else:
        print("  ✓ No missing values found")
    
    # 3. Data type conversions
    print("\n3. DATA TYPE VALIDATION")
    print("-" * 60)
    
    # Ensure categorical columns are optimized
    categorical_cols = ['Category', 'StoreType', 'City', 'PaymentMethod', 'DayOfWeek']
    for col in categorical_cols:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].astype('category')
            print(f"  ✓ Converted {col} to category type")
    
    # 4. Outlier detection
    print("\n4. OUTLIER DETECTION")
    print("-" * 60)
    
    numerical_cols = ['Quantity', 'Price', 'TotalAmount', 'Discount']
    df, outlier_summary = detect_outliers(df, numerical_cols)
    
    if outlier_summary:
        print("  Outliers detected (flagged but not removed):")
        for col, info in outlier_summary.items():
            if info['count'] > 0:
                print(f"    {col}: {info['count']} outliers ({info['percentage']:.2f}%)")
                print(f"      Valid range: [{info['lower_bound']:.2f}, {info['upper_bound']:.2f}]")
    else:
        print("  ✓ No significant outliers detected")
    
    # 5. Final summary
    print("\n" + "="*60)
    print("CLEANING SUMMARY")
    print("="*60)
    print(f"  Initial shape: {initial_rows:,} rows × {initial_cols} columns")
    print(f"  Final shape: {len(df):,} rows × {len(df.columns)} columns")
    print(f"  Rows removed: {initial_rows - len(df):,}")
    print(f"  Data quality: {((len(df) / initial_rows) * 100):.2f}% retained")
    print("="*60)
    
    return df
