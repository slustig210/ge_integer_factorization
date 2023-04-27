from typing import TypeVar

from ge_integers import GEInteger, GaussianInteger, EisensteinInteger
from sieve import extend_primes

PRIMES: list[int] = []


def factor_integer(n: int):
    """Factor an integer in

    Args:
        n (int): 

    Raises:
        ValueError: 

    Returns:
        dict[int, int]: 
    """

    factorization = list[tuple[int, int]]()

    if n < 1:
        raise ValueError(
            "factor_integer requires a positive integer as the first argument")

    if n == 1:
        return factorization

    i = 0
    while True:
        if i >= len(PRIMES):
            # could potentially make this (and PRIMES) a parameter to
            # try different prime generators
            extend_primes(PRIMES)

        prime = PRIMES[i]

        num_divisions = 0
        while n % prime == 0:
            n //= prime
            num_divisions += 1

        if num_divisions != 0:
            factorization.append((prime, num_divisions))

        if n == 1:
            return factorization

        i += 1


T = TypeVar("T", bound=GEInteger)


def factor_ge_integer(z: T) -> list[tuple[T, int]]:
    factorization: list[tuple[T, int]] = []

    typ = type(z)

    for p, count in factor_integer(z.norm()):
        if typ.ramifies(p):
            # evenly split between factor and its conjugate
            # using the fact that 1-i and 1-w are both type (R) as a shortcut
            factor2 = typ(1, -1)
            factor1 = factor2.conj()

            count1 = (count + 1) // 2  # ceil(count / 2)
            factorization.append((factor1, count1))
            z //= factor1**count1

            count2 = count - count1
            if count2 != 0:
                factorization.append((factor2, count // 2))
                z //= factor2**count2

            continue

        if typ.is_inert(p):
            assert count % 2 == 0

            factor = typ(p)
            factorization.append((factor, count // 2))

            z //= factor**(count // 2)
            continue

        # p splits
        factor = typ.factor_type_s(p)

        # either factor or its conjugate divides z
        # idk if this part could be sped up
        num_divisions = 0
        while num_divisions <= count:
            q1 = z // factor
            if q1 * factor == z:
                z = q1
                num_divisions += 1
            else:
                break

        if num_divisions:
            factorization.append((factor, num_divisions))

        remaining = count - num_divisions
        if remaining == 0:
            continue

        factor = factor.conj()

        factorization.append((factor, remaining))
        z //= factor**remaining

    if z != typ(1):
        factorization = [(z, 1)] + factorization

    return factorization