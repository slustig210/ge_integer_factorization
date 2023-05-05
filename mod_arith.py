import random


# follows the pseudocode in Prime Numbers: A Computational Perspective, page 98
# Algorithm 2.3.5
def jacobi_symbol(a: int, m: int):
    """Calculate the Jacobi symbol (a/m)

    Args:
        a (int): Any integer
        m (int): Any odd positive integer

    Raises:
        ValueError: if m is not positive or odd

    Returns:
        int: The value of the Jacobi symbol (a/m)
    """

    if m < 0 or m % 2 == 0:
        raise ValueError("m must be a positive odd integer")

    a %= m

    t = 1

    while a != 0:
        while a % 2 == 0:
            a //= 2
            if (m % 8) in (3, 5):
                t = -t

        a, m = m, a

        if a % 4 == 3 == m % 4:
            t = -t

        a %= m

    if m == 1:
        return t

    return 0


# follows the pseudocode in Prime Numbers: A Computational Perspective, page 459
# Algorithm 9.3.2
# pow is a python builtin, this alg is equivalent to pow(base, exponent, modulus)
def modular_pow(base: int, exponent: int, modulus: int):
    """Computes base**exponent mod modulus by repeated squaring and multiplication.

    Args:
        base (int): any integer
        exponent (int): any non-negative integer
        modulus (int): any positive integer

    Raises:
        ValueError: negative exponent
        ValueError: non-positive modulus

    Returns:
        int: base**exponent % modulus. Equivalent to pow(base, exponent, modulus)
    """

    if exponent < 0:
        raise ValueError("exponent must be a non-negative integer")

    if modulus <= 0:
        raise ValueError("modulus must be a positive integer")

    if modulus == 1:
        return 0

    a = 1
    base %= modulus

    if exponent == 0:
        return 1

    if base == 0:
        return 0

    while exponent != 1:
        if exponent % 2 == 1:
            a = (a * base) % modulus

        base = (base**2) % modulus
        exponent //= 2

    return (a * base) % modulus


# follows pseudocode of algorithm 9.2.11, page 454, from the book
# equivalent to python's math.isqrt
def isqrt(n: int):
    if n < 0:
        raise ValueError("cannot take the square root of a negative integer")

    x: int = 2**((n.bit_length() + 1) // 2)

    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x

        x = y


# follows the pseudocode in Prime Numbers: A Computational Perspective, page 100
# Algorithm 2.3.8
# assumes p is prime and (a/p) = 1
def tonelli_shanks(a: int, p: int):
    """Solves for x in the equation x**2 = a (mod p)

    Args:
        a (int): Any integer such that the Legendre symbol (a/p) is 1
        p (int): Any odd prime

    Raises:
        ValueError: p is even (p must be an odd prime)

    Returns:
        int: an integer x such that x**2 = a (mod p)
    """

    if p % 2 == 0:
        raise ValueError("p must be an odd prime")

    a %= p

    if p % 8 in (3, 7):
        return modular_pow(a, (p + 1) // 4, p)

    if p % 8 == 5:
        x = modular_pow(a, (p + 3) // 8, p)
        if (x**2 % p) != a:
            x = (x * modular_pow(2, (p - 1) // 4, p)) % p
        return x

    # p % 8 == 1

    # usually takes 2 tries, since about half of the
    # range is made up of quadratic nonresidues
    while True:
        d = random.randint(2, p - 2)  # p >= 11 so this should work
        if jacobi_symbol(d, p) == -1:
            break

    # p - 1 = 2**s * t
    s = 0
    t = p - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    big_a = modular_pow(a, t, p)
    big_d = modular_pow(d, t, p)

    m = 0

    for i in range(s):
        if modular_pow((big_a * modular_pow(big_d, m, p)) % p, 2**(s - 1 - i),
                       p) % p == p - 1:

            m += 2**i

    return (modular_pow(a, (t + 1) // 2, p) * modular_pow(big_d, m // 2, p)) % p


# follows the pseudocode in Prime Numbers: A Computational Perspective, page 120
# Algorithm 2.3.12
def cornacchias(d: int, p: int):
    """Solve for x and y in the equation x^2 + dy^2 = p

    Args:
        d (int): Any positive integer less than p
        p (int): Any odd prime

    Raises:
        ValueError: when it is not true that 1 <= d <= p
        ValueError: when d and p are not coprime (p should be prime!)

    Returns:
        tuple[int, int] | None: either (x, y) such that x^2 + dy^2 = p, or None if no solution exists
    """

    if p % 2 == 0:
        raise ValueError("p must be an odd prime")

    if not (1 <= d < p):
        raise ValueError("1 <= d < p must be true")

    j = jacobi_symbol(-d, p)

    if j == -1:
        return None

    if j == 0:
        raise ValueError("p must be an odd prime")

    x0 = tonelli_shanks(-d, p)
    if 2 * x0 < p:
        x0 = p - x0

    a, b = p, x0

    c = isqrt(p)

    while b > c:
        a, b = b, a % b

    t = p - b**2
    td = t // d
    if td * d != t:
        return None

    srtd = isqrt(td)
    if srtd**2 != td:
        return None

    return b, srtd


def cornacchia_solver():
    print("\nWelcome to Cornacchia Solver!\n")
    print("Please input a positive d and an odd prime p,")
    print("And I will try to find integers x and y such that")
    print("x^2 + d * y^2 = p. Bad inputs may result in an infinite loop\n")

    while True:
        try:
            d = int(input("d = "))
            p = int(input("p = "))
        except ValueError:
            print("Please input d and p as integers")
            continue

        try:
            result = cornacchias(d, p)
        except Exception as e:
            print("Error!")
            print(e)
            continue

        if not result:
            print("No solutions!")
            continue

        x, y = result

        print(f"{x}^2 + {d} * {y}^2 = {p}")

        assert x**2 + d * y**2 == p


if __name__ == '__main__':
    cornacchia_solver()
