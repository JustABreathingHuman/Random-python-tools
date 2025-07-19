import random
import operator

def generate_equation(difficulty):
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    if difficulty == 'easy':
        num_range = range(1, 10)
        operations = ['+', '-']
    elif difficulty == 'medium':
        num_range = range(1, 50)
        operations = ['+', '-', '*', '/']
    else:  # hard
        num_range = range(1, 100)
        operations = ['+', '-', '*', '/']

    num1 = random.choice(num_range)
    num2 = random.choice(num_range)
    op = random.choice(operations)

    # Ensure division by zero is handled
    if op == '/' and num2 == 0:
        num2 = random.choice(num_range[1:])  # Choose another number avoiding zero

    equation = f"{num1} {op} {num2}"
    answer = round(opsop, 2)

    return equation, answer

def main():
    difficulty = input("Choose your difficulty (easy, medium, hard): ").lower()
    while difficulty not in ['easy', 'medium', 'hard']:
        print("Invalid difficulty. Please choose 'easy', 'medium', or 'hard'.")
        difficulty = input("Choose your difficulty (easy, medium, hard): ").lower()

    equation, answer = generate_equation(difficulty)
    print(f"Solve the following equation: {equation}")

    try:
        user_answer = float(input("Your answer: "))
        if user_answer == answer:
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer was: {answer}")
    except ValueError:
        print("Invalid input. Please enter a numerical answer.")

if __name__ == "__main__":
    main()