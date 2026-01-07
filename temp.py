from weasyprint import HTML, CSS
import sys
from pathlib import Path

def convert_html_to_pdf(html_file, output_file):
    """
    Convert HTML file to PDF in two different sizes
    
    Args:
        html_file (str): Path to the input HTML file
        output_prefix (str, optional): Prefix for output files. 
                                    If None, uses HTML filename
    """
    html_path = Path(html_file)
    
    # Check if HTML file exists
    if not html_path.exists():
        print(f"Error: File '{html_file}' not found.")
        sys.exit(1)
    
    # Set output file prefix
    # Define page sizes
    sizes = [
        {
            'name': '6x9',
            'width': '6in',
            'height': '9in',
            'file': f"puzzle_6x9.pdf"
        }
    ]
    
    try:
        html = HTML(filename=str(html_path))
        
        for size in sizes:
            print(f"Creating {size['name']} inches PDF...")
            
            # CSS to set page size with no margins
            page_css = CSS(string=f'''
                @page {{
                    margin: 0;
                    padding-left: 0.125qin; 
                    
                }}
                
            ''')
            
            # Write PDF with specified page size
            # html.write_pdf(size['file'], stylesheets=[page_css])
            # html.write_pdf(size['file'])
            html.write_pdf(output_file)


            
            print(f"  ✓ Saved: {size['file']}")
        
        print("\nSuccess! Both PDFs have been created.")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


# pdfkit.from_file('puzzle.html', 'puzzle.pdf')
convert_html_to_pdf(f"template_intro.html", "template_intro.pdf")
convert_html_to_pdf(f"template_answer_description.html", "template_answer_description.pdf")
        