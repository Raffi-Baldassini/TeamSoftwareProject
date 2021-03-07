from random import choice, randint


with open("TextGeneration/Frankenstein.txt", encoding='UTF-8') as inputFile:
    inputText = inputFile.read()


def generateNGrams(textInput, order):

    nGrams = {}

    for charIndex in range(len(textInput) - (order - 1)):
        nGram = textInput[charIndex:charIndex + order]
        if nGram not in nGrams:
            nGrams[nGram] = []
        if charIndex + order >= len(textInput):
            break
        nGrams[nGram].append(textInput[charIndex + order])

    return nGrams


def markovGenerator(textInput, order, Textlength, nGrams=None):

    if not nGrams:
        nGrams = generateNGrams(textInput, order)
    position = randint(0, len(textInput) - order)
    currentNGram = textInput[position:position + order]
    markovString = currentNGram
    for i in range(Textlength):
        if currentNGram in nGrams:
            nextChars = nGrams[currentNGram]
            if nextChars != []:
                nextChar = choice(nextChars)
                markovString += nextChar
                currentNGram = markovString[(len(markovString) -
                                             order):len(markovString)]
            else:
                i -= 1
                currentNGram = markovString[(len(markovString) -
                                             order):len(markovString)]
    return markovString

if __name__ == '__main__':
    print('\nNGram order of 1:\n',markovGenerator(inputText, 1, 30))

    print('\nNGram order of 5:\n',markovGenerator(inputText, 5, 30))
