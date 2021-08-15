import random

systemRandom = random.SystemRandom()

def legendre(a, p):
	if p < 2:
		raise ValueError('p must be >=2')
	if (a == 0) or (a == 1):
		return a
	if a % 2 == 0:
		r = legendre(a // 2, p)
		if ((p * p - 1) % 16) != 0:
			r *= -1
	else:
		r = legendre(p % a, a)
		if a % 4 == 3 and p % 4 == 3:
			r *= -1
	return r


def is_prime(n):
	if n == 2 or n == 3:
		return True
	if n % 2 == 0 or n % 3 == 0:
		return False

	k = 100
	for i in range(k):
		a = random.SystemRandom().randint(2,n-1)
		x = legendre(a, n)
		y = pow(a, (n - 1) // 2, n)
		if (x == 0) or (y != x % n):
			return False
	return True


def mod_inverse(a, m) : 
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
        # q is quotient 
        q = a // m 
        t = m 
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
        # Update x and y 
        y = x - q * y 
        x = t 
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
    return x 

