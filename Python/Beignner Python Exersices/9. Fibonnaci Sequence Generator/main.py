# Generate Fibonnaci Sequence upto user provider input
# Example: n = 7, fib sequence: 0, 1, 1, 2, 3, 5, 8

# USE:
# 1. User Input
# 2. Function
# 3. f-string

def gen_fib(n):
    fibo_seq = [0, 1]

    while len(fibo_seq) < n:
        next_term = fibo_seq[-1] + fibo_seq[-2]
        fibo_seq.append(next_term)
    return fibo_seq

usr_input = input('Enter the length of Fibonnaci Sequence: ')
num_input = int(usr_input)

seq = gen_fib(num_input)
print(f"The first {num_input} terms of the Fibonnaci Sequence is {seq}")