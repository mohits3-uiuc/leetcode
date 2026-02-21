# ============================================================================
# CONTAINS DUPLICATE PROBLEM
# ============================================================================
# The question is simply: "Have I seen this number before?"
# 
# So the best approach is to remember what you've already seen using a set.
# ============================================================================

nums = [1, 2, 3, 4, 5]

## Method 1 Ways to do for loop
# Iterate over the elements directly
for num in nums:
    print(num)

# Method 2 Ways to do for loop
# Iterate using index
for i in range(len(nums)):
    print(nums[i])


# Method 3 Loop over key and value
for i, num in enumerate(nums):
    print(f"Index: {i}, Value: {num}")

# loop a range of numbers
# starts with 1 and goes until 4 but does not include 5
for i in range(1,5):
    print(i)



# loop a range of numbers with step
# starts with 0 and goes until 9 but does not include 10 and 2 is the step
for i in range(0, 10, 2):
    print(i)


# https://neetcode.io/problems/duplicate-integer/question?list=blind75

# Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.

def containsDuplicate(nums):
    seen = set()  # Create an empty set to store seen numbers

    for num in nums:  # Iterate through each number in the input list
        if num in seen:  # Check if the number is already in the set
            return True  # If it is, we have a duplicate, so return True
        seen.add(num)  # If not, add the number to the set

    return False  # If we finish the loop without finding duplicates, return False


## Understanding Self
class Person:
    def set_name(self,name):
        self.name = name
        print("Setting name", self.name)

    def say_hello(self):
        print("Hello, my name is", self.name)

p1 = Person()
p2 = Person()
p1.set_name("Alice")
p2.set_name("Bob")
p2.say_hello("Garce")