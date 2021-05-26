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
    #c2 = (pk**r) *m % p
    c2= pow(pk,r,p) *m %p
    
    return [c1,c2]

def decrypt(sk,c):
    
    m =pow((c[0]**sk)/c[1],1,p) 
   
    return m

