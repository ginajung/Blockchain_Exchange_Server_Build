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
    x = os.urandom(10) # 256 bits
    SHA256.update(x)
    s_x= list(SHA256.hexdigest())
    
    y = os.urandom(10)
    SHA256.update(y)
    s_y= list(SHA256.hexdigest())
    
    if(s_x[63-k:63]==s_y[63-k:63]):
        return (x.hex(),y.hex())
    
#     for i in range(63-k,63):
#         if(s_x[i]==(s_y[i])):
#             continue
#         else:
#             print('Error')
        
#         return( s_x, s_y )
    

    
    





