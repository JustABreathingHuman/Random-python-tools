import random
import math
import json

def setup(height, layers):
    return [[0 for _ in range(height)] for _ in range(layers)]

def createlinks(network):
    layers = len(network)
    nodes = len(network[0])
    connections = []
    for layer in range(layers - 1):
        layer_connections = []
        for _ in range(nodes):
            next_layer_connections = [0 for _ in range(nodes)]
            layer_connections.append(next_layer_connections)
        connections.append(layer_connections)
    return connections

def sigmoid(x):
    x = max(min(x, 20), -20)
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def forwards(network, links):
    for i in range(len(links)):
        for j in range(len(links[i][0])):
            total = 0
            for k in range(len(links[i])):
                total += links[i][k][j] * network[i][k]
            network[i + 1][j] = sigmoid(total)
    return network

def randomiselinks(links, amount=0.1):
    for i in range(len(links)):
        for j in range(len(links[i])):
            for k in range(len(links[i][j])):
                links[i][j][k] = random.uniform(-amount, amount)
    return links

def loadnode(network, binary):
    binary = str(binary)
    for i in range(len(binary)):
        network[0][i] = int(binary[i])
    return network

def extractnode(network):
    return [str(network[-1][i]) for i in range(len(network[-1]))]

def outtobinary(output_list):
    return ''.join(['1' if float(x) > 0.5 else '0' for x in output_list])

def backpropagate(network, links, target, learning_rate):
    target_vals = [int(bit) for bit in target]
    output_layer = network[-1]

    output_errors = [(output_layer[i] - target_vals[i]) * sigmoid_derivative(output_layer[i])
                      for i in range(len(output_layer))]

    for l in reversed(range(len(links))):
        for i in range(len(links[l])):
            for j in range(len(links[l][i])):
                input_val = network[l][i]
                error = output_errors[j]
                delta = learning_rate * error * input_val
                links[l][i][j] -= delta

        if l > 0:
            new_errors = []
            for i in range(len(links[l])):
                back_error = 0
                for j in range(len(links[l][i])):
                    back_error += links[l][i][j] * output_errors[j]
                new_errors.append(back_error * sigmoid_derivative(network[l][i]))
            output_errors = new_errors

    return links

def generate(length):
    return ''.join([str(random.randint(0, 1)) for _ in range(length)])

def flipbits(binary_str):
    return ''.join('1' if bit == '0' else '0' for bit in binary_str)

def trainlog(network, links, epoches, groups, learnrate=0.1):
    for i in range(groups):
        for j in range(epoches):
            target = generate(len(network[0]))
            network = loadnode(network, target)
            network = forwards(network, links)
            links = backpropagate(network, links, flipbits(target), learnrate)
        print(f"Group {i+1} complete.")
    return links

def networksolve(network, links, binary):
    network = loadnode(network, binary)
    network = forwards(network, links)
    return extractnode(network)

def test(network, links):
    testinput = input('Enter a '+str(len(network[0]))+' digit binary text. (E) to exit testing mode. >')
    if testinput != 'e':
        try:
            raw_output = networksolve(network, links, testinput)
            print("Raw out: ", [f"{float(x):.3f}" for x in raw_output])
            print("Binary:  ", outtobinary(raw_output))
        except:
            print('Invalid input.')
        test(network, links)
    else:
        step(network, links)

def step(network, links):
    print('Train(T), Test(Q), Save(S), Load(L), or Exit(E)?')
    do = input('> ')
    if do == 't':
        try:
            epoches = int(input('population?'))
        except:
            print('Invalid input')
            step(network, links)
        try:
            groups = int(input('generation?'))
        except:
            print('Invalid input')
            step(network, links)
        try:
            trainrate = float(input('learning rate: (default is 0.1)'))
        except:
            trainrate = 0.1
        links = trainlog(network, links, epoches, groups, trainrate)
        step(network, links)
    elif do == 'q':
        test(network, links)
    elif do == 's':
        name = input('File name: ')
        with open(name, 'w') as f:
            json.dump(links, f)
        print('links saved')
        step(network, links)
    elif do == 'l':
        name = input('Load: ')
        try:
            with open(name,'r') as f:
                loadlinks = json.load(f)
                loadlength = len(loadlinks)
                if len(links) == loadlength:
                    links = loadlinks
                else:
                    print("file has different network size")
            print('successfully loaded')
        except:
            print('failed to load file')
        step(network, links)
    elif do == 'e':
        print('computing finished')
        pass
    else:
        print('Invalid command')
        step(network, links)

network = setup(7, 4)
links = createlinks(network)
links = randomiselinks(links, 0.1)

step(network, links)