def duplicate_remover(items):
    return list(dict.fromkeys(items))


numbers = [1, 2, 3, 2, 5, 4, 5]
result = duplicate_remover(numbers)

print(f"Orignal: {numbers}")
print(f"Filter-Out: {result}")
