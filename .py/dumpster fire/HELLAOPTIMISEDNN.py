import random
import math
import json
import time

def setup_network(height, layers):
    return [[0.0] * height for _ in range(layers)]

def create_links(network):
    layers, nodes = len(network), len(network[0])
    return [[[0.0 for _ in range(nodes)] for _ in range(nodes)] for _ in range(layers - 1)]

def sigmoid(x):
    x = max(min(x, 20), -20)
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def forward_pass(network, links):
    for layer in range(len(links)):
        for j in range(len(links[layer][0])):
            total_input = sum(links[layer][i][j] * network[layer][i] for i in range(len(links[layer])))
            network[layer + 1][j] = sigmoid(total_input)
    return network

def randomize_links(links, amount=0.1):
    for layer in links:
        for node_weights in layer:
            for i in range(len(node_weights)):
                node_weights[i] = random.uniform(-amount, amount)
    return links

def load_input(network, binary_str):
    for i, bit in enumerate(str(binary_str)):
        network[0][i] = int(bit)
    return network

def extract_output(network):
    return [str(x) for x in network[-1]]

def output_to_binary(outputs):
    return ''.join('1' if float(x) > 0.5 else '0' for x in outputs)

def backpropagation(network, links, target_binary, learning_rate):
    target = [int(b) for b in target_binary]
    output = network[-1]
    output_errors = [(output[i] - target[i]) * sigmoid_derivative(output[i]) for i in range(len(output))]

    for l in reversed(range(len(links))):
        for i in range(len(links[l])):
            for j in range(len(links[l][i])):
                delta = learning_rate * output_errors[j] * network[l][i]
                links[l][i][j] -= delta

        if l > 0:
            next_errors = []
            for i in range(len(links[l])):
                error = sum(links[l][i][j] * output_errors[j] for j in range(len(links[l][i])))
                next_errors.append(error * sigmoid_derivative(network[l][i]))
            output_errors = next_errors

    return links

def generate_binary(length):
    return ''.join(random.choice('01') for _ in range(length))

def flip_binary(binary_str):
    return ''.join('1' if b == '0' else '0' for b in binary_str)

def train(network, links, epochs, generations, learning_rate=0.1):
    input_size = len(network[0])

    tick = 0
    timeremaining = 0
    for g in range(generations):
        total_error = 10
        start_time = time.time()
        tick = tick + 1
        for _ in range(epochs):
            input_binary = generate_binary(input_size)
            expected_output = [int(b) for b in flip_binary(input_binary)]

            network = load_input(network, input_binary)
            network = forward_pass(network, links)

            actual_output = network[-1]
            # Mean squared error per output node
            total_error += sum((actual_output[i] - expected_output[i]) ** 2 for i in range(len(actual_output)))

            links = backpropagation(network, links, flip_binary(input_binary), learning_rate)

        avg_error = total_error / (epochs * input_size)
        generationsremaining = generations - g
        elapsed = time.time() - start_time
        if tick > 10:
            timeremaining = elapsed * generationsremaining
            tick = 0

        print(f"[✔] Generation {g + 1} complete | Avg Error: {avg_error:.5f} | Time remaining: {timeremaining:.2f}s")

    return links

def predict(network, links, binary_input):
    network = load_input(network, binary_input)
    network = forward_pass(network, links)
    return extract_output(network)

def test_loop(network, links):
    while True:
        user_input = input(f'Enter a {len(network[0])}-digit binary string or (E) to exit: ').strip().lower()
        if user_input == 'e':
            break
        if len(user_input) != len(network[0]) or any(c not in '01' for c in user_input):
            print("Invalid input. Must be binary of correct length.")
            continue
        raw_output = predict(network, links, user_input)
        print("Raw output: ", [f"{float(x):.3f}" for x in raw_output])
        print("Binary out:", output_to_binary(raw_output))

def save_links(links):
    name = input("File name to save: ").strip()
    try:
        with open(name, "w") as f:
            json.dump(links, f)
        print("[💾] Saved successfully.")
    except Exception as e:
        print("Save failed:", e)

def load_links():
    name = input("File name to load: ").strip()
    try:
        with open(name, "r") as f:
            links = json.load(f)
        print("[📂] Loaded successfully.")
        return links
    except Exception as e:
        print("Load failed:", e)
        return None

def main_loop():
    height, layers = 7, 4
    network = setup_network(height, layers)
    links = randomize_links(create_links(network), 0.1)

    while True:
        action = input("\n[Menu] Train(T), Test(Q), Save(S), Load(L), Exit(E): ").strip().lower()
        if action == 't':
            try:
                epochs = int(input("Epochs per generation: "))
                generations = int(input("Number of generations: "))
                lr = float(input("Learning rate (default 0.1): ") or "0.1")
                links = train(network, links, epochs, generations, lr)
            except ValueError:
                print("Invalid input.")
        elif action == 'q':
            test_loop(network, links)
        elif action == 's':
            save_links(links)
        elif action == 'l':
            loaded = load_links()
            if loaded:
                links = loaded
        elif action == 'e':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_loop()