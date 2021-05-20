import hashlib
import os

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    
    
    while(True):
        size = 5
        nonce = os.urandom(size)
    
        hex_nonce= hashlib.sha256( nonce ).hexdigest()
        bin_nonce = bin(int(hex_nonce,base=16))[2:]
    
    
        if target_string[:] == bin_nonce[-len(target_string):] and len(target_string) != len(bin_nonce):
            return(nonce)
        else:
            continue
    



