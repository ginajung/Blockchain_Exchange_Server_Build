import hashlib
import os
from random import randint

def hash_collision(k):
    if not isinstance(k,int):
        print( "hash_collision expects an integer" )
        return( b'\x00',b'\x00' )
    if k < 0:
        print( "Specify a positive number of bits" )
        return( b'\x00',b'\x00' )
   
    #Collision finding code goes here
    
    # generate random bytes and get hashing using SHA256
    # convert to hex and to binary bits
    # compare SHA256(x)
    
    r_m= randint(1,20)
    x = os.urandom(r_m) # random bytes with size randomly picked by randint(1,20)
    hex_x= hashlib.sha256( x ).hexdigest()
    x_bin = bin(int(hex_x,base=16))[2:]
        
    while(True):
        r_n= randint(1,20)
        y = os.urandom(r_n)
        hex_y= hashlib.sha256( y ).hexdigest()
        y_bin = bin(int(hex_y,base=16))[2:]
        if x_bin[-k:] == y_bin[-k:] and x !=y:
            return(x,y)
        else:
            continue