import threading
import pandas as pd

class TradeData:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.max_data_size = 100
        self.sides = []
        self.prices = []
        self.sizes = []
        self.ts = []
        self.flg_created_file = False
    
    def add(self, side, price, size, ts):
        self.sides.append(side)
        self.prices.append(price)
        self.sizes.append(size)
        self.ts.append(ts)
        if len(self.sides) > self.max_data_size:
            self.__write_data()
            self.sides = []
            self.prices = []
            self.sizes = []
            self.ts = []
            print(self.symbol, ': Removed data to decrease size.')
    
    def __write_data(self):
        df = pd.DataFrame({'ts':self.ts, 'side':self.sides, 'price':self.prices, 'size':self.sizes})
        if self.flg_created_file:
            df.to_csv('Data/trade/'+'apexpro_'+self.symbol+'_trade.csv', mode='a', header=False, index=False) 
        else:
            df.to_csv('Data/trade/'+'apexpro_'+self.symbol+'_trade.csv', index=False)
            self.flg_created_file = True



class ApexproTradeData:
    @classmethod
    def initialize(cls):
        cls.lock = threading.RLock()
        cls.symbols = []
        cls.trade_data = {}
    
    @classmethod
    #{'topic': 'recentlyTrade.H.BLURUSDC', 'type': 'delta', 'data': [{'T': 1691987057826, 's': 'BLURUSDC', 'S': 'Sell', 'v': '30', 'p': '0.2833', 'L': 'MinusTick', 'i': 'b64b46d2-5f50-5b13-a096-47da9433416e'}], 'cs': 1125027783, 'ts': 1691987057877213}
    def add_data(cls, data):
        symbol = data['data'][-1]['s']
        with cls.lock:
            if symbol not in cls.symbols:
                cls.symbols.append(symbol)
                cls.trade_data[symbol] = TradeData(symbol)
            cls.trade_data[symbol].add(data['data'][-1]['S'], float(data['data'][-1]['p']), float(data['data'][-1]['v']), data['data'][-1]['T'])
    def get_all_data(cls):
        with cls.lock:
            return cls.trade_data
    
    
