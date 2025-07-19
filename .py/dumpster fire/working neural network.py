#working neural network thing

import numpy as np
import random

def generate_data(n_samples=20000):
    operators = ['+', '-', '*', '/']
    expressions = []
    results = []

    for _ in range(n_samples):
        a = random.randint(0, 9)
        b = random.randint(1, 9)
        op = random.choice(operators)

        # Add decimals with some probability
        if random.random() < 0.2:
            a = round(a / random.randint(1, 3), 1)
        if random.random() < 0.2:
            b = round(b / random.randint(1, 3), 1)

        expr = f"{a} {op} {b}"
        try:
            result = round(eval(expr), 2)
            if len(expr) <= 6:  # filter too-long expressions
                expressions.append(expr)
                results.append(result)
        except:
            continue  # skip division by zero

    return expressions, np.array(results).reshape(-1, 1)

char_to_index = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '+': 10, '-': 11, '*': 12, '/': 13, ' ': 14,
    '.': 15
}

def one_hot_encode(expr, max_len=6):
    vec = np.zeros((max_len, len(char_to_index)))
    for i, ch in enumerate(expr):
        vec[i, char_to_index[ch]] = 1
    return vec.flatten()

X_expr, y = generate_data(n_samples=20000)
X = np.array([one_hot_encode(expr, max_len=6) for expr in X_expr])
max_result = np.max(np.abs(y))
y = y / max_result  # normalize outputs

class SimpleNN:
    def __init__(self, input_size, hidden_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, 1) * 0.1
        self.b2 = np.zeros((1, 1))

    def relu(self, x):
        return np.maximum(0, x)

    def relu_deriv(self, x):
        return (x > 0).astype(float)

    def forward(self, x):
        self.z1 = x @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        return self.z2

    def backward(self, x, y, output, lr=0.001):
        error = output - y
        dW2 = self.a1.T @ error
        db2 = np.sum(error, axis=0, keepdims=True)

        da1 = error @ self.W2.T
        dz1 = da1 * self.relu_deriv(self.z1)
        dW1 = x.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # Clip gradients to prevent explosion
        max_grad = 1.0
        for grad in [dW1, db1, dW2, db2]:
            np.clip(grad, -max_grad, max_grad, out=grad)

        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W1 -= lr * dW1
        self.b1 -= lr * db1

    def train(self, x, y, epochs=2000, lr=0.001):
        for i in range(epochs):
            out = self.forward(x)
            self.backward(x, y, out, lr)
            if i % 100 == 0:
                loss = np.mean((out - y) ** 2)
                print(f"Epoch {i} | Loss: {loss:.6f}")

model = SimpleNN(input_size=X.shape[1], hidden_size=64)
model.train(X, y, epochs=5000, lr=0.001)

def predict(expr):
    encoded = one_hot_encode(expr, max_len=6).reshape(1, -1)
    pred = model.forward(encoded)
    return round(pred[0][0] * max_result, 2)

print("\nTest Results:")
test_cases = ["3 + 5", "9 - 2", "4 * 2", "8 / 2", "7 / 3", "6 / 0.5"]
for expr in test_cases:
    try:
        actual = round(eval(expr), 2)
        predicted = predict(expr)
        print(f"{expr} = {predicted} (expected: {actual})")
    except Exception as e:
        print(f"{expr} = Error: {e}")
