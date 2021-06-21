import math

# block 1 ; 50 BTC
# block 2 ; 100 BTC
# input is block height(integer)
# output total number of tokens mined so far

def num_BTC(b):
    # get total block number
    num_block=0
    for h in range (1,b+1):
        num_block += pow(2,h-1)
    
    # get quotient and remainder
    q = num_block // 210000
    mod = num_block % 210000
    #print("num_block", num_block)
    c =0
    if q == 0:
        c = num_block * 50 
    
    else: 
        for i in range (1,q+1):
            pre_c = 50/pow(2,i)*210000.00
            c += pre_c
        c += (50/pow(2,q)) * mod  
    
    c = float(c)
    return c


