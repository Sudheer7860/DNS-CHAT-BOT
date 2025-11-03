"""
Number utilities for calculating mathematical properties and conversions
"""
import math
from typing import List, Dict, Any


def is_prime(n: int) -> bool:
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_factors(n: int) -> List[int]:
    """Get all factors of a number"""
    if n == 0:
        return []
    n = abs(n)
    factors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    return sorted(factors)


def prime_factorization(n: int) -> Dict[int, int]:
    """Get prime factorization of a number"""
    if n == 0:
        return {}
    n = abs(n)
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def is_perfect(n: int) -> bool:
    """Check if a number is perfect (sum of divisors equals the number)"""
    if n < 2:
        return False
    factors = get_factors(n)
    return sum(factors[:-1]) == n


def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number"""
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n


def is_palindrome(n: int) -> bool:
    """Check if a number is a palindrome"""
    s = str(abs(n))
    return s == s[::-1]


def to_binary(n: int) -> str:
    """Convert number to binary"""
    if n >= 0:
        return bin(n)[2:]
    else:
        return '-' + bin(n)[3:]


def to_octal(n: int) -> str:
    """Convert number to octal"""
    if n >= 0:
        return oct(n)[2:]
    else:
        return '-' + oct(n)[3:]


def to_hexadecimal(n: int) -> str:
    """Convert number to hexadecimal"""
    if n >= 0:
        return hex(n)[2:].upper()
    else:
        return '-' + hex(n)[3:].upper()


def to_roman(n: int) -> str:
    """Convert number to Roman numerals (1-3999)"""
    if n <= 0 or n >= 4000:
        return "N/A (out of range 1-3999)"
    
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = ""
    for i in range(len(values)):
        count = n // values[i]
        if count:
            result += numerals[i] * count
            n -= values[i] * count
    return result


def fibonacci_position(n: int) -> int:
    """Check if number is in Fibonacci sequence and return position, -1 if not"""
    if n < 0:
        return -1
    
    a, b = 0, 1
    position = 0
    
    while a < n:
        a, b = b, a + b
        position += 1
    
    return position if a == n else -1


def is_fibonacci(n: int) -> bool:
    """Check if a number is in the Fibonacci sequence"""
    return fibonacci_position(n) != -1


def sum_of_digits(n: int) -> int:
    """Calculate sum of digits"""
    return sum(int(d) for d in str(abs(n)))


def product_of_digits(n: int) -> int:
    """Calculate product of digits"""
    result = 1
    for d in str(abs(n)):
        result *= int(d)
    return result


def get_number_info(n: int) -> Dict[str, Any]:
    """Get comprehensive information about a number"""
    info = {
        'number': n,
        'absolute': abs(n),
        'is_positive': n > 0,
        'is_negative': n < 0,
        'is_zero': n == 0,
        'is_even': n % 2 == 0 if n != 0 else True,
        'is_odd': n % 2 != 0 if n != 0 else False,
        'is_prime': is_prime(n) if n > 0 else False,
        'is_perfect': is_perfect(n) if n > 0 else False,
        'is_armstrong': is_armstrong(n),
        'is_palindrome': is_palindrome(n),
        'is_fibonacci': is_fibonacci(n) if n >= 0 else False,
        'fibonacci_position': fibonacci_position(n) if n >= 0 else -1,
        'factors': get_factors(n) if n != 0 else [],
        'prime_factorization': prime_factorization(n) if n != 0 else {},
        'sum_of_digits': sum_of_digits(n),
        'product_of_digits': product_of_digits(n),
        'binary': to_binary(n),
        'octal': to_octal(n),
        'hexadecimal': to_hexadecimal(n),
        'roman': to_roman(n) if 0 < n < 4000 else "N/A",
        'square': n ** 2,
        'cube': n ** 3,
        'square_root': math.sqrt(abs(n)) if n >= 0 else f"±{math.sqrt(abs(n)):.4f}i",
    }
    
    return info


def get_fun_facts(n: int) -> List[str]:
    """Generate fun facts about a number"""
    facts = []
    
    if n == 0:
        facts.append("Zero is the additive identity - adding 0 to any number gives that number.")
        facts.append("Zero is neither positive nor negative.")
        facts.append("Zero is the only number that cannot be a divisor.")
    elif n == 1:
        facts.append("One is the multiplicative identity - multiplying any number by 1 gives that number.")
        facts.append("One is neither prime nor composite.")
    elif n == 2:
        facts.append("Two is the only even prime number.")
        facts.append("Two is the smallest and first prime number.")
    
    if is_prime(n) and n > 2:
        facts.append(f"{n} is a prime number - it's only divisible by 1 and itself.")
    
    if is_perfect(n):
        facts.append(f"{n} is a perfect number - the sum of its proper divisors equals itself.")
    
    if is_armstrong(n):
        facts.append(f"{n} is an Armstrong number - the sum of its digits raised to the power of the number of digits equals itself.")
    
    if is_palindrome(n):
        facts.append(f"{n} is a palindrome - it reads the same forwards and backwards.")
    
    if is_fibonacci(n) and n > 0:
        pos = fibonacci_position(n)
        facts.append(f"{n} is the {pos}th number in the Fibonacci sequence.")
    
    if n > 0 and n == n ** 0.5 ** 2:
        facts.append(f"{n} is a perfect square ({int(n ** 0.5)}²).")
    
    if n > 0 and round(n ** (1/3)) ** 3 == n:
        facts.append(f"{n} is a perfect cube ({round(n ** (1/3))}³).")
    
    factors = get_factors(n) if n > 0 else []
    if len(factors) == 2 and n > 1:
        facts.append(f"{n} has exactly 2 factors, making it prime.")
    elif len(factors) > 2:
        facts.append(f"{n} has {len(factors)} factors.")
    
    return facts
