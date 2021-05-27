import random
from rsa_util import mod_inverse
from rsa_util import is_prime

#The encryption exponent, e
#Do not change this value
e = 65537

def RSAKeygen(bitlen):
    p = random.SystemRandom().randint(1,pow(2,bitlen))
    q = random.SystemRandom().randint(1,pow(2,bitlen))
    n = p*q
    d = pow(e, -1, (p-1)*(q-1))
    return [n,d]

def RSAEncrypt(n,m):
	c = pow(m,e,n)
	#Code goes here
	return c

def RSADecrypt(n,d,c):
	m = pow (c,d,n)
	#Code goes here
	return m

