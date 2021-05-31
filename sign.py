from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256
import random


def sign(m):
    
	# private key
    #d = random.SystemRandom().randint(1,n-1)
    g = secp256k1.G
    n = secp256k1.q
    
    #generate public key d*g
	#public_key = keys.get_public_key(d,secp256k1)
    
    
    d, publick_key = keys.gen_keypair(secp256k1)
    x1=public_key.x
    y1=public_key.y
    
	#generate signature
	#Your code here
    
# 	r = pow(x1,1,n)
#     if (r==0):
        
#     z = sha256( m )
# 	s = pow(d,-1,n)* pow(z+rd,1,n)
    
    r,s = fastecdsa.ecdsa.sign(m, d, secp256k1, sha256)
    assert isinstance( public_key, point.Point )
    assert isinstance( r, int )
    assert isinstance( s, int )
    return( public_key, [r,s] )