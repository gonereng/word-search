import os
from word_search_generator import WordSearch

csv_file_path = "puzzle.csv"
html_file_name = "puzzle.html"
html_result_file_name = "puzzle_solved.html"

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word Search Grid</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: white;
            padding: 20px;
        }

        .container {
            background: white;
            padding: 20px;
            max-width: 700px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            color: #000;
            margin-bottom: 20px;
            font-size: 28px;
            font-weight: bold;
        }

        .grid {
            display: flex;
            flex-direction: column;
            max-width: 480px;
            margin: 0 auto 30px;
            border: 2px solid #000;
        }

        .row {
            display: flex;
        }

        .cell {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            border: 1px solid #000;
            font-size: 18px;
            font-weight: bold;
            color: #000;
            user-select: none;
        }

        .words-container {
            display: flex;
            gap: 30px;
            margin-top: 30px;
            justify-content: space-between;
        }

        .word-column {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .word-item {
            padding: 10px;
            background: white;
            border: 1px solid #000;
            font-size: 16px;
            font-weight: 600;
            color: #000;
            text-align: center;
            text-transform: uppercase;
        }

        /* Print styles */
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                padding: 0;
            }
            
            @page {
                margin: 0.5in;
            }
        }

        @media (max-width: 600px) {
            .cell {
                width: 30px;
                height: 30px;
                font-size: 14px;
            }
            
            .words-container {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Word Search Puzzle</h1>
        <div class="grid" id="wordSearch">
        GRIDPLACEHOLDER
        </div>
        <div class="words-container">
            <div class="word-column" id="column1">COLUMN1PLACEHOLDER</div>
            <div class="word-column" id="column2">COLUMN2PLACEHOLDER</div>
            <div class="word-column" id="column3">COLUMN3PLACEHOLDER</div>
        </div>
    </div>
</body>
</html>
"""

# COnfigure and generate puzzle
puzzle = WordSearch("dog, cat, pig, horse, donkey, turtle, goat, sheep, gorilla")
puzzle.size = 12
puzzle.directions = "E,S"
# puzzle.show()
if os.path.isfile(csv_file_path):
    os.remove(csv_file_path)
puzzle.save(path=csv_file_path, format="csv")
puzzle.key

# Read in the CSV file
with open(csv_file_path) as file:
    lines = [line.rstrip() for line in file]

# Remove first line
lines = lines[1:]    

grid = ""
grid_solution = ""
solutions = lines[18].replace('"', '', -1)
for i, line in enumerate(lines, start=1):
    # print(line)
    
    solution_word = solutions.split(" ")[0]
    solution_direction = solutions.split(" ")[1]
    solution_start = solutions.split(" ")[3] + solutions.split(" ")[4]

    # Create the grid
    if i <= 12:
        grid += '<div class="row">'
        grid_solution += '<div class="row">'
        chars = line.split(",")
        for j, c in enumerate(chars, start=1):
            grid += f'<div class="cell">{c}</div>'
            
            grid_solution += f'<div class="cell">{c}</div>'
        grid += '</div>'
        grid_solution += '</div>'
        continue
        
    html_template = html_template.replace("GRIDPLACEHOLDER", grid)

    # Get the wordlist
    if i == 15:
        words = line.split(",")
        words_amount = len(words)
        words_per_column = int(words_amount / 3)
        column1 = ""
        for word in words[0:words_per_column]:
            column1 += f'<div class="word-item">{word}</div>'
        html_template = html_template.replace("COLUMN1PLACEHOLDER", column1)

        column2 = ""
        for word in words[words_per_column:2*words_per_column]:
            column2 += f'<div class="word-item">{word}</div>'
        html_template = html_template.replace("COLUMN2PLACEHOLDER", column2)

        column3 = ""
        for word in words[2*words_per_column:]:
            column3 += f'<div class="word-item">{word}</div>'
        html_template = html_template.replace("COLUMN3PLACEHOLDER", column3)

            
with open(html_file_name, 'w') as file:
    file.write(html_template)
        