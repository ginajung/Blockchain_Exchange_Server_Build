from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import math
import sys
import traceback
import time


from algosdk import mnemonic
from algosdk import account
from web3 import Web3

# TODO: make sure you implement connect_to_algo, send_tokens_algo, and send_tokens_eth
from send_tokens import connect_to_algo, connect_to_eth, send_tokens_algo, send_tokens_eth

from models import Base, Order, TX, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


app = Flask(__name__)

""" Pre-defined methods (do not need to change) """


@app.before_request
def create_session():
    g.session = scoped_session(DBSession)


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()


def connect_to_blockchains():
    try:
        # If g.acl has not been defined yet, then trying to query it fails
        acl_flag = False
        g.acl
    except AttributeError as ae:
        acl_flag = True

    try:
        if acl_flag or not g.acl.status():
            # Define Algorand client for the application
            g.acl = connect_to_algo()
    except Exception as e:
        print("Trying to connect to algorand client again")
        print(traceback.format_exc())
        g.acl = connect_to_algo()

    try:
        icl_flag = False
        g.icl
    except AttributeError as ae:
        icl_flag = True

    try:
        if icl_flag or not g.icl.health():
            # Define the index client
            g.icl = connect_to_algo(connection_type='indexer')
    except Exception as e:
        print("Trying to connect to algorand indexer client again")
        print(traceback.format_exc())
        g.icl = connect_to_algo(connection_type='indexer')

    try:
        w3_flag = False
        g.w3
    except AttributeError as ae:
        w3_flag = True

    try:
        if w3_flag or not g.w3.isConnected():
            g.w3 = connect_to_eth()
    except Exception as e:
        print("Trying to connect to web3 again")
        print(traceback.format_exc())
        g.w3 = connect_to_eth()


""" End of pre-defined methods """

""" Helper Methods (skeleton code for you to implement) """


def log_message(message_dict):
    msg = json.dumps(message_dict)

    # TODO: Add message to the Log table

    new_log_obj = Log(message=msg)
            # print( "Log generated" )
    g.session.add(new_log_obj)
    g.session.commit()

    return


def get_algo_keys():

    # TODO: Generate or read (using the mnemonic secret)
    # the algorand public/private keys
    mnemonic_secret = "such chapter crane ugly uncover fun kitten duty culture giant skirt reunion pizza pill web monster upon dolphin aunt close marble dune kangaroo ability merit"
                   
    algo_sk = mnemonic.to_private_key(mnemonic_secret)
    algo_pk = mnemonic.to_public_key(mnemonic_secret)
    
    #algo_sk, algo_pk = account.generateAccount()

    return algo_sk, algo_pk


def get_eth_keys(filename = "eth_mnemonic.txt"):
    w3 = Web3()
    w3.eth.account.enable_unaudited_hdwallet_features()
    acct, mnemonic_secret = w3.eth.account.create_with_mnemonic()
    # # #mnemonic_secret = "such chapter crane ugly uncover fun kitten duty culture giant skirt reunion pizza pill web monster upon dolphin aunt close marble dune kangaroo ability merit"
    # acct = w3.eth.account.from_mnemonic(mnemonic_secret)
    eth_pk = acct._address
    eth_sk = acct._private_key.hex() #private key is of type HexBytes which is not JSON serializable, adding .hex() converts it to a string

    return eth_sk, eth_pk


