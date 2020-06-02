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
    elif m_alg.jacobi_symbol(pow(message, 2) - c, n) == -1:
        b1 = 1
        y = (message + math.sqrt(c)) * (s + math.sqrt(c))
        inv_y = (message - math.sqrt(c)) * (s - math.sqrt(c))
    else:
        raise ValueError
    a = y / inv_y
    b2 = a % 2
    b0 = m_alg.culc_func(message, e, n, a)
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
        (p, q, f) = find_p_q_f(nbits // 3)
        try:
            (c, s, n) = find_c_s(p, q, f)
            (e, d, w) = find_w_e_d(p, q, f, c)
            break
        except ValueError:
            pass
    return (n, e, c, s), (c, s, d, n)


def find_p_q_f(nbits):
    # Make sure that p and q aren't too close or the factoring programs can
    # factor n.
    shift = nbits // 16
    pbits = nbits + shift
    qbits = nbits - shift
    fbits = nbits

    # Choose the two initial primes
    while True:
        p = pg.get_prime(pbits)
        if (p - 3) % 4 == 0 and (p + 1) % 4 == 0:
            break
    while True:
        q = pg.get_prime(qbits)
        if q != p and (q - 3) % 4 == 0 and (q + 1) % 4 == 0:
            break
    while True:
        f = pg.get_prime(fbits)
        if f != p and f != q and (f - 3) % 4 == 0 and (f + 1) % 4 == 0:
            break
    return p, q, f


def find_c_s(p, q, f):
    n = p * q * f
    c = DEFAULT_EXPONENT
    while (p + m_alg.legendre_symbol(c, p)) % 4 != 0 \
            or (q + m_alg.legendre_symbol(c, q)) % 4 != 0 or (f + m_alg.legendre_symbol(c, f)) % 4 != 0:
        c += 1

    s = DEFAULT_EXPONENT
    while m_alg.jacobi_symbol((s ** 2) - c, n) != -1 or math.gcd(s, n) != 1:
        s += 1
    return c, s, n


def find_w_e_d(p, q, f, c):
    w = (p - m_alg.legendre_symbol(c, p)) * (q - m_alg.legendre_symbol(c, q)) * (f - m_alg.legendre_symbol(c, f)) / 8
    e, d = m_alg.mod_calculate_keys(p, q, f, exponent=DEFAULT_EXPONENT)
    return e, d, w
