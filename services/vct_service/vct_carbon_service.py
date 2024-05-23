from py_singleton import singleton
from web3_utils.web3_core import Web3Core
from dotenv import load_dotenv
from decouple import config
import traceback
from utils.logger.logger import SLACK_LOGGER

web3_main_service = Web3Core()
vct_contract = web3_main_service.vct_contract_instance
web3 = web3_main_service._web3

slack_logger = SLACK_LOGGER()

load_dotenv()

ACCOUNT_PRIVATE_KEY = config('ACCOUNT_PRIVATE_KEY')
ACCOUNT_ADDRESS = config('ACCOUNT_ADDRESS')

account_from = {
    'private_key': ACCOUNT_PRIVATE_KEY,
    'address': ACCOUNT_ADDRESS
}

@singleton
class VCTCarbonService(object):
    @staticmethod
    def tokenize_carbon_asset(pool_address, amount, isPreFinanced):
        try:
            # #build transaction
            tokenize_tx = web3_main_service.vct_contract_instance.functions.tokenize(web3.toChecksumAddress(pool_address),amount,isPreFinanced).buildTransaction(
            {
                'from': account_from['address'],
                'nonce': web3.toHex(web3.eth.getTransactionCount(web3.toChecksumAddress(account_from['address'])))
            })
              
            #sign transaction
            tx_create = web3.eth.account.sign_transaction(tokenize_tx, account_from['private_key'])

            #Send tx and wait for receipt
            tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
            return tx_receipt
        except:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def get_pool_balance(pool_address):
        try:
            balance = web3_main_service.vct_contract_instance.functions.balanceOf(web3.toChecksumAddress(pool_address)).call()
            return balance
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())
        
    @staticmethod
    def get_pool_metadata(pool_address):
        try:
            pass
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def get_pool_nft_tokens(pool_address):
        try:
            pass
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def get_token_name():
        try:
            return web3_main_service.vct_contract_instance.functions.name().call()
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())
        
    @staticmethod
    def get_token_metadata():
        try:
            name = web3_main_service.vct_contract_instance.functions.name().call()
            symbol = web3_main_service.vct_contract_instance.functions.symbol().call()
            total_supply = web3_main_service.vct_contract_instance.functions.totalSupply().call()
            return name, symbol, total_supply
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def retire_token(token_id):
        try:
            # #build transaction
            retire__tx = web3_main_service.vct_contract_instance.functions.retire(token_id).buildTransaction(
            {
                'from': account_from['address'],
                'nonce': web3.toHex(web3.eth.getTransactionCount(web3.toChecksumAddress(account_from['address'])))
            })
              
            #sign transaction
            tx_create = web3.eth.account.sign_transaction(retire__tx, account_from['private_key'])

            #Send tx and wait for receipt
            tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
            return tx_receipt
        except:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def list_pools():
        try:
            pass
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())