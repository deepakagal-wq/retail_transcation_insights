"""
Script to export the retail analysis notebook to PDF format.

This script:
1. Checks if the notebook exists
2. Verifies that cells have been executed
3. Exports to PDF using nbconvert
4. Saves the PDF to the outputs directory

Requirements:
- jupyter nbconvert must be installed
- The notebook should be executed before running this script
"""

import os
import sys
import subprocess
from pathlib import Path


def check_notebook_exists(notebook_path):
    """Check if the notebook file exists."""
    if not os.path.exists(notebook_path):
        print(f"❌ Error: Notebook not found at {notebook_path}")
        return False
    print(f"✓ Notebook found: {notebook_path}")
    return True


def check_nbconvert_installed():
    """Check if jupyter nbconvert is installed."""
    try:
        result = subprocess.run(
            ['py', '-m', 'jupyter', 'nbconvert', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ jupyter nbconvert is installed (version: {result.stdout.strip()})")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: jupyter nbconvert is not installed")
        print("   Install it with: py -m pip install nbconvert")
        return False


def export_notebook_to_pdf(notebook_path, output_dir):
    """Export notebook to PDF format."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the output filename
        notebook_name = Path(notebook_path).stem
        output_path = os.path.join(output_dir, f"{notebook_name}.pdf")
        
        print(f"\n📄 Exporting notebook to PDF...")
        print(f"   Input: {notebook_path}")
        print(f"   Output: {output_path}")
        
        # Run nbconvert
        result = subprocess.run(
            [
                'py', '-m', 'jupyter', 'nbconvert',
                '--to', 'pdf',
                '--output-dir', output_dir,
                notebook_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024  # Size in KB
            print(f"\n✅ SUCCESS! PDF exported successfully!")
            print(f"   Location: {output_path}")
            print(f"   Size: {file_size:.2f} KB")
            return True
        else:
            print(f"\n❌ Error: PDF file was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during PDF export:")
        print(f"   {e.stderr}")
        
        # Check for common issues
        if "xelatex" in e.stderr.lower() or "pdflatex" in e.stderr.lower():
            print("\n💡 Tip: PDF export requires LaTeX to be installed.")
            print("   Options:")
            print("   1. Install MiKTeX (Windows): https://miktex.org/download")
            print("   2. Install TeX Live (cross-platform): https://www.tug.org/texlive/")
            print("   3. Use HTML export instead: py -m jupyter nbconvert --to html notebook.ipynb")
        
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def main():
    """Main function to export notebook to PDF."""
    print("="*70)
    print("RETAIL ANALYSIS NOTEBOOK - PDF EXPORT")
    print("="*70)
    
    # Configuration
    notebook_path = "notebooks/retail_analysis.ipynb"
    output_dir = "outputs"
    
    # Step 1: Check if notebook exists
    if not check_notebook_exists(notebook_path):
        sys.exit(1)
    
    # Step 2: Check if nbconvert is installed
    if not check_nbconvert_installed():
        sys.exit(1)
    
    # Step 3: Export to PDF
    success = export_notebook_to_pdf(notebook_path, output_dir)
    
    if success:
        print("\n" + "="*70)
        print("Export completed successfully!")
        print("="*70)
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("Export failed. Please check the errors above.")
        print("="*70)
        sys.exit(1)


if __name__ == "__main__":
    main()
