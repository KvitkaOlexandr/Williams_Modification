import math


def jacobi_symbol(a, b):
    if math.gcd(a, b) != 1:
        return 0
    r = 1
    if a < 0:
        a = -a
        if b % 4 == 3:
            r = -r
    while a != 0:
        t = 0
        while a % 2 == 0:
            t += 1
            a = a / 2
        if t % 2 == 1:
            if b % 8 == 3 or b % 8 == 5:
                r = -r
        if a % 4 == 3 and b % 4 == 3:
            r = -r
        c = a
        a = b % c
        b = c
    return r


def legendre_symbol(a, b):
    if a >= b or a < 0:
        return legendre_symbol(a % b, b)
    elif a == 0 or a == 1:
        return a
    elif a == 2:
        if b % 8 == 1 or b % 8 == 7:
            return 1
        else:
            return -1
    elif a == b - 1:
        if b % 4 == 1:
            return 1
        else:
            return -1
    elif not is_prime(a):
        factors = factorize(a)
        product = 1
        for pi in factors:
            product *= legendre_symbol(pi, b)
        return product
    else:
        if not ((b - 1) // 2) % 2 == 0 or ((a - 1) // 2) % 2:
            return legendre_symbol(b, a)
        else:
            return (-1) * legendre_symbol(b, a)


def is_prime(a):
    return all(a % i for i in range(2, a))


def factorize(n):
    factors = []
    p = 2
    while True:
        while n % p == 0 and n > 0:
            factors.append(p)
            n = n / p
        p += 1
        if p > n / p:
            break
    if n > 1:
        factors.append(int(n))
    return factors


def calculate_keys_custom_exponent(p, q, exponent):
    phi_n = (p - 1) * (q - 1)

    try:
        d = inverse(exponent, phi_n)
    except NotRelativePrimeError as ex:
        raise NotRelativePrimeError(
            exponent, phi_n, ex.d,
            msg="e (%d) and phi_n (%d) are not relatively prime (divider=%i)" %
                (exponent, phi_n, ex.d))

    if (exponent * d) % phi_n != 1:
        raise ValueError("e (%d) and d (%d) are not mult. inv. modulo "
                         "phi_n (%d)" % (exponent, d, phi_n))

    return exponent, d


def mod_calculate_keys_custom_exponent(p, q, f, exponent):
    phi_n = (p - 1) * (q - 1) * (f - 1)

    try:
        d = inverse(exponent, phi_n)
    except NotRelativePrimeError as ex:
        raise NotRelativePrimeError(
            exponent, phi_n, ex.d,
            msg="e (%d) and phi_n (%d) are not relatively prime (divider=%i)" %
                (exponent, phi_n, ex.d))

    if (exponent * d) % phi_n != 1:
        raise ValueError("e (%d) and d (%d) are not mult. inv. modulo "
                         "phi_n (%d)" % (exponent, d, phi_n))

    return exponent, d


def inverse(x, n):
    (divider, inv, _) = extended_gcd(x, n)

    if divider != 1:
        raise NotRelativePrimeError(x, n, divider)

    return inv


def extended_gcd(a, b):
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    return a, lx, ly  # Return only positive values


class NotRelativePrimeError(ValueError):
    def __init__(self, a, b, d, msg=None):
        super(NotRelativePrimeError, self).__init__(
            msg or "%d and %d are not relatively prime, divider=%i" % (a, b, d))
        self.a = a
        self.b = b
        self.d = d