from web3 import Web3
from hexbytes import HexBytes

IP_ADDR='18.188.235.196'
PORT='8545'

w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))


# >>> web3.eth.get_transaction('0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060')
# AttributeDict({
#     'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
#     'blockNumber': 46147,
#     'from': '0xA1E4380A3B1f749673E270229993eE55F35663b4',
#     'gas': 21000,
#     'gasPrice': 50000000000000,
#     'hash': '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060',
#     'input': '0x',
#     'nonce': 0,
#     'to': '0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
#     'transactionIndex': 0,
#     'value': 31337,
# })
# if w3.isConnected():
#     This line will mess with our autograders, but might be useful when debugging
#    print( "Connected to Ethereum node" )
# else:
#     print( "Failed to connect to Ethereum node!" )

def get_transaction(tx):
    tx = {}   #YOUR CODE HERE
    tx= w3.eth.get_transaction(tx)
    return tx

# Return the gas price used by a particular transaction,
#   tx is the transaction
def get_gas_price(tx):
    gas_price = 1 #YOUR CODE HERE
    gas_price = get_transaction(tx)['gasPrice']
    
    return gas_price

def get_gas(tx):
    gas = 1 #YOUR CODE HERE
    gas = w3.eth.get_transaction_receipt(tx)['gasUsed']
    return gas

def get_transaction_cost(tx):
    tx_cost = 1 #YOUR CODE HERE
    tx_cost = get_gas_price(tx) * get_gas(tx)
    return tx_cost


# Now complete the function getBlockCost that, given a block number,
# returns the total cost of all transactions in that block.
# This is the amount that the miner of the block earns from transaction fees.
# (The miner will additionally earn a reward of a certain number of ether
# from having mined a new block.)
# Since this involves querying many transactions, it may take a minute to run.

# >>> web3.eth.get_block(2000000)
# AttributeDict({
#     'difficulty': 49824742724615,
#     'extraData': '0xe4b883e5bda9e7a59ee4bb99e9b1bc',
#     'gasLimit': 4712388,
#     'gasUsed': 21000,
#     'hash': '0xc0f4906fea23cf6f3cce98cb44e8e1449e455b28d684dfa9ff65426495584de6',
#     'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
#     'miner': '0x61c808d82a3ac53231750dadc13c777b59310bd9',
#     'nonce': '0x3b05c6d5524209f1',
#     'number': 2000000,
#     'parentHash': '0x57ebf07eb9ed1137d41447020a25e51d30a0c272b5896571499c82c33ecb7288',
#     'receiptRoot': '0x84aea4a7aad5c5899bd5cfc7f309cc379009d30179316a2a7baa4a2ea4a438ac',
#     'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
#     'size': 650,
#     'stateRoot': '0x96dbad955b166f5119793815c36f11ffa909859bbfeb64b735cca37cbf10bef1',
#     'timestamp': 1470173578,
#     'totalDifficulty': 44010101827705409388,
#     'transactions': ['0xc55e2b90168af6972193c1f86fa4d7d7b31a29c156665d15b9cd48618b5177ef'],
#     'transactionsRoot': '0xb31f174d27b99cdae8e746bd138a01ce60d8dd7b224f7c60845914def05ecc58',
#     'uncles': [],
# })


def get_block_cost(block_num):
    block_cost = 0  #YOUR CODE HERE
    block_count = w3.eth.get_block_transaction_count(block_num)
    
    if ( w3.eth.get_block(block_num)==True):    
        for i in range(0,block_count):
            tranx = w3.eth.get_transaction_by_block(block_num, i)
            block_cost = block_cost + get_transaction_cost(tranx)

    return block_cost

# Return the hash of the most expensive transaction
def get_most_expensive_transaction(block_num):
    max_tx = HexBytes('0xf7f4905225c0fde293e2fd3476e97a9c878649dd96eb02c86b86be5b92d826b6')  #YOUR CODE HERE
    return max_tx
