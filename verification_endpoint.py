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
  
    if content['payload']['platform'] == 'Ethereum':
        # Check Ethereum
#         eth_account.Account.enable_unaudited_hdwallet_features()
#         acct, mnemonic = eth_account.Account.create_with_mnemonic()
#         eth_pk = acct.address
#         eth_sk = acct.key
        payload = json.dumps("helloworld") #json.dumps(content['payload'])
#         eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
#         eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg,eth_sk)
#         eth_sig_obj = sig
#         print( eth_sig_obj.messageHash )
#         if eth_account.Account.recover_message(eth_encoded_msg,signature=eth_sig_obj.signature.hex()) == eth_pk:
#             result = True
        if eth_account.Account.recover_message(payload, sig.signature.hex()) == pk:
            result = True
        else:
            result = False
    else:
        # Check Algorand
        result = True
            
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
