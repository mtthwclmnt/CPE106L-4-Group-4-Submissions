# Contributor: CLEMENTE, Brian Matthew E. 

def navigate_file():
    filename = input("Enter the filename: ")
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        num_lines = len(lines)
        print(f"The file has {num_lines} lines.")
        
        while True:
            try:
                line_number = int(input("Enter a line number (0 to quit): "))
                if line_number == 0:
                    break
                elif 1 <= line_number <= num_lines:
                    print(lines[line_number - 1].strip())
                else:
                    print("Invalid line number. Please enter a number between 1 and", num_lines)
            except ValueError:
                print("Please enter a valid integer.")
    
    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")

if __name__ == "__main__":
    navigate_file()
