import random
import math
import copy

chardict = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','.',' ']

def setup(height,layers):
    out = []
    for _ in range(layers):
        layer = []
        for _ in range(height):
            layer.append(0)
        out.append(layer)
    return out
# simple 2D list init

def clamp(num,min,max):
    if num > max:
        return max
    elif num < min:
        return min
    else:
        return num
# clamp a number

def bi(num,maxi):
    cache = []
    while maxi != 0:
        if num - (2 ** maxi)/2 >= 0:
            num = num - (2 ** maxi)/2
            cache.append('1')
        else:
            cache.append('0')
        maxi = maxi - 1
    return ''.join(cache)
# int to binary str with maxi bits

def encode(string):
    global chardict
    out = []
    bikey = []
    for i in range(len(string)):
        out.append(chardict.index(string[i]))
    for i in range(len(out)):
        bikey.append(bi(out[i],4))
    return ''.join(bikey)
# encode string to binary string

def decode(binary):
    global chardict
    if len(binary) % 4 != 0:
        raise ValueError("Binary length not multiple of 4")
    out = ''
    for i in range(int(len(binary)/4)):
        cache = ''
        for j in range(4):
            cache += binary[j+(i*4)]
        dec = baseten(cache)
        out += chardict[dec]
    return out
# decode binary string to string

def baseten(binary):
    binary = str(binary)
    cache = 0
    for i in range(len(binary)):
        if binary[i] == '1':
            cache += 2 ** (len(binary) - i - 1)
    return cache
# binary string to int

def sigmoid(x):
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        if x < 0:
            return 0.0
        else:
            return 1.0
# sigmoid with overflow catch

def dsigmoid(x):
    return x * (1 - x)
# derivative of sigmoid assuming x already sigmoid(x)

def createlinks(list):
    layers = len(list)
    nodes = len(list[0])
    connections = []
    for layer in range(layers-1):
        layer_connections = []
        for node in range(nodes):
            next_layer_connections = []
            for _ in range(nodes):
                next_layer_connections.append(random.uniform(-1,1))
            layer_connections.append(next_layer_connections)
        connections.append(layer_connections)
    return connections
# create random weighted links from each layer node to next layer nodes

def loadnode(list,binary):
    binary = str(binary)
    for i in range(len(binary)):
        list[0][i] = int(binary[i])
    return list
# load input layer nodes

def calculateforwards(nodes, links):
    for i in range(len(links)):
        for k in range(len(links[i][0])):
            total_input = 0
            for j in range(len(links[i])):
                total_input += nodes[i][j] * links[i][j][k]
            nodes[i+1][k] = round(sigmoid(total_input),2)
    return nodes
# feedforward calculation through network

def extractnode(list):
    out = []
    for i in range(len(list[-1])):
        out.append(str(round(list[-1][i])))
    return ''.join(out)
# extract output layer as string

def solvetobinary(expression):
    global chardict
    result = str(eval(expression))
    cache = []
    for i in range(len(result)):
        cache.append(bi(chardict.index(result[i]),4))
    for i in range(5 - len(cache)):
        cache.insert(0, bi(chardict.index(' '),4))
    return ''.join(cache)
# evaluate expression and return padded binary string

def compare(str1,str2):
    score = 0
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            score += 1
    return score
# count matching bits

def trainbackprop(network, links, learning_rate=0.1):
    # generate training sample
    input_str = generate_expression()
    input_bin = encode(input_str)
    target_bin = solvetobinary(input_str)

    # load input
    network = loadnode(copy.deepcopy(network), input_bin)

    # forward pass
    network = calculateforwards(network, links)

    # prepare output layer error and delta
    output_layer = len(network) - 1
    output_nodes = len(network[output_layer])
    target = []
    for i in range(output_nodes):
        target.append(int(target_bin[i]))

    error = []
    delta = []
    for i in range(output_nodes):
        e = target[i] - network[output_layer][i]
        error.append(e)
        delta.append(e * dsigmoid(network[output_layer][i]))

    # backpropagate error
    for layer in reversed(range(len(links))):
        next_delta = [0 for _ in range(len(network[layer]))]
        for i in range(len(links[layer])):
            for j in range(len(links[layer][i])):
                # update weight
                change = learning_rate * delta[j] * network[layer][i]
                links[layer][i][j] += change
                next_delta[i] += links[layer][i][j] * delta[j]
        if layer != 0:
            # calc delta for previous layer
            new_delta = []
            for i in range(len(next_delta)):
                new_delta.append(next_delta[i] * dsigmoid(network[layer][i]))
            delta = new_delta

    return links
# train one step with backpropagation

def generate_expression():
    op1 = random.randint(1,9)
    op2 = random.randint(1,9)
    oper = '+'
    return str(op1) + oper + str(op2)
# generate simple addition expression string

def networksolvebinary(network, links, binary):
    binary = str(binary)
    network = loadnode(copy.deepcopy(network), binary)
    network = calculateforwards(network, links)
    out = extractnode(network)
    return out
# use network to solve binary input

def traingeneration(network, links, generations, log=0):
    for i in range(generations):
        for _ in range(100):
            links = trainbackprop(network, links, 0.3)
        if log == 1:
            question = '1+1'
            question_bin = encode(question)
            output = networksolvebinary(network, links, question_bin)
            output_decoded = decode(output)
            correct = solvetobinary(question)
            score = compare(output, correct)
            print(score, ", generation:", i + 1, ". currently, 1 + 1 is:", output_decoded)
    return links

# main

network = setup(20,10)
links = createlinks(network)

print("before training:")
print(decode(networksolvebinary(network, links, encode("1+1"))))

links = traingeneration(network, links, 300, log=1)

print("after training:")
print(decode(networksolvebinary(network, links, encode("1+1"))))
