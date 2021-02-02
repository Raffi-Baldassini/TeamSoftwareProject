from random import choice


order = 5

# with open("test.txt") as inputFile:
#     inputText = inputFile.read()

def generateNGrams(textInput, order):

    nGrams = {}

    for charIndex in range(len(textInput)-(order-1)):
        nGram = textInput[charIndex:charIndex+order]
        if nGram not in nGrams:
            nGrams[nGram] = []
        if charIndex+order >= len(textInput):
            break
        nGrams[nGram].append(textInput[charIndex+order])

    
    return nGrams

def markovGenerator(textInput, order, Textlength, nGrams = None):

    if not nGrams:
        nGrams = generateNGrams(textInput, order)

    currentNGram = textInput[0:order]
    markovString = currentNGram
    for i in range(Textlength):
        if currentNGram in nGrams:
            nextChars = nGrams[currentNGram]
            if nextChars != []:
                nextChar = choice(nextChars)
                markovString += nextChar
                currentNGram = markovString[(len(markovString)-order):len(markovString)]
            else:
                i -= 1
                currentNGram = markovString[(len(markovString)-order):len(markovString)]
    return markovString

print(len(markovGenerator(inputText, order, 1000)))
