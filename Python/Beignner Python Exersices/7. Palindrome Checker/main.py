# A String is Palindrome if the answer of the string is same as the original string
# Example: racecar == racecar(reverse)

# USE: 
# 1. User input 
# 2. Function
# 3. f-string


# def is_palindrome(astring):
#     astring = astring.lower()
#     reversed_st = astring[::-1]
#     if astring == reversed_st:
#         return True
#     else:
#         return False
    
# usr_string = input('Enter any string to check is it Reverse String or NOT: ')

# if (is_palindrome(usr_string)):
#     print(f'{usr_string} is Palindrome.')
# else:
#     print(f'{usr_string} is NOT a Palindrome.')


def is_palindrome(astring):
    astring = astring.lower()
    reverse_str = astring[::-1]
    if astring == reverse_str:
        return True
    else:
        return False

usr_str = input("Enter anything it will check REVERSE STRING is VALID or NOT: ")

if(is_palindrome(usr_str)):
    print(f'{usr_str} is PALINDROM')
else:
    print(f'{usr_str} is NOT PALINDROM')