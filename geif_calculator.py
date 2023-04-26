from ge_integers import GEInteger, GaussianInteger, EisensteinInteger
from prime_factorization import factor_ge_integer


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