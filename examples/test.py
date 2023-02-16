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

print(arr2)