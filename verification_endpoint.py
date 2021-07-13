from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    data = request.get_json(silent=True)
    
#     str_con = json.dumps(content)
#     data =json.loads(str_con)
   # sig = data['sig']
    pk = data['payload'][0]['pk']
    platform = data['payload'][0]['platform']

    
    # to save entire 'payload' dictionary
    
#     if content:
#         content_json = json.dumps(content)
#     else:
#         content_json = "no json"   
    
    #Check if signature is valid
    # for eth and algo 
    
    if platform =='Ethereum':
        
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg,sig)
        print( eth_sig_obj.messageHash )
        if eth_account.Account.recover_message(eth_encoded_msg,signature=eth_sig_obj.signature.hex()) == pk:
            result = True
            print( "Eth sig verifies!" )
    elif platform =='Algorand':

        algo_sig_str = algosdk.util.sign_bytes(payload.encode('utf-8'),sig)
        if algosdk.util.verify_bytes(payload.encode('utf-8'),algo_sig_str,pk):
            result = True
            print( "Algo sig verifies!" )
    else:
        result = False

    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
