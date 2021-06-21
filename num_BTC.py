import math

# block 1 ; 50 BTC
# block 2 ; 100 BTC
# input is block height(integer)
# output total number of tokens mined so far

def num_BTC(b):
    # get total block number
    num_block=b
#     for h in range (1,b+1):
#         num_block += pow(2,h-1)
    
    # get quotient and remainder
    q = num_block // 210000
    mod = num_block % 210000
   
    #print("num_block: {}, mod : {}, quoient : {}".format(num_block, mod, q))
    
    c =0
    if q == 0:
        c = num_block * 50 
    
    else: 
        c = (50 * pow(2,-q)) * mod 
        #print (c)
        for i in range (q+1):
            pre_c = 50*pow(2,-i)* 210000
            c += pre_c
    c = float(c)
    return c


