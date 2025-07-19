import random
import math
import copy
import json

chardict = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','.',' ']

def setup(height,layers):
    # Creates network nodes: layers x height nodes initialized to zero
    return [[0 for _ in range(height)] for _ in range(layers)]

def clamp(num,min,max):
    # Clamps num between min and max
    if num > max:
        num = max
    elif num < min:
        num = min
    return num

def bi(num,maxi):
    # Convert num to binary string of length maxi + 1 bits
    # but the code is off by 1? The way you do (2 ** maxi)/2 is confusing.
    # Let's clarify and fix this:
    bits = []
    for i in range(maxi, -1, -1):  # from max bit down to 0
        if num >= 2**i:
            bits.append('1')
            num -= 2**i
        else:
            bits.append('0')
    return ''.join(bits)


def encode(string):
    global chardict
    out = []
    for i in range(len(string)):
        out.append(chardict.index(str(string[i])))
    bikey = []
    for val in out:
        bikey.append(bi(val, 4))
    binary_string = ''.join(bikey)
    # Ensure 20 bits total (5 chars * 4 bits)
    binary_string = binary_string.ljust(20, '0')[:20]
    return binary_string

def createlinks(list_):
    # Creates connections for each node in one layer to each node in next layer
    layers = len(list_)
    nodes = len(list_[0]) if layers > 0 else 0
    connections = []
    for layer in range(layers - 1):
        layer_connections = []
        for node in range(nodes):
            next_layer_connections = [0 for _ in range(nodes)]
            layer_connections.append(next_layer_connections)
        connections.append(layer_connections)
    return connections

def randomiselinks(links, amount):
    # Randomly perturb link weights by amount within [-1, 1]
    links_copy = copy.deepcopy(links)
    for i in range(len(links_copy)):
        for j in range(len(links_copy[i])):
            for k in range(len(links_copy[i][j])):
                delta = random.uniform(-amount, amount)
                links_copy[i][j][k] = clamp(round(links_copy[i][j][k] + delta, 2), -1, 1)
    return links_copy

def solvetobinary(expression):
    # Evaluate expression, convert result to binary based on chardict indices
    global chardict
    try:
        result = str(eval(expression))
    except Exception as e:
        # Avoid crashes on bad input
        result = ' ' * 5

    cache = []
    for ch in result:
        try:
            idx = chardict.index(ch)
        except ValueError:
            idx = chardict.index(' ')  # fallback space for unknown chars
        cache.append(bi(idx, 3))  # 4 bits per char

    # pad to length 5 (20 bits)
    while len(cache) < 5:
        cache.insert(0, bi(chardict.index(' '), 3))

    return ''.join(cache)

