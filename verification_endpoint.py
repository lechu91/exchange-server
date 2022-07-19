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
    message = content['payload']['message']
    pk = content['payload']['pk']
    payload = json.dumps(content['payload'])
 
    if content['payload']['platform'] == 'Ethereum':
        
        # Check Ethereum
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        
        if eth_account.Account.recover_message(eth_encoded_msg, signature=sig) == pk:
            result = True
        else:
            result = False
    else:
        # Check Algorand

        payload = "Sign this!"

        algo_sk, algo_pk = algosdk.account.generate_account()
        algo_sig_str = algosdk.util.sign_bytes(payload.encode('utf-8'),algo_sk)

        if algosdk.util.verify_bytes(payload.encode('utf-8'),algo_sig_str,algo_pk):
            result = True
            print( "Algo sig verifies!" )
        )
        
        else:
            result = False
            
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
