import random
import math
        
def random_function(difficulty, textinput):
    
    difficulty = input(textinput)
    
    if difficulty == "Easy":
        x = (random.randint(1,10))
        y = (random.randint(1,10))
    elif difficulty == "Medium":
        x = (random.randint(5,25))
        y = (random.randint(5,25))
    elif difficulty == "Hard":
        x = (random.randint(10,100))
        y = (random.randint(10,100))
    else:    
        restart('bozo THAT WAS NOT A DIFFICULTYYYYYY! Easy, Medium, Hard')
    
    ThingyThatIsUseful = random.randint(0,3) #choose number from 0 to 3
    
    ops = [ '+' , '-' , '*' , '/'] #operators are +,-,*,/
    
    equation = f"{x} {ops[ThingyThatIsUseful]} {y}" # equation is x, random item from list, y
    print(f"Your random question is: {equation}")

    expression = str(x) + ops[ThingyThatIsUseful] + str(y) #buddy this aint working before because the variable 'operator' wasn't a thing, it was called 'ops'

    CorrectAnswer = eval(expression)

    UserAnswer = input('Type your anwser here:')

    if UserAnswer == str(CorrectAnswer):
        print('well done bozo')
        
        restart("nice job. try harder ones. Easy, Medium or Hard?")
        
    elif UserAnswer == 'idk':

        print('lol you stupid')
        
        restart('Blud try Easy First before you do Hard or Medium.')
        
    else:
        print("Wrong , it is "+ str(CorrectAnswer)) # JUST ADD A SPACE IN THE "WRONG " IT WORKS THE SAME
    
    restart('please do Easy instead of Medium or Hard.')

    
    #difficulty = input("Choose the difficulty you would like. The options are Easy, Medium and Hard.")

def restart(textinput):
        random_function(None, textinput)
        exit()

random_function(None, 'choose a difficulty that suits you. Easy, Medium and Hard.') # parameters are difficulty, and the prompt that is displayed in the Input.

