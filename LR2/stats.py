# ACANTILADO, MARIA ANGELICA

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
    modes = [num for num, count in counts.items() if count == max_count]

    return modes[0] if len(modes) == 1 else min(modes)  # Return a single number


def main():
    """Tests the statistical functions with a sample list."""
    sample_data = [4, 1, 2, 2, 3, 5, 4, 4]  # Example list

    print(f"Mean: {mean(sample_data)}")
    print(f"Median: {median(sample_data)}")
    print(f"Mode: {mode(sample_data)}")


# Ensures the script runs only when executed directly
if __name__ == "__main__":
    main()
