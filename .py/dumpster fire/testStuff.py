pi = 0
n = 1

while True:
    pi = pi + 4 / n
    n = n + 2
    pi = pi - 4 / n
    n = n + 2
    print(pi)