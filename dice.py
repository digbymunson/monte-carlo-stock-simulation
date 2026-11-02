import random

def rolldie ():
    global sum
    roll1 = random.randint(1,6)
    roll2 = random.randint(1,6)

    sum = roll1 + roll2
    
    return sum
    
trials = 1000

def go(trials):
    n=0
    for i in range (trials):
        
        if rolldie() > 9:
            n+=1

    probability = n / trials
    return probability


print(go(trials))
