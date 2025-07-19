import math

num = 2
pi = 0

while True:
    pi = num * math.radians(math.sin(180 / num)) * 1
    num = num + 10000
    print(str(pi))