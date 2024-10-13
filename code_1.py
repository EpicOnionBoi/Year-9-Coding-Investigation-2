from collections import defaultdict
import ast
import random
import matplotlib.pyplot as plt

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

with open('pair_freqs_raw.txt', 'r') as file:
    pairs_freqs = [ast.literal_eval(line.strip()) for line in file]
pairs_freqs_sorted = sorted(pairs_freqs, key=lambda x: x[1], reverse=True)[:50]
letter_pairs = [f"{pair[0][0]}{pair[0][1]}" for pair in pairs_freqs_sorted]
frequencies = [pair[1] for pair in pairs_freqs_sorted]
plt.figure(figsize=(10, 6))
plt.bar(letter_pairs, frequencies, color='skyblue')
plt.xlabel('Letter Pairs')
plt.ylabel('Frequencies')
plt.title('Top 50 Most Frequent Letter Pairs')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('graph.png')

def randomchoice(thing):
    results = defaultdict(int)
    for e in range(1000):
        result = random.choice(thing)
        results[result]+=1
    return results

def randompair(pairsfile, start_char=None, second_char=None):
    with open(pairsfile, 'r') as file:
        lines = file.readlines()
    data = []
    frequencies = []
    for line in lines:
        pair, frequency = ast.literal_eval(line.strip())
        data.append(pair)
        frequencies.append(frequency)
    if start_char:
        if second_char:
            filtered_data = [pair for pair in data if pair[0] == start_char and pair[1] == second_char]
            filtered_frequencies = [frequencies[i] for i, pair in enumerate(data) if pair[0] == start_char and pair[1] == second_char]
        else:
            filtered_data = [pair for pair in data if pair[0] == start_char]
            filtered_frequencies = [frequencies[i] for i, pair in enumerate(data) if pair[0] == start_char]
        chosenpair = random.choices(filtered_data, weights=filtered_frequencies, k=1)[0]
    else:
        chosenpair = random.choices(data, weights=frequencies, k=1)[0]
    return chosenpair

print("Welcome to the Tiny Language Model\nUse the menu below to use the Tiny Language Model\n(1) Basic statistics (number of names, shortest, longest, etc)\n(2) Split a name into letter pairs\n(3) Display the first _ lines of the sorted pairs frequency table\n(4) Display pairs starting with a particular character\n(5) Flip the coin and demonstrate correctness\n(6) Spin the numbered wheel and demonstrate correctness\n(7) Print a pair of letters starting with a specific character with probability relative to frequency\n(8) Generate _ new names starting with letter _\n(9) Generate _ random names\n(10) Demonstrate the result of an untrained character-pair freq. table\n(11) Evaluate a name against the model by printing its pair probabilities")
option = input("Enter 1 to 10, or anything else to quit: ")
if option == "1":
    print(f"The number of names, shortest names, and longest names are: {countshortlongnames(names)}, respectively.")
elif option == "2":
    name = input("Name: ")
    letterpairs(name)
elif option == "3":
    with open('pair_freqs_raw.txt', 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            pair, frequency = ast.literal_eval(line.strip())
            data.append((pair, frequency))
        datasorted = sorted(data, key=lambda x: x[1], reverse=True)
        linenumbers = int(input("Enter the number of lines to display: "))
        for e in range(min(linenumbers, len(datasorted))):
            letterpair = ''.join(datasorted[e][0])
            print(f"{letterpair} {datasorted[e][1]}")
elif option == "4":
    chosenletter = input("Pick thy letter: ")
    resultingpairs = chosenletterpairs(chosenletter, pairlist)
    for pair in resultingpairs:
        print(pair)
elif option == "5":
    coin = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    print(f"The coin toss result is {random.choice(coin)}")
    print("Here are the results after repeating this 1000 times:")
    results = randomchoice(coin)
    for choice, count in results.items():
        print(f"{choice}: {count} times")
elif option == "6":
    spinner = [0, 0, 1, 2, 3, 3, 3, 3, 3, 3]
    print(f"The spinner result is {random.choice(spinner)}")
    print("Here are the results after repeating this 1000 times:")
    results = randomchoice(spinner)
    for choice, count in results.items():
        print(f"{choice}: {count} times")
elif option == "7":

else:
    quit()