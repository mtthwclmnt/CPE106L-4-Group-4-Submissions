# CLEMENTE, BRIAN MATTHEW E. (2023180065)

class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = [0] * number

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        self.scores[i - 1] = score

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
   
    def getAverage(self):
        """Returns the average score."""
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name  + "\nScores: " + " ".join(map(str, self.scores))
    
    def __eq__(self, other):
        """Tests for equality based on student names."""
        return self.name == other.name
    
    def __lt__(self, other):
        """Tests if one student's name is less than another's."""
        return self.name < other.name
    
    def __ge__(self, other):
        """Tests if one student's name is greater than or equal to another's."""
        return self.name >= other.name


def main():
    """Tests the comparison operators."""
    student1 = Student("Charlie", 3)                        # lowercase letters will be considered *greater* than uppercase (e.g. ethan vs Ethan)
    student2 = Student("David", 3)
    student3 = Student("Charlie", 3)
    
    print("Testing Equality:")
    print(f"student1 == student2: {student1 == student2}")  # False (Charlie != David)
    print(f"student1 == student3: {student1 == student3}")  # True (Charlie == Charlie)
    
    print("\nTesting Less Than:")
    print(f"student1 < student2: {student1 < student2}")  # True (Charlie comes BEFORE David, alphabetically)
    print(f"student2 < student1: {student2 < student1}")  # False (Charlie comes AFTER David, alphabetically)
    
    print("\nTesting Greater Than or Equal To:")
    print(f"student1 >= student2: {student1 >= student2}")  # False (Charlie comes BEFORE David)
    print(f"student2 >= student1: {student2 >= student1}")  # True (David comes AFTER Charlie)
    print(f"student1 >= student3: {student1 >= student3}")  # True (Charlie is IDENTICAL to Charlie)


if __name__ == "__main__":
    main()