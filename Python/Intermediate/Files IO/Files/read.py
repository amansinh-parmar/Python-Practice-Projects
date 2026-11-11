f = open('doc.txt', 'r')

# read entire file
data = f.read()

# read first line only
line1 = f.readline()
# print(data)
# read second line only
print(line1)
line2 = f.readline()
print(line2)
f.close()


with open ('sample.txt', 'w+') as f:
    new_data = f.write('Hello AI, Please write this')
    print(new_data)

with open('sample.txt', 'a') as f:
    new_add = f.write(' & I also want to Append this.')
    print(new_data)