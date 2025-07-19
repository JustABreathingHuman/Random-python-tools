import random
import math
import copy

#random hill climbing training

chardict = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','.',' '] #yeah maybe dont train division right now :/

def setup(height,layers):
    return [[0 for _ in range(height)] for _ in range(layers)]
#x is layers, y is height
#list[x][y]

def clamp(num,min,max):
    if num > max:
        num = max
    elif num < min:
        num = min
    else:
        pass
    return(num)
#self explanatory ahh

def bi(num,maxi):
    cache = []
    while maxi != 0:
        if num - (2 ** maxi)/2 >= 0:
            num = num - (2 ** maxi)/2
            cache.append('1')
        else:
            cache.append('0')
        maxi = maxi - 1
    cache = ''.join(cache)
    return(cache)
#to binary, first value is int, second value is binary places

def encode(string):
    global chardict
    out = []
    bikey = []
    for i in range(len(string)):
        out.append(chardict.index(str(string[i])))
    for i in range(len(out)):
        bikey.append(str(bi(out[i],4)))
    string = ''.join(bikey)
    return(string)
#encodes an expression with any of the characters from the dict to binary with 4 letters per character

def createlinks(list):
    layers = 0
    for i in range(len(list)):
        layers = layers + 1
        nodes = len(list[layers - 1])
    connections = []
    for layer in range(layers - 1):
        layer_connections = []
        for node in range(nodes):
            next_layer_connections = [0 for _ in range(nodes)]
            layer_connections.append(next_layer_connections)
        connections.append(layer_connections)
    return connections
#creates links (effectors) for each node to the next node automatically based on the list

def randomiselinks(links, amount):
    links_copy = copy.deepcopy(links)
    for i in range(len(links_copy)):
        for j in range(len(links_copy[i])):
            for k in range(len(links_copy[i][j])):
                links_copy[i][j][k] = round(
                    links_copy[i][j][k] + clamp(random.randint(-100 * amount, 100 * amount) / 100, -1, 1), 2)
    return links_copy
#randomises all links values

def solvetobinary(expression):
    global chardict
    result = str(eval(expression))
    cache = []
    for i in range(len(result)):
        cache.append(bi(chardict.index(str(result[i])),4))
    for i in range(5 - len(cache)):
        cache.insert(0,bi(chardict.index(' '),4))
    return(''.join(cache))
#allows an equation in the form of a string to be solved, and then outputs in accordance to chardict in blocks of binary

def decode(binary):
    global chardict
    if len(binary) % 4 != 0:
        raise ValueError("Binary string length must be a multiple of 4")
    out = ''
    for i in range(int(len(binary)/4)):
        cache = ''
        for j in range(4):
            cache = cache+binary[j+(i*4)]
        cache = baseten(cache)
        cache = chardict[cache]
        out = out+str(cache)
    return(out)
#decodes binary code in blocks of 4 in accordance to chardict

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
#weighted average or smth idk

def baseten(binary):
    binary = str(binary)
    cache = 0
    for i in range(len(binary)):
        if binary[i] == '1':
            cache += 2 ** (len(binary) - i - 1)
    return(cache)
#converts binary to base 10

def calculateforwards(nodes, links):
    for i in range(len(links)):
        for k in range(len(links[i][0])):
            total_input = 0
            for j in range(len(links[i])):
                total_input += nodes[i][j] * links[i][j][k]
            nodes[i+1][k] = round(sigmoid(total_input),2)
    return nodes
#calculates all nodes with weights and averages of links

def loadnode(list,binary):
    binary = str(binary)
    for i in range(len(binary)):
        list[0][i] = int(binary[i])
    return(list)
#inserts all primary input nodes into network

def extractnode(list):
    out = []
    for i in range(len(list[-1])):
        out.append(str(round(list[-1][i])))
    cache = ''.join(out)
    return(cache)
#extracts all output nodes from network

def generatedata():
    global chardict
    cache = []
    op1 = random.randint(1,9)
    op2 = random.randint(1,9)
    oper = chardict[random.randint(10,10)] #only addition :/
    if random.randint(0,0) == 1: # only second option, FIX LATER
        cache.append(op1)
        cache.append(oper)
        cache.append(op2)
        for i in range(2):
            cache.append(' ')
    else:
        cache.append(op1)
        cache.append(' ')
        cache.append(oper)
        cache.append(' ')
        cache.append(op2)
    cache = encode(cache)
    return(cache)
#generates a random equation into binary

def compare(str1,str2):
    cache = 0
    for i in range(len(str(str1))):
        if str(str1[i]) == str(str2[i]):
            cache = cache + 1
    return(cache)
#compares two strings by letter similarity

def train(network, links, random):
    load = generatedata()
    load_decoded = decode(load)
    correctbinary = solvetobinary(load_decoded)
    load_encoded = encode(load_decoded)

    network_old = loadnode(copy.deepcopy(network), load_encoded)
    network_old = calculateforwards(network_old, links)
    out_old = extractnode(network_old)

    links_new = randomiselinks(links, random)
    network_new = loadnode(copy.deepcopy(network), load_encoded)
    network_new = calculateforwards(network_new, links_new)
    out_new = extractnode(network_new)

    score_old = compare(correctbinary, out_old)
    score_new = compare(correctbinary, out_new)

    if score_new > score_old:
        return links_new
    else:
        return links
#training using score comparison

def networksolvebinary(network, links, binary):
    binary = str(binary)
    network = loadnode(network, binary)
    network = calculateforwards(network, links)
    out = extractnode(network)
    return(out)
#uses the network to solve a binary string

def solveusertobinary(network, links):
    question = input('input simple operation (eg. 1 + 3, 2 + 5): ')
    question = encode(question)
    output = networksolvebinary(network, links, question)
    return(output)
#the network solves the user's input, auto converts from str to binary

def traingeneration(network, links, random, generations, log):
    for i in range(generations):
        for j in range(100):
            links = train(network, links, random)
        if log == 1:
            test = generatedata()
            out = networksolvebinary(network, links, test)
            test = decode(test)
            correct = solvetobinary(test)
            score = compare(out, correct)
            question = '1 + 1'
            question = encode(question)
            benchmark = networksolvebinary(network, links, question)
            benchmark = decode(benchmark)
            print(score,", generation: ",i + 1,". currently, 1 + 1 is: ",benchmark)
    return(links)
#trains with score comparison in groups of 100, can log output

# Example run
network = setup(20, 10)
links = createlinks(network)
links = randomiselinks(links, 1)

print(calculateforwards(network, links))
decodestr = '1+2'
decodestr = encode(decodestr)
network = loadnode(network, decodestr)
print(calculateforwards(network, links))
print(extractnode(network))
print(decode(extractnode(network)))
print(generatedata())

print(decode(solveusertobinary(network, links)))

links = traingeneration(network, links, 0.1, 500, 1)
print(decode(solveusertobinary(network, links)))


#print(links)
#print(solvetobinary('1+1'))
#print(decode(solvetobinary('1+1')))
#print(baseten('0101'))

#uhh so basically input is still binary, but now the weights can be negative. just round((output +1)/2) to get binary again