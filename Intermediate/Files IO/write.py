# Write a text in file However, It would be vanished the old data
# f = open('doc.txt', 'w')
# Write a text in file But, it won't be vanished instead it would be append into the file.
# f = open('doc.txt', 'a')

# # f.write('Heyy, Mr. AI Engineer')
# f.write('\n After this I would be move to Object Orinted Programming.')
# # print(f)
# f.close()

# f = open('sample.txt', 'r+')
f = open('sample.txt', 'w+')

# f.write('This is File I/O. Where you learn how to operate the file with with PYTHON.')
data = f.read()
f.write('Hello AI, ')
print(data)
f.close()