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

# Function to count letter pairs across all names
def countpairs(names):
    noendpairs = defaultdict(int)  # Dictionary to count letter pairs excluding start/end markers
    startendpairs = defaultdict(int)  # Dictionary to count start and end letter pairs
    for name in names:
        startendpairs[('#', name[0])] += 1  # Count the pair for the start of the name
        for e in range(len(name) - 1):
            pair = (name[e], name[e+1])  # Create pairs of adjacent letters
            noendpairs[pair] += 1  # Count each pair
        startendpairs[(name[-1], '$')] += 1  # Count the pair for the end of the name
    return noendpairs, startendpairs  # Return both dictionaries
pairlist = countpairs(names)  # Get the letter pair counts

# Write the raw pair frequencies to 'pair_freqs_raw.txt'
with open('pair_freqs_raw.txt', 'w') as f:
    for pair, number in pairlist[0].items():  # Write non-start/end pairs
        f.write(f"({pair}, {number})\n")
    for pair, number in pairlist[1].items():  # Write start/end pairs
        f.write(f"({pair}, {number})\n")

# Read the raw pair frequencies and sort them alphabetically by letter pairs
pairs = []
with open('pair_freqs_raw.txt', 'r') as file:
    for line in file:
        pair, freq = eval(line.strip())  # Safely evaluate each line as a Python expression
        pairs.append((pair, freq))  # Add pairs to the list
sorted_pairs = sorted(pairs, key=lambda pair: (pair[0][0], pair[0][1]))  # Sort pairs alphabetically

# Write the sorted pair frequencies to 'pair_freqs_sorted.txt'
with open('pair_freqs_sorted.txt', 'w') as file:
    for pair, freq in sorted_pairs:
        file.write(f"{pair} {freq}\n")

# Function to get letter pairs starting with a specified letter
def chosenletterpairs(letter, pairs):
    chosenpairs = [pair for pair in pairs if pair[0][0] == letter]  # Filter pairs starting with the letter
    return chosenpairs

with open('pair_freqs_raw.txt', 'r') as file:
        pairlist = [ast.literal_eval(line.strip()) for line in file.readlines()]

# Plot the top 50 most frequent letter pairs
pairs_freqs_sorted = sorted(pairlist, key=lambda x: x[1], reverse=True)[:50]  # Get top 50 frequent pairs
letter_pairs = [f"{pair[0][0]}{pair[0][1]}" for pair in pairs_freqs_sorted]  # Extract letter pairs
frequencies = [pair[1] for pair in pairs_freqs_sorted]  # Extract frequencies
plt.figure(figsize=(10, 6))
plt.bar(letter_pairs, frequencies, color='skyblue')  # Create a bar chart of letter pairs
plt.xlabel('Letter Pairs')  # X-axis label
plt.ylabel('Frequencies')  # Y-axis label
plt.title('Top 50 Most Frequent Letter Pairs')  # Title of the plot
plt.xticks(rotation=90)  # Rotate x-axis labels for readability
plt.tight_layout()
plt.savefig('graph.png')  # Save the graph to a file

# Function to simulate random choices and count results
def randomchoice(thing):
    results = defaultdict(int)  # Dictionary to store results
    for e in range(1000):  # Simulate 1000 random choices
        result = random.choice(thing)  # Randomly choose from the input list
        results[result] += 1  # Increment count for the chosen item
    return results

