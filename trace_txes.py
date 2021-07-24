from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []

        
# tx_hash - (string) the tx_hash on the Bitcoin blockchain
# n - (int) the position of this output in the transaction
# amount - (int) the value of this transaction output (in Satoshi)
# owner - (string) the Bitcoin address of the owner of this output
# time - (Datetime) the time of this transaction as a datetime object
# inputs - (TXO[]) a list of TXO objects

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4) 
    
    
    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        #pass
        #YOUR CODE HERE
          
# - connect to the Bitcoin blockchain, 
# - and retrieve the nth output of the transaction with the given hash.
# - create a new object with the fields, ('tx_hash’, 'n’, 'amount’, ‘owner’ and ‘time’) the values retrieved from the blockchain. 
# This method does not need to initialize the list 'inputs’. 
# Note that the ‘time’ field should be converted to a datetime object (using the datetime.fromtimestamp method)
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        tx_dict ={}
        tx_hash 
        tx_dict['n'] = tx['vout'][1]
        tx_dict['amount'] = tx['vout'][0]
        tx_dict['owner'] =tx['vout'][2]['addresses']['address']
        tx_dict['time'] = tx['blocktime']
        tx['vout'][2]
        #__init__(   )
    
        return tx_dict


    def get_inputs(self,d=1):
        pass
        #YOUR CODE HERE
        tx = rpc_connection.getrawtransaction(tx_hash,True)
# - connect to the Bitcoin blockchain, 
# - populate the list of inputs, up to a depth   d .
# In other words, if   d=1  it should create TXO objects to populate self.inputs with the appropriate TXO objects. If   d=2  it should also populate the inputs field of each of the TXOs in self.inputs etc.

#Note that every Bitcoin transaction has a list of transaction outputs, indexed by the field 'n’.