Here begins the new branch

## Python Basics and First Assignment

This repository is a beginner's guide to Python, covering fundamental concepts and syntax. Screenshots related to this assignment are saved in OneDrive.

## Table of Contents
- [Python Basics and First Assignment](#python-basics-and-first-assignment)
- [Table of Contents](#table-of-contents)
- [Comments](#comments)
- [Raw Strings](#raw-strings)
- [Variables](#variables)
- [Output](#output)
- [Input](#input)
- [Casting](#casting)
- [Data Types](#data-types)
- [Logical Operators](#logical-operators)
- [Conditionals Syntax](#conditionals-syntax)
- [Loop Syntax](#loop-syntax)
- [function syntax](#function-syntax)
    - [Arbitrary Keyword Arguments, \*\*kwargs](#arbitrary-keyword-arguments-kwargs)
    - [function with return](#function-with-return)
    - [Lambda Functions](#lambda-functions)
- [Classes](#classes)
- [Inheritance](#inheritance)
- [Iterators](#iterators)
- [Polymorphism](#polymorphism)
- [Modules](#modules)
- [Datetime](#datetime)
- [JSON Handling](#json-handling)
    - [Importing](#importing)
    - [Exporting](#exporting)
- [Exception Handling](#exception-handling)
- [File Handling](#file-handling)
    - [Syntax](#syntax)
- [CSV API](#csv-api)

## Comments
```python
# This is a single-line comment
```
```python
"""
This is a multiline
string, but can also
be used as a comment
"""
```

## Raw Strings
Prefix the string with 'r' to create a raw string. This way, backslashes won't be treated as escape characters.

x = r"file\path"

## Variables
```python
x = 0                                             # assign variable
X = "string"                                      # X != x ; variables are case-sensitive!
x, y, z = "Orange", "Banana", "Cherry"            # Multiple variables can be set at once
x, y, z = fruits = ["Orange", "Banana", "Cherry"] # This is called "list unpacking"
```

## Output
```python
print("Hello, World!")
```
Use this to clear the terminal:
```python
os.system('cls')
```

## Input
```python
var = input("prompt")
```

## Casting
```python
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
```

## Data Types
These are the datatypes of Python:
| Data Type         | Example        |
| ----------------- | -------------- |
| Text Type         | `str`          |
| Numeric Types     | `int`, `float`, `complex` |
| Sequence Types    | `list`, `tuple`, `range` |
| Mapping Type      | `dict`         |
| Set Types         | `set`, `frozenset` |
| Boolean Type      | `bool`         |
| Binary Types      | `bytes`, `bytearray`, `memoryview` |
| None Type         | `NoneType`     |

To fetch `x`'s datatype:
```python
print(type(x))
```

## Logical Operators
- `and`
- `or`
- `not`

## Conditionals Syntax
```python
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")
```

## Loop Syntax
```python
i = 1
while i < 6:
  print(i)
  i += 1

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
```

## function syntax
Define:
```python
def my_function(*args):   # The asterisk (*) means any number of arg can be passed
  # any variable declared here are local scope, but can be declared global as such:
  global var
  var = "this is declared within my_function()"
  print("Hello from a function, first arg is",args[0])
```
Call:
```python
my_function("python","second arg")
print(var)
```

#### Arbitrary Keyword Arguments, **kwargs
If the number of keyword arguments is unknown, add a double ** before the parameter name:
```python
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Slim", lname = "Shady")
```

#### function with return
```python
def my_function(x):
  return 5 * x

print(my_function(3))
```

#### Lambda Functions
```python
x = lambda a, b, c: a + b + c  # [value] = lambda [input] : [output]
print(x(5, 6, 2))
```

## Classes
All classes have a function called `__init__()`, which is always executed when
the class is being initiated. Use the `__init__()` function to assign values to object properties, or other
operations that are necessary to do when the object is being created.

Define class:
```python
class Person:                      # create class structure
    def __init__(self, name, age):  
        self.name = name           # define attributes
        self.age = age

    def __str__(self):             # this is the equivalent of toString() in java
        return f"{self.name}({self.age})"
    
    def myfunc(self):
        print("Hello my name is " + self.name)
```
Create instance:
```python
p1 = Person("Slim Shady", 36)     # create instance
print(p1.name)                    # access attributes, or
print(p1)                         # use __str__
```

## Inheritance
```python
class Student(Person):                 # Student extends Person
    def __init__(self, fname, lname):
        super().__init__(fname, lname) # Call parents constructor (init)
        # add properties
```

## Iterators
The iterator protocol consist of the methods `__iter__()` and `__next__()`:

```python
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 10:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

next(myiter)  # +1
next(myiter)  # +1
next(myiter)  # +1
#...

for x in myiter:
	print(x)
```

## Polymorphism
```python
class Car:
    def move(self):
        print("Drive!")

class Boat:
    def move(self):
        print("Sail!")

# result is Car(...).move() != Boat(...).move()
```

## Modules
```python
import mymodule               # from mymodule.py
mymodule.greeting("Jonathan")
```

## Datetime
```python
import datetime
```

## JSON Handling

#### Importing

```python
import json

x =  '{ "name":"John", "age":30, "city":"New York"}'
y = json.loads(x) # parse x
print(y["age"])   # the result is a Python dictionary
```

#### Exporting
```python
import json

x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

y = json.dumps(x) # convert into JSON
print(y)          # the result is a JSON string
```

## Exception Handling

```python
try:
  print("Hello")
except NameError:
  print("Variable x is not defined")
except:
  print("Something went wrong")
else:
  print("Nothing went wrong")
finally:
  print("The 'try except' is finished")
```

## File Handling

The key function for working with files in Python is the open() function.
The open() function takes two parameters; filename, and mode.
There are four different methods (modes) for opening a file:

| Mode | Description                                   |
|------|-----------------------------------------------|
| **r**  | Default value. Opens a file for reading. Throws an error if the file does not exist.    |
| **a**  | Opens a file for appending. Creates the file if it does not exist.                      |
| **w**  | Opens a file for writing. Creates the file if it does not exist.                        |
| **x**  | Creates the specified file. Returns an error if the file already exists.                |

| **t**  | <span style="font-weight:normal">Default value. Text mode.</span>  |
|-|-|
| **b**  | <span style="font-weight:normal">Binary mode (e.g., for handling images). </span>  |


#### Syntax

**Open**
```python
file = open(filepath)
file = open(filepath, "rt")
```

**Create**
```python
file = open(filepath, "x")
```

**Read**
```python
file.read()
file.readline()
```

**Write**
```python
fileA = open(fpA,"a")
fileB = open(fpB,"w")
fileA.write("") # will append to file
fileB.write("") # will overwrite file
```

**Close**
```python
file.close()
```

**Delete**
```python
import os
if os.path.exists(file):
    os.remove(file)
os.rmdir(emptyFolder)
```

## CSV API
```python
import csv
with open('eggs.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
```