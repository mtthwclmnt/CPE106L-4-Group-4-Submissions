#CHALZEA FRANSEN C. DYTIANQUIN
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

#--------------------------------------------------------------------------------------------------------------------#

#VANCE DAVID G. SAMIA
def mean(numbers):
    """Compute the mean of a list of numbers."""
    if not numbers:
        raise ValueError("The list of numbers is empty.")
    return sum(numbers) / len(numbers)

def median(numbers):
    """Compute the median of a list of numbers."""
    if not numbers:
        raise ValueError("The list of numbers is empty.")
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        # If even, return the average of the two middle numbers
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        # If odd, return the middle number
        return sorted_numbers[mid]

def mode(numbers):
    """Compute the mode of a list of numbers."""
    if not numbers:
        raise ValueError("The list of numbers is empty.")
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_freq]
    if len(modes) == len(numbers):
        # All numbers appear with the same frequency (no mode)
        return None
    return modes[0]  # Return the first mode if there are multiple

def get_user_input():
    """Get the size of the list and individual values from the user."""
    numbers = []
    size = int(input("Enter the size of the list: "))
    for i in range(size):
        value = float(input(f"Enter value {i + 1}: "))
        numbers.append(value)
    return numbers

# Example usage with user input
if __name__ == "__main__":
    user_numbers = get_user_input()
    print("Mean:", mean(user_numbers))
    print("Median:", median(user_numbers))
    print("Mode:", mode(user_numbers))

#--------------------------------------------------------------------------------------------------------------------#

#MARIA ANGELICA ACANTILADO

def mean(numbers):
    """Compute the mean of a list of numbers."""
    return sum(numbers) / len(numbers)

def median(numbers):
    """Compute the median of a list of numbers."""
    numbers.sort()
    n = len(numbers)
    mid = n // 2
    if n % 2 == 0:
        return (numbers[mid - 1] + numbers[mid]) / 2
    else:
        return numbers[mid]

def enhanced_mode(numbers):
    """Compute the mode(s) of a list of numbers. Returns multiple modes if applicable."""
    if not numbers:
        raise ValueError("The list of numbers is empty.")
    
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1

    max_freq = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_freq]

    if len(modes) == len(set(numbers)):  
        return None  # No mode if all numbers appear equally

    return modes if len(modes) > 1 else modes[0]  # Return list if multiple, else single mode

# Get user input
num_values = int(input("How many values do you want to enter? "))

numbers = []
for i in range(1, num_values + 1):
    suffix = "th"
    if i == 1:
        suffix = "st"
    elif i == 2:
        suffix = "nd"
    elif i == 3:
        suffix = "rd"
    
    value = float(input(f"Enter the {i}{suffix} value: "))
    numbers.append(value)

# Display results
print("=" * 28)
print("Mean:", mean(numbers))
print("Median:", median(numbers))
print("Mode:", enhanced_mode(numbers))
