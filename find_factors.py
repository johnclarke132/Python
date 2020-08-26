def find_factors(number):
    return [n for n in range(1, number+1) if number % n == 0]


print(find_factors(6))
