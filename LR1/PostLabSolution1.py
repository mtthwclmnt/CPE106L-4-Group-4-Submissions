def median(li):
    li.sort()
    if len(li) % 2 == 0:
        f = li[len(li) // 2]
        s = li[len(li) // 2 - 1]
        m = (f + s) / 2
    else:
        m = li[len(li) // 2]

    return m

# Calculating Mean
def mean(li):
    sum_list = sum(li)
    return sum_list / len(li)

# Calculating Mode
def mode(li):
    mode1 = max(li, key=li.count)
    return mode1

# Input for the number of values
num_values = int(input('How many values do you want to enter? '))

li = []
# Input for the specified number of values
for i in range(num_values):
    li.append(int(input('Enter a value for the list: ')))

# Output the results
print("List:", li)
print("Mode:", mode(li))
print("Median:", median(li))
print("Mean:", mean(li))
