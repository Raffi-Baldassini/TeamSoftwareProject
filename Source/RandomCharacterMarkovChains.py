import json, random, time, platform


def import_text_file(filePath):
    '''
    Returns a file as a string
    
    Args:
        filePath: Path to desired file
    
    Returns:
        File as string

    '''

    with open(filePath, encoding='UTF-8') as wordFile:
        wordString = wordFile.read()
    return wordString


def generate_letter_frequency_dictionary(inputString):
    '''
    Creates a Dictionary containing letters that appeared and their total appearances

    Args:
        inputString: The String we want to generate the Frequency Dictionary for
    
    Returns:
        The created Dictionary
    '''

    frequencyDic = {}

    for char in inputString:
        if char.isalpha():
            if char not in frequencyDic:
                frequencyDic[char] = 0
            frequencyDic[char] += 1

    return frequencyDic


def generate_frequency_JSON(frequencyDictionary, fileName):
    '''
    Converts a python dictionary to JSON
    '''

    if platform.system() == 'Linux':
        with open(f'TextGeneration/{fileName}.json', 'w',
                  encoding='UTF-8') as frequencyOutput:
            json.dump(frequencyDictionary, frequencyOutput)
    elif platform.system() == 'Windows':
        with open(f'TextGeneration\\{fileName}.json', 'w',
                  encoding='UTF-8') as frequencyOutput:
            json.dump(frequencyDictionary, frequencyOutput)


def read_frequency_JSON(fileName):
    '''
    Reads a JSON file and returns it as a dictionary

    Args:
        fileName: Name of the file that should be read
    
    Returns:
        the converted JSON as a dictionary
    '''
    with open(fileName, 'r', encoding='UTF-8') as frequencyJSON:
        frequencyDictionary = json.load(frequencyJSON)

    return frequencyDictionary


def generate_random_string(frequencyDictionary, stringChars, stringLength):
    '''
    Generates a random string using the principles of Markov Chains

    Args:
        frequencyDictionary: dictionary containing letters and their total appearances
        stringChars: characters we want to use to generate our string
        stringLength: length of the generated string
    
    Returns:
        Random String
    '''

    charWeights = [frequencyDictionary[char] for char in stringChars]
    randomString = ''
    for i in range(stringLength):
        randomString += str(random.choices(stringChars,
                                           charWeights)).strip('[]"\'')

    return randomString


if __name__ == '__main__':

    startTime = time.time()
    if platform.system() == 'Linux':
        wordString = import_text_file('TextGeneration/Texts/EnglishWords.txt')
        letterDictionary = generate_letter_frequency_dictionary(wordString)
        letterDictionary = read_frequency_JSON(
            'TextGeneration/LetterFrequency.json')

    elif platform.system() == 'Windows':
        wordString = import_text_file(
            'TextGeneration\\Texts\\EnglishWords.txt')
        letterDictionary = generate_letter_frequency_dictionary(wordString)
        letterDictionary = read_frequency_JSON(
            'TextGeneration\\LetterFrequency.json')

    for i in range(10):
        print(
            generate_random_string(
                letterDictionary,
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                random.randint(4, 7)))
    print(f"{time.time() - startTime}")
