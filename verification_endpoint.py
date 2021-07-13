from flask import Flask, request, jsonify
from flask_restful import Api
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
    content = request.get_json(silent=True)

    sig = content['sig']
    pk = content['payload'][0]['pk']
    platform = content['payload'][0]['platform']
    payload = json.dumps(content['payload'])

    
    # for eth and algo 
    if platform == "Ethereum":        
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        eth_sig_obj = sig        
        if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
            result = True
            print( "Eth sig verifies!" )
            
    if platform == "Algorand":        
        if algosdk.util.verify_bytes(payload.encode('utf-8'),sig,pk):
            result = True
            print( "Algo sig verifies!" )
#     else:
#         result = False

    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
