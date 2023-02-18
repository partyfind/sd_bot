import json
import random
import math
#print('fu fu fun-21'.find('fun-22'))
arr = []
arr2 = []
i = 1
for j in ['11','22','33','44','55']:
    arr.append([j])
    if i % 3 == 0:
        arr2.append(arr)
        arr = []
    i += 1
if arr != []:
    arr2.append(arr)

#print(arr2)
#with open("random.json") as file:
    #r = json.load(file)
#print(r)

arr = []
with open('random.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for i in data['messages']:
        if i['text'] != '':
            arr.append(i['text'])
print(data['messages'][222]['text'])
#print(math.ceil(random.uniform(1, 3000)))
