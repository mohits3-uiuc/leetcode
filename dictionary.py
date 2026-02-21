## 1. Understand Dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

## 2. Creating dictionary
dict = {"key1": "value1", "key2": "value2"}

## 3. Accessing values from Dictionary
print("""Accessing values from Dictionary""")
print(person["name"])
print(dict["key1"])
# if key does not exist
# print(person["country"]) # this will raise KeyError
print(person.get("name"))
print(person.get("country")) # this will return None

## 4. Adding and Updating values in Dictionary
print("""Adding and Updating values in Dictionary""")
d= {}
d["apple"] = 1  # Adding a new key-value pair to the dictionary with key "apple" and value 1
d["apple"] += 2 # Updating the value of the key "apple" by adding 2
d["banana"] = 3  # Adding a new key-value pair to the dictionary with key "banana" and value 3
d["banana"] += 1 # Updating the value of the key "banana" by adding 1
print(d.get("apple")) # Output: 3
print(d)

## 5. Looping through Dictionary
print("""Looping through Dictionary""")
# Loop through keys
print("Loop through keys")
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    print(key, d[key])

for key in person:
    print(key, person[key])

# Loop through key and value
print("Loop through key and value")
for key,value in person.items():
    print(key, value)

# looping through values
print("Looping through values")
for value in person.values():
    print(value)

## 6. Check if key exists in Dictionary
print("""Check if key exists in Dictionary""")
if "name" in person:
    print("Name exists in person")

## 7. Frequency Counter
print("""Frequency Counter""")
nums = [1, 2, 3, 4, 5, 2, 3]
freq = {}
for n in nums:
    freq[n] = freq.get(n, 0) + 1

print(freq)

## 8. defaultdict (Cleaner Way)
from collections import defaultdict
freq = defaultdict(int)
for n in nums:
    freq[n] += 1

print(freq)

## 9. Importannt Methods
print("""Importannt Methods""")
d = {"a": 1, "b": 2, "c": 3}
print(d.keys())   # Output: dict_keys(['a', 'b', 'c'])
print(d.values()) # Output: dict_values([1, 2, 3])
print(d.items())  # Output: dict_items([('a', 1), ('b', 2), ('c', 3)])
print(d.get("a")) # Output: 1
print(d.get("d", "Not Found")) # Output: Not Found
print(d.update({"d": 4})) # Output: None (update method does not return anything)
print(d) # Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

## 10. Sorting a Dictionary
print("""Sorting a Dictionary""")
d = {"b": 2, "c": 3, "a": 1}
# Sort by keys
sorted_by_keys = dict(sorted(d.items()))
print("Sorted by keys:", sorted_by_keys) # Output: {'a': 1, 'b': 2, 'c': 3}
sorted_by_values = dict(sorted(d.items(), key=lambda item: item[1]))
print("Sorted by values:", sorted_by_values) # Output: {'a': 1, 'b': 2, 'c': 3}

## Common Interview Questions
print("""Common Interview Questions""")
# 1. Given a list of integers, return a dictionary with the count of each integer
nums = [1, 2, 3, 4, 5, 2, 3]
freq = {}
for n in nums:
    freq[n] = freq.get(n, 0) + 1        
print(freq) # Output: {1: 1, 2: 2, 3: 2, 4: 1, 5: 1}

#2. Given a string, return a dictionary with the count of each character
s = "hello world"
char_freq = {}
for char in s:
    char_freq[char] = char_freq.get(char, 0) + 1
print(char_freq) # Output: {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1} 

# 3. Given a list of words, return a dictionary with the count of each word
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
word_freq = {}
for word in words:
    word_freq[word] = word_freq.get(word, 0) + 1
print(word_freq) # Output: {'apple': 3, 'banana': 2, 'orange': 1}   

## Common Interview Problems Using Dict
# - Two Sum
# - Group Anagrams
# - Top K Frequent Elements
# - Majority Element
# - Subarray Sum Equals K
# - LRU Cache
# - First Non-Repeating Character

