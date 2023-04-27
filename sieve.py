from math import isqrt
import sys

DEFAULT_EXTEND_PRIMES = 100


def sieve_of_eratosthenes(n: int):
    """Creates a list of size n + 1 where l[i] is True iff
    i is a prime number.

    Args:
        n (int): The size of the sieve

    Raises:
        ValueError: when n is less than 2

    Returns:
        list[bool]: a list of size n + 1 where l[i] is True iff
                    i is a prime number
    """

    if n < 2:
        raise ValueError("n must be at least 2")

    sieve = [True] * (n + 1)
    sieve[0] = False
    sieve[1] = False

    i = 2
    i2 = 4
    while i2 <= n:
        if not sieve[i]:
            i += 1
            i2 = i**2
            continue

        for j in range(i2, n + 1, i):
            sieve[j] = False

        i += 1
        i2 = i**2

    return sieve


def extend_primes(primes: list[int], new_max: int | None = None):
    """Given a list of all primes from 2 to primes[-1], generate all primes
    from primes[-1] + 2 to new_max, and append it to the previous list.
    Basically perform one segment of the segmented Sieve of Eratosthenes,
    which is a more memory efficient version of the sieve.

    Args:
        primes (list[int]): A list of all primes from 2 to primes[-1]. Can be empty
        new_max (int | None, optional): The new maximum value of a prime in the list.
                Defaults to None, in which case 2 * primes[-1] is used.

    Raises:
        ValueError: when new_max is less than 2
    """

    if new_max and new_max < 2:
        raise ValueError("new_max must be at least 2")

    if not primes:
        primes += generate_primes(new_max if new_max else DEFAULT_EXTEND_PRIMES)
        return

    if new_max == None:
        new_max = 2 * primes[-1]
    elif new_max <= primes[-1]:
        return

    sieve = [True] * (new_max - primes[-1])

    for prime in primes:
        if prime > new_max // 2:
            break

        for i in range(primes[-1] - (primes[-1] % prime) + prime, new_max + 1,
                       prime):
            sieve[i - primes[-1] - 1] = False

    i = primes[-1] + 1
    i2 = i**2
    while i2 <= new_max:
        if not sieve[i - primes[-1] - 1]:
            i += 1
            i2 = i**2
            continue

        for j in range(i2, new_max + 1, i):
            sieve[j - primes[-1] - 1] = False

        i += 1
        i2 = i**2

    primes.extend(
        i for i, is_prime in enumerate(sieve, primes[-1] + 1) if is_prime)


def generate_primes(n: int):
    """Find all primes between 2 and n

    Args:
        n (int): the maximum number to find primes at

    Returns:
        list[int]: a list of all primes between 2 and n
    """
    return [
        i for i, is_prime in enumerate(sieve_of_eratosthenes(n)) if is_prime
    ]


def generate_primes_segmented(n: int):
    """Find all primes between 2 and n. Uses a segmented sieve to use less memory.

    Args:
        n (int): the maximum number to find primes at

    Returns:
        list[int]: a list of all primes between 2 and n
    """
    primes: list[int] = []
    step = isqrt(n)

    for new_max in range(step, step, n):
        extend_primes(primes, new_max)

    extend_primes(primes, n)
    return primes


def output_primes_to_file_compressed(output_file: str,
                                     max_prime: int = 1_000_000):

    primes = generate_primes_segmented(max_prime)

    with open(output_file, 'wb') as f:
        for p in primes:
            f.write(p.to_bytes(4, 'little'))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        output_primes_to_file_compressed(sys.argv[1])
    elif len(sys.argv) == 3:
        try:
            output_primes_to_file_compressed(sys.argv[1], int(sys.argv[2]))
        except ValueError:
            print("Please input an integer as max_integer")
    else:
        print("Usage: python sieve.py output_file [max_integer]")
