import itertools
import sys
from stuff import word_dict
import asyncio


async def find_possible(lst):

    returned_list = []
    for subset in itertools.permutations(lst,len(lst)):
        possible = ''
        for letter in subset:
            possible += letter
        if len(possible) == len(lst):
            returned_list.append(possible)
 
    return returned_list

def binary_search_string(word,lst):
    lower = 0
    upper = len(lst) - 1
    while(lower<=upper):
        mid = (lower + upper)//2
        midpoint = lst[mid]
        if midpoint > word:
            upper = mid - 1
        elif midpoint < word:
            lower = mid + 1
        elif lst[mid] == word:
            return True
    return False

async def return_words(lst, word_set):

    returned_list = []

    for word in lst:
        if binary_search_string(word,word_dict[len(word)]) or  binary_search_string(word.capitalize(),word_dict[len(word)]):
            # Some words are capitalized in the word_set
            returned_list.append(word)

    return returned_list


async def find_words(word):

    anagram_lst = []
    anagram = word
    
    for char in anagram:
        anagram_lst.append(char)

    possible_words = await find_possible(anagram_lst)
    actual_words = await return_words(possible_words, word_dict)
    answer = []
    if len(actual_words) == 0:
        print('None found')
        answer.append('None Found')
        return answer
    else:
        for item in set(actual_words):
            # Running through in set form prevents duplicates
            answer.append(item)
        return answer

