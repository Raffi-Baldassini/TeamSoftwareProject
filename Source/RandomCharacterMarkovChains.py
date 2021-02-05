import json, random, time


def importTextFile(filePath):
    '''
    Returns a file as a string
    
    Args:
        filePath: Path to desired file
    
    Returns:
        File as string

    '''

    with open(filePath) as wordFile:
        wordString = wordFile.read()
    return wordString


def generateLetterFrequencyDictionary(inputString):
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

def generateFrequencyJSON(frequencyDictionary):

    '''
    Converts a python dictionary to JSON
    '''
    
    with open('LetterFrequency.json', 'w') as frequencyOutput:
        json.dump(frequencyDictionary, frequencyOutput)

def readFrequencyJSON(fileName):

    '''
    Reads a JSON file and returns it as a dictionary

    Args:
        fileName: Name of the file that should be read
    
    Returns:
        the converted JSON as a dictionary
    '''
    with open(fileName, 'r') as frequencyJSON:
        frequencyDictionary = json.load(frequencyJSON)

    return frequencyDictionary

def generateRandomString(frequencyDictionary, stringChars, stringLength):

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
        randomString += str(random.choices(stringChars, charWeights)).strip('[]"\'')
    
    return randomString

if __name__ == '__main__':
    
    startTime = time.time()
    #wordString = importTextFile('..\\corncob_lowercase.txt')
    #letterDictionary = generateLetterFrequencyDictionary(wordString)
    letterDictionary = readFrequencyJSON('TextGeneration\\LetterFrequency.JSON')
    print(generateRandomString(letterDictionary, list(letterDictionary.keys()), 26))
    print(f"{time.time() - startTime}")