from flask import Flask, request
from web3_utils.web3_core import Web3Core
from services.vcg_service.vcg_token_service import VCGGovernanceTokenService
from services.vct_service.vct_carbon_service import VCTCarbonService
from utils.logger.logger import SLACK_LOGGER
import traceback
import json
from decimal import *
from mnemonic import Mnemonic
from eth_account import Account
import secrets

app = Flask(__name__)

web3_main_service = Web3Core()
web3 = web3_main_service._web3

_vcg_token_service = VCGGovernanceTokenService()
_vct_carbon_token_service = VCTCarbonService()
slack_logger = SLACK_LOGGER()

def generate_new_eth_address():
    priv = secrets.token_hex(32)
    _private_key = "0x" + priv
    acct = Account.from_key(_private_key)
    return acct.address, _private_key

def get_pool_vct_balance(pool):
    bal = _vct_carbon_token_service.get_pool_balance(pool)
    return bal

@app.route('/')
def Home():
    return 'Ok'

@app.route('/api/token/tokenize', methods=['POST','GET'])
def tokenize():
    amount = request.args['amount']
    isPrefinanced = True if request.args['prefinanced'] == "true" else False
    
    try:
        address, private_key = generate_new_eth_address()

        formated_address = web3.toChecksumAddress(address)

        tx = _vct_carbon_token_service.tokenize_carbon_asset(formated_address, int(amount), isPrefinanced)

        pool_vcg_balance = _vcg_token_service.get_user_vcg_balance(formated_address)
        pool_vct_balance = get_pool_vct_balance(formated_address)

        print(tx)
        if tx != None:
            return {
                'pool_address': address,
                'private_key': private_key,
                'vct_balance': pool_vct_balance,
                'vcg_balance': int(pool_vcg_balance) / (10 ** 18),
                #'logs': tx,
                'message': 'Success'
            }
        else:
            return {
                'pool_address': address,
                'private_key': private_key,
                'vct_balance': pool_vct_balance,
                'vcg_balance': int(pool_vcg_balance) / ( 10 ** 18),
                'logs': None,
                'message': 'Error Sending Transaction'
            }

    except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

@app.route('/api/token/<int:id>/retire', methods=['POST','GET'])
def retire(id):
    try:
        tx_hash = _vct_carbon_token_service.retire_token(int(id))
        if tx_hash != None:
            return {
                'message': 'Success',
            }
        else:
            return {
                'message': 'Error.',
            }
    except Exception as e:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())

@app.route('/api/wallet/eth/generate', methods=['GET'])
def generate_wallet():
    try:
        mnemo = Mnemonic("english")
        words = mnemo.generate(strength=256)
        seed = mnemo.to_seed(words, passphrase="")
        #_account = web3.eth.account.create(web3.utils.randomHex(32))
        account = web3.eth.account.privateKeyToAccount(seed[:32])
        private_key = account.privateKey
        public_key = account.address

        address, private_key = generate_new_eth_address()

        return {
           'address': address,
            'private_key': private_key,
            #'mnemonic':''# mnemonic
        }
    except:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())

@app.route('/api/dao/name', methods=['GET'])
def get_dao_name():
    try:
        name = web3_main_service.vcg_contract_instance.functions.name().call()
        app.logger.info('Success')
        return {'name':name}
    except:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())

#*************** VCG Goervance Token **************************#
@app.route('/api/vcg/metadata', methods=['GET'])
def fetch_vcg_metadata():
    try:
        name, total_supply, symbol = _vcg_token_service.get_token_metadata()
        return {
            'name' :name,
            'symbol': symbol,
            'total_supply': int(total_supply) / (10 ** 18)
        }
    except:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())
    
@app.route('/api/vct/metadata')
def fetch_vct_metadata():
    try:
        name, symbol, total_supply = _vct_carbon_token_service.get_token_metadata()
        return {
            'name' :name,
            'symbol': symbol,
            'total_supply': total_supply
        }
    except:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())
        return {
                'message': 'Error',
                'data': {}
            }
        
@app.route('/api/vcg/user/balance', methods=['POST', 'GET'])
def fetch_user_balance():
    try:
        address = web3.toChecksumAddress(request.args['user_address'])
        available_balance = _vcg_token_service.get_user_vcg_balance(address)
        return {
                'address': address,
                'balance': int(available_balance) / ( 10 ** 18) 
            }
        
    except Exception as e:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())

@app.route('/api/vct/user/balance', methods=['GET', 'POST'])
def fetch_user_vct_balance():
    try:
        address = web3.toChecksumAddress(request.args['pool_address'])
        balance = get_pool_vct_balance(address)
        if balance != None:
            return {
                'message': 'Success',
                'error': '',
                'address': address,
                'vct_balance': balance
            }
        else:
            return {
                'message': 'Error',
                'error': 'Could not fetch balance',
                'address': address,
                'vct_balance': ''
        }

    except Exception as e:
        traceback.print_exc()
        slack_logger.log_message_to_slack(traceback.format_exc())

   