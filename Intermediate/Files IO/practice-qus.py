# ==>> Question 1:
# Replace the Javascript with Python
# with open('practice.txt', 'r') as f:
#     data = f.read()

#     new_data = data.replace('JavaScript', 'Python')
#     print(new_data)
#     f.close()

# ==>> Question 2:
# Save the replaced text into file
# with open('practice.txt', 'w') as f:
#     f.write(new_data)

# ==>> Question 3:
# Check the word inside the File:
# def check_for_word():
#     find = 'practice'

#     with open('practice.txt', 'r') as f:
#         f.read()

#         if find not in f:
#             print('Not Found it!!')
#         else:
#             print('Found it..')

# check_for_word()

# ==>> Question 4:
# Check the file in which does have "python"
# def check_word_line():
#     word = 'Python'
#     data = True
#     line_no = 1

#     with open('practice.txt', 'r') as f:
#         while data:
#             data = f.readline()
#             if (word in data):
#                 print(line_no)
#             line_no += 1

#         return - 1
# check_word_line()
# Find "learing" word
# def check_line():
#     word = 'learning'
#     data = True
#     line = 1
#     with open('practice.txt', 'r') as f:
#         while data:
#             data = f.readline()
#             if (word in data):
#                 print(line)
#             line +=1
#     return -1 
# check_line()

# Check the all the numbers inside the txt file
# def add_num():
#     with open('number.txt', 'r') as f:
#         data = f.read()
#         print(data)
#         num = ""
#         for i in range(len(data)):
#             if(data[i] == ","):
#                 print(int(num))
#                 num = ''
#             else:
#                 num += data[i]
# add_num()

# count = 0

# with open('number.txt', 'r') as f:
#     data = f.read()
#     print(data)

#     nums = data.split(',')
#     for val in nums:
#         if (int(val) % 2 == 0):
#             count += 1

# print(count)

count = 0

with open('number.txt', 'r') as f:
    data = f.read()
    print(data)

    nums = data.split(',')
    for val in nums:
        if(int(val) % 2 == 0):
            count += 1

print(count)