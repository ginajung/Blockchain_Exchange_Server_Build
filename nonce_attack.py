from fastecdsa.keys import export_key, gen_keypair
from fastecdsa import curve, ecdsa, keys
from fastecdsa.point import Point
import os
import hashlib

#sig1 and sig2 should be lists of length 2, i.e., sig1 = [r1,s1] and sig2 = [r2,s2]
def recoverkey( sig1, sig2, m1, m2, pk ):
        if sig1[0] != sig2[0]:
            print( "Signatures were generated with different nonces" )
        #Your code here
        d = 0
        return d

