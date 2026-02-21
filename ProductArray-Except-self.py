# ============================================================================
# PRODUCT OF ARRAY EXCEPT SELF
# ============================================================================
# Problem: Given an integer array nums, return an array answer such that 
#          answer[i] is equal to the product of all elements of nums except nums[i].
#
# Constraints:
#   - Must run in O(n) time
#   - Cannot use division operation
#   - Follow-up: Can you solve it with O(1) extra space? (output array doesn't count)
#
# Core Logic:
#   The product except self = (product of all elements to the left) × (product of all elements to the right)
#   
#   We make two passes:
#   1. LEFT PASS: Calculate prefix products (everything to the left)
#   2. RIGHT PASS: Multiply by suffix products (everything to the right)
#
# Example: nums = [1, 2, 3, 4]
#   Left products:  [1, 1, 2, 6]     → prefix[i] = product of all elements before i
#   Right products: [24, 12, 4, 1]   → suffix[i] = product of all elements after i
#   Final result:   [24, 12, 8, 6]   → result[i] = prefix[i] × suffix[i]
#
#   Breakdown:
#   - answer[0] = 1 × (2×3×4) = 24
#   - answer[1] = 1 × (3×4) = 12
#   - answer[2] = (1×2) × 4 = 8
#   - answer[3] = (1×2×3) × 1 = 6
#
# Time Complexity: O(n) - Two passes through the array
# Space Complexity: O(1) - Only output array (not counted), constant extra space
# ============================================================================
