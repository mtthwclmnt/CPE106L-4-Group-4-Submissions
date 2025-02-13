# BRIAN MATTHEW E. CLEMENTE

def navigate_file():
    # Prompt user for filename
    filename = input("Enter the filename: ")            
    try:
        # Open and read all files from the specified file
        with open(filename, 'r') as file:               
            lines = file.readlines()
        
        num_lines = len(lines)
        print(f"The file has {num_lines} lines.")
        
        while True:
            try:
                # Prompt user for a line number to display
                line_number = int(input("\nEnter a line number (0 to quit): "))           
                if line_number == 0:
                    break           # Exit the loop if user enters 0 as input
                elif 1 <= line_number <= num_lines:
                    # Display the requested line
                    print(lines[line_number - 1].strip())           
                else:
                    print("Invalid line number. Please enter a number between 1 and", num_lines)
            except ValueError:
                print("Please enter a valid integer.")      # Handle non-integer input
    
    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")       # Handle missing file error

if __name__ == "__main__":
    navigate_file()     # Run the function when the script is executed