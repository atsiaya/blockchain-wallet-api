from py_singleton import singleton
from web3 import Web3
from web3_utils.abi.dao import verst_carbon_dao_abi
from web3_utils.abi.vcg import vcg_reward_token_abi
from web3_utils.abi.vct import vct_contract_abi
from utils.consts import WEB3_CONSTS

web3 = Web3(Web3.HTTPProvider(WEB3_CONSTS.aclhemy_url))

@singleton
class Web3Core(object):
    dao_contract_instance = web3.eth.contract(address=WEB3_CONSTS.dao_contract_address, abi=verst_carbon_dao_abi)
    vcg_contract_instance = web3.eth.contract(address=WEB3_CONSTS.vcg_reward_contract_address, abi=vcg_reward_token_abi)
    vct_contract_instance = web3.eth.contract(address=WEB3_CONSTS.vct_contract_address, abi=vct_contract_abi)
    _web3 = web3

