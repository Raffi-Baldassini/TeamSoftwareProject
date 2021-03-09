import json, time, random, platform
from .RandomCharacterMarkovChains import import_text_file, generate_frequency_JSON, read_frequency_JSON


def generate_word_dictionary(inputString):
    '''
    Processes a string into a dictionary suitable for operating on

    Args:
        inputString: A string containing the body of text we wish to use
    
    Returns: 
        Dictionary of format: {Word: {Subsequent Word: frequency}}
    '''
    order = 2
    wordList = inputString.split()
    wordDictionary = {}
    finalNGram = None
    firstNGram = None
    for i in range(len(wordList)):
        appendItem = get_NGram(wordList, i, order)
        if i == 0:
            firstNGram = appendItem
        nextNGram = get_NGram(wordList, i+order, order)
        if appendItem not in wordDictionary:
            wordDictionary[appendItem] = {}
        if nextNGram not in wordDictionary[appendItem]:
            wordDictionary[appendItem][nextNGram] = 0
        wordDictionary[appendItem][nextNGram] += 1
        finalNGram = nextNGram

    if finalNGram not in wordDictionary:
        wordDictionary[finalNGram] = {firstNGram: 1}

    return wordDictionary

def get_NGram(wordList, position, order):
    '''
    Generates an NGram of words

    Args:
        wordList: List containing every word in the text being analysed
        position: index of first word in the NGram in the list
        order: Length of generated NGram

    Returns:
        A NGram of specified length
    '''
    output = ''
    for i in range(order):
        index = position + i
        if index >= len(wordList):
            index = index - len(wordList)
            output = output + ' ' + wordList[index]
        else:
            output = output + ' ' + wordList[index]

    return output.strip()

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

        if not inputString[char].isalpha() and inputString[char] not in ['.', ',', ';', '?']:
            inputString[char] = ' '
    cleanedText = ''
    cleanedText = cleanedText.join(inputString).split()

    for word in range(len(cleanedText)):
        if not check_valid_word(cleanedText[word]):
            cleanedText[word] = ''
    
    return ' '.join(map(str, cleanedText))



def check_valid_word(checkedWord):
    '''
    Checks if the word we are adding is valid

    Args:
        checkedWord: Word to be tested
    
    Returns:
        True or False based on validity of word
    '''
    blacklist = ['Project', 'Gutenberg', '\ufeffthe', 'pglaf', 'ebooks,', '.']
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
        clean_input_text(
            import_text_file(
                'TextGeneration\\Frankenstein.txt'
            )))
    generate_frequency_JSON(wordDictionary, 'FrankensteinWordFrequency')
    startTime = time.time()
    if platform.system() == 'Linux':
        wordDictionary = read_frequency_JSON(
            'TextGeneration/FrankensteinWordFrequency.json')
    elif platform.system() == 'Windows':
        wordDictionary = read_frequency_JSON(
            'TextGeneration\\FrankensteinWordFrequency.JSON'
        )

    print(time.time() - startTime)
    for i in range(10):

        print(*generate_random_paragraph(wordDictionary, 30))
        print('\n')
