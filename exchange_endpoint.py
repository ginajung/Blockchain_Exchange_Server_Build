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
import sys

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()


""" Suggested helper methods """

def check_sig(payload,sig):
    
    pass

def fill_order(order,txes=[]):
    
    pass
  
def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    # Hint: use json.dumps or str() to get it in a nice string form
    pass

""" End of helper methods """



@app.route('/trade', methods=['POST'])
def trade():
    print("In trade endpoint")
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]

        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
        
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
            
        #Your code here
        #Note that you can access the database session using g.session
        
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
            
            # 1. INSERT : generate new_order_obj from new_order dictionary
            
            new_order_obj = Order( receiver_pk=content['payload']['receiver_pk'],sender_pk=content['payload']['sender_pk'], buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'], buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'], signature = content['sig'])
  
           
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



        # TODO: Check the signature
    
    
        # TODO: Add the order to the database
        
        # TODO: Fill the order
        
        # TODO: Be sure to return jsonify(True) or jsonify(False) depending on if the method was successful
        

@app.route('/order_book')
def order_book():
    #Your code here
    #Note that you can access the database session using g.session
    orders = g.session.query(Order).filter(Order.sender_pk !=None, Order.receiver_pk !=None, Order.buy_currency !=None, Order.sell_currency !=None, Order.buy_amount!=None, Order.sell_amount!=None, Order.signature!=None).all() 
#     orders = g.session.query(Order).all()
    
    data_dic =[]
    #data_dic ={'data': []}
    
#     # save orders as a list of dicts / convert to JSON
    for order in orders:
        data_dic['data'].append(order.__dict__)

        new_order_dict = {}
        new_order_dict['sender_pk'] = order.sender_pk
        new_order_dict['receiver_pk'] = order.receiver_pk
        new_order_dict['buy_currency'] = order.buy_currency
        new_order_dict['sell_currency'] = order.sell_currency
        new_order_dict['buy_amount'] = order.buy_amount
        new_order_dict['sell_amount'] = order.sell_amount
        new_order_dict['signature'] = order.signature
        data_dic['data'].append(new_order_dict)
        #data_dic.add(new_order_dict)

  
    return jsonify(data_dic)
    


if __name__ == '__main__':
    app.run(port='5002')