def fill_order(new_order_obj, orders):
    # TODO:
    # Match orders (same as Exchange Server II)
    # Validate the order has a payment to back it (make sure the counterparty also made a payment)
    # Make sure that you end up executing all resulting transactions!

    for existing_order in orders:

        if existing_order.buy_currency == new_order_obj.sell_currency and \
        existing_order.sell_currency == new_order_obj.buy_currency and \
        existing_order.sell_amount / existing_order.buy_amount >= new_order_obj.buy_amount/new_order_obj.sell_amount:

          # Handle matching order
            # Set the filled field to be the current timestamp on both orders
            new_order_obj.filled = datetime.now()
            existing_order.filled = datetime.now()

            # Set counterparty_id to be the id of the other order
            new_order_obj.counterparty_id = existing_order.id
            existing_order.counterparty_id = new_order_obj.id

            break;

    # 3. If one of the orders is not completely filled (i.e. the counterparty’s sell_amount is less than buy_amount):
        if new_order_obj.sell_amount > existing_order.buy_amount:

    # 4 Create a new order for remaining balance

            child_order_new = {}

            child_order_new['sender_pk'] = new_order_obj.sender_pk
            child_order_new['receiver_pk'] = new_order_obj.receiver_pk
            child_order_new['buy_currency'] = new_order_obj.buy_currency
            child_order_new['sell_currency'] = new_order_obj.sell_currency

            exchange_rate_new = new_order_obj.buy_amount/new_order_obj.sell_amount

            child_sell_amount = new_order_obj.sell_amount-existing_order.buy_amount
            child_buy_amount = exchange_rate_new * child_sell_amount

            child_order_new['sell_amount'] = child_sell_amount
            child_order_new['buy_amount'] = child_buy_amount

            child_order_newobj = Order(sender_pk=child_order_new['sender_pk'], receiver_pk=child_order_new['receiver_pk'],buy_currency=child_order_new['buy_currency'], sell_currency=child_order_new['sell_currency'],buy_amount=child_order_new['buy_amount'], sell_amount=child_order_new['sell_amount'])

            g.session.add(child_order_newobj)
            child_order_newobj.creator_id = new_order_obj.id
            g.session.commit()

        if new_order_obj.buy_amount < existing_order.sell_amount:
                # child order for counterparty
            child_order_ex = {}
            child_order_ex['sender_pk'] = existing_order.sender_pk
            child_order_ex['receiver_pk'] = existing_order.receiver_pk
            child_order_ex['buy_currency'] = existing_order.buy_currency
            child_order_ex['sell_currency'] = existing_order.sell_currency
            child_order_ex['buy_amount'] = existing_order.buy_amount

                # any value such that the implied exchange rate of the new order is at least that of the old order

            exchange_rate_ex = existing_order.buy_amount/existing_order.sell_amount

            child_ex_sell_amount = existing_order.sell_amount-new_order_obj.buy_amount
            child_ex_buy_amount = exchange_rate_ex * child_ex_sell_amount

            child_order_ex['sell_amount'] = child_ex_sell_amount
            child_order_ex['buy_amount'] = child_ex_buy_amount

            child_order_exobj = Order(sender_pk=child_order_ex['sender_pk'], receiver_pk=child_order_ex['receiver_pk'],
                                    buy_currency=child_order_ex['buy_currency'], sell_currency=child_order_ex['sell_currency'],
                                    buy_amount=child_order_ex['buy_amount'], sell_amount=child_order_ex['sell_amount'])

            g.session.add(child_order_exobj)
            child_order_exobj.creator_id = existing_order.id
            g.session.commit()

    print('line 215: filled')

    txes = []
    
    tx_neworder = {
            'platform':new_order_obj.buy_currency,
            'amount': min(new_order_obj.buy_amount, existing_order.sell_amount),
            'order_id': new_order_obj.id,
            'receiver_pk': new_order_obj.receiver_pk,
            'order': new_order_obj,
            'tx_id': new_order_obj.tx_id }    

    txes.append(tx_neworder)

    tx_exorder = {
            'platform':existing_order.buy_currency,
            'amount': min(existing_order.buy_amount, new_order_obj.sell_amount),
            'order_id': existing_order.id,
            'receiver_pk': existing_order.receiver_pk,
            'order' : existing_order,
            'tx_id': existing_order.tx_id } 
    txes.append(tx_exorder)  
    
    execute_txes(txes)


    pass
  
