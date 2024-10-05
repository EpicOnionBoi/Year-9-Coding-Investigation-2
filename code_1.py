from collections import defaultdict
import ast
import random

with open('names.txt', 'r') as f:
    names = f.readlines()
    names = [name.strip() for name in names]

def countshortlongnames(names):
    number = len(names)
    shortest = min(names, key=len)
    longest = max(names, key=len)
    return number, shortest, longest

def letterpairs(name):
    pairs = []
    for e in range(len(name) - 1):
        pairs.append([name[e], name[e+1]])
    print(pairs)

def countpairs(names):
    noendpairs = defaultdict(int)
    startendpairs = defaultdict(int)
    for name in names:
        startendpairs[('#', name[0])] += 1
        for e in range(len(name) - 1):
            pair = (name[e], name[e+1])
            noendpairs[pair] += 1
        startendpairs[(name[-1], '$')] += 1
    return noendpairs, startendpairs
pairlist = countpairs(names)

with open('pair_freqs_raw.txt', 'w') as f:
    for pair, number in pairlist[0].items():
        f.write(f"({pair}, {number})\n")
    for pair, number in pairlist[1].items():
        f.write(f"({pair}, {number})\n")

def chosenletterpairs(letter, pairs):
    chosenpairs = [pair for pair in pairs if pair[0][0] == letter]
    return chosenpairs

with open('pair_freqs_raw.txt', 'r') as file:
        pairlist = [ast.literal_eval(line.strip()) for line in file.readlines()]

def randomchoice(thing):
    results = defaultdict(int)
    for e in range(100):
        result = random.choice(thing)
        results[result]+=1
    return results

print("Welcome to the Tiny Language Model\nUse the menu below to use the Tiny Language Model\n(1) Basic statistics (number of names, shortest, longest, etc)\n(2) Split a name into letter pairs\n(3) Display the first _ lines of the sorted pairs frequency table\n(4) Display pairs starting with a particular character\n(5) Flip the coin and demonstrate correctness\n(6) Spin the numbered wheel and demonstrate correctness\n(7) Generate _ new names starting with letter _\n(8) Generate _ random names\n(9) Demonstrate the result of an untrained character-pair freq. table\n(10) Evaluate a name against the model by printing its pair probabilities")
option = input("Enter 1 to 10, or 0 to quit: ")
if option == "0":
    quit()
elif option == "1":
    print(countshortlongnames(names))
elif option == "2":
    name = input("Name: ")
    letterpairs(name)
#elif option == "3":

elif option == "4":
    chosenletter = input("Pick thy letter: ")
    resultingpairs = chosenletterpairs(chosenletter, pairlist)
    for pair in resultingpairs:
        print(pair)
elif option == "5":
    coin = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    print(random.choice(coin))
    print(randomchoice(coin))
elif option == "6":
    spinner = [0, 0, 1, 2, 3, 3, 3, 3, 3, 3]
    print(random.choice(spinner))
    print(randomchoice(spinner))