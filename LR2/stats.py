# ACANTILADO, MARIA ANGELICA and DYTIANQUIN, CHALZEA FRANSEN C.

def mean(numbers):
    """Returns the mean (average) of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def median(numbers):
    """Returns the median of a list of numbers."""
    if not numbers:
        return 0
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]


def mode(numbers):
    """Returns the mode (most frequent value) of a list of numbers."""
    if not numbers:
        return 0
    from collections import Counter
    counts = Counter(numbers)
    max_count = max(counts.values())

    if max_count == 1:  # No repeated numbers
        return "None"

    modes = [num for num, count in counts.items() if count == max_count]
    return modes[0] if len(modes) == 1 else min(modes)  # Return a single mode


def main():
    """Test the statistical functions with user input."""
    try:
        user_input = input("Enter numbers separated by spaces: ").strip()
        
        if not user_input:
            print("Error! No input provided.")
            return
        
        # Convert input string to a list of floats
        list_numbers = list(map(float, user_input.split()))

        if len(list_numbers) < 2:
            print("Error! You must enter at least two numbers.")
            return

        print("List:", list_numbers)
        print("Mean:", mean(list_numbers))
        print("Median:", median(list_numbers))
        print("Mode:", mode(list_numbers))

    except ValueError:
        print("Invalid input. Please enter numeric values separated by spaces.")
    except ValueError:
        print("\nError! Invalid input. Please enter only numbers separated by spaces.")


# Ensures the script runs only when executed directly
if __name__ == "__main__":
    main()
