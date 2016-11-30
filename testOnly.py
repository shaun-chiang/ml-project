randArray = [323,748,2346,9,45.04,425.3,2346,2790]
randArray.sort(reverse=True)
print(randArray)
smallArray = randArray[:3]
print(smallArray)

if 2346 in smallArray:
    print(2346 in smallArray)
    smallArray.remove(2346)
else:
    print(False)
print(smallArray)
if 2346 in smallArray:
    print(2346 in smallArray)
    smallArray.remove(2346)
else:
    print(False)
print(smallArray)
if 2346 in smallArray:
    print(2346 in smallArray)
    smallArray.remove(2346)
else:
    print(False)
print(smallArray)