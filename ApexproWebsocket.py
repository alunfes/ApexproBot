

'''
~/.local/share/virtualenvs/ApexproBot-M9Nd6v3e/lib/python3.11/site-packages/parsimonious/expressions.pyのfrom inspect import getargspecをgetfullargspecに修正

・apexproの全active tickerのtraede dataをwsでsubscribeする。
https://public.bybit.com/trading/
'''


import asyncio

from apexpro.constants import APEX_WS_MAIN
from apexpro.websocket_api import WebSocket
from ApexproRestAPI import ApexproRestAPI
from ApexproTradeData import ApexproTradeData
from ApexproDepthData import ApexproDepthData

import pandas as pd
import time

class ApexproWebsocket:
    def __init__(self) -> None:
        self.key = ''
        self.ws = WebSocket(endpoint=APEX_WS_MAIN)
        

    def callback_trade(self, message):
        if message['type'] == 'delta':
            ApexproTradeData.add_data(message)
            print(message['data'][-1]['s'] + '-' + message['data'][-1]['S'] + ': ' + str(message['data'][-1]['v'])+ ' @'+ str(message['data'][-1]['p']))
        elif message['type'] == 'snapshot':
            pass
        else:
            print('Unknown data type!')
            print(message)


    def callback_depth(self, message):
        '''
        'topic': 'orderBook25.H.BTCUSDC', 'type': 'snapshot', 'data': {'s': 'BTCUSDC', 'b': [['26502.0', '11.600'], ['26502.5', '2.632'], ['26503.0', '5.760'], ['26503.5', '8.408'], ['26504.0', '8.472'], ['26504.5', '9.256'], ['26505.0', '4.624'], ['26505.5', '8.224'], ['26506.0', '4.680'], ['26506.5', '3.128'], ['26510.5', '1.888'], ['26511.5', '3.912'], ['26523.5', '0.227'], ['26530.0', '0.149'], ['26549.5', '13.920'], ['26550.0', '7.424'], ['26550.5', '7.704'], ['26551.0', '9.624'], ['26551.5', '2.064'], ['26552.0', '3.032'], ['26552.5', '4.168'], ['26553.0', '3.792'], ['26553.5', '1.712'], ['26554.0', '7.736'], ['26554.5', '6.856']], 'a': [['26555.0', '1.755'], ['26555.5', '0.225'], ['26556.0', '0.888'], ['26559.5', '0.001'], ['26560.0', '4.528'], ['26561.0', '6.297'], ['26561.5', '3.792'], ['26562.0', '5.720'], ['26562.5', '5.721'], ['26563.5', '7.736'], ['26565.5', '4.865'], ['26567.5', '2.796'], ['26568.0', '3.568'], ['26606.0', '3.304'], ['26608.0', '1.560'], ['26608.5', '4.202'], ['26609.0', '2.624'], ['26609.5', '3.552'], ['26610.0', '11.128'], ['26610.5', '11.592'], ['26611.0', '9.632'], ['26611.5', '11.744'], ['26612.0', '5.008'], ['26612.5', '1.088'], ['26626.5', '5.439']], 'u': 5496963}, 'cs': 1149719309, 'ts': 1692339921178495}
        {'topic': 'orderBook25.H.BTCUSDC', 'type': 'delta', 'data': {'s': 'BTCUSDC', 'b': [['26554.0', '0'], ['26501.5', '11.456']], 'a': [['26555.5', '1.785']], 'u': 5496964}, 'cs': 1149719309, 'ts': 1692339921178499}
        '''
        #print(message)
        ApexproDepthData.add_data(message)




    async def start(self):
        ApexproTradeData.initialize()
        ApexproDepthData.initialize()
        tickers = await self.get_all_tickers()
        for ticker in tickers['symbols']:
            #self.ws.trade_stream(self.callback_trade, ticker)
            self.ws.depth_stream(self.callback_depth,ticker,25)
        while True:
            await asyncio.sleep(0.1)

    async def get_all_tickers(self):
        api = ApexproRestAPI()
        return await api.get_tickers()

if __name__ == '__main__':
    ws = ApexproWebsocket()
    asyncio.run(ws.start())