def execute_txes(txes):

    if txes is None:
        return True
    if len(txes) == 0:
        return True
        
    print( f"Trying to execute {len(txes)} transactions" )
    print( f"IDs = {[tx['order_id'] for tx in txes]}" )
    eth_sk, eth_pk = get_eth_keys()
    algo_sk, algo_pk = get_algo_keys()
    
    if not all( tx['platform'] in ["Algorand","Ethereum"] for tx in txes ):
        print( "Error: execute_txes got an invalid platform!" )
        print( tx['platform'] for tx in txes )

    algo_txes = [tx for tx in txes if tx['platform'] == "Algorand" ]
    eth_txes = [tx for tx in txes if tx['platform'] == "Ethereum" ]

    print('line 237: sorted for execution')
    # TODO: 
    #       1. Send tokens on the Algorand and eth testnets, appropriately
    #          We've provided the send_tokens_algo and send_tokens_eth skeleton methods in send_tokens.py
    #       2. Add all transactions to the TX table

    if eth_txes.count != 0:

        eth_txids = send_tokens_eth(g.w3,eth_sk,eth_txes)

        for eth_txid in eth_txids:

            eth_tx = g.w3.eth.getTransaction(eth_txid)
            # how to get 'order_id'???  ,
            new_tx_object = TX(platform = "Ethereum", receiver_pk = eth_tx["to"], order_id= eth_txes['order_id'], tx_id = eth_txid )
            g.session.add(new_tx_object)
            g.session.commit()
            print('line 285: eth_tx executed')

    if algo_txes.count !=0:
        algo_txids = send_tokens_algo(g.acl,algo_sk,algo_txes)

        for algo_txid in algo_txids:
            tx = g.icl.search_transactions(algo_txid)
            for algo_tx in tx['transactions']:

                # how to get 'order_id'???   
                new_tx_object = TX(platform = "Algorand", receiver_pk = algo_tx['payment-transaction']['receiver'],order_id= algo_txes['order_id'], tx_id = algo_txid )
                g.session.add(new_tx_object)
                g.session.commit()    
               
## Instead.. try to generate TX object with tx 

    # if eth_txes.count != 0:
    #     for eth_tx in eth_txes:

    #         eth_txid = send_tokens_eth(g.w3,algo_sk,eth_tx)
        
    #         new_tx_object = TX(platform = "Ethereum", receiver_pk = eth_tx["receiver_pk"], order_id= eth_tx['order_id'], order = eth_tx.order, tx_id = eth_txid )
    #         g.session.add(new_tx_object)
    #         g.session.commit()
    #         print('line 285: eth_tx executed')

    # if algo_txes.count !=0:

    #     for algo_tx in algo_txes:
    #         algo_txid = send_tokens_algo(g.acl,eth_sk,algo_tx)
    #         new_tx_object = TX(platform = "Algorand", receiver_pk = algo_tx['receiver_pk'], order_id= algo_tx['order_id'], order = algo_tx.order, tx_id = algo_txid )
    #         g.session.add(new_tx_object)
    #         g.session.commit()

    #     print('line 292: algo_tx executed')

    pass

""" End of Helper methods"""
  
@app.route('/address', methods=['POST'])
def address():
    if request.method == "POST":
        content = request.get_json(silent=True)
        if 'platform' not in content.keys():
            print( f"Error: no platform provided" )
            return jsonify( "Error: no platform provided" )
        if not content['platform'] in ["Ethereum", "Algorand"]:
            print( f"Error: {content['platform']} is an invalid platform" )
            return jsonify( f"Error: invalid platform provided: {content['platform']}"  )
        
        if content['platform'] == "Ethereum":
            # Your code here
            eth_sk, eth_pk = get_eth_keys()
            return jsonify( eth_pk )
        if content['platform'] == "Algorand":
            # Your code here
            algo_sk, algo_pk = get_algo_keys()
            return jsonify( algo_pk )

