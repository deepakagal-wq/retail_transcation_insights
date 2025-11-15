# Data File Information

## Required Data File

This project requires a retail transactions dataset in CSV format.

### File Name
`Retail_Transactions_Dataset.csv`

### Location
Place the CSV file in the project root directory (same level as README.md)

### Why is the data file not included?

The dataset file (160+ MB) exceeds GitHub's file size limit of 100 MB. Therefore, it's not included in the repository.

### Where to get the data

1. **If you received this project as part of a course**: The dataset should be provided separately by your instructor
2. **If you're using your own data**: Ensure your CSV file matches the expected format (see below)
3. **Sample data**: You can create a sample dataset following the format specification

### Expected Data Format

The CSV file must contain the following columns:

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| TransactionID | String | Unique transaction identifier |
| Date | Date | Transaction date (YYYY-MM-DD format) |
| CustomerID | String | Customer identifier |
| ProductID | String | Product identifier |
| ProductName | String | Product name |
| Category | String | Product category |
| Quantity | Integer | Quantity purchased |
| Price | Float | Unit price |
| TotalAmount | Float | Total transaction amount |
| Discount | Float | Discount percentage (0-100) |
| StoreType | String | Type of store (e.g., Online, Physical) |
| City | String | City location |
| PaymentMethod | String | Payment method used |

### Example Data Structure

```csv
TransactionID,Date,CustomerID,ProductID,ProductName,Category,Quantity,Price,TotalAmount,Discount,StoreType,City,PaymentMethod
TXN001,2024-01-15,CUST001,PROD001,Laptop,Electronics,1,999.99,999.99,0,Online,New York,Credit Card
TXN002,2024-01-15,CUST002,PROD002,T-Shirt,Clothing,2,29.99,59.98,10,Physical,Los Angeles,Cash
```

### Data Size Recommendations

- **Minimum**: 1,000 rows for meaningful analysis
- **Recommended**: 10,000+ rows for robust insights
- **Maximum**: No hard limit, but performance may vary with very large datasets (>1M rows)

### Setting Up Your Data

1. Obtain or create your retail transactions CSV file
2. Rename it to `Retail_Transactions_Dataset.csv`
3. Place it in the project root directory:
   ```
   retail-transaction-insights/
   ├── Retail_Transactions_Dataset.csv  ← Place file here
   ├── README.md
   ├── modules/
   └── ...
   ```
4. Verify the file is in place:
   ```bash
   # Windows
   dir Retail_Transactions_Dataset.csv
   
   # macOS/Linux
   ls -lh Retail_Transactions_Dataset.csv
   ```

### Alternative: Using Git LFS (Advanced)

If you need to version control large data files, consider using Git Large File Storage (LFS):

```bash
# Install Git LFS
git lfs install

# Track CSV files with LFS
git lfs track "*.csv"

# Add and commit
git add .gitattributes
git add Retail_Transactions_Dataset.csv
git commit -m "Add dataset with Git LFS"
git push
```

Learn more: https://git-lfs.github.com/

### Troubleshooting

**Issue**: "File not found" error when running the analysis
- **Solution**: Ensure the CSV file is named exactly `Retail_Transactions_Dataset.csv` and is in the project root

**Issue**: "Parser error" when loading data
- **Solution**: Verify the CSV format matches the expected structure above

**Issue**: Memory errors with large files
- **Solution**: The code uses memory optimization, but for very large files (>2GB), consider processing in chunks

### Data Privacy Note

If using real customer data:
- Ensure you have proper authorization
- Consider anonymizing sensitive information
- Follow data protection regulations (GDPR, CCPA, etc.)
- Do not commit real customer data to public repositories

---

For more information, see the main [README.md](README.md)
