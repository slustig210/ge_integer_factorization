from typing import TypeVar

from ge_integers import GEInteger, GaussianInteger, EisensteinInteger
from sympy.ntheory import factorint

T = TypeVar("T", bound=GEInteger)


def factor_ge_integer(z: T) -> list[tuple[T, int]]:
    factorization: list[tuple[T, int]] = []

    typ = type(z)

    norm_factorization: dict[int, int] = factorint(z.norm())

    for p, count in norm_factorization.items():
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
        while num_divisions < count:
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


def factor_and_print_ge_integer(z: GEInteger):
    l = factor_ge_integer(z)

    strs = []
    for p, e in l:
        s = str(p)
        if e == 1:
            strs.append(s)
            continue

        if s[0] != '(':
            s = f'({s})'

        strs.append(f'{s}^{e}')

    print(f"{z} = " + " * ".join(strs))

    # double check the product
    prod = type(z)(1)
    for p, e in l:
        prod *= p**e

    assert z == prod


def main():
    print("\nFactor a G/E Integer!")
    while True:
        print("\n[1] Gaussian Integer\n[2] Eisenstein Integer\n[3] Exit\n")
        choice_str = input("Pick a choice: ")
        try:
            choice = int(choice_str)
        except ValueError:
            choice = 0

        if not (1 <= choice <= 3):
            print("Please enter a valid choice (1, 2, 3)")
            continue

        if choice == 3:
            break

        if choice == 1:
            typ = GaussianInteger
            print("Enter a Gaussian integer to factor (ex: 5 + 8i):")
        else:
            typ = EisensteinInteger
            print("Enter an Eisenstein integer to factor (ex: 5 + 8w):")

        z_str = input()

        try:
            z = typ.from_string(z_str)
        except ValueError:
            print("Please enter a valid input for " + typ.__name__)
            continue

        print(f"Input: {z}")

        factor_and_print_ge_integer(z)


if __name__ == '__main__':
    main()