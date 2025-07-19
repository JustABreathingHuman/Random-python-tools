from random import *

def step():
    do = input('what to do?')
    if do == 'hunt':
        lvl = input('difficulty')
        battle(int(lvl))
    elif do == 'character':
        charinit(input('which character?'))
        step()
    elif do == 'exit':
        exit()
    else:
        print('wtf')
        step()

def battle(lvl):
    battle = 1
    global char
    global hp
    global maxhp
    global atk
    global spd
    global enemyhp
    global sp
    enemyhp = 40 + (lvl*80)
    global enemymaxhp
    enemymaxhp = enemyhp
    global enemyatk
    enemyatk = 7+(lvl*5)
    global enemyspd
    enemyspd = 25+(lvl*5)
    
    global turn
    global av
    global enemyav
    global playerturn
    global enemyturn
    global credits
    sp = 3
    turninit()
    while battle == 1:
        print('')
        turn = turncalc()

        if hp <= 0:
            battle = 0
            print('battle lost')
        if enemyhp <= 0:
            battle = 0
            print('battle won')
        if enemyhp > 0 and hp > 0:
            if enemyav > av:
                if enemyturn == 1:
                    enemyaction()
                    enemyturn = 0
                if playerturn == 1:
                    action()
                    playerturn = 0
            else:
                if playerturn == 1:
                    action()
                    playerturn = 0
                if enemyturn == 1:
                    enemyaction()
                    enemyturn = 0
    credits = credits + 20 + random()*lvl*5
    step()

def turncalc():
    charactertalentchack()
    global spd
    global enemyspd
    global turn
    global av
    global enemyav
    global playerturn
    global enemyturn

    av = av + spd
    enemyav = enemyav + enemyspd
    if av >= 100:
        av = av - 100
        playerturn = 1
    if enemyav >= 100:
        enemyav = enemyav - 100
        enemyturn = 1
    
    return(turn)

def action():
    global sp
    global talent
    global talent2
    global char
    global atk
    global enemyhp
    global enemymaxhp
    global hp
    global maxhp
    print('skill points:', sp)

    if char == 'lance':
        do = input("b or s?(basic attack or skill)")
        if do == 'b':
            enemyhp = enemyhp - (atk * 0.5)
            print('used basic attack and dealt', (atk * 0.5) ,'damage')
            print('enemy health:', round(100*(enemyhp / enemymaxhp)),'%')
            if sp < 5:
                sp = sp + 1
        elif do == "s":
            if sp > 0:
                talent = 3
                print('Gained damage reduction stacks')
                sp = sp - 1
            else: action()
        else:
            action()

    if char == "blade":
        if talent2 > 0:
            print('currently in enhanced form.')
        do = input('b or s?(basic attack or skill)')
        if do == 'b':
            if talent2 > 0:
                enemyhp = enemyhp - (maxhp * 0.1)
                hp = hp - round((maxhp * 0.1))
                print('consumed hp for attack')
                print('used enhanced basic attack and dealt', (maxhp * 0.1) ,'damage')
                print('enemy health:', round(100*(enemyhp / enemymaxhp)),'%')
                talent = talent + 1
                talent2 = talent2 - 1
            elif talent2 == 0:
                enemyhp = enemyhp - (maxhp * 0.05)
                print('used basic attack and dealt', (maxhp * 0.05) ,'damage')
                print('enemy health:', round(100*(enemyhp / enemymaxhp)),'%')
            if sp < 5:
                sp = sp + 1
        elif do == 's':
            if talent2 == 0:
                sp = sp - 1
                talent2 = 3
                hp = hp - round((maxhp * 0.1))
                print('consumed own hp to enhance basic attack')
            else:
                print('cannot use skill when already in enhanced form')
                action()
        else:
            action()

def enemyaction():
    global enemyatk
    global hp
    global maxhp
    global talent
    global char
    global enemyhp
    dmg = 0
    if char == 'lance':
        if talent > 0:
            talent = talent - 1
            print('hit by enemy, now', talent ,'stacks of talent remaining')
            dmg = 1/3
    if char == 'blade':
        talent = talent + 1
        print('hit by enemy, now', talent ,'stacks of talent')

    hp = hp - round(enemyatk-(enemyatk*dmg))
    print('enemy attacked and dealt', round(enemyatk-(enemyatk*dmg)) ,'damage')
    print('you have', hp ,'health left')

def charinit(character):
    global sp
    global char
    global hp
    global maxhp
    global atk
    global spd
    global talent
    global talent2
    talent = 0
    talent2 = 0
    sp = 0
    if character == 'lance':
        char = 'lance'
        hp = 100
        maxhp = 100
        atk = 20
        spd = 50
    if character == 'blade':
        char = 'blade'
        hp = 150
        maxhp = 150
        atk = 10
        spd = 35

def charactertalentchack():
    global talent
    global enemyhp
    global maxhp
    global hp
    if char == 'blade':
        if talent == 4:
            print('')
            print('counter unleashed.')
            enemyhp = enemyhp - (maxhp * 0.1)
            hp = hp + round((maxhp * 0.25))
            if hp > maxhp:
                hp = maxhp
            print('dealt', (maxhp * 0.1) ,'damage to enemy and healed hp')
            print('enemy current hp:', enemyhp)
            print('self hp:', hp)
            talent = 0

def turninit():
    global turn
    global av
    global enemyav
    global playerturn
    global enemyturn
    turn = 0
    av = 0
    enemyav = 0
    playerturn = 0
    enemyturn = 0

def enemyinit():
    global enemyatk
    global enemyhp
    global enemymaxhp
    global enemyspd

    enemyatk = 0
    enemyhp = 0
    enemymaxhp = 0
    enemyspd = 0

credits = 0

charinit('lance')
enemyinit()
step()