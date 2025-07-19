import random
import time

health = 10
maxhealth = 10
attack = 2 
level = 1
exp = 0
explevelup = 10
stamina = 10
maxstamina = 10
money = 0

items = ['herbs', 'stick', 'stone', 'mushrooms', 'mushroom paste','minced herbs']
inventory = [0, 0, 0, 0, 0, 0]

def craft():
    craft = input('what do you want to craft? (type help to see recipes )')
    if craft == 'help':
        print('mushroom paste: 2 mushrooms')
        print('minced herbs: 3 herbs and a stone')
    
    else:
        
        amount = input('how many do you want to craft?')
        if amount.isnumeric():
            for i in range(int(amount)):
                if craft == 'mushroom paste':
                    time.sleep(0.1)
                    if inventory[3] >= 2:
                        inventory[3] -= 2
                        inventory[4] += 1    
                        print('you crafted mushroom paste')        
                
                elif craft == 'minced herbs':
                    time.sleep(0.2)
                    if inventory[0] >= 2 and inventory[2] >= 1:
                        inventory[0] -= 2
                        inventory[2] -= 1
                        inventory[5] += 1
                        print('you crafted minced herbs') 
                
                else:
                    print('sorry, could not find that item.')
    
    step()

def checkitem():
    checkitem = input('which number?')
    if checkitem.isnumeric():
        print('you have ',inventory[int(checkitem)] ,'of this item.')
        print(items[int(checkitem)])
    else:
        print('not a valid answer')
        
    step()

def explore():
    global stamina
    global level
    
    found = 0
    
    for i in range(random.randint(16,28 * ((level + 1) / 2))):
        if stamina > 0:
            time.sleep(0.2)
            stamina = stamina - 0.1
            print('exploring...')
            if random.randint(0,3) == 0:
                print('you found something!')
                gainitem(0,3,random.randint(1,3))
                found = found + 1
    efficiency = found / i
    print('your efficiency was', round(efficiency * 100),'%.')
    print(stamina)
    inventorycheck()

def gainitem(min, max, amount):
    for i in range(amount):
        target = random.randint(min, max)
        inventory[target] = inventory[target] + 1

def huntask():
    huntlevel = input('what level enemy do you wish to fight? ')
    if huntlevel.isnumeric():
        hunt(int(huntlevel))
    else:
        print('sorry, not a valid hunt level. must be a interger.')
        step()
    
def levelup():
    global exp
    global explevelup
    global level
    global health
    global maxhealth
    global attack
    global stamina
    global maxstamina
    exp = exp - explevelup
    explevelup = (explevelup + 5) * 2
    level = level + 1
    health = health + (health * 0.35)
    maxhealth = maxhealth + (maxhealth * 0.35)
    attack = attack + (attack * 0.25)
    maxstamina = maxstamina + (maxstamina * 0.6)
    stamina = maxstamina
    print('you have levelled up to level ', level,'. your max health is ', maxhealth,' and your max stamina is now' , maxstamina)
    print('you have ', health, ' health,', attack, ' attack and ',stamina, 'stamina')
    
def hunt(lvl):
    global health
    global attack
    global exp
    global explevelup
    level = float(lvl)
    enemyhealth = 2 * (level + random.randint(0,2))
    enemyattack = lvl + random.randint(0,1)
    while enemyhealth > 0:
        print("you attacked the enemy with", attack, "damage")
        enemyhealth = enemyhealth - attack
        print("enemy has ", enemyhealth, " health left")
        print(' ')
        
        time.sleep(0.75)
        
        if enemyhealth > 0:
            print("the enemy attacked you with", enemyattack, "damage")
            health = health - enemyattack
            print("you have ", health, " health left")
            print(' ')
            
            time.sleep(0.75)
            
            if health <= 0:
                print('you died')
                exit()
    gainexp = random.randint(2*lvl, 3* lvl)
    exp = exp + gainexp
    if exp >= explevelup:
        levelup()
    print('you defeated the enemy. you gained ', gainexp, 'exp')
    gainitem(0,lvl,random.randint(lvl,lvl * 3))
    print("you have ", health, " health left")
    print(' ')
    print('the enemy dropped some items and now your inventory is:')
    inventorycheck()
    
def useitem():
    
    global health
    global maxhealth
    global stamina
    global maxstamina
    
    item = input('which item do you want to use?')
    if item == 'herbs':
        if inventory[0] > 0:
            inventory[0] -= 1    
            print('you consumed one herb and healed', maxhealth * 0.05 + 1, 'health.')
            health = health + maxhealth * 0.05 + 1
            if health > maxhealth:
                health = maxhealth
            stamina = stamina + stamina * 0.2 + 2
            if stamina > maxstamina:
                stamina = maxstamina
            print('you now have', health, 'health.')
            print('you now have', stamina, 'stamina.')
            
    elif item == 'minced herbs':
        if inventory[5] > 0:
            inventory[5] -= 1    
            print('you consumed one minced herbs and healed', maxhealth * 0.11 + 2.3, 'health.')
            health = health + maxhealth * 0.11 + 2.3
            if health > maxhealth:
                health = maxhealth
            print('you now have', health, 'health.')
    
    else:
        print('sorry, could not find that item.')
    
    step()
    
def inventorycheck():
    print('you have:')
    for i in range(len(inventory)):
        if inventory[i] != 0:
            print('number of' ,items[i], ': ', inventory[i])
    
    step()
    
def town():
    global money
    global action 
    
    if action == 'sell':
        print('sellable items are:')
        print('mushroom paste for 15c each')
        item = input('which item?')
        amount = input('how much?')
        if item == 'mushroom paste':
            for i in range(int(amount)):
                if inventory[4] > 0:
                    money = money + 15
                    inventory[4] =- 1
    
    else:
        pass
    print(money)
    inventorycheck()
                
        
    
def step():
    
    print('')
    
    global inventory
    global items
    global exp
    global explevelup
    global maxhealth
    global health
    global attack
    global action
    
    do = input('what do you want to do? (help)')
    if do == 'help':
        print('hunt to kill other dogs, explore to find items. use inventory to see your items. checkitem to what item a number is, and craft to craft while useitem to use a item you have.')
        step()
    
    elif do == 'hunt':
        huntask()
        
    elif do == 'inventory':
        inventorycheck()
        
    elif do == 'profile':
        print('health', health)
        print('max health', maxhealth)
        print('attack', attack)
        print('exp', exp)
        print('exp needed to advance to the next level', explevelup)
        print('level', level)
        print('money', money)
        step()
    
    elif do == 'explore':
        explore()
    
    elif do == 'checkitem':
        checkitem()

    elif do == 'useitem':
        useitem()
    
    elif do == 'craft':
        craft()
    
    elif do == 'exit':
        exit()
        
    elif do == 'town':
        action = str(input('sell, buy or bank?'))
        town()
    
    else:
        print("sorry, there is no command called: '" ,do, "'. try again.")
        step()
        
step()