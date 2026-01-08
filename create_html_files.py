import sys
import os
import re
import glob
from pathlib import Path
from word_search_generator import WordSearch
from weasyprint import HTML, CSS
from multiprocessing import Process


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
            for i in range(0, len(valid_words), 9):
                chunk = valid_words[i:i+9]
                outfile.write(','.join(chunk) + '\n')
        
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

category_name = "fishing"
html_file_name = "puzzle.html"
html_result_file_name = "puzzle_solved.html"
words_files = glob.glob(os.path.join(category_name,"words","*.md"))
for file in words_files:
    filter_and_deduplicate_words(file, os.path.join(category_name, "formatted_words", os.path.basename(file)))
formatted_words_files = glob.glob(os.path.join(category_name,"formatted_words","*.md"))


html_template = open('template.html', 'r').read()
html_solution_template = open('template_solution.html', 'r').read()


page = 0
for words_file in formatted_words_files:
    category = os.path.splitext(os.path.basename(words_file))[0]

    with open(words_file) as file:
        allWords = [line.rstrip() for line in file]
        # needs 6 lines
        allWords = allWords[:9]
        for p, w in enumerate(allWords, start=1):

            # Configure and generate puzzle+
            puzzle = WordSearch(w)
            puzzle.size = 15
            puzzle.directions = "E,S,NE,SE"
            # Read in the CSV file
            if (len(puzzle.placed_words.items) != len(puzzle.words.items)):
                print(f"{p} could not be placed, skipping...")
                continue
            page += 1
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


            # For solution add two columns

            
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


