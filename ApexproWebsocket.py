

'''
~/.local/share/virtualenvs/ApexproBot-M9Nd6v3e/lib/python3.11/site-packages/parsimonious/expressions.pyのfrom inspect import getargspecをgetfullargspecに修正

・apexproの全active tickerのtraede dataをwsでsubscribeする。

'''


import asyncio

from apexpro.constants import APEX_WS_MAIN
from apexpro.websocket_api import WebSocket
from ApexproRestAPI import ApexproRestAPI
from ApexproTradeData import ApexproTradeData

import pandas as pd
import time

class ApexproWebsocket:
    def __init__(self) -> None:
        self.key = ''
        self.ws = WebSocket(endpoint=APEX_WS_MAIN)
        

    def callback(self, message):
        if message['type'] == 'delta':
            ApexproTradeData.add_data(message)
            print(message['data'][-1]['s'] + '-' + message['data'][-1]['S'] + ': ' + str(message['data'][-1]['v'])+ ' @'+ str(message['data'][-1]['p']))
        elif message['type'] == 'snapshot':
            pass
        else:
            print('Unknown data type!')
            print(message)

    async def start(self):
        ApexproTradeData.initialize()
        tickers = await self.get_all_tickers()
        for ticker in tickers['symbols']:
            self.ws.trade_stream(self.callback, ticker)
        while True:
            await asyncio.sleep(0.1)

    async def get_all_tickers(self):
        api = ApexproRestAPI()
        return await api.get_tickers()

if __name__ == '__main__':
    ws = ApexproWebsocket()
    asyncio.run(ws.start())