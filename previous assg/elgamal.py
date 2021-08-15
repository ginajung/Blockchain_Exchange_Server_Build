import random 

from params import p
from params import g

# g is chosen to have order q , g^q = 1 mod p

def keygen():
    # if q is the order of g
#     if( pow(g,q,p)==1):
#         a = random.SystemRandom().randint(1,q)
#     # if q is unknown, (1,p)
#     else: 
    a = random.SystemRandom().randint(1,p)
    h = pow(g,a,p)
    sk = a
    pk = h
    
    return pk,sk

def encrypt(pk,m):
    # set  (𝑐1,𝑐2)=(𝑔^𝑟𝑚𝑜𝑑𝑝,ℎ^𝑟⋅𝑚 𝑚𝑜𝑑 𝑝) 
    
    r = random.SystemRandom().randint(1,p)
    c1 = pow(g,r,p)      
    pre_c2= pow(pk,r,p)* pow(m,1,p)
    c2 = pow(pre_c2,1, p)
    return c1,c2

def decrypt(sk,c):
    # 𝑚=𝑐2/𝑐1^𝑎 𝑚𝑜𝑑 𝑝
    
    mes = pow(c[1],1,p)* pow(c[0],-sk,p) 
    m=mes%p
    return m