@app.route('/trade', methods=['POST'])
def trade():
    print( "In trade", file=sys.stderr )
    connect_to_blockchains()
    eth_sk, eth_pk = get_eth_keys()
    algo_sk, algo_pk = get_algo_keys()
    #get_keys()
    if request.method == "POST":
        content = request.get_json(silent=True)
        columns = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform", "tx_id", "receiver_pk","sender_pk"]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            log_message(content)
            return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            log_message(content)
            return jsonify( False )
        
        # Your code here
        
        # 1. Check the signature
        
        sig = content['sig']
        pk = content['payload']['sender_pk']
        plt = content['payload']['platform']
        payload = json.dumps(content['payload'])
        
        result = False
    
        # for eth and algo 
        if plt == "Ethereum":        
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
            eth_sig_obj = sig        
            if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
                print( "Eth_verified" ) 
                result = True          
            
        if plt == "Algorand":        
            if algosdk.util.verify_bytes(payload.encode('utf-8'),sig,pk):
                print( "Algo_verified" ) 
                result = True
                
        # 2. Add the order to the table

        if (result == True ) :
            # if verified, insert into Order table
            # 1. INSERT : generate new_order_obj from new_order dictionary
            
            new_order_obj = Order( receiver_pk=content['payload']['receiver_pk'],sender_pk=content['payload']['sender_pk'],\
                                  buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'], \
                                  buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'],\
                                  signature = content['sig'],tx_id =content['payload']['tx_id'])
            
           
            g.session.add(new_order_obj)
            g.session.commit()
            
                        
        # 3a. Check if the order is backed by a transaction equal to the sell_amount (this is new)        
            # when an order comes in 
            # - check that user transmitted "sell_amount" to the exchanges' address
            # - if the signature verifies and the order matches, \
            #   the exchange must send tokens to both counterparties on the appropriate changes
        
        # 3b. Fill the order (as in Exchange Server II) if the order is valid
        # # 


            if new_order_obj.sell_currency == "Ethereum":  

                eth_tx = g.w3.eth.get_transaction(new_order_obj.tx_id)
                
                if eth_tx['value'] == new_order_obj.sell_amount and eth_tx['from'] == new_order_obj.sender_pk and eth_tx['to'] == eth_pk :

                    print('line 401: ethOrder is valid') 
                    orders = g.session.query(Order).filter(Order.filled == None).all()            
                    fill_order(new_order_obj, orders)            
                    print('line 400: filled eth_orders') 
                    
             
            if new_order_obj.sell_currency == "Algorand": 
                
               
                tx = g.acl.search_transactions(new_order_obj.tx_id)                
                
                for algo_tx in tx['transactions']:
                    
                    if algo_tx['payment-transaction']['amount'] == new_order_obj.sell_amount and algo_tx['payment-transaction']['receiver'] == algo_pk and algo_tx['transactions']['sender'] == new_order_obj.sender_pk :
                
                        print('line 450: algoOrder is valid') 
                        orders = g.session.query(Order).filter(Order.filled == None).all()
                        fill_order(new_order_obj, orders)            
                        print('line 453: filled algo orders') 


            # orders = g.session.query(Order).filter(Order.filled == None).all()
            # fill_order(new_order_obj, orders)            
            # print('line 400: filled orders') 
            
        
    
 # not verify then, insert into Log table
        if result ==False:
            new_log_obj = Log(message = payload)
            #print( "Log generated" )   
            g.session.add(new_log_obj)
            g.session.commit()
            
        
        return jsonify(True)

@app.route('/order_book')
def order_book():
    #fields = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "signature", "tx_id", "receiver_pk", "sender_pk"]

    orders = g.session.query(Order).all()
    data_dic ={'data': []}
    
#     # save orders as a list of dicts / convert to JSON
    for order in orders:
        
        new_order_dict = {}
        new_order_dict['sender_pk'] = order.sender_pk
        new_order_dict['receiver_pk'] = order.receiver_pk
        new_order_dict['buy_currency'] = order.buy_currency
        new_order_dict['sell_currency'] = order.sell_currency
        new_order_dict['buy_amount'] = order.buy_amount
        new_order_dict['sell_amount'] = order.sell_amount
        new_order_dict['signature'] = order.signature
        new_order_dict['tx_id'] = order.tx_id
        data_dic['data'].append(new_order_dict)
  
    return jsonify(data_dic)
    
if __name__ == '__main__':
    app.run(port='5002')
