num = 0
c = 0
score = 0
j = 0
i = 0
clist = []
moves = 0

def solve(number):
    global oldscore
    global c
    global i
    global k
    global listedc
    global num
    global score
    global moves    
    
    score = 0
    while score != 16:
        moves = 0
        for j in range(4):
            c = clist[number]
            listedc = list(c)
            for k in range(4):
                score = 0
                for i in range(16):
                    num = listedc[i]
                    score = score + int(num)
                oldscore = score
                listedc[k + (j * 4)] = 1 - int(listedc[k + (j * 4)])
                for i in range(16):
                    num = listedc[i]
                    score = score + int(num)
                if oldscore > score:
                    listedc[k + (j * 4)] = 1 - int(listedc[k + (j * 4)])
                else:
                    moves =+ 1
        print(listedc)
        c = "".join(int(listedc))
        print(c)
        for j in range(4):
            listedc = list(c)
            for k in range(4):
                score = 0
                for i in range(16):
                    num = listedc[i]
                    score = score + int(num)
                oldscore = score
                listedc[k * 4 + j] = 1 - int(listedc[k * 4  + j])
                for i in range(16):
                    num = listedc[i]
                    score = score + int(num)
                if oldscore > score:
                    listedc[k * 4 + j] = 1 - int(listedc[k * 4  + j])
                else:
                    moves =+ 1
        c = "".join(listedc)
        
        for j in range(4):
            listedc = list(c)
            for k in range(4):
                score = 0
                for i in range(16):
                    num = listedc[i]
                    score = score + int(num)
                oldscore = score
                oldlist = listedc
    print(moves)
    
for j in range(65535):  
    print('loading',round((j + 1)/655.35),'%')
    c = j
    c = int(c) + 1
    c = format(int(c), "016b")
    score = 0
    for i in range(16):
        num = c[i]
        score = score + int(num)
    if score % 2 == 0:
        clist.append(c)

print(len(clist))
#print(len(clist),'legal magic locks found!')
#for i in range(len(clist)):
#    solve(i)

oldscore = 0
listedc = []