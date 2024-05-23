from py_singleton import singleton

@singleton
class WEB3_CONSTS(object):
    aclhemy_url = 'https://polygon-mumbai.g.alchemy.com/v2/XXGBKxwudOEfk0lt_F0hICAzFO5b_zt4'
    dao_contract_address = '0x2Ee15232589ca27bf14049428A8f2C55Ba046082'
    vcg_reward_contract_address ='0xB47a20EBe13Af2005B2C519Cfeb5A61617caEBbC'
    vct_contract_address = '0xb006997dcAA8Ae4Be1910DF3633D67658f54568d'

class SLACK_CONSTS(object):
    slack_webhook_url = 'https://hooks.slack.com/services/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'