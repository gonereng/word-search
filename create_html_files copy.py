import sys
import os
import re
import glob
from pathlib import Path
from word_search_generator import WordSearch
from weasyprint import HTML, CSS
from multiprocessing import Process
import concurrent.futures
from pypdf import PdfWriter


def filter_and_deduplicate_words(input_file, output_file):
    seen_words = set()
    valid_words = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                word = line.strip()
                
                # Skip empty lines
                if not word:
                    continue
                
                # Check if word contains only A-Z letters (case insensitive)
                if re.match(r'^[A-Za-z]+$', word):
                    # Convert to lowercase for case-insensitive duplicate checking
                    word_lower = word.lower()
                    
                    # Only add if not already seen
                    if word_lower not in seen_words:
                        seen_words.add(word_lower)
                        valid_words.append(word)
        
        # Write valid words to output file (9 words per line, comma-separated)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for word in valid_words:
                outfile.write(word + '\n')
        
        print(f"Successfully processed {len(valid_words)} unique valid words")
        print(f"Output written to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error: {e}")

def need_to_be_colored(i,j):
    for key, word in enumerate(puzzle.words.items, start=1):
        for coordinates in word.coordinates:
            if i == coordinates[0] and j == coordinates[1]:
                return (True, key)
    else:
        return (False, -1)

def get_answer_key(word):
    word = word.upper()
    value = ""
    for item in puzzle.words.items:
        if item.text == word:
            start = item.coordinates[0]
            end = item.coordinates[-1]
            start_col = int(start[1]) + 1
            start_row = int(start[0]) + 1
            end_col = int(end[1]) + 1
            end_row = int(end[0]) + 1
            value += f"Start ({str(start_col)}:{str(start_row)}) End ({str(end_col)}:{str(end_row)})"
    return value

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
            'file': os.path.join(category_name,"output",f"{prefix}_6x9.pdf")
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

def create_single_page(page):
    # open template files
    html_template = open('template.html', 'r').read()
    html_solution_template = open('template_solution.html', 'r').read()

    grid = ""
    grid_solution = ""            

    grid += '<div class="row"><div class="cell number">&nbsp;</div>'
    grid_solution += '<div class="row"><div class="cell number">&nbsp;</div>'
    for i in range(15):
        grid += F'<div class="cell number">{i + 1}</div>'
        grid_solution += f'<div class="cell number">{i + 1}</div>'
    grid += '</div>'
    grid_solution += '</div>'
    for i, row in enumerate(puzzle.cropped_puzzle, start=0):
        grid += '<div class="row">'
        grid_solution += '<div class="row">'
        grid += f'<div class="cell number">{i + 1}</div>'
        grid_solution += f'<div class="cell number">{i + 1}</div>'
        for j, c in enumerate(row, start=0):
            grid += f'<div class="cell">{c}</div>'
            needs_to_be_colored, index = need_to_be_colored(i,j)
            if needs_to_be_colored:        
                grid_solution += f'<div class="cell selected-{str(index)}">{c}</div>'
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

    words_per_column = int(words_amount / 3)
    solution_column1 = ""
    for word in words[0:words_per_column]:
        solution_column1 += f'<div class="word-item"><p>{word.strip()}</p><span>{get_answer_key(word.strip())}</span></div>'

    solution_column2 = ""
    for word in words[words_per_column:2*words_per_column]:
        solution_column2 += f'<div class="word-item"><p>{word.strip()}</p><span>{get_answer_key(word.strip())}</span></div>'
        
    solution_column3 = ""
    for word in words[2*words_per_column:]:
        solution_column3 += f'<div class="word-item"><p>{word.strip()}</p><span>{get_answer_key(word.strip())}</span></div>'

    html_blank_template = html_template.replace("CATEGORYPLACEHOLDER", category).replace("GRIDPLACEHOLDER", grid).replace("COLUMN1PLACEHOLDER", column1).replace("COLUMN2PLACEHOLDER", column2).replace("COLUMN3PLACEHOLDER", column3).replace("NUMBERPLACEHOLDER", str(page))
    html_sol_template = html_solution_template.replace("CATEGORYPLACEHOLDER", category).replace("GRIDPLACEHOLDER", grid_solution).replace("COLUMN1PLACEHOLDER", solution_column1).replace("COLUMN2PLACEHOLDER", solution_column2).replace("COLUMN3PLACEHOLDER", solution_column3).replace("NUMBERPLACEHOLDER", str(page))
                
    with open(os.path.join(category_name, "output", f"{page} - {html_file_name}"), 'w') as file:
        file.write(html_blank_template)
            
    with open(os.path.join(category_name, "output", f"{page} - {html_result_file_name}"), 'w') as file:
        file.write(html_sol_template)

