import random

#alpha: selfish miners mining power (percentage),
# 1-alpha: honest mining power
#gamma: the ratio of honest miners choose to mine on the selfish miners pool's block
# 1-gamma : honest choose on honest 
#N: number of simulations run

def Simulate(alpha,gamma,N, seed):
    # DO NOT CHANGE. This is used to test your function despite randomness
    random.seed(seed)
  
    #the same as the state of the state machine in the slides (selfish blocks - honest blocks)
    state=0
    # the length of the blockchain
    ChainLength=0
    # the revenue of the selfish mining pool
    SelfishRevenue=0
    # Hiddenblock
   
    
    
    #A round begin when the state=0
    for i in range(N):
        r=random.random()
        if state==0:
            #The selfish pool has 0 hidden block.
            
            if r<=alpha:
                #The selfish pool mines a block.
                #They don't publish it. 
                state=1
                
            else:
                #The honest miners found a block.
                #The round is finished : the honest miners found 1 block
                # and the selfish miners found 0 block.
                ChainLength+=1
                state=0
                
        elif state==1:
            #The selfish pool has 1 hidden block.
            Hiddenblock = 1
            if r<=alpha:
                #The selfish miners found a new block.
                #Write a piece of code to change the required variables.
                #You might need to define new variable to keep track of the number of hidden blocks.
                
                Hiddenblock += 1
                state = 2
                
            else:
                #Write a piece of code to change the required variables. 
                state = -1
                ChainLength +=1
                

        elif state==-1:
            #It's the state 0' in the slides (the paper of Eyal and Gun Sirer)
            #There are three situations! 
            #Write a piece of code to change the required variables in each one.
            
            Hiddenblock =0
            if r<=alpha:
                #selfish find a block on pool head
                # pool obtain a revenue of 2
                state = 0
                ChainLength +=1
                SelfishRevenue +=2
                
                
            elif r<=alpha+(1-alpha)*gamma:
                # others find a block after pool head
                # both obtain a revenue of 1 each
                state = 0
                ChainLength +=1
                SelfishRevenue +=1
                
            else:
                # others find a block after others' head
                # others obtain a revenue of 2
                state = 0
                ChainLength+=1

        elif state==2:
            
             #The selfish pool has 2 hidden block.
            if r<=alpha:
                state = 3
                
            else:
                #The honest miners found a block.
                state =0
                ChainLength+=2
                SelfishRevenue +=2

        elif state>2:
            Hiddenblock = state
            if r<=alpha:
                #The selfish miners found a new block
                state += state
                Hiddenblock += 1
            else:
                #The honest miners found a block
                while(Hiddenblock > 2):
                    state -= state
                    Hiddenblock -= 1
                    ChainLength+=1
                    SelfishRevenue +=1

    return float(SelfishRevenue)/ChainLength

""" 
  Uncomment out the following lines to try out your code
  DON'T include it in your final submission though.
"""

# #let's run the code with the follwing parameters!
# alpha=0.35
# gamma=0.5
# Nsimu=10**7
# seed = 100

# #This is the theoretical probability computed in the original paper
# print("Theoretical probability :",(alpha*(1-alpha)**2*(4*alpha+gamma*(1-2*alpha))-alpha**3)/(1-alpha*(1+(2-alpha)*alpha)))
# print("Simulated probability :",Simulate(alpha,gamma,Nsimu, seed))
