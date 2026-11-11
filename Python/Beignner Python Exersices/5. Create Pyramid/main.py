#Create Pyramid

#     *
#    ***
#   *****
#  *******
# *********

rows = 10

for i in range(1, rows + 1):
    #print spaces
    print(" "*(rows - i), end="")

    #print *
    print("*"*(2*i - 1))


row = 10
for i in range(1, row + 1):
    print(" "*(row - i), end="")
    print("*"*(2*i-1))