import os
import sys
from pathlib import Path
from word_search_generator import WordSearch
from weasyprint import HTML, CSS
from pypdf import PdfWriter
import glob


html_file_name = "puzzle.html"
html_result_file_name = "puzzle_solved.html"
folder_name = "IT"
words_file = os.path.join(folder_name, "formatted_words.txt")

html_template = "" 
with open('template.html', 'r') as content_file:
    html_template = content_file.read()

html_solution_template = "" 
with open('template_solution.html', 'r') as content_file:
    html_solution_template = content_file.read()

with open(words_file) as file:
    allWords = [line.rstrip() for line in file]

    for page, w in enumerate(allWords, start=1):

        # Configure and generate puzzle+
        puzzle = WordSearch(w)
        puzzle.size = 12
        puzzle.directions = "E,S"
        # puzzle.show()
        # if os.path.isfile(csv_file_path):
        #     os.remove(csv_file_path)
        # puzzle.save(path=csv_file_path, format="csv")
        puzzle.key
        # Read in the CSV file
        

        grid = ""
        grid_solution = ""


        def need_to_be_colored(i,j):
            for word in puzzle.words.items:
                for coordinates in word.coordinates:
                    if i == coordinates[0] and j == coordinates[1]:
                        return True
            else:
                return False

        def get_answer_key(word):
            word = word.upper()
            value = ""
            for item in puzzle.words.items:
                if item.text == word:
                    start = item.coordinates[0]
                    end = item.coordinates[-1]
                    start_col = int(start[0]) + 1
                    start_row = int(start[1]) + 1
                    end_col = int(end[0]) + 1
                    end_row = int(end[1]) + 1
                    value += f"Start: ({str(start_col)} {str(start_row)}) End: ({str(end_col)} {str(end_row)})"
            return value

        grid += '<div class="row"><div class="cell number">&nbsp;</div><div class="cell number">1</div><div class="cell number">2</div><div class="cell number">3</div><div class="cell number">4</div><div class="cell number">5</div><div class="cell number">6</div><div class="cell number">7</div><div class="cell number">8</div><div class="cell number">9</div><div class="cell number">10</div><div class="cell number">11</div><div class="cell number">12</div></div>'
        grid_solution += '<div class="row"><div class="cell number">&nbsp;</div><div class="cell number">1</div><div class="cell number">2</div><div class="cell number">3</div><div class="cell number">4</div><div class="cell number">5</div><div class="cell number">6</div><div class="cell number">7</div><div class="cell number">8</div><div class="cell number">9</div><div class="cell number">10</div><div class="cell number">11</div><div class="cell number">12</div></div>'
        for i, row in enumerate(puzzle.cropped_puzzle, start=0):
            grid += '<div class="row">'
            grid_solution += '<div class="row">'
            grid += f'<div class="cell number">{i + 1}</div>'
            grid_solution += f'<div class="cell number">{i + 1}</div>'
            for j, c in enumerate(row, start=0):
                grid += f'<div class="cell">{c}</div>'
                if need_to_be_colored(i,j):        
                    grid_solution += f'<div class="cell selected">{c}</div>'
                else:
                    grid_solution += f'<div class="cell">{c}</div>'
            grid += '</div>'
            grid_solution += '</div>'

        words = w.split(",")
        words_amount = len(words)
        words_per_column = int(words_amount / 3)
        column1 = ""
        for word in words[0:words_per_column]:
            column1 += f'<div class="word-item">{word}</div>'

        column2 = ""
        for word in words[words_per_column:2*words_per_column]:
            column2 += f'<div class="word-item">{word}</div>'

        column3 = ""
        for word in words[2*words_per_column:]:
            column3 += f'<div class="word-item">{word}</div>'


        # For solution add two columns

        solution_column1 = ""
        for word in words:
            solution_column1 += f'<p>{word.strip()} <span>{get_answer_key(word.strip())}</span></p>'


        html_blank_template = html_template.replace("GRIDPLACEHOLDER", grid).replace("COLUMN1PLACEHOLDER", column1).replace("COLUMN2PLACEHOLDER", column2).replace("COLUMN3PLACEHOLDER", column3).replace("NUMBERPLACEHOLDER", str(page))
        html_solution_template = html_solution_template.replace("GRIDPLACEHOLDER", grid_solution).replace("COLUMN1PLACEHOLDER", solution_column1).replace("NUMBERPLACEHOLDER", str(page))
                    
        with open(f".\{folder_name}\{page} - {html_file_name}", 'w') as file:
            file.write(html_blank_template)
                
        with open(f".\{folder_name}\{page} - {html_result_file_name}", 'w') as file:
            file.write(html_solution_template)

        def convert_html_to_pdf(html_file, output_prefix=None):
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
            if output_prefix is None:
                prefix = html_path.stem
            else:
                prefix = output_prefix
            
            # Define page sizes
            sizes = [
                {
                    'name': '6x9',
                    'width': '6in',
                    'height': '9in',
                    'file': f".\{folder_name}\{prefix}_6x9.pdf"
                },
                {
                    'name': '8.5x11',
                    'width': '8.5in',
                    'height': '11in',
                    'file': f".\{folder_name}\{prefix}_8.5x11.pdf"
                }
            ]
            
            try:
                html = HTML(filename=str(html_path))
                
                for size in sizes:
                    print(f"Creating {size['name']} inches PDF...")
                    
                    # CSS to set page size with no margins
                    page_css = CSS(string=f'''
                        @page {{
                            size: {size['width']} {size['height']};
                            margin: 0;
                            padding: 0.4in 0;
                        }}
                        body {{
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            background-image: url("background.jpg");
                            background-size: contain;
                        }}
                        .container {{
                            margin: 0;
                            padding: 0;
                            width: 100%;
                        }}
                        .grid {{
                            margin-left: auto;
                            margin-right: auto;
                        }}
                        .words-container {{
                            margin-left: auto;
                            margin-right: auto;
                        }}
                    ''')
                    
                    # Write PDF with specified page size
                    html.write_pdf(size['file'], stylesheets=[page_css])
                    
                    print(f"  ✓ Saved: {size['file']}")
                
                print("\nSuccess! Both PDFs have been created.")
                
            except Exception as e:
                print(f"Error during conversion: {e}")
                sys.exit(1)


        # pdfkit.from_file('puzzle.html', 'puzzle.pdf')
        convert_html_to_pdf(f".\{folder_name}\{page} - {html_file_name}")
        convert_html_to_pdf(f".\{folder_name}\{page} - {html_result_file_name}")

pdf_writer = PdfWriter()


files = [f for f in glob.glob("./IT/*6x9.pdf")]



# Add each PDF to the writer
for pdf_file in files:
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
output_file = "Complete_6x9.pdf"
try:
    with open(output_file, 'wb') as output:
        pdf_writer.write(output)
    print(f"\n✓ Success! Combined PDF saved as: {output_file}")
    print(f"  Total pages: {len(pdf_writer.pages)}")
except Exception as e:
    print(f"Error writing output file: {e}")
    sys.exit(1)