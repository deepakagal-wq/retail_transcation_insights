"""
Script to export the retail analysis notebook to HTML format.

This is an alternative to PDF export that doesn't require LaTeX.
The HTML file can be opened in any web browser and printed to PDF if needed.

Requirements:
- jupyter nbconvert must be installed
- The notebook should be executed before running this script
"""

import os
import sys
import subprocess
from pathlib import Path


def export_notebook_to_html(notebook_path, output_dir):
    """Export notebook to HTML format."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the output filename
        notebook_name = Path(notebook_path).stem
        output_path = os.path.join(output_dir, f"{notebook_name}.html")
        
        print(f"\n📄 Exporting notebook to HTML...")
        print(f"   Input: {notebook_path}")
        print(f"   Output: {output_path}")
        
        # Run nbconvert
        result = subprocess.run(
            [
                'py', '-m', 'jupyter', 'nbconvert',
                '--to', 'html',
                '--output-dir', output_dir,
                notebook_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024  # Size in KB
            print(f"\n✅ SUCCESS! HTML exported successfully!")
            print(f"   Location: {output_path}")
            print(f"   Size: {file_size:.2f} KB")
            print(f"\n💡 Tip: You can open this HTML file in a browser and print to PDF")
            return True
        else:
            print(f"\n❌ Error: HTML file was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during HTML export:")
        print(f"   {e.stderr}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def main():
    """Main function to export notebook to HTML."""
    print("="*70)
    print("RETAIL ANALYSIS NOTEBOOK - HTML EXPORT")
    print("="*70)
    
    # Configuration
    notebook_path = "notebooks/retail_analysis.ipynb"
    output_dir = "outputs"
    
    # Check if notebook exists
    if not os.path.exists(notebook_path):
        print(f"❌ Error: Notebook not found at {notebook_path}")
        sys.exit(1)
    
    print(f"✓ Notebook found: {notebook_path}")
    
    # Export to HTML
    success = export_notebook_to_html(notebook_path, output_dir)
    
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
