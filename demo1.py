# Printing "Hello, World!"
print("Hello, World!")

# Variables and data types
name = "Alice"  # String
age = 30        # Integer
height = 1.65     # Float
is_student = False # Boolean

# Operators
x = 10
y = 3
print(x + y)  # Addition
print(x - y)  # Subtraction
print(x * y)  # Multiplication
print(x / y)  # Division
print(x // y) # Floor division
print(x % y)  # Modulus
print(x ** y) # Exponentiation

# Conditional statements
if age >= 18:
    print("Adult")
else:
    print("Minor")

# Loops
for i in range(5):
    print(i)

j = 0
while j < 5:
    print(j)
    j += 1

# Functions
def greet(name):
    return "Hello, " + name + "!"

print(greet("Bob"))
