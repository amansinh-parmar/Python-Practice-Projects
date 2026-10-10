# Find the number of words in a sentence 
# Example: "How are you?" -> 3

# USE:
# 1. User Input
# 2. Function
# 3. f-string

# Additional Tasks: Count only words

def count_words(sentence):
    word_list = sentence.split()
    print(word_list)
    return len(word_list)

usr_input = input("Please enter your sentence here: ")

num_word = count_words(usr_input)
print(f'The number of words in your sentence is {num_word}')