def decode(binary):
    global chardict
    if len(binary) % 4 != 0:
        raise ValueError("Binary string length must be a multiple of 4")
    out = ''
    for i in range(len(binary) // 4):
        block = binary[i*4:(i+1)*4]
        idx = baseten(block)
        if idx >= len(chardict):
            idx = chardict.index(' ')  # safeguard
        out += chardict[idx]
    return out

def sigmoid(x):
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0 if x < 0 else 1

def baseten(binary):
    # Convert binary string to integer
    return int(binary, 2)

def calculateforwards(nodes, links):
    # Calculate activations forward through the network
    for layer_idx in range(len(links)):
        for node_idx_next in range(len(links[layer_idx][0])):
            total_input = 0
            for node_idx_current in range(len(links[layer_idx])):
                total_input += nodes[layer_idx][node_idx_current] * links[layer_idx][node_idx_current][node_idx_next]
            nodes[layer_idx + 1][node_idx_next] = round(sigmoid(total_input), 2)
    return nodes

def loadnode(list_, binary):
    input_size = len(list_[0])
    binary = str(binary)
    # Pad or truncate to fit input size
    binary = binary.ljust(input_size, '0')[:input_size]
    for i in range(input_size):
        list_[0][i] = int(binary[i])
    return list_

def extractnode(list_, soft=False):
    # Extract output nodes from final layer, optionally soft round
    out = []
    for val in list_[-1]:
        if soft:
            val = soft_round(val)
        else:
            val = round(val)
        out.append(str(int(val)))
    return ''.join(out)

def generatedata():
    global chardict
    cache = []
    op1 = random.randint(1,9)
    op2 = random.randint(1,9)
    oper = chardict[10]  # only addition '+'
    if random.randint(0, 0) == 1:
        cache.append(str(op1))
        cache.append(oper)
        cache.append(str(op2))
        for _ in range(2):
            cache.append(' ')
    else:
        cache.append(str(op1))
        cache.append(' ')
        cache.append(oper)
        cache.append(' ')
        cache.append(str(op2))
    encoded = encode(cache)
    return encoded

def soft_round(x, steepness=10):
    return 1 / (1 + math.exp(-steepness * (x - 0.5)))

def compare(str1, str2):
    # Updated compare to reward matches and penalize mismatches gently
    if len(str1) != len(str2):
        raise ValueError("Strings must be same length")
    score = 0
    for b1, b2 in zip(str1, str2):
        if b1 == b2:
            score += 1
        else:
            score -= 0.5
    return score

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

def networksolvebinary(network, links, binary, hard):
    network = loadnode(copy.deepcopy(network), binary)
    network = calculateforwards(network, links)
    out = extractnode(network, hard)
    return out

def solveusertobinary(network, links):
    question = input('input simple operation (eg. 1 + 3, 2 + 5): ')
    question = encode(question)
    output = networksolvebinary(network, links, question, False)
    return output

def traingeneration(network, links, random, population, samplesize, log):
    linkscache = [links]
    networkscorecache = []
    testscache = [generatedata() for _ in range(samplesize)]

    def hamming_distance(s1, s2):
        assert len(s1) == len(s2)
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

    def diversity_score(outputs):
        n = len(outputs)
        if n < 2:
            return 0
        total_distance = 0
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                total_distance += hamming_distance(outputs[i], outputs[j])
                count += 1
        return total_distance / count

    CORRECTNESS_WEIGHT = 1.0
    DIVERSITY_WEIGHT = 0.5  # low weight to avoid ignoring correctness

    # Baseline
    score = 0
    baseline_outputs = []
    for i in range(samplesize):
        out = networksolvebinary(network, links, testscache[i], False)
        baseline_outputs.append(out)
        decoded = decode(testscache[i])
        correct = solvetobinary(decoded)
        score += compare(correct, out)
    diversity = diversity_score(baseline_outputs)
    networkscorecache.append(CORRECTNESS_WEIGHT * score + DIVERSITY_WEIGHT * diversity)

    # Population candidates
    for i in range(population):
        candidate_links = copy.deepcopy(linkscache[0])
        candidate_links = train(network, candidate_links, random)
        score = 0
        candidate_outputs = []
        for n in range(samplesize):
            out = networksolvebinary(network, candidate_links, testscache[n], False)
            candidate_outputs.append(out)
            decoded = decode(testscache[n])
            correct = solvetobinary(decoded)
            score += compare(correct, out)
        diversity = diversity_score(candidate_outputs)
        networkscorecache.append(CORRECTNESS_WEIGHT * score + DIVERSITY_WEIGHT * diversity)
        linkscache.append(candidate_links)

    # Pick best
    best_score = float('-inf')
    best_index = 0
    for i in range(len(linkscache)):
        if networkscorecache[i] > best_score:
            best_score = networkscorecache[i]
            best_index = i

    output = [linkscache[best_index]]
    if log == 1:
        output.append(networkscorecache[best_index] / samplesize)
    return output

def trainnetwork(network, links):
    test = '1 + 1'
    test = encode(test)
    generations = int(input('how many generations? '))
    for i in range(generations):
        output = traingeneration(network, links, 0.2, 5, 50, 1)
        links = output[0]
        benchmark = networksolvebinary(network, links, test, False)
        benchmark = decode(benchmark)
        print(f'gen {i + 1}. average score: {round(output[1], 2)}. currently, 1 + 1 is: {benchmark}')
    run(network, links)

def run(network, links):
    while True:
        choose = input('keep training, save, load, test or stop? y/s/l/t/n ')
        if choose == 'y':
            trainnetwork(network, links)
        elif choose == 's':
            with open('output.txt', 'w') as f:
                json.dump(links, f)
        elif choose == 'l':
            with open('output.txt', 'r') as f:
                links = json.load(f)
        elif choose == 't':
            print(decode(solveusertobinary(network, links)))
        elif choose == 'n':
            break
        else:
            print('invalid input')

# Initialize network and links
network = setup(20, 10)
links = createlinks(network)
links = randomiselinks(links, 1)
print(decode(solveusertobinary(network, links)))

run(network, links)
