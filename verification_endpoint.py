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
    
    eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
  
    if content['payload']['platform'] == 'Ethereum':
        
        
        eth_account.Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = eth_account.Account.create_with_mnemonic()

        eth_pk = acct.address
        eth_sk = acct.key

        a_payload = "Sign this!"

        a_eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        a_eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg,eth_sk)

#         if eth_account.Account.recover_message(a_eth_encoded_msg,signature=a_eth_sig_obj.signature.hex()) == eth_pk:
#             print( "Eth sig verifies!" )
        
        # Check Ethereum
        # eth_account.Account.recover_message(eth_encoded_msg, sig.hex()) == pk:
        
        if eth_account.Account.recover_message(eth_encoded_msg, signature=sig.signature.hex()) == pk:
            result = True
        else:
            result = False
    else:
        # Check Algorand
        result = True
            
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
