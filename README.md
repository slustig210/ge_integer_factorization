# Gaussian/Eisenstein Integer Factorization Calculator

Hi! I have 10 pages of documentation in a PDF document so this doc will be brief :)

## General program layout

All of the functions that perform modular arithmetic are in the file `mod_arith.py`.

The classes defining Gaussian and Eisenstein integers are in the file `ge_integers.py`.

Lastly, the function for factoring a G/E integer into G/E primes is located in `ge_factorization.py`.

## Running the code


The only requirement is sympy. I wrote this in python3.10, but tried to make it so 3.9 works as well, but haven't tested it. So make sure you are running python3.9+.

Install sympy using `pip install sympy`, or `pip install -r requirements.txt`.

Then, run the code with the command `python ge_factorization.py`.
