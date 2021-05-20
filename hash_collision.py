import hashlib
import os

SHA256 = hashlib.sha256()

def hash_collision(k):
    if not isinstance(k,int):
        print( "hash_collision expects an integer" )
        return( b'\x00',b'\x00' )
    if k < 0:
        print( "Specify a positive number of bits" )
        return( b'\x00',b'\x00' )
   
    #Collision finding code goes here
    
    # generate random bytes / compare SHA256(x)
    while(True):
        x = os.urandom(2) # 256 bits
        SHA256.update(x)
        hex_x= SHA256.hexdigest()
        x_bin = bin(int(hex_x,base=16))[:]
        
    
        y = os.urandom(2)
        SHA256.update(y)
        hex_y= SHA256.hexdigest()
        y_bin = bin(int(hex_y,base=16))[:]
    
        if x_bin[-k:]==y_bin[-k:] and x !=y:
            return(x,y)
    
