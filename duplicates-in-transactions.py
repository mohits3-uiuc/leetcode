def looping():
    nums = [1, 2, 3, 4, 5, 2, 3]
    for num in nums:
        print(num)

def looping_2():
    nums = [1, 2, 3, 4, 5, 2, 3]
    for i in range (len(nums)):
        print(i, nums[i])

looping_2()

### Understand Dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Creating dictionary
dict = {"key1": "value1", "key2": "value2"}

## accessing values from Dictionary
print(person["name"])
print(dict["key1"])
# if key does not exist
# print(person["country"]) # this will raise KeyError
print(person.get("name"))
print(person.get("country")) # this will return None

## Adding and Updating values in Dictionary
