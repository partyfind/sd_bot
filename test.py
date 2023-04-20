from langdetect import detect
import random
import json
def get_random_prompt():
    arr = []
    with open('random.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['messages']:
            if i['text'] != '':
                arr.append(i['text'])
    n = random.randint(0, len(arr) - 1)
    print(arr[n])
    if detect(arr[n]) == 'ru':
        print(111)
        r = get_random_prompt()
    else:
        r = arr[n]
    return  r
print(222)
print(get_random_prompt())