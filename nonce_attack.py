from fastecdsa.keys import export_key, gen_keypair
from fastecdsa import curve, ecdsa, keys
from fastecdsa.point import Point
import os
from hashlib import sha256

#sig1 and sig2 should be lists of length 2, i.e., sig1 = [r1,s1] and sig2 = [r2,s2]
def recoverkey( sig1, sig2, m1, m2, pk ):
    
        if sig1[0] != sig2[0]:
            print( "Signatures were generated with different nonces" )
        #Your code here
        
        while(True):
            
            d, public_key = keys.gen_keypair(secp256k1)
            if(pk == public_key and m1 != m2):
                
#                 r1,s1 = ecdsa.sign(m1, d, secp256k1, sha256)
#                 r2,s2 = ecdsa.sign(m2, d, secp256k1, sha256)
                ver1 =ecdsa.verify(sig1, m1, pk, secp256k1, sha256)
                ver2 = ecdsa.verify(sig2, m2, pk, secp256k1, sha256)
                if (ver1==True and ver2== True):
                    return d
                else:
                    continue
                
            # to veryfy
            