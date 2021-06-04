from fastecdsa.keys import export_key, gen_keypair
from fastecdsa import curve, ecdsa, keys
from fastecdsa.point import Point
import os
from hashlib import sha256

#sig1 and sig2 should be lists of length 2, i.e., sig1 = [r1,s1] and sig2 = [r2,s2]
def recoverkey( sig1, sig2, m1, m2, pk ):
    
    # Key generation : private key = d , public key = pk =dG
    # Signature : r = kG.x.  if the same nonce(k) used, then r will be same/ s is different
    
    
    if sig1[0] != sig2[0]:
        print( "Signatures were generated with different nonces" )
    
    # when r1 == r2 , recover k 
    else:
    # order of g
        g = secp256k1.G
        n = secp256k1.q
        r1 = sig1[0]
        r2 = sig2[0]
        s1 = sig1[1]
        s2 = sig2[1]
        z1 = sha256(m1)
        z2 = sha256(m2)
        
    # recover, k = 'nonce' & d private key
        k =(pow((s1-s2),1,n)* pow((z1−z2),−1,n)) % n
        pre_d = (s1 % n)* pow((k-z1),1,n)*pow(r,-1,n)
        d = pre_d % n
        
    
    # if correct k, then r1 = r2 = kG.x   
    # (keys.get_public_key(k,secp256k1).x == r1)&&
        if (keys.get_public_key(k,secp256k1).x == r1 or keys.get_public_key(k,secp256k1).x == -r1 ):
            
    # if correct d, then pk =dG
            if ((keys.get_public_key(d, secp256k1) == pk)):
                return d
           

    # ecdsa.verify(sig1, m1, pk, secp256k1, sha256) 