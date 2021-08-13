from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from algosdk import mnemonic
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import math
import sys
import traceback


# TODO: make sure you implement connect_to_algo, send_tokens_algo, and send_tokens_eth
from send_tokens import connect_to_algo, connect_to_eth, send_tokens_algo, send_tokens_eth

from models import Base, Order, TX
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
    
    return

def get_algo_keys():
    
    # TODO: Generate or read (using the mnemonic secret) 
    # the algorand public/private keys
    
    mnemonic_secret = "soft quiz moral bread repeat embark shed steak chalk joy fetch pilot shift floor identify poverty index yard cannon divorce fatal angry mistake abandon voyage"
    algo_sk = mnemonic.to_private_key(mnemonic_secret)
    algo_pk = mnemonic.to_public_key(mnemonic_secret)
  
    return algo_sk, algo_pk


def get_eth_keys(filename = "eth_mnemonic.txt"):
    #w3 = Web3()
    w3 = connect_to_eth()
    w3.eth.account.enable_unaudited_hdwallet_features()
   # acct,mnemonic_secret = w3.eth.account.create_with_mnemonic()
    mnemonic_secret = "soft quiz moral bread repeat embark shed steak chalk joy fetch pilot shift floor identify poverty index yard cannon divorce fatal angry mistake abandon voyage"
    
    acct = w3.eth.account.from_mnemonic(mnemonic_secret)
    eth_pk = acct._address
    eth_sk = acct._private_key.hex()
    # TODO: Generate or read (using the mnemonic secret) 
    # the ethereum public/private keys
    
    return eth_sk, eth_pk


  
def fill_order(order, txes=[]):
    # TODO: Process order !!  txes=[]??
    # Match orders (same as Exchange Server II)
    # Validate the order has a payment to back it (make sure the counterparty also made a payment)
    # Make sure that you end up executing all resulting transactions!
          
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

    # TODO: 
    #       1. Send tokens on the Algorand and eth testnets, appropriately
    #          We've provided the send_tokens_algo and send_tokens_eth skeleton methods in send_tokens.py
    #       2. Add all transactions to the TX table

# class TX(Base):
#     __tablename__ = 'txes'
#     id = Column(Integer,primary_key=True)
#     platform = Column(Enum(*PLATFORMS))
#     receiver_pk = Column(String(256)) #The transaction receiver (the transaction sender should be the exchange itself)
#     order_id = Column(Integer,ForeignKey('orders.id')) #The id of the order that created the transaction
#     order = relationship("Order", foreign_keys='TX.order_id' )
#     tx_id = Column(String(256)) #The transaction ID of the executed transaction (should correspond to a transaction on the platform given by 'platform')

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
            #Your code here
            eth_sk, eth_pk = get_eth_keys()
            return jsonify( eth_pk )
        if content['platform'] == "Algorand":
            #Your code here
            algo_sk, algo_pk = get_algo_keys()
            return jsonify( algo_pk )

@app.route('/trade', methods=['POST'])
def trade():
    print( "In trade", file=sys.stderr )
    connect_to_blockchains()
    get_keys()
    if request.method == "POST":
        content = request.get_json(silent=True)
        columns = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform", "tx_id", "receiver_pk",  "sender_pk"]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            return jsonify( False )
        
        # Your code here
        
        # 1. Check the signature
        
        # 2. Add the order to the table
        
        # 3a. Check if the order is backed by a transaction equal to the sell_amount (this is new)

        # 3b. Fill the order (as in Exchange Server II) if the order is valid
        
        # 4. Execute the transactions
        
        # If all goes well, return jsonify(True). else return jsonify(False)
       

        sig = content['sig']
        pk = content['payload']['sender_pk']
        platform = content['payload']['platform']
        payload = json.dumps(content['payload'])

        result = False
    
    # 1. Check the signature
        # for eth and algo 
        if platform == "Ethereum":        
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
            eth_sig_obj = sig        
            if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
                #print( "Eth_verified" ) 
                result = True
           
            
        if platform == "Algorand":        
            if algosdk.util.verify_bytes(payload.encode('utf-8'),sig,pk):
                #print( "Algo_verified" ) 
                result = True
            
        #print(result)
        
     # 2. Add the order to the table
    
         # if verified, insert into Order table
        if result == True :
            new_order_obj = Order( receiver_pk=content['payload']['receiver_pk'],sender_pk=content['payload']['sender_pk'], buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'], buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'], signature = content['sig'],tx_id =content['payload']['tx_id'])
  
            #print( "Order generated" )   
            g.session.add(new_order_obj)
            g.session.commit()
            
                    
# FROM PROCESS_ORDER() code
    
        # 2. CHECK MATCH : check if matching to any existing order, stop
            orders = g.session.query(Order).filter(Order.filled == None).all()   
   
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
            if new_order_obj.sell_amount > existing_order.buy_amount :
        
                
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
    
                child_order_newobj = Order( sender_pk=child_order_new['sender_pk'],receiver_pk=child_order_new['receiver_pk'], \
                                   buy_currency=child_order_new['buy_currency'],sell_currency=child_order_new['sell_currency'],\
                                        buy_amount=child_order_new['buy_amount'], sell_amount=child_order_new['sell_amount'] )

                g.session.add(child_order_newobj) 
                child_order_newobj.creator_id = new_order_obj.id
                g.session.commit()
                
            if new_order_obj.buy_amount < existing_order.sell_amount :
                # child order for counterparty
                child_order_ex = {}
                child_order_ex['sender_pk'] = existing_order.sender_pk
                child_order_ex['receiver_pk'] = existing_order.receiver_pk
                child_order_ex['buy_currency'] = existing_order.buy_currency
                child_order_ex['sell_currency'] = existing_order.sell_currency
                child_order_ex['buy_amount'] = existing_order.buy_amount
    
                #any value such that the implied exchange rate of the new order is at least that of the old order
                
                exchange_rate_ex = existing_order.buy_amount/existing_order.sell_amount
                
                child_ex_sell_amount = existing_order.sell_amount-new_order_obj.buy_amount
                child_ex_buy_amount = exchange_rate_ex * child_ex_sell_amount
                
                child_order_ex['sell_amount'] = child_ex_sell_amount
                child_order_ex['buy_amount'] = child_ex_buy_amount
                
                child_order_exobj = Order( sender_pk=child_order_ex['sender_pk'],receiver_pk=child_order_ex['receiver_pk'], \
                                        buy_currency=child_order_ex['buy_currency'],sell_currency=child_order_ex['sell_currency'],\
                                        buy_amount=child_order_ex['buy_amount'], sell_amount=child_order_ex['sell_amount'] )

                g.session.add(child_order_exobj) 
                child_order_exobj.creator_id = existing_order.id
                g.session.commit()
                
        
        # not verify then, insert into Log table
        if result ==False:
            new_log_obj = Log(message = payload)
            #print( "Log generated" )   
            g.session.add(new_log_obj)
            g.session.commit()
            
            
    return jsonify(True)


@app.route('/order_book')
def order_book():
    fields = [ "buy_currency", "sell_currency", "buy_amount", "sell_amount", "signature", "tx_id", "receiver_pk" ]
    
    #Your code here : return a list of all orders in the database.

    orders = g.session.query(Order).all()
    
    data_dic ={'data': []}
    
    # save orders as a list of dicts / convert to JSON
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