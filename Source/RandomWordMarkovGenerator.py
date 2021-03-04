import json, time, random, platform
from RandomCharacterMarkovChains import import_text_file, generate_frequency_JSON, read_frequency_JSON

def generate_word_dictionary(inputString):
    '''
    Processes a string into a dictionary suitable for operating on

    Args:
        inputString: A string containing the body of text we wish to use
    
    Returns: 
        Dictionary of format: {Word: {Subsequent Word: frequency}}
    '''
    wordList = inputString.split()
    wordDictionary = {}
    for i in range(len(wordList) - 1):
        #Not necessary to define these variables, but makes functionality clear
        currentWord = wordList[i].strip('(!?){}[];:’‘_"“”$')
        nextWord = wordList[i + 1].strip('(!?){}[];:’‘_"“”$')
        if not (check_valid_word(nextWord)):
            nextWord = wordList[i + 2].strip('(!?){}[];:’‘_"“”$')
        if check_valid_word(currentWord):
            if currentWord not in wordDictionary:
                wordDictionary[currentWord] = {nextWord: 0}
            if nextWord not in wordDictionary[currentWord]:
                wordDictionary[currentWord][nextWord] = 0
            wordDictionary[currentWord][nextWord] += 1
        else:
            pass

    return wordDictionary

def clean_input_text(inputString):
    '''
    Cleans the input text, removing obscure characters and splitting dashed words

    Args:
        inputString: A string containing the text we wish to clean
    
    Returns:
        The cleaned text
    '''

    inputString = list(inputString)
    for char in range(len(inputString)):

        if not inputString[char].isalpha():
            inputString[char] = ' '
    cleanedText = ''
    return cleanedText.join(inputString)

def check_valid_word(checkedWord):
    '''
    Checks if the word we are adding is valid

    Args:
        checkedWord: Word to be tested
    
    Returns:
        True or False based on validity of word
    '''
    blacklist = ['Project','Gutenberg', '\ufeffthe', 'pglaf', 'ebooks,']
    if checkedWord in blacklist:
        return False

    for char in checkedWord:
        invalidChars = ['-', '’', '—', 'æ', 'ô', 'é', 'è', 'å', 'ê']
        if char.isdigit() or char in invalidChars:
            return False
    
    return True

def generate_random_paragraph(wordDictionary, length):

    '''
    Creates a random paragrpah using markov chains

    Args:
        wordDictionary: Dictionary containing words and all subsequent words with their counts
        length: Length we wish the generated paragraph to be in words
    
    Returns:
        Generated paragraph
    '''

    output = []
    
    currentWord = random.choice(list(wordDictionary.keys()))
    output.append(currentWord)

    for i in range(length):
        nextWords = wordDictionary[currentWord]
        wordWeights = list(nextWords.values())
        currentWord = random.choices(list(nextWords.keys()), wordWeights)[0]
        output.append(currentWord)

    return output


if __name__ == '__main__':

    wordDictionary = generate_word_dictionary(
        clean_input_text(import_text_file(
            'c:\\Users\\Raffi\\Documents\\College\\Programming\\TeamSoftwareProject\\Source\\TextGeneration\\Frankenstein.txt'
        )))
    generate_frequency_JSON(wordDictionary, 'FrankensteinWordFrequency')
    startTime = time.time()
    if platform.system() == 'Linux':
        wordDictionary = read_frequency_JSON('TextGeneration/FrankensteinWordFrequency.json')
    elif platform.system() == 'Windows':
        wordDictionary = read_frequency_JSON('c:\\Users\\Raffi\\Documents\\College\\Programming\\TeamSoftwareProject\\Source\\TextGeneration\\FrankensteinWordFrequency.JSON')

    print(time.time() - startTime)
    for i in range(100):
        
        print(*generate_random_paragraph(wordDictionary, 100))
        print('\n')
        