def randompair(pairsfile, startcharacter=None, secondcharacter=None, untrained=False):
    with open(pairsfile, 'r') as file:
        lines = file.readlines()  # Read lines from the pair file
    data = []
    frequencies = []
    for line in lines:
        pair, frequency = ast.literal_eval(line.strip())  # Safely parse each line
        data.append(pair)  # Store letter pair
        frequencies.append(frequency)  # Store frequency
    if untrained:
        frequencies = [1] * len(frequencies)  # If untrained, treat all frequencies equally
    if startcharacter:  # Filter by start character if specified
        if secondcharacter:  # Further filter by second character if specified
            filtered_data = [pair for pair in data if pair[0] == startcharacter and pair[1] == secondcharacter]
            filtered_frequencies = [frequencies[i] for i, pair in enumerate(data) if pair[0] == startcharacter and pair[1] == secondcharacter]
        else:
            filtered_data = [pair for pair in data if pair[0] == startcharacter]
            filtered_frequencies = [frequencies[i] for i, pair in enumerate(data) if pair[0] == startcharacter]
        chosenpair = random.choices(filtered_data, weights=filtered_frequencies, k=1)[0]  # Choose a pair based on weights
    else:
        chosenpair = random.choices(data, weights=frequencies, k=1)[0]  # Choose randomly if no filters
    return chosenpair

# Function to generate a name based on letter pair probabilities
def generatename(pairsfile, usersecondletter=None, untrained=False):
    if usersecondletter:
        currentpair = randompair(pairsfile, startcharacter='#', secondcharacter=usersecondletter, untrained=untrained)
    else:
        currentpair = randompair(pairsfile, startcharacter='#', untrained=untrained)
    generatedname = currentpair[1]  # Initialize generated name with the second character of the first pair
    while currentpair[1] != '$':  # Continue until the end marker '$' is reached
        currentpair = randompair(pairsfile, startcharacter=currentpair[1], untrained=untrained)
        if currentpair[1] != '$':  # Append the second character of the current pair
            generatedname += currentpair[1]
    return generatedname  # Return the generated name

def calculatepairprobability(pair, freq_file):
    totalcount = 0
    specificpaircount = 0
    with open(freq_file, 'r') as file:
        lines = file.readlines()  # Read lines from the frequency file
        for line in lines:
            pair_data, frequency = ast.literal_eval(line.strip())  # Safely evaluate each line
            totalcount += frequency  # Sum the frequencies
            if pair_data == pair:  # Check if the current pair matches the specified pair
                specificpaircount = frequency  # Get the frequency of the specific pair
    probability = specificpaircount / totalcount if totalcount > 0 else 0.0  # Calculate probability
    return probability  # Return the calculated probability

# Print the welcome message and menu options for the user
print("Welcome to the Tiny Language Model\nUse the menu below to use the Tiny Language Model\n(1) Basic statistics (number of names, shortest, longest, etc)\n(2) Split a name into letter pairs\n(3) Display the first _ lines of the sorted pairs frequency table\n(4) Display pairs starting with a particular character\n(5) Flip the coin and demonstrate correctness\n(6) Spin the numbered wheel and demonstrate correctness\n(7) Print a pair of letters starting with a specific character with probability relative to frequency\n(8) Generate _ new names starting with letter _\n(9) Generate _ random names\n(10) Demonstrate the result of an untrained character-pair freq. table\n(11) Evaluate a name against the model by printing its pair probabilities")

# Prompt the user to enter an option
option = input("Enter 1 to 10, or anything else to quit: ")

# Option 1: Display basic statistics about names
if option == "1":
    print(f"The number of names, shortest names, and longest names are: {countshortlongnames(names)}, respectively.")

# Option 2: Split a user-provided name into letter pairs
elif option == "2":
    name = input("Name: ")  # Prompt for a name
    print(letterpairs(name))  # Display the letter pairs of the name

# Option 3: Display sorted pairs frequency from a file
elif option == "3":
    with open('pair_freqs_raw.txt', 'r') as file:  # Open the frequency file for reading
        lines = file.readlines()  # Read all lines from the file
        data = []  # Initialize an empty list to store pairs and frequencies
        for line in lines:  # Loop through each line in the file
            pair, frequency = ast.literal_eval(line.strip())  # Safely evaluate the line
            data.append((pair, frequency))  # Add the pair and frequency to the list
        datasorted = sorted(data, key=lambda x: x[1], reverse=True)  # Sort data by frequency in descending order
        linenumbers = int(input("Enter the number of lines to display: "))  # Prompt for number of lines to display
        for e in range(min(linenumbers, len(datasorted))):  # Loop through the sorted data
            letterpair = ''.join(datasorted[e][0])  # Join the pair into a string
            print(f"{letterpair} {datasorted[e][1]}")  # Print the letter pair and its frequency

