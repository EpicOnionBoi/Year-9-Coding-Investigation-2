from collections import defaultdict
with open('names.txt', 'r') as f:
    names = f.readlines()
    names = [name.strip() for name in names]

def countshortlongnames(names):
    number = len(names)
    shortest = min(names, key=len)
    longest = max(names, key=len)
    return number, shortest, longest

print(countshortlongnames(names))
name = input("Name: ")
def letterpairs(name):
    pairs = []
    for e in range(len(name) - 1):
        pairs.append([name[e], name[e+1]])
    print(pairs)
letterpairs(name)

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