import math
import prime_generator as pg
import math_algorithms as m_alg


DEFAULT_EXPONENT = 65537


def encrypt(message, public):
    n, e, c, s = public
    if message < 0:
        raise ValueError('Only non-negative numbers are supported')

    if message > n:
        raise OverflowError("The message %i is too long for n=%i" % (message, n))

    if m_alg.jacobi_symbol(pow(message, 2) - c, n) == 1:
        b1 = 0
        y = message + math.sqrt(c)
        inv_y = message - math.sqrt(c)
    elif m_alg.jacobi_symbol(pow(message, 2), n) == 1:
        b1 = 1
        y = (message + math.sqrt(c)) * (s + math.sqrt(c))
        inv_y = (message - math.sqrt(c)) * (s - math.sqrt(c))
    else:
        b1 = 1
        y = (message + math.sqrt(c)) * (s + math.sqrt(c))
        inv_y = (message - math.sqrt(c)) * (s - math.sqrt(c))
    a = y / inv_y
    b2 = a % 2
    b0 = pow(message, e, n)
    return b0, b1, b2


def decrypt(crypto, private):
    c, s, d, n = private
    c0, c1, c2 = crypto
    a = (pow(c0, 2) + c) / (pow(c0, 2) - c)
    inv_a = (pow(c0, 2) - c) / (pow(c0, 2) + c)
    x = int((pow(a, d) + pow(inv_a, -d)) / 2)
    y = int((pow(a, d) - pow(inv_a, -d)) / (2 * math.sqrt(c)))
    a1 = x + y * math.sqrt(c)
    if a1 < 0 < c2 < 0 or a1 < 0 < c2:
        a1 = -a1
    if c1 == 1:
        a1 *= ((s - math.sqrt(c)) / (s + math.sqrt(c)))
    message = pow(c0, d, n)
    return message


def gen_keys(nbits):
    # Regenerate p and q values, until calculate_keys doesn't raise a
    # ValueError.
    while True:
        (p, q) = find_p_q(nbits // 2)
        try:
            (c, s, n) = find_c_s(p, q)
            (e, d, w) = find_w_e_d(p, q, c)
            break
        except ValueError:
            pass
    return (n, e, c, s), (c, s, d, n)


def find_p_q(nbits):
    # Make sure that p and q aren't too close or the factoring programs can
    # factor n.
    shift = nbits // 16
    pbits = nbits + shift
    qbits = nbits - shift

    # Choose the two initial primes
    while True:
        p = pg.get_prime(pbits)
        if (p - 3) % 4 == 0 and (p + 1) % 4 == 0:
            break
    while True:
        q = pg.get_prime(qbits)
        if q != p and (q - 3) % 4 == 0 and (q + 1) % 4 == 0:
            break
    return p, q


def find_c_s(p, q):
    n = p * q
    c = DEFAULT_EXPONENT
    while (p + m_alg.legendre_symbol(c, p)) % 4 != 0 or (q + m_alg.legendre_symbol(c, q)) % 4 != 0:
        c += 1

    s = DEFAULT_EXPONENT
    while m_alg.jacobi_symbol((s ** 2) - c, n) != -1 or math.gcd(s, n) != 1:
        s += 1
    return c, s, n


def find_w_e_d(p, q, c):
    w = ((p - m_alg.legendre_symbol(c, p)) * (q - m_alg.legendre_symbol(c, q))) / 4
    e, d = m_alg.calculate_keys_custom_exponent(p, q, exponent=DEFAULT_EXPONENT)
    return e, d, w
