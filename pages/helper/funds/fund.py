"""fund class use for calculating funds parameters"""
# from datetime import datetime
import json
import requests
import pandas as pd
from funds.helper.helper import persianNumberToEnglish

class Fund():
    """Helper class for fund calculation"""
    def __init__(self, name, fund_address, code, metrics):
        self.name = name
        self.fund_address = fund_address
        self.code = code
        self.history = None
        self.update_fund_data()
        self.update_closing_price()
        self.metric = metrics

    def update_fund_data(self):
        response = requests.get(self.fund_address+"/Fund/GetLeveragedNAV", timeout=60)
        json_object = json.loads(response.text)
        json_object = json.loads(json_object)

        self.BaseUnitsCancelNAV = persianNumberToEnglish(json_object["BaseUnitsCancelNAV"])
        self.BaseUnitsTotalNetAssetValue = persianNumberToEnglish(json_object["BaseUnitsTotalNetAssetValue"])
        self.BaseUnitsTotalSubscription = persianNumberToEnglish(json_object["BaseUnitsTotalSubscription"])
        self.SuperUnitsCancelNAV = persianNumberToEnglish(json_object["SuperUnitsCancelNAV"])
        self.SuperUnitsSubscriptionNAV = persianNumberToEnglish(json_object["SuperUnitsSubscriptionNAV"])
        self.SuperUnitsTotalSubscription = persianNumberToEnglish(json_object["SuperUnitsTotalSubscription"])
        self.SuperUnitsTotalNetAssetValue = persianNumberToEnglish(json_object["SuperUnitsTotalNetAssetValue"])

        response = requests.get(self.fund_address+"/Chart/AssetCompositions?type=getnavtotal", timeout=60)
        json_object = json.loads(response.text)
        self.CashAsset = 0
        for x in json_object['List']:
            if x["x"] == 'اوراق مشارکت' or x["x"] == 'نقد و بانک (سپرده)':
                self.CashAsset = self.CashAsset + x["y"]/100
        self.Asset = 1 - self.CashAsset
        
        response = requests.get(self.fund_address+"/Chart/TotalNAV?type=getnavtotal", timeout=60)
        json_object = json.loads(response.text)
        self.performance = {}
        if len(json_object[2]['List']) >= 7:
            self.performance["هفتگی"]=(json_object[2]['List'][6]["y"]-json_object[2]['List'][0]["y"])/json_object[2]['List'][0]["y"]
        else:
            self.performance["هفتگی"]=0
        if len(json_object[2]['List']) >= 23:
            self.performance["ماهانه"]=(json_object[2]['List'][22]["y"]-json_object[2]['List'][0]["y"])/json_object[2]['List'][0]["y"]
        else:
            self.performance["ماهانه"]=0
        if len(json_object[2]['List']) >= 67:
            self.performance["فصلی"]=(json_object[2]['List'][66]["y"]-json_object[2]['List'][0]["y"])/json_object[2]['List'][0]["y"]
        else:
            self.performance["فصلی"]=0
    def update_closing_price(self):

        url = "https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{}".format(self.code)
        header = {"User-Agent": "PostmanRuntime/7.29.0"}
        response = requests.get(url, headers=header, timeout=60).json()
        self.pClosing = response["closingPriceInfo"]["pClosing"]
        self.last = response["closingPriceInfo"]["pDrCotVal"]

    def get_price_history(self):
        url = "https://cdn.tsetmc.com/api/ClosingPrice/GetChartData/{}/D".format(self.code)
        header = {"User-Agent": "PostmanRuntime/7.29.0"}
        response = requests.get(url, headers=header, timeout=60).json()
        shiraz = pd.json_normalize(response['closingPriceChartData'])
        shiraz['datetime'] = pd.to_datetime(shiraz["dEven"]+19603987200, unit='s').dt.strftime("%Y%m%d").astype(int)
        self.history = shiraz

    def sharpe_ratio(self):
        return self.metric.sharpe_ratio(self)
    def sortino_ratio(self):
        return self.metric.sortino_ratio(self)
    def alpha(self, benchmark):
        return self.metric.alpha(self, benchmark)
    def r_squared(self, benchmark):
        "calculate r squared value of fund"
        return self.metric.r_squared(self, benchmark)
    def treynor_ratio(self, risk_free_rate):
        "calculate treynor ratio of fund"
        return self.metric.treynor_ratio(self, risk_free_rate)
    def jensens_alpha(self, benchmark):
        "calculate jensens alpha of fund"
        return self.metric.jensens_alpha(self, benchmark)
    def capture_ratio(self, benchmark):
        "calculate capture ratio of fund"
        return self.metric.capture_ratio(self, benchmark)
    def drawdown_analysis(self):
        "calculate drawdown of fund"
        return self.metric.drawdown_analysis(self)
