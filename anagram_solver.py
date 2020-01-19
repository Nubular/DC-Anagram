import itertools
import sys
from stuff import word_set


def find_possible(lst):
    """
    Return all possible combinations of letters in lst

    @type lst: [str]
    @rtype: [str]
    """
    returned_list = []
    for subset in itertools.permutations(lst,len(lst)):
        possible = ''
        for letter in subset:
            possible += letter
        if len(possible) == len(lst):
            returned_list.append(possible)
 
    return returned_list


def return_words(lst, word_set):
    """
    Return combinations in that are words in word_set

    @type lst: [str]
    @type word_set: set(str)
    @rtype: [str]
    """
    returned_list = []

    for word in lst:
        if word in word_set or word.capitalize() in word_set:
            # Some words are capitalized in the word_set
            returned_list.append(word)

    return returned_list


def find_words(word):
    """
    Main function to run the program
    """
    anagram_lst = []
    anagram = word
    
    for char in anagram:
        anagram_lst.append(char)

    possible_words = find_possible(anagram_lst)
    actual_words = return_words(possible_words, word_set)

    print('Solutions:')
    if len(actual_words) == 0:
        print('None found')
    else:
        for item in set(actual_words):
            # Running through in set form prevents duplicates
            print(item)
 

find_words('dunsay')