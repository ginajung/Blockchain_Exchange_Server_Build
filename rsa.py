import random
from rsa_util import mod_inverse
from rsa_util import is_prime

#The encryption exponent, e
#Do not change this value
e = 65537

def RSAKeygen(bitlen):
    while(True):
        p = random.SystemRandom().randint(1,pow(2,bitlen))
        if (is_prime(p)): 
            while(True):
                q = random.SystemRandom().randint(1,pow(2,bitlen))
                if (is_prime(q)):
                    n = p*q
                    d = mod_inverse(e,(p-1)*(q-1))
                    return [n,d]
                else:
                    continue
        else:
            continue

def RSAEncrypt(n,m):
	c = pow(m,e,n)
	#Code goes here
	return c

def RSADecrypt(n,d,c):
	m = pow (c,d,n)
	#Code goes here
	return m

