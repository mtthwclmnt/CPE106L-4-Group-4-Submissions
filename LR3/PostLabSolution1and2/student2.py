#VANCE DAVID G. SAMIA

import random
from student import Student

def main():
    #Creates and sorts a shuffled list of Student objects.
    students = [
        Student("Alice", 3),
        Student("Charlie", 3),
        Student("Ethan", 3),
        Student("David", 3),
        Student("Bob", 3)
    ]
    
    print("Original List:")
    for student in students:
        print(student)
    
    # Shuffle the list
    random.shuffle(students)
    print("\nShuffled List:")
    for student in students:
        print(student)
    
    # Sort the list
    students.sort()
    print("\nSorted List:")
    for student in students:
        print(student)

if __name__ == "__main__":
    main()
