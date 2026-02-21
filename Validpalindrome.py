# ============================================================================
# VALID PALINDROME
# ============================================================================
# Problem: Given a string s, return true if it is a palindrome, otherwise false.
#          A palindrome reads the same forward and backward after converting 
#          all uppercase letters to lowercase and removing all non-alphanumeric characters.
#
# Constraints:
#   - Only consider alphanumeric characters (letters and numbers)
#   - Ignore cases (uppercase = lowercase)
#
# Core Logic:
#   Use two pointers: one at the start (left) and one at the end (right)
#   1. Skip non-alphanumeric characters from both ends
#   2. Compare characters (case-insensitive)
#   3. If characters don't match → not a palindrome
#   4. Move pointers toward center
#   5. If pointers meet → it's a palindrome!
#
# Example: s = "A man, a plan, a canal: Panama"
#   Clean version: "amanaplanacanalpanama"
#   - Compare 'a' and 'a' ✓
#   - Compare 'm' and 'm' ✓
#   - Compare 'a' and 'a' ✓
#   - Continue... all match! → True
#
# Example: s = "race a car"
#   Clean version: "raceacar"
#   - Compare 'r' and 'r' ✓
#   - Compare 'a' and 'a' ✓
#   - Compare 'c' and 'c' ✓
#   - Compare 'e' and 'a' ✗ → False
#
# Time Complexity: O(n) - Single pass with two pointers
# Space Complexity: O(1) - Only using pointers, no extra space
# ============================================================================