def initialize(category_name):
    # Remove duplicates per file
    words_files = glob.glob(os.path.join(category_name,"words","*.*"))

    for file in words_files:
        filter_and_deduplicate_words(file, os.path.join(category_name, "formatted_words", os.path.basename(file)))
    return glob.glob(os.path.join(category_name,"formatted_words","*.*"))

def extract_categories_to_files(input_file, folder):    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content by category headers
        # Pattern matches "Category:" (case-insensitive) followed by the category name
        category_pattern = r'(?i)category:(.+?)(?=\n)'
        
        # Find all category positions
        matches = list(re.finditer(category_pattern, content))
        
        if not matches:
            print("No categories found in the file.")
            return
        
        # Process each category
        for i, match in enumerate(matches):
            category_name = match.group(1).strip()
            start_pos = match.end()
            
            # Determine end position (start of next category or end of file)
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            
            # Extract words for this category
            category_content = content[start_pos:end_pos].strip()
            
            # Split into lines and filter out empty lines
            words = [line.strip() for line in category_content.split('\n') if line.strip()]
            
            # Create filename from category name (sanitize for filesystem)
            filename = re.sub(r'[^\w\s-]', '', category_name).strip()
            # filename = re.sub(r'[-\s]+', '_', filename)
            filename = os.path.join(folder, "words", f"{filename}.txt")
            
            # Write words to file
            with open(filename, 'w', encoding='utf-8') as out_file:
                for word in words:
                    out_file.write(word + '\n')
            
            print(f"Created '{filename}' with {len(words)} words")
        
        print(f"\nSuccessfully processed {len(matches)} categories")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")


category_name = "food"
html_file_name = "puzzle.html"
html_result_file_name = "puzzle_solved.html"


if __name__ == "__main__":

    Path(f"./{category_name}/finished").mkdir(parents=True, exist_ok=True)
    Path(f"./{category_name}/words").mkdir(parents=True, exist_ok=True)
    Path(f"./{category_name}/formatted_words").mkdir(parents=True, exist_ok=True)
    Path(f"./{category_name}/output").mkdir(parents=True, exist_ok=True)
    
    extract_categories_to_files("words.txt", category_name)

    formatted_words_files = initialize(category_name)

    page = 0
    for words_file in formatted_words_files:
        category = os.path.splitext(os.path.basename(words_file))[0]

        with open(words_file) as file:
        # reads all files into list
            allWords = [line.rstrip() for line in file]
            current_word_number = 0
            words_len = len(allWords) 
            while(current_word_number <= words_len):

                w = ",".join(allWords[current_word_number:current_word_number+9])
                current_word_number += 9

                puzzle = WordSearch(w)
                puzzle.size = 15
                puzzle.directions = "E,S,NE,SE"
                # Read in the CSV file
                while (len(puzzle.placed_words.items) < len(puzzle.words.items)):
                    if current_word_number < words_len - 1:
                        for unplaced_word in puzzle.unplaced_words.items:
                            unplaced_word_text = unplaced_word.text.title()
                            next_word = allWords[current_word_number]
                            print(f"Could not place {unplaced_word_text}, replacing with {next_word}")
                            current_word_number+=1
                            w = w.replace(unplaced_word_text, next_word)
                            puzzle.remove_words(unplaced_word_text)
                            puzzle.add_words(next_word)
                    else:
                        print(f"No next word available in {category}, breaking out")
                        break
                    
                if(current_word_number + 9 < words_len):
                    page += 1
                    create_single_page(page)
                else:
                    print(f"Not enough words left in {category} the create entire page")
                    break

    # input("Press Enter to continue...")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = []
        for i in range(60):
            results.append(executor.submit(convert_html_to_pdf, os.path.join(category_name, "output", f"{i+1} - puzzle.html")))
            results.append(executor.submit(convert_html_to_pdf, os.path.join(category_name, "output", f"{i+1} - puzzle_solved.html")))
        
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())


    convert_non_puzzles(os.path.join("template_intro.html"), os.path.join(category_name, "template_intro.pdf"))
    convert_non_puzzles(os.path.join("template_answer_description.html"), os.path.join(category_name, "template_answer_description.pdf"))

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
