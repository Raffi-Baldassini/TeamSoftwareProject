from gutenberg.acquire import load_etext, get_metadata_cache
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts, get_metadata, list_supported_metadatas
import os, platform
from RandomCharacterMarkovChains import import_text_file, generate_frequency_JSON, read_frequency_JSON
from RandomWordMarkovGenerator import generate_word_dictionary, clean_input_text

gutenbergCodes = [84, 1342, 64317, 1080, 11, 98, 25344, 5200]
gutenbergDict = {}

'''
These two lines are required to run this code, however, the cache.populate() method takes a few hours to complete.
It is not recommended that you use this script unless you have a need to/intend to expand on its functionality
cache = get_metadata_cache()
cache.populate()
'''

def setup():
    '''
    Scrapes the books in gutenbergCodes and adds them to text generation directory, only needs to run once
    '''
    for code in gutenbergCodes:
        title = list(get_metadata('title', code))
        title = title[0].split(':')
        title = title[0].split(';')
        title = title[0].split('\r')
        title = title[0].strip()
        title = title.replace(' ', '_')
        gutenbergDict[code] = (title)
    for code in gutenbergDict:
        book = strip_headers(load_etext(code)).strip()
        with open(f'TextGeneration\\Texts\\{gutenbergDict[code]}.txt',
                  'w',
                  encoding='UTF-8') as output:
            output.write(book)
        wordDict = generate_word_dictionary(clean_input_text(book))
        generate_frequency_JSON(
            wordDict,
            f'FrequencyDictionaries\\{gutenbergDict[code]}_Word_Frequency')


def dict_clean():

    '''
    Cleans the text of the books, and outputs the frequency dictionaries.
    Needs to run each time generate_word_dictionary, or clean_input_text is updated
    '''
    if platform.system() == 'Linux':
        books = os.listdir('TextGeneration/Texts')
        books.remove('EnglishWords.txt')
        for book in books:
            filepath = f'TextGeneration/Texts/{book}'
            with open(filepath, encoding='UTF-8') as book_text:
                wordDict = generate_word_dictionary(
                    clean_input_text(book_text.read()))
            book = book[0:-4]
            generate_frequency_JSON(
                wordDict, f'FrequencyDictionaries/{book}_Word_Frequency')

    elif platform.system() == 'Windows':
        books = os.listdir('TextGeneration\\Texts')
        books.remove('EnglishWords.txt')
        for book in books:

            filepath = 'TextGeneration\\Texts\\' + book
            with open(filepath, encoding='UTF-8') as book_text:
                wordDict = generate_word_dictionary(
                    clean_input_text(book_text.read()))
            book = book[0:-4]
            generate_frequency_JSON(
                wordDict, f'FrequencyDictionaries\\{book}_Word_Frequency')


if __name__ == '__main__':

    dict_clean()