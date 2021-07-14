from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):

#INSERT : generate order_obj from order_dict
    order_obj = Order( sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'],\
                      sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )

    #Alternatively, this code inserts the same record and is arguably more readable
    #     fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount']
    #     order_obj = Order(**{f:order[f] for f in fields})

    session.add(order_obj)
    session.commit()
    
# CHECK MATCH : check if matching to any existing orders
    
    for existing_order in session:
        
        if existing_order.filled == None and existing_order.buy_currency == order.sell_currency and \
        existing_order.sell_currency == order.buy_currency and \
        existing_order.sell_amount / existing_order.buy_amount >= order.buy_amount/order.sell_amount:
            
            # Handle matching order
            # set filled with current timestamp
            order_obj.filled = datetime.now()
            existing_order.filled = datetime.now()  
            # set counterparty_id
            order_obj.counterparty_id = existing_order.id   
            
            # 3. If one of the orders is not completely filled (i.e. the counterparty’s sell_amount is less than buy_amount):
            if existing_order.sell_amount<= existing_order.buy_amount:
                # You can then try to fill the new order

                # 4 Create a new order for remaining balance ==> make_order? 
                #       - The new order should have the created_by field set to the id of its parent order
                #       - The new order should have the same pk and platform as its parent order
                #       - The sell_amount of the new order can be any value such that 
                #.        the implied exchange rate of the new order is at least that of the old order
                child_order = {}
                child_order['sender_pk'] = order['sender_pk']
                child_order['receiver_pk'] = order['receiver_pk']
                child_order['buy_currency'] = order['buy_currency']
                child_order['sell_currency'] = order['sell_currency']
                child_order['buy_amount'] = order['buy_amount']
    
                #any value such that the implied exchange rate of the new order is at least that of the old order
                exchange_rate = order_obj.buy_amount/order_obj.sell_amount
                child_order['sell_amount'] = random.randint(exchange_rate,10)
    
    
                child_order_obj = Order( sender_pk=child_order['sender_pk'],receiver_pk=child_order['receiver_pk'], \
                                        buy_currency=child_order['buy_currency'],sell_currency=child_order['sell_currency'],\
                                        buy_amount=child_order['buy_amount'], sell_amount=child_order['sell_amount'] )

                session.add(child_order_obj)
                session.commit()
                child_order_obj.creator_id = order_obj.id
                pass
    


# Fill the child-order
# 1. Each order matches at most one other (to match one order against multiple others create derivative orders, 
#    and set the “created_by” field as described above)
# 2. Any derived orders must have an implied exchange rate that is at least the original exchange rate, 
#.   i.e., buy_amount/sell_amount on the new order must be at least the buy_amount/sell_amount on the order that created it



    