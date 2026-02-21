# ============================================================================
# 1. TWO SUM PROBLEM
# ============================================================================
# Problem: Given an array of integers nums and an integer target, return 
#          indices of the two numbers such that they add up to target.
#
# Constraints:
#   - Each input has exactly one solution
#   - Cannot use the same element twice
#   - Can return the answer in any order
#
# Core Logic:
#   For each number, we ask: "Have I seen the complement (target - num) before?"
#   - If YES: We found our pair! Return both indices.
#   - If NO: Remember this number and its index for future lookups.
#
# Example: nums = [2, 7, 11, 15], target = 9
#   - See 2: complement = 7, not seen yet → store {2: 0}
#   - See 7: complement = 2, found at index 0 → return [0, 1]
#
# Time Complexity: O(n) - Single pass through the array
# Space Complexity: O(n) - Store up to n elements in the dictionary
# ============================================================================

def twoSum(nums, target):
    seen = {}  # Dictionary to store {number: index} for all numbers we've seen

    for i, num in enumerate(nums):  # Iterate through each number with its index
        complement = target - num  # Calculate what number we need to reach the target

        if complement in seen:  # Check if we've seen the complement before
            return [seen[complement], i]  # Found it! Return both indices

        seen[num] = i  # Store current number and its index for future lookups

    return []  # No solution found (shouldn't happen per problem constraints)