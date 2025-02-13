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
