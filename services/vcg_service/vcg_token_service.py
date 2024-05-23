from py_singleton import singleton
from web3_utils.web3_core import Web3Core
from utils.logger.logger import SLACK_LOGGER
import traceback

web3_main_service = Web3Core()
vcg_contract = web3_main_service.vcg_contract_instance
web3 = web3_main_service._web3

slack_logger = SLACK_LOGGER()

@singleton
class VCGGovernanceTokenService(object):
    @staticmethod
    def get_token_metadata():
        try:
            name = web3_main_service.vcg_contract_instance.functions.name().call()
            total_supply = web3_main_service.vcg_contract_instance.functions.totalSupply().call()
            symbol = web3_main_service.vcg_contract_instance.functions.symbol().call()
            return name, total_supply, symbol
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def transfer(address_from, address_to, _token_amount):
        try:
            nonce = web3.eth.getTransactionCount(address_from)
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())

    @staticmethod
    def get_user_vcg_balance(user_address):
        try:
            return web3_main_service.vcg_contract_instance.functions.balanceOf(user_address).call()
        except Exception as e:
            traceback.print_exc()
            slack_logger.log_message_to_slack(traceback.format_exc())
        
    