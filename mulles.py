
def format_words(input_file, output_file, words_per_row=9):
    """
    Reads words from input file (one word per line) and writes them
    to output file with specified number of words per row.
    
    Args:
        input_file: Path to input text file
        output_file: Path to output text file
        words_per_row: Number of words per row (default: 9)
    """
    try:
        # Read all words from input file
        with open(input_file, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        
        # Write words to output file with specified words per row
        with open(output_file, 'w', encoding='utf-8') as f:
            for i in range(0, len(words), words_per_row):
                row = words[i:i + words_per_row]
                f.write(', '.join(row) + '\n')
        
        print(f"Successfully formatted {len(words)} words into {output_file}")
        print(f"Created {(len(words) + words_per_row - 1) // words_per_row} rows")
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    input_filename = "./IT/words.txt"
    output_filename = "./IT/formatted_words.txt"
    
    format_words(input_filename, output_filename, words_per_row=9)