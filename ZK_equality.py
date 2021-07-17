from zksk import Secret, DLRep
from zksk import utils

def ZK_equality(G,H):

    
    #Enc(m)=(r∗G,m∗G+r∗H)
    
    #C1 =r1∗G
    #C2=r1∗H+m∗G
    #D1=r2∗G
    #D2=r2∗H+m∗G
 


# Setup: Peggy and Victor agree on two group generators.
# Since Peggy is *committing* rather than encrypted Peggy doesn't know DL_G(H)
G, H = utils.make_generators(num=2, seed=42)

# Setup: generate a secret randomizer for the commitment scheme.
r = Secret(utils.get_random_num(bits=128))

# This is Peggy's secret bit.
top_secret_bit = 1

# A Pedersen commitment to the secret bit.
C = top_secret_bit * G + r.value * H

# Peggy's definition of the proof statement, and proof generation.
# (The first or-clause corresponds to the secret value 0, and the second to the value 1. Because
# the real value of the bit is 1, the clause that corresponds to zero is marked as simulated.)
stmt = DLRep(C, r * H, simulated=True) | DLRep(C - G, r * H)
zk_proof = stmt.prove()


    #Generate a NIZK proving equality of the plaintexts
    
    
        #stmt = DLRep(C1,r1*G) & DLRep(C2,r1*H+m*G) & DLRep(D1,r2*G) & DLRep(D2,r2*H+m*G)

    #Return two ciphertexts and the proof
    return (C1,C2), (D1,D2), zk_proof

