#!/usr/bin/python3

from algosdk import mnemonic
from algosdk import account
from web3 import Web3


from algosdk.v2client import algod
from algosdk.v2client import indexer
from algosdk import mnemonic
from algosdk.future import transaction
from algosdk import account


def get_algo_keys():
    
    # TODO: Generate or read (using the mnemonic secret) 
    # the algorand public/private keys
    mnemonic_secret = "soft quiz moral bread repeat embark shed steak chalk joy fetch pilot shift floor identify poverty index yard cannon divorce fatal angry mistake abandon voyage"
    algo_sk = mnemonic.to_private_key(mnemonic_secret)
    algo_pk = mnemonic.to_public_key(mnemonic_secret)
    
    return algo_sk, algo_pk

