from word_search_generator import WordSearch

with open("./test/words/words.txt") as file:
    # reads all files into list
    allWords = [line.rstrip() for line in file]
    i = 0
    words_len = len(allWords) 
    while(i <= words_len):

        words = ",".join(allWords[i:i+9])
        i += 9
        puzzle = WordSearch(words)
        puzzle.size = 15
        puzzle.directions = "E,S,NE,SE"
        # Read in the CSV file
        if (len(puzzle.placed_words.items) != len(puzzle.words.items)):
            unplaced_word = puzzle.unplaced_words.items[0].text.title()
            next_word = allWords[i]
            print(f"Could not place {unplaced_word}, replacing with {next_word}")
            i+=1
            words = words.replace(unplaced_word, next_word)
            puzzle.remove_words(puzzle.unplaced_words.items[0].text)
            puzzle.add_words(next_word)
        # puzzle.show()
        if(i + 9 > words_len):
            break
        print(words)

