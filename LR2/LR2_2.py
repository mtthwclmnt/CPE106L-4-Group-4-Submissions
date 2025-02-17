#VANCE DAVID G. SAMIA
def main():
    # Prompt the user for a filename
    file_name = input("Enter the file name: ")

    try:
        # Open and read the file, storing lines in a list
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Check if the file is empty
        if not lines:
            print("The file is empty.")
            return

        # Main loop for navigating lines
        while True:
            print(f"\nThe file contains {len(lines)} lines.")
            line_number = int(input("Enter a line number or 0 to quit): "))

            if line_number == 0:
                print("Exiting program.")
                break
            elif 1 <= line_number <= len(lines):
                print(f"Line {line_number}: {lines[line_number - 1].strip()}")
            else:
                print("Invalid line number. Please enter a valid number.")

    except FileNotFoundError:
        print("Error: File not found. Please enter a valid filename.")
    except ValueError:
        print("Error: Please enter a valid integer.")

if __name__ == "__main__":
    main()
