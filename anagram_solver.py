import itertools
import sys
from word_set import word_set
import asyncio
 
async def return_words(freq):
    returned_list = []
    for string in word_set:
        word_freq = [0]*26
        flag=True
        for char in string:
            if(char>='a' and char <='z'):
                word_freq[ord(char)-ord('a')]+=1
            elif(char>='A' and char <='Z'):
                word_freq[ord(char)-ord('A')]+=1
            else:
                flag=False
                break
        if word_freq==freq and flag:
            returned_list.append(string)
    return returned_list


async def find_words(word):


    anagram = word
    freq = [0]*26
    
    for char in anagram:
        if(char>='a' and char <='z'):
            freq[ord(char)-ord('a')]+=1
        else:
            freq[ord(char)-ord('A')]+=1


    actual_words = await return_words(freq)
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
    words = await find_words("aergon")
    for string in words:
        print(string)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())