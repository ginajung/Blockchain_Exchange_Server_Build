from random import randint

from params import p
from params import g

# p-1 = 2q
# g is chosen to have order q , g^q = 1 mod p


q = pow(g,-1,p)
assert (q*g)%p ==1

def keygen():
    # if q is the order of g
    #q = ordermod(g,p)
    a = randint(1,q)
    
    # if q is unknown, (1,p)
    h = pow(g,a,p)
    sk = a
    pk = h
    
    return pk,sk

def encrypt(pk,m):
    r = randint(1,q)
    c1 = pow(g,r,p)   
  # c2 = h^r *m mod p
    mes= (pk**r)*m
    c2 = mes % p
    return [c1,c2]

def decrypt(sk,c):
    
    c1= c[0]**sk
    c2 =c[1]
    m = c2/c1 % p
    return m

