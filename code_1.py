from collections import defaultdict  # Import defaultdict for storing counts of letter pairs
import ast  # Import ast to evaluate strings as Python expressions
import random  # Import random module for random choices
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs

# Read the names from the 'names.txt' file
with open('names.txt', 'r') as f:
    names = f.readlines()  # Read all lines from the file
    names = [name.strip() for name in names]  # Strip whitespace from each name

# Function to count names and identify shortest/longest names
def countshortlongnames(names):
    number = len(names)  # Count the total number of names
    minlength = min(len(name) for name in names)  # Find the shortest name length
    maxlength = max(len(name) for name in names)  # Find the longest name length
    shortestnames = [name for name in names if len(name) == minlength]  # List of shortest names
    longestnames = [name for name in names if len(name) == maxlength]  # List of longest names
    return number, shortestnames, longestnames  # Return results

# Function to split a name into letter pairs, adding start and end markers
def letterpairs(name):
    namestartend = '#' + name + '$'  # Add start (#) and end ($) markers to the name
    pairs = []
    for e in range(len(namestartend) - 1):  # Loop through the name and create pairs of adjacent letters
        pairs.append((namestartend[e], namestartend[e + 1]))
    return pairs

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

pairs = []
with open('pair_freqs_raw.txt', 'r') as file:
    for line in file:
        pair, freq = eval(line.strip())
        pairs.append((pair, freq))
sorted_pairs = sorted(pairs, key=lambda pair: (pair[0][0], pair[0][1]))
with open('pair_freqs_sorted.txt', 'w') as file:
    for pair, freq in sorted_pairs:
        file.write(f"{pair} {freq}\n")

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

def randompair(pairsfile, startcharacter=None, secondcharacter=None, untrained=False):
    with open(pairsfile, 'r') as file:
        lines = file.readlines()
    data = []
    frequencies = []
    for line in lines:
        pair, frequency = ast.literal_eval(line.strip())
        data.append(pair)
        frequencies.append(frequency)
    if untrained:
        frequencies = [1] * len(frequencies)
    if startcharacter:
        if secondcharacter:
            filtered_data = [pair for pair in data if pair[0] == startcharacter and pair[1] == secondcharacter]
            filtered_frequencies = [frequencies[i] for i, pair in enumerate(data) if pair[0] == startcharacter and pair[1] == secondcharacter]
        else:
            filtered_data = [pair for pair in data if pair[0] == startcharacter]
            filtered_frequencies = [frequencies[i] for i, pair in enumerate(data) if pair[0] == startcharacter]
        chosenpair = random.choices(filtered_data, weights=filtered_frequencies, k=1)[0]
    else:
        chosenpair = random.choices(data, weights=frequencies, k=1)[0]
    return chosenpair

def generatename(pairsfile, usersecondletter=None, untrained=False):
    if usersecondletter:
        currentpair = randompair(pairsfile, startcharacter='#', secondcharacter=usersecondletter, untrained=untrained)
    else:
        currentpair = randompair(pairsfile, startcharacter='#', untrained=untrained)
    generatedname = currentpair[1]
    while currentpair[1] != '$':
        currentpair = randompair(pairsfile, startcharacter=currentpair[1], untrained=untrained)
        if currentpair[1] != '$':
            generatedname += currentpair[1]
    return generatedname

def calculatepairprobability(pair, freq_file):
    totalcount = 0
    specificpaircount = 0
    with open(freq_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            pair_data, frequency = ast.literal_eval(line.strip())
            totalcount += frequency
            if pair_data == pair:
                specificpaircount = frequency
    if totalcount > 0:
        probability = specificpaircount / totalcount
        return probability
    else:
        return 0.0

print("Welcome to the Tiny Language Model\nUse the menu below to use the Tiny Language Model\n(1) Basic statistics (number of names, shortest, longest, etc)\n(2) Split a name into letter pairs\n(3) Display the first _ lines of the sorted pairs frequency table\n(4) Display pairs starting with a particular character\n(5) Flip the coin and demonstrate correctness\n(6) Spin the numbered wheel and demonstrate correctness\n(7) Print a pair of letters starting with a specific character with probability relative to frequency\n(8) Generate _ new names starting with letter _\n(9) Generate _ random names\n(10) Demonstrate the result of an untrained character-pair freq. table\n(11) Evaluate a name against the model by printing its pair probabilities")
option = input("Enter 1 to 10, or anything else to quit: ")
if option == "1":
    print(f"The number of names, shortest names, and longest names are: {countshortlongnames(names)}, respectively.")
elif option == "2":
    name = input("Name: ")
    print(letterpairs(name))
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
    startcharacter = (input("Enter character that the pair should start with: ")).lower()
    print(randompair('pair_freqs_raw.txt', startcharacter=startcharacter))
elif option == "8":
    startcharacter = (input("Enter character that the name(s) should start with: ")).lower()
    namenumber = int(input("Enter the number of names to generate: "))
    for e in range(namenumber):
        print(generatename('pair_freqs_raw.txt', usersecondletter=startcharacter))
elif option == "9":
    namenumber = int(input("Enter the number of names to generate: "))
    for e in range(namenumber):
        print(generatename('pair_freqs_raw.txt'))
elif option == "10":
    namenumber = int(input("Enter the number of names to generate: "))
    for e in range(namenumber):
        print(generatename('pair_freqs_raw.txt', untrained=True))
elif option == "11":
    name = input("Name: ")
    pairs = letterpairs(name)
    pair_probabilities = {}
    for pair in pairs:
        probability = calculatepairprobability(pair, 'pair_freqs_raw.txt')
        pair_probabilities[pair] = probability
    for pair, prob in pair_probabilities.items():
        print(f"Probability of the letter pair {pair} occurring: {prob:.4f}")
else:
    quit()