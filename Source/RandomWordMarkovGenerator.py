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
    wordList = inputString.split()
    wordDictionary = {}
    for i in range(len(wordList) - 1):
        #Not necessary to define these variables, but makes functionality clear
        currentWord = wordList[i]
        nextWord = wordList[i + 1]
        if currentWord not in wordDictionary:
            wordDictionary[currentWord] = {nextWord: 1}
        if nextWord not in wordDictionary[currentWord]:
            wordDictionary[currentWord][nextWord] = 0
        wordDictionary[currentWord][nextWord] += 1

    return wordDictionary


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

    # wordDictionary = generate_word_dictionary(
    #     import_text_file(
    #         'c:\\Users\\Raffi\\Documents\\College\\Programming\\TeamSoftwareProject\\Source\\TextGeneration\\Frankenstein.txt'
    #     ))
    # generate_frequency_JSON(wordDictionary, 'FrankensteinWordFrequency')
    startTime = time.time()
    if platform.system() == 'Linux':
        wordDictionary = read_frequency_JSON('TextGeneration/FrankensteinWordFrequency.JSON')
    elif platform.system() == 'Windows':
        wordDictionary = read_frequency_JSON('TextGeneration\\FrankensteinWordFrequency.JSON')
    print(time.time() - startTime)
    for i in range(1):
        
        print(*generate_random_paragraph(wordDictionary, 20))
        
