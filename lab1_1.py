import random
arr_length = random.randint(1000, 10000)
data = [random.randint(0, 1) for i in range(arr_length)]
zeros = data.count(0)
ones = data.count(1)
print(
    f"Array length: {len(data)}\nZeros percentage: {round((zeros/len(data)*100),2)}%\nOnes percentage: {round((ones/len(data)*100),2)}")

for window in range(2, len(data)):
    current_pairs = []
    zeros_pairs = []
    ones_pairs = []
    for i in range(len(data)):
        pair = data[i:i+window]
        if len(pair) == window:
            current_pairs.append(pair)
        if sum(pair) == 0:
            zeros_pairs.append(pair)
        if sum(pair) == len(pair):
            ones_pairs.append(pair)
    zeros_percentage = round((len(zeros_pairs)/len(current_pairs)*100), 2)
    ones_percentage = round((len(ones_pairs)/len(current_pairs)*100), 2)
    if ((zeros_percentage or ones_percentage) != 0) and ((zeros_percentage or ones_percentage) > 0.1):
        print(
            f"For window {window}:\nZeros pairs: {zeros_percentage}%\nOnes pairs: {ones_percentage}%")
