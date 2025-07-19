import time
import random

def repeatLoading(word,times,waitafter):
    for i in range(times):
        print(word + '.')
        time.sleep(10 / random.randint(1, 1000))
        print(word + '..')
        time.sleep(10 / random.randint(1, 1000))
        print(word + '...')
        time.sleep(10 / random.randint(1, 1000))
        time.sleep(waitafter)

def loadingscreen():
    repeatLoading('booting', 3, 2)
    print('auxilary power functions normal.')
    repeatLoading('Loading cmd-systems', 1, 2)    
    print('power low - x-system not available.')
    
    loadingcontinue = input('continue loading? y/n   ')
    
    if loadingcontinue == 'y   ':
        pass
    elif loadingcontinue == 'n':
        repeatLoading('closing', 1, 0)
        exit()
        
    repeatLoading('normalizing systems' , 2, 1)
    
    print('done')
    
loadingscreen()