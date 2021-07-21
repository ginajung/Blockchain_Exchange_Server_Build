from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine, select, MetaData, Table
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from sqlalchemy.ext.declarative import declarative_base

from models import Base, Order, Log

engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

#These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(DBSession) #g is an "application global" https://flask.palletsprojects.com/en/1.1.x/api/#application-globals

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()

"""
-------- Helper methods (feel free to add your own!) -------
"""

def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    
    pass

"""
---------------- Endpoints ----------------
"""
    
@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
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
            
        #Your code here
        
        sig = content['sig']
        pk = content['payload']['sender_pk']
        platform = content['payload']['platform']
        payload = json.dumps(content['payload'])

        result = False
    
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
        # if verified, insert into Order table
        if result == True :
            new_order_obj = Order( receiver_pk=content['payload']['receiver_pk'],sender_pk=content['payload']['sender_pk'], buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'], buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'], signature = content['sig'])
  
            #print( "Order generated" )   
            g.session.add(new_order_obj)
            g.session.commit()
        
        # not verify then, insert into Log table
        if result ==False:
            new_log_obj = Log(message = payload)
            #print( "Log generated" )   
            g.session.add(new_log_obj)
            g.session.commit() 
 #   return
    
    
@app.route('/order_book')
def order_book():
    #Your code here : return a list of all orders in the database.
    #Note that you can access the database session using g.session   
    orders = g.session.query(Order).filter(Order.sender_pk !=None, Order.receiver_pk !=None, Order.buy_currency !=None, Order.sell_currency !=None, Order.buy_amount!=None, Order.sell_amount!=None, Order.signature!=None).all() 
#     orders = g.session.query(Order).all()
    
    data_dic ={'data': []}
    
#     # save orders as a list of dicts / convert to JSON
    for order in orders:
        #data_dic['data'].append(order.__dict__)

        new_order_dict = {}
        new_order_dict['sender_pk'] = order.sender_pk
        new_order_dict['receiver_pk'] = order.receiver_pk
        new_order_dict['buy_currency'] = order.buy_currency
        new_order_dict['sell_currency'] = order.sell_currency
        new_order_dict['buy_amount'] = order.buy_amount
        new_order_dict['sell_amount'] = order.sell_amount
        new_order_dict['signature'] = order.signature
        data_dic['data'].append(new_order_dict)

    #json.dumps(data_dic)
  
    return jsonify(data_dic)

if __name__ == '__main__':
    app.run(port='5002')
