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

from models import Base, Order, Log
from verification_endpoint import verify

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

def log_message(d)
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
        pk = content['payload']['pk']
        platform = content['payload']['platform']
        payload = json.dumps(content['payload'])

        result = False
    
        # for eth and algo 
        if platform == "Ethereum":        
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        eth_sig_obj = sig        
            if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
                result = True
            #print( "Eth sig verifies!" )
            
        if platform == "Algorand":        
            if algosdk.util.verify_bytes(payload.encode('utf-8'),sig,pk):
                result = True
            #print( "Algo sig verifies!" )

        
        if result = True :
            new_order_obj = Order(sender_pk=content['payload']['sender_pk'],receiver_pk=content['payload']['receiver_pk'],\ buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'],buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'] )
   
            create_session()
            g.session.add(new_order_obj)
            g.session.commit()
        
        # not verify then, insert Log table
        if result =False:
            new_log_obj = Log(message = payload)
            g.session.add(new_log_obj)
            g.session.commit()

#         return jsonify(result)

        #Note that you can access the database session using g.session

@app.route('/order_book')
def order_book():
    #Your code here : return a list of all orders in the database.
    #Note that you can access the database session using g.session
    
    
    orders = session.query(Order).filter(Order.sender_pk!=None and  Order.receiver_pk!=None and Order.buy_currency!=None and Order.sell_currency!=None and Order.buy_amount!=None and Order.sell_amount!=None and Order.signature”!=None).all() 
    
    
    data = [order.__dict__ for order in orders]
    json.dumps(data)    
    
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(port='5002')
