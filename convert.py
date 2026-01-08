from multiprocessing import Process
import concurrent.futures
from pypdf import PdfWriter
import glob
import os

from pathlib import Path
import sys
from weasyprint import HTML, CSS


def convert_html_to_pdf(html_file):
    html_path = Path(html_file)
    
    nbr = int(html_path.name[0:html_path.name.index("-")-1])
    
    # Check if HTML file exists
    if not html_path.exists():
        print(f"Error: File '{html_file}' not found.")
        sys.exit(1)
    
    # Set output file prefix
    prefix = html_path.stem
    
    # Define page sizes
    sizes = [
        {
            'name': '6x9',
            'width': '6in',
            'height': '9in',
            'file': os.path.join("fishing","output",f"{prefix}_6x9.pdf")
        },
        # {
        #     'name': '8.5x11',
        #     'width': '8.5in',
        #     'height': '11in',
        #     'file': f".\{folder_name}\{prefix}_8.5x11.pdf"
        # }
    ]
    
    try:
        html = HTML(filename=str(html_path))
        
        for size in sizes:
            print(f"Creating {size['file']} inches PDF...")
            
            # CSS to set page size with no margins
            padding = "padding-left: 0.127in;"
            if nbr % 2 == 0:
                padding = "padding-right: 0.127in;"

            page_css = CSS(string=f'''
                @page {{
                    margin: 0;
                    {padding}                         
                }}
            ''')
            
            # Write PDF with specified page size
            html.write_pdf(size['file'], stylesheets=[page_css])

        # return f"  ✓ Saved: {size['file']}"
            print(f"  ✓ Saved: {size['file']}")
        
        # print("\nSuccess! Both PDFs have been created.")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

def convert_non_puzzles(html_file, output_file):
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

if __name__ == "__main__":

    category_name = "fishing"

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = []
        for i in range(60):
            results.append(executor.submit(convert_html_to_pdf, os.path.join(category_name, "output", f"{i+1} - puzzle.html")))
            results.append(executor.submit(convert_html_to_pdf, os.path.join(category_name, "output", f"{i+1} - puzzle_solved.html")))
        
        for f in concurrent.futures.as_completed(results):
            print(f.result())


    convert_non_puzzles(os.path.join(category_name, "template_intro.html"), os.path.join(category_name, "template_intro.pdf"))
    convert_non_puzzles(os.path.join(category_name, "template_answer_description.html"), os.path.join(category_name, "template_answer_description.pdf"))

    pdf_writer = PdfWriter()

    files = [f for f in glob.glob(os.path.join(category_name, "output", "./IT/*6x9.pdf"))]

    #Add the intro

    pdf_path = Path(os.path.join(category_name, "template_intro.pdf"))
    pdf_writer.append(str(pdf_path))
    pdf_writer.add_blank_page()

    # Add each PDF to the writer
    for i in range(60):
        pdf_file = os.path.join(category_name, "output", f"{i+1} - puzzle_6x9.pdf")
        pdf_path = Path(pdf_file)
        
        if not pdf_path.exists():
            print(f"Warning: File '{pdf_file}' not found. Skipping...")
            continue
        
        print(f"Adding: {pdf_file}")
        
        try:
            # Append entire PDF
            pdf_writer.append(str(pdf_path))
        except Exception as e:
            print(f"Error adding {pdf_file}: {e}")
            continue

    pdf_path = Path(os.path.join(category_name, "template_answer_description.pdf"))
    pdf_writer.append(str(pdf_path))
    pdf_writer.add_blank_page()

    for i in range(60):
        pdf_file = os.path.join(category_name, "output", f"{i+1} - puzzle_solved_6x9.pdf")
        pdf_path = Path(pdf_file)
        
        if not pdf_path.exists():
            print(f"Warning: File '{pdf_file}' not found. Skipping...")
            continue
        
        print(f"Adding: {pdf_file}")
        
        try:
            # Append entire PDF
            pdf_writer.append(str(pdf_path))
        except Exception as e:
            print(f"Error adding {pdf_file}: {e}")
            continue

    # Write combined PDF
    output_file = os.path.join(category_name, "finished", f"Complete_6x9_{category_name}.pdf") 
    try:
        with open(output_file, 'wb') as output:
            pdf_writer.write(output)
        print(f"\n✓ Success! Combined PDF saved as: {output_file}")
        print(f"  Total pages: {len(pdf_writer.pages)}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)