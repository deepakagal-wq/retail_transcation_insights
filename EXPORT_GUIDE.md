# Notebook Export Guide

This guide explains how to export the retail analysis notebook to PDF or HTML format.

## Prerequisites

Before exporting, ensure:
1. ✅ All notebook cells have been executed
2. ✅ All visualizations are displayed correctly
3. ✅ The notebook is saved

## Method 1: Export to PDF (Recommended)

### Requirements
- `nbconvert` package (included in requirements.txt)
- LaTeX distribution (MiKTeX or TeX Live)

### Steps

1. **Install LaTeX** (if not already installed):
   - **Windows**: Download and install [MiKTeX](https://miktex.org/download)
   - **macOS**: Install MacTeX via `brew install --cask mactex`
   - **Linux**: Install TeX Live via `sudo apt-get install texlive-xetex`

2. **Run the export script**:
   ```bash
   py export_to_pdf.py
   ```

3. **Find your PDF**:
   - Location: `outputs/retail_analysis.pdf`
   - The script will display the file location and size

### Troubleshooting PDF Export

**Issue**: "xelatex not found" or "pdflatex not found"
- **Solution**: Install a LaTeX distribution (see step 1 above)

**Issue**: "nbconvert not installed"
- **Solution**: Run `py -m pip install nbconvert`

**Issue**: PDF generation fails with encoding errors
- **Solution**: Ensure all text in the notebook uses UTF-8 encoding

## Method 2: Export to HTML (Alternative)

If you can't install LaTeX or prefer HTML format:

### Steps

1. **Run the HTML export script**:
   ```bash
   py export_to_html.py
   ```

2. **Find your HTML file**:
   - Location: `outputs/retail_analysis.html`
   - Open in any web browser

3. **Convert HTML to PDF** (optional):
   - Open the HTML file in Chrome/Edge
   - Press `Ctrl+P` (or `Cmd+P` on Mac)
   - Select "Save as PDF" as the destination
   - Adjust settings for best results:
     - Layout: Portrait
     - Margins: Default
     - Background graphics: Enabled

## Method 3: Manual Export via Jupyter

### Export to PDF

1. Open the notebook in Jupyter
2. Go to `File` → `Download as` → `PDF via LaTeX (.pdf)`
3. Save the file to the `outputs/` directory

### Export to HTML

1. Open the notebook in Jupyter
2. Go to `File` → `Download as` → `HTML (.html)`
3. Save the file to the `outputs/` directory

## Method 4: Command Line (Advanced)

### PDF Export
```bash
py -m jupyter nbconvert --to pdf --output-dir outputs notebooks/retail_analysis.ipynb
```

### HTML Export
```bash
py -m jupyter nbconvert --to html --output-dir outputs notebooks/retail_analysis.ipynb
```

### With Custom Template
```bash
py -m jupyter nbconvert --to pdf --template classic --output-dir outputs notebooks/retail_analysis.ipynb
```

## Verification Checklist

After exporting, verify your PDF/HTML contains:

- [ ] All section headings are visible and properly formatted
- [ ] All visualizations are displayed correctly
- [ ] All tables and data outputs are readable
- [ ] Code cells are formatted properly (if included)
- [ ] Page breaks are appropriate
- [ ] File size is reasonable (typically 1-10 MB)

## Export Options

### Include/Exclude Code Cells

To export without code cells (cleaner report):
```bash
py -m jupyter nbconvert --to pdf --no-input --output-dir outputs notebooks/retail_analysis.ipynb
```

### Custom Output Name
```bash
py -m jupyter nbconvert --to pdf --output "Retail_Analysis_Report_2024" --output-dir outputs notebooks/retail_analysis.ipynb
```

## Best Practices

1. **Before exporting**:
   - Run all cells from top to bottom
   - Clear any error messages
   - Ensure all visualizations are displayed
   - Save the notebook

2. **For professional reports**:
   - Use `--no-input` to hide code cells
   - Add markdown cells with narrative and insights
   - Use clear section headings
   - Include a title cell at the top

3. **For large notebooks**:
   - Consider splitting into multiple notebooks
   - Reduce figure DPI if file size is too large
   - Use `--ExecutePreprocessor.timeout=600` for long-running cells

## Common Issues and Solutions

### Issue: "Notebook does not appear to be JSON"
**Solution**: The notebook file is corrupted. Restore from backup or recreate.

### Issue: "Failed to run command"
**Solution**: Ensure Jupyter and nbconvert are installed: `py -m pip install jupyter nbconvert`

### Issue: PDF is too large
**Solution**: Reduce figure DPI in visualization functions or use HTML export instead

### Issue: Visualizations are cut off
**Solution**: Adjust figure sizes in the notebook before exporting

### Issue: Special characters not displaying
**Solution**: Use XeLaTeX engine: `--pdf-engine=xelatex`

## Additional Resources

- [nbconvert Documentation](https://nbconvert.readthedocs.io/)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [LaTeX Installation Guide](https://www.latex-project.org/get/)

## Support

If you encounter issues not covered in this guide:
1. Check the error message carefully
2. Ensure all prerequisites are installed
3. Try the HTML export method as an alternative
4. Verify the notebook runs without errors in Jupyter
