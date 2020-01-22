import itertools
import sys
from word_set import word_set
import asyncio

dictionary = {}

def make_dict():
    for word in word_set:
        word_freq = [0]*26
        for char in word:
            if(char>='a' and char <='z'):
                word_freq[ord(char)-ord('a')]+=1
            elif(char>='A' and char <='Z'):
                word_freq[ord(char)-ord('A')]+=1
        key = tuple(word_freq)
        if not key in dictionary:
            dictionary[key] = [word]
        else:
            dictionary[key].append(word)

async def find_words(anagram):

    word = anagram
    word_freq = [0]*26
    for char in word:
        if(char>='a' and char <='z'):
            word_freq[ord(char)-ord('a')]+=1
        elif(char>='A' and char <='Z'):
            word_freq[ord(char)-ord('A')]+=1
    try:
        actual_words = dictionary[tuple(word_freq)]
    except:
        actual_words = []

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

async def main():
    make_dict()
    words = await find_words("yunta")
    print(words)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())