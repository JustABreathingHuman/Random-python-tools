import random
numlist = []
thing = []

num = 0
for i in range(20):
    num = num + 1
    numlist.append(num)
    
print(numlist)

def randomlist():
    num = 0
    place = 0
    for j in range(20):
        place = random.randint(0 , len(numlist) - 1)
        thing.append(numlist[place])
        numlist.pop(place)
        num = num + 1
        
randomlist()

print(thing)