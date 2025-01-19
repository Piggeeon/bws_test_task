import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])

BET_MAKER_CHANGE_STATE_URL = "http://bet_maker:8000/bet"
