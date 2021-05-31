from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256
import random


def sign(m):
	
    # order of g
    g = secp256k1.G
    n = secp256k1.q
    
    #generate private key: d and public key: d*g 
    d, publick_key = keys.gen_keypair(secp256k1)
    
	#generate signature
    r,s = fastecdsa.ecdsa.sign(m, d, secp256k1, sha256)

    assert isinstance( public_key, point.Point )
    assert isinstance( r, int)
    assert isinstance( s, int)
    return( public_key, [r,s])