# Option 4: Display pairs starting with a specific character
elif option == "4":
    chosenletter = input("Pick thy letter: ")  # Prompt for a starting letter
    resultingpairs = chosenletterpairs(chosenletter, pairlist)  # Get pairs starting with the chosen letter
    for pair in resultingpairs:  # Loop through the resulting pairs
        print(pair)  # Print each pair

# Option 5: Simulate a coin flip and show results
elif option == "5":
    coin = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]  # Define coin states (0=tails, 1=heads)
    print(f"The coin toss result is {random.choice(coin)}")  # Print the result of a random coin flip
    print("Here are the results after repeating this 1000 times:")  # Message for results
    results = randomchoice(coin)  # Get results of 1000 coin flips
    for choice, count in results.items():  # Loop through the results
        print(f"{choice}: {count} times")  # Print the count for each coin side

# Option 6: Simulate a spinner and show results
elif option == "6":
    spinner = [0, 0, 1, 2, 3, 3, 3, 3, 3, 3]  # Define spinner outcomes
    print(f"The spinner result is {random.choice(spinner)}")  # Print the result of a random spinner spin
    print("Here are the results after repeating this 1000 times:")  # Message for results
    results = randomchoice(spinner)  # Get results of 1000 spinner spins
    for choice, count in results.items():  # Loop through the results
        print(f"{choice}: {count} times")  # Print the count for each outcome

# Option 7: Print a random pair starting with a specific character
elif option == "7":
    startcharacter = (input("Enter character that the pair should start with: ")).lower()  # Prompt for starting character
    print(randompair('pair_freqs_raw.txt', startcharacter=startcharacter))  # Print a random pair starting with that character

# Option 8: Generate new names starting with a specific letter
elif option == "8":
    startcharacter = (input("Enter character that the name(s) should start with: ")).lower()  # Prompt for starting letter
    namenumber = int(input("Enter the number of names to generate: "))  # Prompt for number of names to generate
    for e in range(namenumber):  # Loop for the number of names
        print(generatename('pair_freqs_raw.txt', usersecondletter=startcharacter))  # Generate and print each name

# Option 9: Generate random names without specific starting letter
elif option == "9":
    namenumber = int(input("Enter the number of names to generate: "))  # Prompt for number of names to generate
    for e in range(namenumber):  # Loop for the number of names
        print(generatename('pair_freqs_raw.txt'))  # Generate and print each random name

# Option 10: Generate names using untrained frequencies
elif option == "10":
    namenumber = int(input("Enter the number of names to generate: "))  # Prompt for number of names to generate
    for e in range(namenumber):  # Loop for the number of names
        print(generatename('pair_freqs_raw.txt', untrained=True))  # Generate and print each untrained name

# Option 11: Evaluate a name against the model's pair probabilities
elif option == "11":
    name = input("Name: ")  # Prompt for a name
    pairs = letterpairs(name)  # Get the letter pairs of the name
    pair_probabilities = {}  # Initialize a dictionary for pair probabilities
    for pair in pairs:  # Loop through each letter pair
        probability = calculatepairprobability(pair, 'pair_freqs_raw.txt')  # Calculate the probability of the pair
        pair_probabilities[pair] = probability  # Store the probability in the dictionary
    for pair, prob in pair_probabilities.items():  # Loop through the probabilities
        print(f"Probability of the letter pair {pair} occurring: {prob:.4f}")  # Print each pair's probability

# If the input doesn't match any options, quit the program
else:
    quit()  # Exit the program