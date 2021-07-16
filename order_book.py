from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(new_order):

#INSERT : generate new_order_obj from new_order dictionary
    new_order_obj = Order(sender_pk=new_order['sender_pk'],receiver_pk=new_order['receiver_pk'], buy_currency=new_order['buy_currency'],\
                      sell_currency=new_order['sell_currency'],buy_amount=new_order['buy_amount'], sell_amount=new_order['sell_amount'] )
   
    session.add(new_order_obj)
    session.commit()
    
# CHECK MATCH : check if matching to any existing order, stop
    orders = session.query(Order).filter(Order.filled == None).all()   
   
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
        #  created_by field set to the id of its parent order
        #  the same pk and platform as its parent order
        #  The sell_amount of the new order can be any value such that the implied exchange rate of the new order is at least that of the old order
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

        session.add(child_order_newobj) 
        child_order_newobj.creator_id = new_order_obj.id
        session.commit()
                
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

        session.add(child_order_exobj) 
        child_order_exobj.creator_id = existing_order.id
        session.commit()
                
               
        pass
    
