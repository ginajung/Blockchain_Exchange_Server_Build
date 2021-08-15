#!/usr/bin/python3
import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account, encoding

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)  # create the client account
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

# Generate an account
#sk, pk = account.generate_account()

mnemonic_phrase = "sight garment riot tattoo tortoise identify left talk sea ill walnut leg robot myth toe perfect rifle dizzy spend april build legend brother above hospital";
account_private_key = mnemonic.to_private_key(mnemonic_phrase)
account_public_key = mnemonic.to_public_key(mnemonic_phrase)

print(account_public_key)

def send_tokens( receiver_pk, tx_amount ):
    # getting transaction parameters
    
    params = acl.suggested_params()
    gen=params.gen
    gh=params.gh
    first_valid_round = params.first
    fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    
    if tx_amount < min_balance:
        # create transaction
        tx = transaction.PaymentTxn(account_public_key, fee, first_valid_round, last_valid_round, gh, receiver_pk, tx_amount)
        signed_tx = tx.sign(account_private_key)
    
    # submit the transaction to the Algorand Testnet

    try:
        tx_confirm = acl.send_transaction(signed_tx)
#        print('Transaction sent with ID', txid = signed_tx.transaction.get_txid())
        wait_for_confirmation(acl, txid = signed_tx.transaction.get_txid())
    except Exception as e:
        print(e)
    txid = signed_tx.transaction.get_txid()
    return account_public_key, txid


# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo
