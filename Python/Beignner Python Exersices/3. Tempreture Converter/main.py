# #Convert Celsius to Fehrenhit
# def celsius_to_fehrenhit(x):
#     ferhrenhit = (x * 9/5) + 32
#     return ferhrenhit

# user_celsius = input("Enter the Celsius to get FEhrenhit: ")
# number = int(user_celsius)

# converted_celsius = celsius_to_fehrenhit(number)


def celsius_to_ferhrenhit(x):
    ferhrenhit = (x * 9/5) + 32
    return ferhrenhit

usr_input = input("Enter your Celsius and convert into Ferhenhit: ")
num = int(usr_input)

celsius = celsius_to_ferhrenhit(num)
print('Converted Temprature:',celsius)